#!/usr/bin/env python3
"""Read-only progress summary for one generated runbook project."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
from pathlib import Path


def process_is_running(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        # A status command may be sandboxed more tightly than the parent
        # Supervisor process. Permission denied still proves that the PID
        # exists, so report it as active.
        return True
    return True


def load_states(database: Path) -> list[sqlite3.Row]:
    if not database.is_file():
        return []
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        return connection.execute(
            "SELECT task_id, status, active_pid, next_action, continuation_summary, updated_at FROM task_state ORDER BY task_id"
        ).fetchall()
    finally:
        connection.close()


def collection_progress(
    task_ids: list[str],
    states: list[sqlite3.Row],
    *,
    creation_label: str = "files created",
) -> str:
    """Summarise one named runbook collection.

    A shared state database can hold several collections (for example, B-series
    authoring batches and C/D-series coordination runbooks).  Callers must pass
    only the states belonging to the collection being displayed.
    """
    recorded = {row["task_id"] for row in states}
    accepted = sum(row["status"] == "accepted" for row in states)
    active = [row for row in states if row["status"] != "accepted" and process_is_running(row["active_pid"])]
    needs_attention = [
        row
        for row in states
        if row["status"] != "accepted" and row not in active
    ]
    not_yet_run = sum(task_id not in recorded for task_id in task_ids)
    parts = [f"{len(task_ids)} {creation_label}", f"{accepted} accepted"]
    if active:
        parts.append(f"{len(active)} running")
    if needs_attention:
        parts.append(f"{len(needs_attention)} needs attention")
    if not_yet_run:
        parts.append(f"{not_yet_run} not yet run")
    return " · ".join(parts)


def states_for(task_ids: list[str], states: list[sqlite3.Row]) -> list[sqlite3.Row]:
    """Return durable task states that belong to ``task_ids`` only."""
    identifiers = set(task_ids)
    return [row for row in states if row["task_id"] in identifiers]


def main() -> None:
    parser = argparse.ArgumentParser(description="Show read-only E2E factory progress for a generated project.")
    parser.add_argument("project", nargs="?", help="Project name under projects/.")
    parser.add_argument("--project", dest="project_option", help="Project name under projects/.")
    arguments = parser.parse_args()
    project_name = arguments.project_option or arguments.project or os.getenv("E2E_PROJECT_NAME", "e2e-fantasy-quest")
    root = Path(__file__).resolve().parents[1]
    workspace = root / "projects" / project_name
def reserved_r_outputs(workspace: Path, generated_ids: list[str]) -> tuple[int, list[str]]:
    """Return manifest-reserved R IDs that B writers have not materialised yet."""
    manifest = workspace / "planning" / "runbook-authoring-manifest.json"
    if not manifest.is_file():
        return 0, []
    try:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return 0, []
    generated = set(generated_ids)
    reserved = [
        contract
        for contract in payload.get("r_contracts", [])
        if isinstance(contract, dict)
        and isinstance(contract.get("id"), str)
        and contract["id"] not in generated
    ]
    return len(reserved), sorted({str(contract.get("authoring_batch", "")) for contract in reserved if contract.get("authoring_batch")})


    database = workspace / ".state" / "factory.sqlite3"
    if not workspace.is_dir():
        available = sorted(path.name for path in (root / "projects").glob("*") if path.is_dir())
        raise SystemExit(f"Project not found: {workspace}\nAvailable projects: {', '.join(available) or '(none)'}")
    if not database.is_file():
        raise SystemExit(f"No factory state yet: {database}\nRun: supervisor-run --project {project_name}")

    states = load_states(database)
    accepted = [row["task_id"] for row in states if row["status"] == "accepted"]
    pending = [row for row in states if row["status"] != "accepted"]
    factory_ids = [path.stem for path in sorted((root / "runbooks").glob("F*.md"))]
    recorded_ids = {row["task_id"] for row in states}
    unstarted = [task_id for task_id in factory_ids if task_id not in recorded_ids]
    b_ids = [path.stem for path in sorted((workspace / "authoring-runbooks").glob("B*.md"))]
    control_ids = [
        path.stem
        for path in sorted((workspace / "authoring-runbooks").glob("[CD]*.md"))
    ]
    r_ids = [path.stem for path in sorted((workspace / "runbooks").glob("R*.md"))]
    b_states = load_states(workspace / ".state" / "authoring-runbooks.sqlite3")
    b_collection_states = states_for(b_ids, b_states)
    control_states = states_for(control_ids, b_states)
    active_collections = [
        ("factory", row) for row in states if process_is_running(row["active_pid"])
    ] + [
        ("B-series", row) for row in b_collection_states if process_is_running(row["active_pid"])
    ] + [
    reserved_r_count, reserved_r_batches = reserved_r_outputs(workspace, r_ids)
        ("authoring coordination", row) for row in control_states if process_is_running(row["active_pid"])
    ]

    print(f"Runbook generator status — {project_name}")
    print(f"Workspace: {workspace}")
    print(f"State: {database}")
    print(f"Factory tasks: {collection_progress(factory_ids, states)}")
    print(f"B-series authoring tasks: {collection_progress(b_ids, b_collection_states)}")
    if control_ids:
        print(f"Authoring coordination tasks (C/D): {collection_progress(control_ids, control_states)}")
    r_summary = f"R-series implementation handoff: {len(r_ids)} R files generated"
    if reserved_r_count:
        r_summary += f" · {reserved_r_count} reserved for {'/'.join(reserved_r_batches)}"
    print(r_summary + " · not run by this factory")
    if active_collections:
        print("Active:")
        for collection, row in active_collections:
            print(f"- {collection} · {row['task_id']} · pid {row['active_pid']} · {row['next_action']} · {row['continuation_summary']}")
    elif pending:
        print("Next pending:")
        row = pending[0]
        print(f"- {row['task_id']} · {row['status']} · {row['next_action']} · {row['continuation_summary']}")
    elif unstarted:
        print("Next pending:")
        print(f"- {unstarted[0]} · not started · run `supervisor-run --project {project_name}` to continue")
    else:
        print("Factory collection complete.")
    if accepted:
        print("Accepted: " + ", ".join(accepted))


if __name__ == "__main__":
    main()
