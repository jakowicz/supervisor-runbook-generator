#!/usr/bin/env python3
"""Read-only progress summary for one generated runbook project."""

from __future__ import annotations

import argparse
import os
import sqlite3
from collections import Counter
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

    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    states = connection.execute(
        "SELECT task_id, status, active_pid, next_action, continuation_summary, updated_at FROM task_state ORDER BY task_id"
    ).fetchall()
    connection.close()
    counts = Counter(row["status"] for row in states)
    active = [row for row in states if process_is_running(row["active_pid"])]
    accepted = [row["task_id"] for row in states if row["status"] == "accepted"]
    pending = [row for row in states if row["status"] != "accepted"]
    factory_ids = [path.stem for path in sorted((root / "runbooks").glob("F*.md"))]
    recorded_ids = {row["task_id"] for row in states}
    unstarted = [task_id for task_id in factory_ids if task_id not in recorded_ids]
    b_count = len(list((workspace / "authoring-runbooks").glob("B*.md")))
    r_count = len(list((workspace / "runbooks").glob("R*.md")))

    print(f"Runbook generator status — {project_name}")
    print(f"Workspace: {workspace}")
    print(f"State: {database}")
    print(
        f"Factory tasks: {len(factory_ids)} total · {counts['accepted']} accepted · "
        f"{len(pending) + len(unstarted)} pending ({len(unstarted)} not started)"
    )
    print(f"Generated runbooks: {b_count} B-series writers · {r_count} R-series product tasks")
    if active:
        print("Active:")
        for row in active:
            print(f"- {row['task_id']} · pid {row['active_pid']} · {row['next_action']} · {row['continuation_summary']}")
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
