# GC0001 coverage checkpoint

## Scope and conclusion

This checkpoint audits the completed `G0001`–`G0005` design-evidence wave. Its
canonical design coverage and dependency chain are closed, but the QB-A
catalogue's card-level editorial acceptance boundary is not. The manifest must
therefore remain pending. `GD0002` is the one bounded successor that owns every
item in that boundary; a later `GQ` audit, not this checkpoint, may evaluate
manifest completion after `GD0002` supplies the required evidence.

## Ownership, cap, canonical coverage, and closure

| Owning batch | Declared G outputs | Cap | Canonical coverage | Dependency closure |
| --- | --- | --- | --- | --- |
| `GB0001` | `G0001`, `G0002` | 2 of 5 | `GAME-001`–`GAME-004`; `GPI-001`–`GPI-007` | `G0002` depends on `G0001`; closed. |
| `GB0002` | `G0003`, `G0004` | 2 of 5 | `GAME-005`–`GAME-008`; `GPI-008`–`GPI-011` | `G0003` depends on `G0002`; `G0004` depends on `G0003`; closed. |
| `GB0003` | `G0005` | 1 of 5 | `GAME-009`–`GAME-012`; `GPI-012`–`GPI-015` | `G0005` depends on `G0004`; closed. |

Each completed G task declares the same `design_authoring_batch` as its owning
batch's output list. The allocated canonical sets cover every `GAME-001`
through `GAME-012` and `GPI-001` through `GPI-015` exactly once. No rejected
or decision-gated module is allocated. The detailed evidence outputs are:

- `G0001`: question-card and QB-A catalogue bible.
- `G0002`: adjudication and freshness bible.
- `G0003`: round lifecycle bible.
- `G0004`: score, streak, and results bible.
- `G0005`: accessibility, recovery, and target-parity bible.

## Evidence inspected

- `G0001` provides card grammar, original-expression and permitted-source
  policy, quota tables, provenance fields, and a two-review workflow for four
  QB-A batches. The 48 inventory records remain explicitly `draft`, have
  `PROV-<ID>` placeholders, and have pending review records.
- `G0002` provides deterministic select, true/false, ordered, and typed
  adjudication; 20 fixtures; withdrawal/correction lifecycle states; and
  seeded anti-repeat and shortage fixtures. Publication-dependent selection is
  conditional while no QB-A card is eligible.
- `G0003` provides `TUT-01`–`TUT-05` First Whistle transitions, Mixed Fixture
  seeded selection/shortage fixtures, an optional-off timer, offline and
  interruption lifecycle, and accessibility review.
- `G0004` provides the capped 100-point score/streak rule; wrong, blank,
  timeout, and abandon recovery; idempotent results/milestones; edge fixtures;
  and text, non-colour, captioned/muted audio-equivalent feedback.
- `G0005` provides touch, pointer, keyboard, and gamepad mappings;
  non-audio/non-colour equivalents; recovery/offline/update states; and
  shared-rule, shared-content, shared-save web/PWA/Android/iOS parity
  evidence.

## Incomplete QB-A editorial boundary

The following is the complete remaining evidence boundary and is owned solely
by `GD0002`:

1. `GPI-001` lacks completed card-level resolvable provenance and two distinct
   accepted current-revision reviews for `QB-A-01`–`QB-A-48`.
2. `GPI-002`–`GPI-005` are each a finite 12-card `draft` batch at revision 1,
   with placeholder provenance and two pending reviews. Placeholder records
   cannot enter selection.
3. `GAME-002` lacks accepted original-expression, factual-source/provenance,
   factual/rights, accessibility/copy, and independent second-review decisions
   for every current card revision.
4. `GAME-004` and `GAME-006` have deterministic policy and fixture evidence,
   but published QB-A candidate use remains conditional on the accepted records
   above.

There are no blocked product decisions in this wave.

## Successor and manifest guardrail

`GD0002` is the exactly one bounded successor. It is limited to an editorial
acceptance register for the existing 48 records in the four existing 12-card
batches; it may not add cards, alter quiz scope, create implementation
runbooks, or accept the manifest. It must retain any rejected, unresolved,
withdrawn, conflicted, or incompletely reviewed card as ineligible with its
exact reason.

`planning/game-design-manifest.json` is intentionally still `pending`: its
`final_audit` is `null`, `GC0001` is a pending checkpoint, and no `GQ` final
manifest audit has been created. Only after `GD0002` closes every item above may
a later `GQ` audit run the dedicated completion check, update canonical
bible/inventory records, and accept the manifest.

## Checkpoint result

The five completed G tasks satisfy ownership, cap, canonical-coverage, and
dependency-closure checks. Their design-rule evidence is preserved, while the
single unclosed QB-A editorial acceptance boundary is accurately deferred to
`GD0002`; manifest acceptance is deliberately deferred to a later `GQ` audit.
