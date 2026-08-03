# Round lifecycle bible

**Scope:** accepted design evidence for `GAME-005`, `GAME-006`, `GPI-008`, and
`GPI-009`. This defines a future-core contract and fixtures, not production
content or an implementation. All content IDs refer to the frozen package held
by the run; no network response, wall clock, UI ordering, or random source can
alter a fixture result.

## GPI-008 — First Whistle tutorial

`First Whistle` is a fixed five-card, non-timed onboarding round. It is
available from a new local profile when the installed tutorial package is
present, including offline. It does not need sign-in, a purchase, notifications,
or a remote service. Each card has the indicated one purpose; its final
published wording, answer IDs, provenance, and two reviews are governed by the
question-card and adjudication bibles before it may ship.

| Position / ID | Fixed format | Instructional purpose | Required resolution and next state |
| --- | --- | --- | --- |
| 1 / `TUT-01` | four-option select | Read the prompt, choose one labelled option, and confirm. | Accepted or rejected select submission resolves the attempt, exposes text feedback, and opens `TUT-02`. |
| 2 / `TUT-02` | short typed answer | Enter a short answer and confirm; only configured canonical text/aliases are accepted. | A typed submission resolves through GAME-003 normalisation, shows canonical answer/explanation if rejected, and opens `TUT-03`. |
| 3 / `TUT-03` | true/false | Recognise that feedback says whether the resolved answer was accepted. | Submission resolves once; feedback is available in text plus non-colour state, then opens `TUT-04`. |
| 4 / `TUT-04` | ordered pair | Inspect the explanation after resolving an answer. | Submission resolves once; explanation is available before continue, then opens `TUT-05`. |
| 5 / `TUT-05` | four-option select | Pause deliberately, confirm that the current safe state is saved, then resume and finish. | Explicit pause commits a snapshot after the unresolved card is displayed; resume restores `TUT-05`; resolved completion commits result and `first_whistle_complete`. |

The tutorial's card sequence is exactly `[TUT-01, TUT-02, TUT-03, TUT-04,
TUT-05]`; it has no selection seed, repeat filter, timer, skip, or reordering.
The tutorial selection never silently substitutes an unavailable card. If its
fixed package is unavailable or invalid, start is blocked with a plain-language
retry/return-home state.

### Tutorial deterministic fixtures

Fixture input includes a frozen `tutorial-v1` package containing the five IDs,
a new local profile, and the stated actions. `resolve` means the matching
GAME-003 fixture supplies an immutable accepted/rejected attempt; the
particular football fact is deliberately not duplicated here.

| ID | Input / action | Expected deterministic state, record, and visible outcome |
| --- | --- | --- |
| `TUT-FX-01` | Start `tutorial-v1`; resolve `TUT-01`; continue. | Active card changes `TUT-01 → TUT-02`; one immutable TUT-01 attempt exists; no timer state is created. |
| `TUT-FX-02` | From TUT-02 submit a configured typed alias, resolve, continue. | `TUT-02 → TUT-03`; outcome is the configured GAME-003 alias result and is not recomputed on continue. |
| `TUT-FX-03` | From TUT-03 submit an incorrect valid true/false value, resolve, continue. | `TUT-03 → TUT-04`; rejected text/non-colour feedback and canonical answer/explanation are recorded before continue. |
| `TUT-FX-04` | From TUT-04 submit its configured ordered pair, resolve, inspect explanation, continue. | `TUT-04 → TUT-05`; explanation availability is recorded; inspection does not change score, streak, or card position. |
| `TUT-FX-05` | Display TUT-05; `Pause`; restart; `Resume`; resolve; complete. | Pause snapshot has `activeCardId=TUT-05`, no unresolved answer, package `tutorial-v1`; restart restores that card; completion creates exactly one `first_whistle_complete` milestone and an immutable result. |
| `TUT-FX-06` | Repeat the completion command in TUT-FX-05 with the same completed-run ID and interaction ID. | Return the recorded completion/result; no second milestone, history entry, or score event is added. |
| `TUT-FX-07` | Start tutorial while offline with `tutorial-v1` cached; pause at TUT-05; restart while still offline. | Start, snapshot read, and resume succeed using cached package only; no network request is required. |
| `TUT-FX-08` | Start tutorial with no compatible cached tutorial package. | No run is created; show initial-content-required/retry/return-home state. It must not offer a substituted or partial tutorial. |

## GPI-009 — Mixed Fixture selection

`Mixed Fixture` starts with `(catalogueSnapshotId, selectionSeed, theme,
repeatLedger, timerMode)`. `theme` is either one selected category or
`kickoff_mix`; requested count is always ten. The selection first applies the
GAME-004 frozen-catalogue, publication, withdrawal, filter, anti-repeat, and
SHA-256 ordering policy. It then constructs the longest deterministic prefix
whose next card would not create a run of three equal `format` or three equal
`difficulty`. At each position, choose the first ranked candidate that keeps
both run lengths at two or fewer. If none does, choose the first ranked
candidate and append a variety-shortage record. This tie-free rule makes
selection reproducible and never rerolls.

The saved selection contains selected card IDs/revisions, their frozen package
and rule versions, rank inputs, `selectionSeed`, timer mode, and both shortage
records. A shortage is displayed before start with the plain-language key
`selection_shortage_reuse_disclosed` (reuse/unfilled) and/or
`selection_shortage_variety_disclosed` (three-in-a-row unavoidable). A category
with no eligible cards does not create a run; it shows unavailable-category and
offers another eligible theme.

### Seeded Mixed Fixture fixtures

In these fixtures `ranked` is the ascending SHA-256 ordering already calculated
from the stated frozen snapshot and seed under GAME-004. Each token is
`ID:format:difficulty`; all candidates are published, in theme, and eligible
after the repeat policy unless a shortage field says otherwise.

| ID | Snapshot / seed / ranked candidates | Expected selected IDs and records |
| --- | --- | --- |
| `MIX-FX-01` | `MF-1` / `north`; `A:S:1,B:T:2,C:O:3,D:S:2,E:T:1,F:O:2,G:S:3,H:T:1,I:O:2,J:S:1,K:T:3,L:O:1` | `A,B,C,D,E,F,G,H,I,J`; 10 fresh cards, no reuse/unfilled/variety shortage; every adjacent triple differs in both format and difficulty. |
| `MIX-FX-02` | `MF-2` / `west`; `A:S:1,B:S:2,C:S:3,D:T:1,E:O:2,F:T:3,G:O:1,H:S:2,I:T:1,J:O:3` | `A,B,D,C,E,F,G,H,I,J`; C moves after D because `A,B,C` would be three selects; no shortage. |
| `MIX-FX-03` | `MF-3` / `east`; `A:S:1,B:T:1,C:O:1,D:S:2,E:T:2,F:O:2,G:S:3,H:T:3,I:O:3,J:S:1` | `A,B,D,C,E,F,G,H,I,J`; D moves before C because the first three ranked cards share difficulty 1; no shortage. |
| `MIX-FX-04` | `MF-4` / `south`; `A:S:1,B:S:2,C:S:3,D:S:1,E:S:2,F:S:3,G:S:1,H:S:2,I:S:3,J:S:1` | `A,B,C,D,E,F,G,H,I,J`; formats have no alternative, so record format variety shortages at positions 3–10 with `selection_shortage_variety_disclosed` before start. |
| `MIX-FX-05` | `MF-5` / `cup`; fresh ranked `A:S:1,B:T:2,C:O:3,D:S:2,E:T:1,F:O:2,G:S:3,H:T:2`, then reused ranked `I:O:3,J:S:1`; requested 10 | Select A–H then I,J; record reused IDs I,J and `selection_shortage_reuse_disclosed`; variety rule is still evaluated over the final order. |
| `MIX-FX-06` | `MF-6` / `cup`; seven eligible ranked `A:S:1,B:T:2,C:O:3,D:S:2,E:T:1,F:O:2,G:S:3`; requested 10 | Select A–G only; record `requestedCount=10`, `eligibleAvailable=7`, `unfilledCount=3`, and `selection_shortage_reuse_disclosed`; do not pad with unpublished, withdrawn, or invented cards. |
| `MIX-FX-07` | `MF-7` / `empty-theme`; no eligible candidates | No run/snapshot; show unavailable-category and eligible-theme choice. |

## Optional timer and round lifecycle

Timer is an accessibility-neutral optional display mode: `off` is the default
and tutorial always forces `off`. Starting a standard round freezes the chosen
mode. `on` records elapsed active seconds only; it does not change selection,
adjudication, score, streak, or availability. Pause, background interruption,
and recovery stop elapsed time. A timeout can be emitted only for an explicitly
enabled timer according to the separately implemented GAME-007 scoring rule.

| Transition | Preconditions | Required result |
| --- | --- | --- |
| `home → selecting_theme` | Compatible cached standard package. | Show themes and timer choice defaulted to off. |
| `selecting_theme → ready` | Valid theme and deterministic selection. | Show selected count and any shortage disclosure before start. |
| `ready → active(card 1)` | Start accepted. | Freeze cards/revisions/package/rules/seed/timer mode into run snapshot. |
| `active(card n) → feedback(card n)` | One valid submission or enabled-timer timeout. | Create one immutable attempt; prevent a duplicate submission from creating another. |
| `feedback(card n) → active(card n+1)` | Continue and `n < cardCount`. | Save resolved safe boundary before showing the next unresolved card. |
| `feedback(last) → results` | Continue after final resolution. | Commit result once; reopening is idempotent. |
| `active or feedback → paused` | Explicit pause, background/interruption, or app shutdown at safe boundary. | Persist current safe snapshot; timer stops; no answer is inferred or submitted. |
| `paused → active or feedback` | Resume compatible confirmed snapshot. | Restore exact card, resolved-feedback state if any, selection and timer mode; content cannot switch mid-round. |
| `paused → recovery` | Draft corrupt/incompatible or write interrupted. | Preserve last confirmed snapshot and offer resume it, discard draft, or return home; never overwrite silently. |

### Lifecycle deterministic fixtures

| ID | Input / action | Expected result |
| --- | --- | --- |
| `LIFE-FX-01` | Start `MIX-FX-01` with no timer choice. | Run records `timerMode=off`; no timeout is schedulable or shown. |
| `LIFE-FX-02` | Start `MIX-FX-01` with timer on; 12 active seconds; pause; wait 30 seconds; resume. | Elapsed value is 12 on pause and resume; 30 paused seconds are excluded. |
| `LIFE-FX-03` | Resolve card 1, then retry its submit command with same interaction ID. | One attempt/score event exists and active card is card 2 exactly once. |
| `LIFE-FX-04` | On active card 4, app backgrounds; process terminates; restart. | Restore the last confirmed active-card-4 snapshot with no inferred answer; timer remains stopped until resumed. |
| `LIFE-FX-05` | Resolve card 4, then storage write fails before promotion. | Keep prior confirmed snapshot, surface retry/continue-without-saving, and do not claim card 4 was saved. |
| `LIFE-FX-06` | A compatible package update arrives during an active `MF-1` run. | Current run continues on its frozen package; update stages for between rounds only. |
| `LIFE-FX-07` | Restart with corrupt draft but valid confirmed card-4 snapshot. | Quarantine draft and offer the confirmed snapshot or discard; do not silently start a different selection. |
| `LIFE-FX-08` | Complete and reopen a standard result with the same completed-run ID. | Return the stored result; no duplicate aggregate history, score, or milestone is created. |
| `LIFE-FX-09` | From home with compatible cached package, choose the `cup` theme and leave timer off. | Traverse `home → selecting_theme → ready`; ready state shows the deterministic `MIX-FX-05` IDs/count and its reuse disclosure before start. |
| `LIFE-FX-10` | Start the ready state in LIFE-FX-09. | Traverse `ready → active(card 1)` and commit frozen IDs/revisions, `MF-5`, selection seed, rule/package versions, and `timerMode=off`. |
| `LIFE-FX-11` | Resolve and continue cards 1–9 of LIFE-FX-01, then resolve and continue card 10. | Each of the first nine continuations traverses `feedback(card n) → active(card n+1)` after a safe save; the tenth traverses `feedback(last) → results` once. |
| `LIFE-FX-12` | Pause from feedback after resolving card 4, restart, and resume. | Traverse `feedback → paused → feedback`; card-4 feedback, explanation availability, and frozen selection are restored without a second attempt. |
| `LIFE-FX-13` | Detect an incompatible/corrupt draft while paused and choose the recovery route. | Traverse `paused → recovery`; retain the confirmed snapshot and show resume-confirmed/discard-draft/return-home choices. |

## Accessibility and release boundary

Every transition has a visible text state and an equivalent touch, pointer,
keyboard, and gamepad action. Focus is visible; pause/resume, timer state,
shortage disclosure, save success/failure, selected answer, correct/incorrect,
and explanation are never communicated by colour, animation, or audio alone.
Timer on/off is labelled, reversible before start, and compatible with reduced
motion and muted/captioned feedback. There is no ranked, daily, live, event,
account-only, or target-exclusive round mode in this scope.

Release validation requires exactly `TUT-FX-01`–`TUT-FX-08`,
`MIX-FX-01`–`MIX-FX-07`, and `LIFE-FX-01`–`LIFE-FX-13`, with each named tutorial
card and every lifecycle transition covered above. Published card facts and
answer rules remain subject to the editorial/provenance validation contracts.
