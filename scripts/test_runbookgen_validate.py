"""Tests for deterministic generated-project evidence gates."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("runbookgen_validate.py")
SPEC = importlib.util.spec_from_file_location("runbookgen_validate", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def _editorial_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "project"
    evidence = workspace / "design-evidence"
    evidence.mkdir(parents=True)
    card_ids = [f"QB-A-{index:02d}" for index in range(1, 13)]
    register_records = []
    authored_records = []
    for card_id in card_ids:
        authored_records.append({
            "cardId": card_id,
            "batchId": "GPI-002",
            "revision": 1,
            "originalityRecord": {
                "playerFacing": {
                    "prompt": f"Question {card_id}?",
                    "instruction": "Choose one answer.",
                    "options": ["One", "Two"],
                    "canonicalAnswer": "One",
                    "explanation": "One is correct.",
                },
            },
            "provenanceRecord": {
                "sourceRoutes": [{
                    "locator": "https://example.test/source",
                    "retrievedAt": "2026-08-03",
                    "assertionMap": [{"assertion": "Fact", "sourceLocator": "https://example.test/source"}],
                }],
            },
        })
        register_records.append({
            "cardId": card_id,
            "batchId": "GPI-002",
            "revision": 1,
            "status": "published",
            "selectionEligible": True,
            "originalityRecord": {"decision": "accepted"},
            "provenance": {"decision": "accepted"},
            "reviews": [
                {"role": "factual_rights_editor", "reviewerId": "facts-a", "decision": "accepted", "reviewedRevision": 1},
                {"role": "accessibility_copy_editor", "reviewerId": "access-b", "decision": "accepted", "reviewedRevision": 1},
            ],
            "releaseGate": {"decision": "accepted", "releasedRevision": 1},
        })
    (evidence / "qba-editorial-acceptance-register.json").write_text(
        json.dumps({"batches": [{"batchId": "GPI-002", "cardIds": card_ids}], "records": register_records}),
        encoding="utf-8",
    )
    (evidence / "gpi-002-r1-originality-and-provenance.json").write_text(
        json.dumps({"records": authored_records}),
        encoding="utf-8",
    )
    return workspace


def test_editorial_gate_accepts_complete_bounded_evidence(tmp_path: Path) -> None:
    workspace = _editorial_workspace(tmp_path)

    assert validator.editorial_evidence_errors(
        workspace, "GPI-002", require_authoring=True, require_release=True
    ) == []


def test_editorial_gate_rejects_false_release_claims(tmp_path: Path) -> None:
    workspace = _editorial_workspace(tmp_path)
    register_path = workspace / "design-evidence" / "qba-editorial-acceptance-register.json"
    register = json.loads(register_path.read_text(encoding="utf-8"))
    register["records"][0]["selectionEligible"] = False
    register["records"][0]["reviews"] = []
    register_path.write_text(json.dumps(register), encoding="utf-8")

    errors = validator.editorial_evidence_errors(
        workspace, "GPI-002", require_authoring=True, require_release=True
    )

    assert any("two accepted revision-1 reviews" in error for error in errors)
    assert any("published and selectionEligible" in error for error in errors)
