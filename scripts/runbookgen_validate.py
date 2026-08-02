#!/usr/bin/env python3
"""Deterministically validate creative coverage in a generated project.

This is a planning-quality gate, not product/release evidence.  It prevents a
factory from calling a game complete while the creative direction exists only
as prose or is represented by a generic schema task.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ID_PATTERNS = {
    "game": re.compile(r"\bGAME-[A-Z0-9-]+\b"),
    "assets": re.compile(r"\bASSET-[A-Z0-9-]+\b"),
    "audio": re.compile(r"\bAUDIO-[A-Z0-9-]+\b"),
    "narrative": re.compile(r"\bNAR-[A-Z0-9-]+\b"),
}


def front_matter(path: Path) -> dict[str, str]:
    document = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", document, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            result[key.strip()] = value.strip()
    return result


def identifiers(path: Path, kind: str) -> set[str]:
    return set(ID_PATTERNS[kind].findall(path.read_text(encoding="utf-8"))) if path.is_file() else set()


def values(value: object) -> list[str]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return []


def object_items(value: object) -> list[dict[str, object]]:
    """Return only JSON-object entries from a list-like field."""
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def is_game_workspace(workspace: Path) -> bool:
    initial = workspace / "INITIAL.md"
    return initial.is_file() and "Game" in initial.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", help="Project name under projects/, or an absolute project workspace path. Defaults to the active Supervisor project.")
    parser.add_argument("--require-r-series", action="store_true", help="Require every creative item to have a generated, required-media R contract.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    project_value = args.project
    if not project_value:
        database = Path(__import__("os").environ.get("SUPERVISOR_DATABASE_PATH", ""))
        if database.name.endswith(".sqlite3") and database.parent.name == ".state":
            project_value = str(database.parent.parent)
        else:
            parser.error("project is required outside a Supervisor project run")
    workspace = Path(project_value).expanduser()
    if not workspace.is_absolute():
        workspace = root / "projects" / workspace
    workspace = workspace.resolve()
    specification = workspace / "specification"
    catalogue_path = workspace / "planning" / "implementation-catalogue-index.json"
    manifest_path = workspace / "planning" / "runbook-authoring-manifest.json"
    errors: list[str] = []
    if not catalogue_path.is_file():
        errors.append("missing planning/implementation-catalogue-index.json")
        catalogue: dict[str, object] = {}
    else:
        catalogue = json.loads(catalogue_path.read_text(encoding="utf-8"))
    contracts = {item.get("id"): item for item in catalogue.get("contracts", []) if isinstance(item, dict) and isinstance(item.get("id"), str)}
    coverage = catalogue.get("creative_coverage", {})
    if not isinstance(coverage, dict):
        errors.append("creative_coverage must be an object")
        coverage = {}
    expected = {
        "game": identifiers(specification / "02-game-design-bible.md", "game"),
        "assets": identifiers(specification / "04-asset-direction.md", "assets"),
        "audio": identifiers(specification / "04-audio-direction.md", "audio"),
        "narrative": identifiers(specification / "02-narrative-content-model.md", "narrative"),
    }
    selected_modules: set[str] = set()
    design_units: list[dict[str, object]] = []
    bible_json = specification / "02-game-design-bible.json"
    if bible_json.is_file():
        try:
            payload = json.loads(bible_json.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                errors.append("02-game-design-bible.json must be a JSON object")
            else:
                selected_modules = set(values(payload.get("selected_modules")))
                design_units = object_items(payload.get("design_units"))
                if is_game_workspace(workspace) and not values(payload.get("game_archetypes")):
                    errors.append("02-game-design-bible.json needs non-empty game_archetypes")
        except json.JSONDecodeError:
            errors.append("02-game-design-bible.json is not valid JSON")
    if is_game_workspace(workspace):
        if not bible_json.is_file():
            errors.append("game is missing specification/02-game-design-bible.json")
        if not selected_modules:
            errors.append("game design bible needs at least one selected module")
        if not design_units:
            errors.append("game design bible needs non-empty design_units")
        if not expected["game"]:
            errors.append("game is missing stable GAME-* IDs in 02-game-design-bible.md")
        if not expected["assets"]:
            errors.append("game is missing stable ASSET-* IDs in 04-asset-direction.md")
        if not expected["audio"]:
            errors.append("game is missing stable AUDIO-* IDs in 04-audio-direction.md")
        if "narrative" in selected_modules and not expected["narrative"]:
            errors.append("narrative module is selected but 02-narrative-content-model.md has no stable NAR-* IDs")
        units_by_module: dict[str, set[str]] = {}
        unit_ids: set[str] = set()
        for unit in design_units:
            unit_id = unit.get("id")
            module = unit.get("module")
            if not isinstance(unit_id, str) or not ID_PATTERNS["game"].fullmatch(unit_id):
                errors.append("each game design unit needs a stable GAME-* id")
                continue
            if not isinstance(module, str) or not module:
                errors.append(f"game design unit {unit_id} needs a selected module")
                continue
            if module not in selected_modules:
                errors.append(f"game design unit {unit_id} references unselected module {module}")
            if not isinstance(unit.get("production_mode"), str) or not unit["production_mode"]:
                errors.append(f"game design unit {unit_id} needs a production_mode")
            unit_ids.add(unit_id)
            units_by_module.setdefault(module, set()).add(unit_id)
        for module in sorted(selected_modules):
            if not units_by_module.get(module):
                errors.append(f"selected game module {module!r} has no GAME-* design unit")
        if expected["game"] != unit_ids:
            errors.append("GAME-* IDs in 02-game-design-bible.md must exactly match JSON design_units")

        inventory_path = workspace / "planning" / "game-production-inventory.json"
        inventory: list[dict[str, object]] = []
        if not inventory_path.is_file():
            errors.append("game is missing planning/game-production-inventory.json")
        else:
            try:
                inventory_payload = json.loads(inventory_path.read_text(encoding="utf-8"))
                entries = inventory_payload.get("entries") if isinstance(inventory_payload, dict) else inventory_payload
                inventory = object_items(entries)
                if not inventory:
                    errors.append("game-production-inventory.json needs non-empty entries")
            except json.JSONDecodeError:
                errors.append("game-production-inventory.json is not valid JSON")
        inventory_by_design: dict[str, list[dict[str, object]]] = {}
        for entry in inventory:
            design_id = entry.get("game_design_id")
            module = entry.get("module")
            if not isinstance(design_id, str) or design_id not in unit_ids:
                errors.append("each game-production-inventory entry needs a known game_design_id")
                continue
            if not isinstance(module, str) or module not in selected_modules:
                errors.append(f"inventory entry for {design_id} needs a selected module")
            if not isinstance(entry.get("production_kind"), str) or not entry["production_kind"]:
                errors.append(f"inventory entry for {design_id} needs a production_kind")
            if not entry.get("planned_quantity"):
                errors.append(f"inventory entry for {design_id} needs a planned_quantity")
            if not isinstance(entry.get("verification"), str) or not entry["verification"]:
                errors.append(f"inventory entry for {design_id} needs verification")
            inventory_by_design.setdefault(design_id, []).append(entry)
        for unit_id in sorted(unit_ids):
            if not inventory_by_design.get(unit_id):
                errors.append(f"game design unit {unit_id} has no production-inventory entry")
    shards = {item.get("id") for item in catalogue.get("expansion_queue", []) if isinstance(item, dict)}
    for kind, expected_ids in expected.items():
        if not expected_ids:
            continue
        mapping = coverage.get(kind)
        if not isinstance(mapping, dict):
            errors.append(f"creative_coverage.{kind} is missing")
            continue
        for item_id in sorted(expected_ids):
            entry = mapping.get(item_id)
            if not isinstance(entry, dict):
                errors.append(f"{kind} {item_id} has no coverage entry")
                continue
            imp_ids = values(entry.get("imp_ids"))
            if not imp_ids:
                errors.append(f"{kind} {item_id} has no concrete IMP contract")
            for imp_id in imp_ids:
                contract = contracts.get(imp_id)
                if not isinstance(contract, dict):
                    errors.append(f"{kind} {item_id} references unknown {imp_id}")
                elif item_id not in values(contract.get("creative_coverage_ids")):
                    errors.append(f"{kind} {item_id} is not declared by {imp_id}.creative_coverage_ids")
            roles = set(values(entry.get("roles")))
            if not roles:
                errors.append(f"{kind} {item_id} has no creation/integration/QA role")
            shard = entry.get("shard")
            if shard not in {"current", *shards}:
                errors.append(f"{kind} {item_id} has invalid shard {shard!r}")
    manifest_contracts: list[dict[str, object]] = []
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_contracts = [item for item in manifest.get("r_contracts", []) if isinstance(item, dict)]
    by_catalogue = {item.get("catalogue_id"): item for item in manifest_contracts if isinstance(item.get("catalogue_id"), str)}
    for kind, expected_ids in expected.items():
        mapping = coverage.get(kind, {}) if isinstance(coverage.get(kind, {}), dict) else {}
        for item_id in expected_ids:
            entry = mapping.get(item_id, {}) if isinstance(mapping.get(item_id, {}), dict) else {}
            for imp_id in values(entry.get("imp_ids")):
                contract = by_catalogue.get(imp_id)
                if contract is None:
                    if args.require_r_series:
                        errors.append(f"{kind} {item_id} has no allocated R contract for {imp_id}")
                    continue
                r_path = root / str(contract.get("output_path", ""))
                if not r_path.is_file():
                    errors.append(f"{kind} {item_id} allocated {contract.get('id')} but its R file is missing")
                    continue
                meta = front_matter(r_path)
                field = (
                    "game_design_ids" if kind == "game" else
                    "asset_ids" if kind == "assets" else
                    "audio_ids" if kind == "audio" else "narrative_ids"
                )
                impact = "asset_impact" if kind == "assets" else "audio_impact" if kind == "audio" else None
                if impact and meta.get(impact) != "required":
                    errors.append(f"{contract.get('id')} must mark {impact}: required for {item_id}")
                if item_id not in values(meta.get(field)):
                    errors.append(f"{contract.get('id')} does not reserve {item_id} in {field}")
    print(f"Creative coverage gate — {workspace.name}")
    for kind, entries in expected.items():
        print(f"{kind}: {len(entries)} declared")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: every declared creative item has an owned implementation route.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
