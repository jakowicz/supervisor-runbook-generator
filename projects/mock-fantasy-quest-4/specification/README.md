# Canonical specification index

This directory is the canonical, resumable specification for **mock-fantasy-quest-4**. It consolidates F001–F010 without overriding [`INITIAL.md`](../INITIAL.md), which remains the source of truth. A later author must cite stable IDs here rather than rediscovering scope.

## Control rules

- **P0** is an original, offline-capable 2D single-player fantasy RPG: one town, one dungeon, a short guided campaign and ending, exploration, dialogue/quests, party turn combat, inventory, local saves/recovery, settings/accessibility, responsive web, and PWA distribution.
- Target-neutral rules live in `requirements.*`; the web/PWA differences live in `platform-appendix.md`. PWA is a delivery adaptation of the shared game, not a second game.
- `Final Fantasy V` is a functional scope reference for party-based turn adventure only. It permits no copied expression: names, lore, text, art, music, maps, layouts, UI flows, or interaction choreography.
- `proposed` requirements and every `GATE-*` are not implementation authorisation. Resolve their linked `DEC-*` record before allocating dependent work.

## Chapter register

| Chapter ID | Document / owner | Depends on | State |
| --- | --- | --- | --- |
| SPEC-00 | `00-domain-discovery.md` / product discovery | INITIAL | complete |
| SPEC-01 | `01-product-brief.md` / product | SPEC-00 | complete |
| SPEC-02 | `02-feature-model.md` / game design | SPEC-00–01 | complete |
| SPEC-03 | `03-technical-contract.md` / technical design | SPEC-00–02 | complete |
| SPEC-04 | `04-experience-contract.md` / experience design | SPEC-00–03 | complete |
| SPEC-04A | `04-asset-direction.md` / visual asset direction | SPEC-04 | complete; P0 asset families allocated by later catalogue expansion |
| SPEC-04B | `04-audio-direction.md` / audio direction | SPEC-04 | complete; P0 cue map allocated by later catalogue expansion |
| SPEC-11 | `requirements.md`, `requirements.json` / F011 specification owner | SPEC-00–04, planning 05–10 | complete |
| SPEC-12 | `traceability-matrix.md` / F011 specification owner | SPEC-11 | complete; runbook IDs pending F012+ |
| SPEC-13 | `decision-log.md` / product owner | SPEC-00–04 | open decisions recorded |
| SPEC-14 | `platform-appendix.md` / technical + experience owner | SPEC-11 | complete; thresholds gated |
| SPEC-15 | `domain-completeness-review.md` / F011 specification owner | SPEC-00–04, SPEC-11 | complete; gated domains retained |

## Bounded expansion protocol

Expand one domain chapter at a time, preserving IDs and this register: identify entities/rules, authoring inputs, dependencies, P0 boundary, target adaptations, verification, and open decisions. Proposed detailed chapters are shell/session, campaign content, combat, progression/inventory, persistence/recovery, experience/accessibility, PWA/release, and connected-scope holds. A chapter can move from `planned` to `complete` only when its requirements, trace rows, and decision/risk links exist; it never closes a human gate.
