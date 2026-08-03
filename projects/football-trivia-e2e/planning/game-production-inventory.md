# Game production inventory

**Source:** `specification/02-game-design-bible.json`. This inventory is the
bounded bridge from canonical design units to authored production work. All
entries are first-release planned; the bible's rejected modules remain rejected
with their recorded reasons. `GPI-*` IDs are stable and map one-to-one or
one-to-many to `GAME-*` units.

| Design unit | Inventory IDs and finite scope | Dependency | Owner | Verification route |
| --- | --- | --- | --- | --- |
| GAME-001 | GPI-001: one card schema, five format fixtures | — | Editorial + tooling | Schema/negative fixtures |
| GAME-002 | GPI-002–005: four named 12-card batches, QB-A-01–48 | GPI-001 | Editorial + two reviewers | Provenance, review, quota, uniqueness validator |
| GAME-003 | GPI-006: four handlers, 20 adjudication fixtures | GPI-001 | Rules + core | Deterministic acceptance/rejection fixtures |
| GAME-004 | GPI-007: selection policy, 8 seeded fixtures | GPI-002–005 | Editorial + core | Repeat/shortage/withdrawal tests |
| GAME-005 | GPI-008: TUT-01–05 fixed tutorial | GPI-001, 006, 013–014 | Design + editorial | Offline completion/resume test |
| GAME-006 | GPI-009: one 10-card Mixed Fixture template | GPI-002–007 | Rules + core | Seeded selection lifecycle |
| GAME-007 | GPI-010: rule table, 12 edge fixtures | GPI-006, 009 | Rules + accessibility | Score/streak equivalent-feedback tests |
| GAME-008 | GPI-011: result and milestone states | GPI-009–010, 014 | Design + UI | Idempotence/recovery lifecycle tests |
| GAME-009 | GPI-012: profile/settings plus four input maps | — | Accessibility + platform | Input and accessibility review |
| GAME-010 | GPI-013: four recovery states, eight faults | GPI-011 | Persistence + accessibility | Fault-injection recovery tests |
| GAME-011 | GPI-014: cache/update notices and six fixtures | GPI-002–005, 013 | Release + platform | Offline/update/error tests |
| GAME-012 | GPI-015: four-target parity/certification matrix | GPI-012–014 | Platform + release | Target evidence and certification checklist |

The machine-readable [inventory](game-production-inventory.json) is
authoritative for each original brief, asset/audio linkage, and verification.
All referenced visuals (`ASSET-*`) and cues (`AUDIO-*`) are original-production
work: each is reviewed for provenance, non-copying, accessibility equivalence,
manifest validity, integration trigger, and runtime fallback before release.
