# Score, streak, and results bible

**Scope:** accepted design evidence for `GAME-007`, `GAME-008`, `GPI-010`, and
`GPI-011`. This is a deterministic future-core contract, not implementation or
production content. It consumes immutable `GAME-003` adjudication outcomes and
the frozen run/card sequence from `GPI-009`. A run ID, attempt ID, interaction
ID, and completion ID are stable UUID-like opaque values; retries reuse the
relevant ID and never derive a second event from timing, UI order, or a network
response.

## GPI-010 — score and streak contract

An attempt first resolves exactly once to one of `correct`, `wrong`, `blank`,
`timeout`, or `abandoned`. `blank` is an explicit confirm with no answer;
`timeout` may occur only when the player explicitly chose the enabled timer
mode; and `abandoned` records a deliberate abandon command, never an inferred
answer from pause, backgrounding, crash, or loss of focus. Pausing and recovery
therefore preserve the unresolved attempt and are not scoring outcomes.

`scoreBefore`, `streakBefore`, `scoreDelta`, `streakAfter`, and `scoreAfter`
are written to the immutable score event when the attempt resolves. The event
is the source of a reopened feedback or result surface; the score is never
recomputed from changed content or presentation settings.

| Resolved outcome | Score delta | Streak after resolution | Feedback state | Continue/recovery rule |
| --- | ---: | ---: | --- | --- |
| `correct`, streak before 0–1 | +100 | streak before + 1 | `correct_base` | Explanation and continue are available. |
| `correct`, streak before 2 | +125 | 3 | `correct_streak` | First streak bonus is +25; announce the three-in-a-row state. |
| `correct`, streak before 3 | +150 | 4 | `correct_streak` | Bonus rises to +50. |
| `correct`, streak before 4 | +175 | 5 | `correct_streak` | Bonus rises to +75. |
| `correct`, streak before 5 | +200 | 6 | `correct_streak_cap` | The bonus reaches its +100 cap. |
| `correct`, streak before 6 or more | +200 | streak before + 1 | `correct_streak_cap` | Bonus stays capped at +100; no further increase. |
| `wrong` | +0 | 0 | `incorrect` | Show canonical answer/explanation; player may continue or pause. |
| `blank` | +0 | 0 | `blank` | Explain that no answer was submitted; player may continue or pause. |
| `timeout` | +0 | 0 | `timeout` | Only valid with frozen `timerMode=on`; show the answer/explanation and continue/pause controls. |
| `abandoned` | +0 | 0 | `abandoned` | End this run recoverably; preserve its partial result and offer resume/replay/theme/exit as applicable. |

The active streak has no maximum. After a correct resolution, `bonus =
min(100, max(0, 25 × (streakAfter - 2)))`; thus the first three-correct streak
adds +25 and every later correct adds another +25 until the +100 cap. A correct
answer is worth at most 200 points. `scoreAfter = scoreBefore + scoreDelta`;
score is a non-negative monotonic total. `bestActiveSessionStreak` is the
maximum resolved correct streak in this run and never falls when the active
streak resets. A retry is a new `runId`; it retains aggregate history but never
overwrites the prior run's attempts or score events.

### Equivalent feedback requirements

Each feedback state exposes the same outcome in four independently useful
forms. Assets and cues may decorate these forms but cannot be the only carrier
of meaning.

| State | Required text and semantic label | Required non-colour visual | Caption/mute audio equivalent | Reduced-motion behaviour |
| --- | --- | --- | --- | --- |
| `correct_base` | “Correct. +100 points. Streak: N.” | Success icon/pattern plus labelled score panel. | If the correct cue plays, caption `Correct; 100 points; streak N`; mute leaves all text visible. | Static labelled state; no animation required. |
| `correct_streak` | “Correct. +[100 + bonus] points. Streak: N. Streak bonus +[25/50/75].” | Success icon/pattern plus a labelled streak marker. | Caption names correct result, points, streak, and bonus; mute changes no score information. | Replace celebration movement with static marker. |
| `correct_streak_cap` | “Correct. +200 points. Streak: N. Bonus capped at +100.” | Success icon/pattern plus labelled cap marker. | Caption names capped bonus and points; mute changes no score information. | Static cap marker; no pulsing or forced animation. |
| `incorrect`, `blank`, `timeout` | Outcome name, “+0 points”, “Streak reset”, canonical answer, and explanation. | Distinct labelled error/empty/time pattern; not red or animation alone. | Caption names outcome, zero points, reset, answer, and explanation availability; mute leaves this text visible. | Static feedback and controls. |
| `abandoned` | “Round ended. No points lost. Streak reset.” plus the recovery/next action. | Distinct labelled exit/interrupted pattern. | Caption names end state and next action; mute leaves this text visible. | Static end state and focusable action. |

Screen-reader semantics announce the same text once per resolved attempt. Focus
moves to the feedback heading, not an animation. All feedback includes visible
continue, pause, and where relevant replay/theme/exit actions with equivalent
touch, pointer, keyboard, and gamepad operation.

### Score and feedback edge fixtures

All fixtures start from a frozen `Mixed Fixture` run unless stated otherwise.
Each `resolve` command has a unique interaction ID, and a repeated command uses
the same one.

| ID | Input / action | Expected immutable record and visible outcome |
| --- | --- | --- |
| `SCORE-FX-01` | Correct with score 0, streak 0. | One event: `+100`, streak 1, score 100, `correct_base`; text/non-colour/caption equivalents agree. |
| `SCORE-FX-02` | From streak 1, correct. | One event: `+100`, streak 2, score rises by 100; no bonus message. |
| `SCORE-FX-03` | From score 200, streak 2, correct. | One event: `+125`, streak 3, score 325, `correct_streak`; text and caption name +25 bonus. |
| `SCORE-FX-04` | From score 325, streak 3, correct. | One event: `+150`, streak 4, score 475; bonus rises to +50. |
| `SCORE-FX-05` | From score 475, streak 4, correct. | One event: `+175`, streak 5, score 650; feedback names the +75 bonus. |
| `SCORE-FX-06` | From score 650, streak 5, correct; then from streak 6, correct again. | The first event is `+200`, streak 6, score 850, `correct_streak_cap`; the second is `+200`, streak 7, score 1050, proving the +100 cap does not rise. |
| `SCORE-FX-07` | From score 1050, streak 7, resolve `wrong`. | One zero-point event, active streak 0, score remains 1050, best streak remains 7; answer/explanation and static non-colour feedback are available. |
| `SCORE-FX-08` | From score 1050, streak 4, explicitly submit blank. | One zero-point `blank` event, active streak 0, score remains 1050; no answer is guessed and continue/pause remain available. |
| `SCORE-FX-09` | With frozen `timerMode=on`, from score 1050, streak 3, let the enabled timer expire. | One zero-point `timeout` event, active streak 0, score remains 1050; answer/explanation and static timeout feedback are available. |
| `SCORE-FX-10` | With frozen `timerMode=off`, wait beyond the configured duration. | No timeout, attempt, score event, or streak reset is created; card remains unresolved. |
| `SCORE-FX-11` | From score 450, streak 4, choose abandon; reopen the partial result. | One zero-point `abandoned` event/reset and one partial result; score remains 450, no completion milestone is awarded, and reopening returns that record. |
| `SCORE-FX-12` | Resolve a correct answer, then resend the same resolve command/interaction ID; enable mute and reduced motion before reopening feedback. | Exactly one attempt and score event exist; reopened feedback is static and text/non-colour equivalent remains complete with no audio required. |

## GPI-011 — results and local milestone contract

### Result states

| State | Trigger and required stored fields | Available actions | Milestone effect |
| --- | --- | --- | --- |
| `in_progress` | A run with frozen content/rules, score events, and a current safe boundary. | Resume, pause, abandon, return home only through a safe boundary. | None. |
| `completed_result` | Last resolved attempt is continued; immutable `ResultSummary` has `runId`, `completionId`, answered, correct, score, best active-session streak, category, outcome counts, and action labels. | Replay (new run), choose theme, exit, reopen result. | Tutorial only: request `first_whistle_complete`. |
| `abandoned_result` | Explicit abandon; immutable partial summary has the same fields plus `endedReason=abandoned`. | Resume only if a compatible safe snapshot precedes abandonment; otherwise replay, choose theme, exit, reopen result. | None. |
| `recovery` | Draft is corrupt/incompatible or a write was interrupted; last confirmed snapshot is retained. | Resume confirmed, discard draft, return home. | None until a real completion commits. |

`answered` counts immutable resolved attempts. `correct` counts only `correct`.
`score` and `bestActiveSessionStreak` copy the committed score-event ledger.
The summary identifies the frozen category, not a current theme label that may
change. It displays score, answered/correct, best active-session streak,
category, and labelled replay/choose-theme/exit actions. It has no rank, RPG
level, loot, social comparison, or account dependency.

### Completion and milestone idempotence

Completion is a single atomic logical operation keyed by `(runId, completionId)`:
write/retrieve the immutable `ResultSummary`, write/retrieve its aggregate
history entry, and, only for a completed tutorial, write/retrieve
`first_whistle_complete`. A duplicate command with that key returns the stored
objects unchanged. A completion command for a different run ID is not a retry;
it may create a distinct result and, for another tutorial run, returns the
existing milestone rather than a second one.

The `first_whistle_complete` milestone is a presence state keyed to the local
profile, not a counter. Its first stored value includes the source tutorial
run/completion ID and completion timestamp. Later tutorial completions may add
their own immutable history/result once, but cannot replace those provenance
fields or create another milestone. Reopen, restart, failed UI acknowledgement,
and recovery replay are reads unless they initiate a new run.

### Result and lifecycle fixtures

| ID | Input / action | Expected deterministic state and idempotence result |
| --- | --- | --- |
| `RESULT-FX-01` | Complete a standard 10-card run, then reopen using its run/completion ID. | One `completed_result`, history entry, and score ledger are stored; reopen returns them without any duplicate completion or milestone. |
| `RESULT-FX-02` | Complete `tutorial-v1` TUT-05, then repeat completion after restart with the same IDs. | Exactly one result/history entry and one profile `first_whistle_complete` presence state; retry returns both unchanged. |
| `RESULT-FX-03` | Explicitly abandon after card 4, restart, and open its result. | One `abandoned_result`, zero-point abandon event, and no completion milestone; partial score/history is recoverable and no attempt is inferred for card 5. |
| `RESULT-FX-04` | Pause at an unresolved card, background/terminate, restart, then resume and complete. | Restore the confirmed unresolved card with no abandon/blank/timeout event; later completion creates one result and eligible tutorial milestone only once. |
| `RESULT-FX-05` | On final-card completion, result write is interrupted; restart with a valid prior confirmed snapshot and corrupt draft. | Enter `recovery`, retain snapshot, offer resume-confirmed/discard-draft/return-home; no result or milestone is claimed until a successful completion commits. |
| `RESULT-FX-06` | Complete a tutorial, confirm deletion of local history/profile/snapshots, restart, and complete a new tutorial run. | Deletion returns to first launch and removes old local records only after confirmation; the new profile/run can create one new result and one new milestone, with no duplicate residual completion. |

## Release boundary

Release validation requires `SCORE-FX-01`–`SCORE-FX-12` and
`RESULT-FX-01`–`RESULT-FX-06`: exactly 18 fixtures. Wrong, blank, enabled
timeout, and explicit abandon are all recoverable outcomes with a monotonic
score and no duplicate completion. Pause, interruption, and recovery are not
substitutes for those outcomes and cannot silently manufacture an attempt.
