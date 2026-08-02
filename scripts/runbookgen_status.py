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
        try:
            return connection.execute(
                "SELECT task_id, status, active_pid, next_action, continuation_summary, updated_at FROM task_state ORDER BY task_id"
            ).fetchall()
        except sqlite3.OperationalError as error:
            # Child state databases are created before their first task is
            # claimed. An empty SQLite file is therefore valid progress state,
            # not a status-command failure.
            if "no such table: task_state" in str(error):
                return []
            raise
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Show read-only E2E factory progress for a generated project.")
    parser.add_argument("project", nargs="?", help="Project name under projects/.")
    parser.add_argument("--project", dest="project_option", help="Project name under projects/.")
    arguments = parser.parse_args()
    project_name = arguments.project_option or arguments.project or os.getenv("E2E_PROJECT_NAME", "e2e-fantasy-quest")
    root = Path(__file__).resolve().parents[1]
    workspace = root / "projects" / project_name
    database = workspace / ".state" / "factory.sqlite3"
    if not workspace.is_dir():
        available = sorted(path.name for path in (root / "projects").glob("*") if path.is_dir())
        raise SystemExit(f"Project not found: {workspace}\nAvailable projects: {', '.join(available) or '(none)'}")
    if not database.is_file():
        raise SystemExit(f"No factory state yet: {database}\nRun: supervisor-run --project {project_name}")

    states = load_states(database)
    pending = [row for row in states if row["status"] != "accepted"]
    factory_ids = [path.stem for path in sorted((root / "runbooks").glob("F*.md"))]
    recorded_ids = {row["task_id"] for row in states}
    unstarted = [task_id for task_id in factory_ids if task_id not in recorded_ids]
    g_ids = [path.stem for path in sorted((workspace / "game-design-runbooks").glob("G*.md"))]
    b_ids = [path.stem for path in sorted((workspace / "authoring-runbooks").glob("B*.md"))]
    control_ids = [
        path.stem
        for path in sorted((workspace / "authoring-runbooks").glob("[CD]*.md"))
    ]
    r_ids = [path.stem for path in sorted((workspace / "runbooks").glob("R*.md"))]
    reserved_r_count, reserved_r_batches = reserved_r_outputs(workspace, r_ids)
    b_states = load_states(workspace / ".state" / "authoring-runbooks.sqlite3")
    g_states = load_states(workspace / ".state" / "game-design-runbooks.sqlite3")
    g_collection_states = states_for(g_ids, g_states)
    b_collection_states = states_for(b_ids, b_states)
    control_states = states_for(control_ids, b_states)
    active_collections = [
        ("factory", row) for row in states if process_is_running(row["active_pid"])
    ] + [
        ("G-series game design", row) for row in g_collection_states if process_is_running(row["active_pid"])
    ] + [
        ("B-series", row) for row in b_collection_states if process_is_running(row["active_pid"])
    ] + [
        ("authoring coordination", row) for row in control_states if process_is_running(row["active_pid"])
    ]

    print(f"Runbook generator status — {project_name}")
    print(f"Workspace: {workspace}")
    print(f"State: {database}")
    print("\nFactory stages")
    print(f"- {collection_progress(factory_ids, states, creation_label='stages available')}")
    print("\nGame design")
    if g_ids:
        print(f"- G design runbooks: {collection_progress(g_ids, g_collection_states, creation_label='G files created')}")
    else:
        print("- Not created yet (or not applicable for this product)")
    print("\nRunbook authoring")
    print(f"- B writers: {collection_progress(b_ids, b_collection_states, creation_label='B files created')}")
    if control_ids:
        print(f"- C/D coordination: {collection_progress(control_ids, control_states, creation_label='coordination files created')}")
    print("\nR-series handoff")
    print(f"- {len(r_ids) + reserved_r_count} R runbooks planned in total")
    print(f"- {len(r_ids)} R Markdown files generated")
    if reserved_r_count:
        print(f"- {reserved_r_count} R files reserved for {'/'.join(reserved_r_batches)} to write")
    print("- R files are not run by this factory; a separate implementation supervisor owns them")
    print("\nCurrent generator work")
    if active_collections:
        for collection, row in active_collections:
            print(f"- {collection} · {row['task_id']} · pid {row['active_pid']} · {row['next_action']} · {row['continuation_summary']}")
    else:
        print("- None")
    if not active_collections and pending:
        print("\nFactory attention needed")
        row = pending[0]
        print(f"- {row['task_id']} · {row['status']} · {row['next_action']} · {row['continuation_summary']}")
    elif not active_collections and unstarted:
        print("\nFactory attention needed")
        print(f"- {unstarted[0]} · not started · run `supervisor-run --project {project_name}` to continue")
    elif not active_collections:
        unaccepted_authoring = [row for row in [*b_collection_states, *control_states] if row["status"] != "accepted"]
        unstarted_authoring = len(b_ids) + len(control_ids) - len({row["task_id"] for row in [*b_collection_states, *control_states]})
        if unaccepted_authoring or unstarted_authoring:
            pending_authoring = sorted(
                row["task_id"] for row in unaccepted_authoring
            )
            unstarted_ids = sorted(
                set(b_ids + control_ids) - {row["task_id"] for row in [*b_collection_states, *control_states]}
            )
            next_task = (pending_authoring or unstarted_ids or ["unknown"])[0]
            print("\nNext authoring work")
            print(f"- {next_task} · run `supervisor-run --project {project_name}` to continue")
        else:
            print("\nFactory and authoring collections complete; the R-series handoff is ready.")


if __name__ == "__main__":
    main()
