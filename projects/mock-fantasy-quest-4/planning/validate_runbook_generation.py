#!/usr/bin/env python3
"""Structural quality gate for generated B-series and R-series runbooks.

This validates planning artefacts only; it is never product or release evidence.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
MANIFEST_PATH = ROOT / "planning/runbook-authoring-manifest.json"
CATALOGUE_PATH = ROOT / "planning/implementation-catalogue-index.json"
R_ID, F_ID = re.compile(r"^R\d{4}$"), re.compile(r"^F\d{3}$")
LIST_FIELDS = {
    "dependencies", "requirement_ids", "source_specifications",
    "source_catalogue_ids", "factory_stages", "asset_ids", "audio_ids",
    "playwright_spec", "playwright_specs",
}

def values(value):
    return value if isinstance(value, list) else ([value] if value else [])

def parse_value(value):
    value = value.strip().strip("\"'")
    if value == "[]": return []
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip("\"'") for item in value[1:-1].split(",") if item.strip()]
    return value

def front_matter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"): return {}
    end = text.find("\n---", 4)
    if end < 0: return {}
    result, key = {}, None
    for line in text[4:end].splitlines():
        if line.lstrip().startswith("-") and key:
            result.setdefault(key, []).append(parse_value(line.split("-", 1)[1]))
        elif ":" in line:
            key, value = line.split(":", 1); key = key.strip(); value = parse_value(value)
            # Authoring runbooks use compact comma-delimited metadata for
            # these schema-defined lists. Preserve scalar prose fields such as
            # asset_brief verbatim while normalising only list metadata.
            result[key] = [item.strip() for item in value.split(",") if item.strip()] if key in LIST_FIELDS and isinstance(value, str) else value
    return result

def headings(path):
    return {re.sub(r"[^a-z0-9]+", "-", match.group(1).lower()).strip("-")
            for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", path.read_text(encoding="utf-8"), re.M)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wave", help="validate allocations through this B batch")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST_PATH.read_text())
    catalogue = json.loads(CATALOGUE_PATH.read_text())
    batches = {b["id"]: b for b in manifest["batches"]}
    contracts = manifest["r_contracts"]
    if args.wave:
        if args.wave not in batches: parser.error("unknown B batch: " + args.wave)
        contracts = [c for c in contracts if batches.get(c.get("authoring_batch"), {}).get("order", 999) <= batches[args.wave]["order"]]
    records = {r["id"]: r for r in catalogue["contracts"]}
    errors, missing, blocked, unverified = [], [], [], []
    def fail(text): errors.append(text)
    ids = [c.get("id", "") for c in contracts]
    if ids != sorted(ids): fail("manifest R IDs are not sequence ordered")
    for item, count in Counter(ids).items():
        if count > 1: fail("duplicate manifest R ID " + item)
    paths = [c.get("output_path", "") for c in contracts]
    for item, count in Counter(paths).items():
        if count > 1: fail("duplicate output path " + item)
    assets, browser_paths = {}, defaultdict(list)
    # The authoring collection is part of the gate: each allocated batch must
    # exist, identify itself, and be the sole owner of its manifest R IDs.
    for batch_id, batch_record in batches.items():
        batch_path = ROOT / "authoring-runbooks" / f"{batch_id}.md"
        meta = front_matter(batch_path) if batch_path.is_file() else {}
        if not meta: fail(f"{batch_id}: missing or invalid B-series front matter")
        elif meta.get("task_id") != batch_id: fail(f"{batch_id}: task ID mismatch in authoring runbook")
        if len(batch_record.get("r_contract_ids", [])) > 7: fail(f"{batch_id}: exceeds seven-contract batch limit")
    for contract in contracts:
        rid, batch = contract.get("id", ""), contract.get("authoring_batch", "")
        if not R_ID.fullmatch(rid): fail(f"invalid R ID {rid!r}")
        if batch not in batches or rid not in batches.get(batch, {}).get("r_contract_ids", []): fail(f"{rid}: authoring batch ownership mismatch")
        catalogue_ids = values(contract.get("source_catalogue_ids"))
        if not catalogue_ids or contract.get("catalogue_id") not in catalogue_ids: fail(f"{rid}: missing or inconsistent catalogue provenance")
        for cid in catalogue_ids:
            if cid not in records: fail(f"{rid}: unknown catalogue ID {cid}")
        if contract.get("catalogue_id") in records and not records[contract["catalogue_id"]].get("requirement_ids"): fail(f"{rid}: catalogue record lacks requirement links")
        specs = values(contract.get("source_specifications"))
        if not specs: fail(f"{rid}: missing source_specifications")
        for link in specs:
            file_name, _, anchor = link.partition("#"); source = ROOT / file_name
            if not link.startswith("specification/") or not source.is_file() or (anchor and anchor not in headings(source)):
                fail(f"{rid}: unresolved canonical specification link {link}")
        stages = values(contract.get("factory_stages"))
        if not stages or any(not F_ID.fullmatch(s) for s in stages): fail(f"{rid}: invalid factory_stages")
        for dependency in values(contract.get("dependencies")):
            if dependency not in ids: fail(f"{rid}: dependency {dependency} is outside allocation")
            elif dependency >= rid: fail(f"{rid}: dependency {dependency} does not precede contract")
        impact, asset_ids = contract.get("asset_impact"), values(contract.get("asset_ids"))
        if impact not in {"required", "not_applicable"}: fail(f"{rid}: invalid asset_impact")
        if "asset_ids" not in contract: fail(f"{rid}: asset_ids absent")
        if impact == "required":
            if not asset_ids or not contract.get("asset_brief") or not contract.get("visual_style_version"): fail(f"{rid}: required assets lack IDs, brief, or style version")
            for asset in asset_ids:
                if not re.fullmatch(r"ASSET-[A-Z0-9-]+", asset): fail(f"{rid}: unstable asset ID {asset}")
                if asset in assets: fail(f"asset {asset} ambiguously owned by {assets[asset]} and {rid}")
                assets[asset] = rid
        elif asset_ids: fail(f"{rid}: non-asset contract reserves asset IDs")
        if batches.get(batch, {}).get("state") in {"blocked_on_gate", "blocked", "repairable"}: blocked.append(rid)
        r_path = REPOSITORY / contract.get("output_path", "")
        if not r_path.is_file(): missing.append(rid); continue
        meta = front_matter(r_path)
        for field in ("task_id", "sequence", "source_specifications", "source_catalogue_ids", "authoring_batch", "factory_stages", "asset_impact", "asset_ids"):
            if field not in meta: fail(f"{rid}: {r_path.name} lacks {field}")
        if "requirement_ids" not in meta: fail(f"{rid}: {r_path.name} lacks requirement_ids")
        if meta.get("task_id") != rid: fail(f"{rid}: task ID mismatch")
        if values(meta.get("requirement_ids")) != records.get(contract.get("catalogue_id"), {}).get("requirement_ids", []): fail(f"{rid}: requirement_ids differ from catalogue")
        for field in ("source_specifications", "source_catalogue_ids", "authoring_batch", "factory_stages", "asset_impact", "asset_ids"):
            if values(meta.get(field)) != values(contract.get(field)): fail(f"{rid}: {field} differs from manifest")
        browser, specs = meta.get("browser_impact", "not_applicable"), values(meta.get("playwright_spec", meta.get("playwright_specs")))
        if browser == "not_applicable" and specs: fail(f"{rid}: browser path on non-browser contract")
        if browser != "not_applicable" and (not specs or not set(records.get(contract.get("catalogue_id"), {}).get("targets", [])) & {"web", "pwa"}): fail(f"{rid}: browser metadata outside browser behaviour scope")
        for spec in specs: browser_paths[spec].append(rid)
        body = r_path.read_text(encoding="utf-8")
        if "## Verification" not in body: unverified.append(rid)
        if not re.search(r"^## Asset assessment\s*$", body, re.M | re.I): fail(f"{rid}: missing explicit Asset assessment section")
    for path, owners in browser_paths.items():
        if len(owners) > 1: fail(f"duplicate browser test path {path}: {', '.join(owners)}")
    graph = {c["id"]: values(c.get("dependencies")) for c in contracts}; active, done = set(), set()
    def visit(node):
        if node in active: fail("unsupported circular dependency through " + node); return
        if node not in done:
            active.add(node)
            for dep in graph[node]:
                if dep in graph: visit(dep)
            active.remove(node); done.add(node)
    for node in graph: visit(node)
    # Discovered families need a canonical source and a category-appropriate
    # catalogue/verification route. Explicitly held connected scope is a valid
    # reviewed outcome, not a missing P0 implementation contract.
    review = ROOT / "specification/domain-completeness-review.md"
    for line in review.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("| System") or line.startswith("| ---"): continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) != 5: continue
        family, source, _deps, authoring, decision = cells
        if "SPEC-" not in source: fail(f"domain family {family}: no specification chapter")
        if "hold" in decision.lower(): continue
        keywords = [word.lower() for word in re.findall(r"[A-Za-z]{5,}", family)]
        searchable = json.dumps(catalogue).lower()
        if not any(word in searchable for word in keywords): fail(f"domain family {family}: no catalogue traceability")
        if authoring.lower() not in {"none", "n/a"} and not authoring: fail(f"domain family {family}: no content/authoring approach")
    allocated = {c.get("catalogue_id") for c in contracts}
    unallocated = [cid for cid in records if cid not in allocated]
    print("Runbook-generation structural quality gate (not product/release evidence)")
    chapter_count = len(list((ROOT / "specification").glob("*.md")))
    source_link_count = sum(len(values(c.get("source_specifications"))) for c in contracts)
    print(f"canonical specification chapters: {chapter_count}")
    print(f"specification provenance links: {source_link_count}")
    for label, result in (("catalogue contracts", list(records)), ("manifest contracts", ids), ("R files missing", missing), ("blocked contracts", blocked), ("unverified contracts", unverified), ("unallocated catalogue contracts", unallocated), ("reserved asset IDs", list(assets)), ("browser test paths", list(browser_paths))):
        print(f"{label}: {len(result)}" + (" (" + ", ".join(sorted(result)) + ")" if result else ""))
    for error in errors: print("ERROR:", error)
    return 1 if errors or missing or unverified else 0
if __name__ == "__main__": sys.exit(main())
