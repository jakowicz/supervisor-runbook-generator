"""Regression tests for the human-readable runbook generator status."""

from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("runbookgen_status.py")
SPEC = importlib.util.spec_from_file_location("runbookgen_status", MODULE_PATH)
assert SPEC and SPEC.loader
status = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(status)


def test_factory_progress_does_not_count_project_recovery_tasks() -> None:
    rows = [
        {"task_id": "F001", "status": "accepted", "active_pid": None},
        {"task_id": "AR0001-DEADBEEF", "status": "accepted", "active_pid": None},
        {"task_id": "AR0002-DEADBEEF", "status": "interrupted", "active_pid": None},
    ]

    factory_rows = status.states_for(["F001", "F002"], rows)

    assert factory_rows == [rows[0]]
    assert status.collection_progress(
        ["F001", "F002"], factory_rows, creation_label="stages available"
    ) == "2 stages available · 1 accepted · 1 not yet run"


def test_recovery_task_identifier_is_not_an_f_series_identifier() -> None:
    assert status.re.fullmatch(r"AR[0-9A-Z-]+", "AR0001-2F73F873")
    assert not status.re.fullmatch(r"F\d+", "AR0001-2F73F873")
