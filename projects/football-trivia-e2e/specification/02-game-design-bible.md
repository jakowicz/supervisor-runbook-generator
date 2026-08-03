# 02 — Game design bible

**Status:** bounded first-release proposal. This is an original 2D, solo
football-trivia game; it is not a football simulation, RPG, or social product.
The selected modules arise from the F001 discovery map and support the first
useful journey in `02-feature-model.md`.

## Game decision

| Archetype | Selected because | Explicitly not promised |
| --- | --- | --- |
| Football trivia / knowledge puzzle | The brief calls for themed football rounds, varied formats, validation, and a curated bank. | Licensed data feeds or copied questions. |
| Turn-based card-like quiz | One prompt is resolved before the next and supports touch, keyboard, mouse, and gamepad. | Board traversal, real-time action, or match play. |
| Single-player quick session | Casual adults need a useful session in a few minutes, including interruption-safe return. | Opponents, ranking, chat, or multiplayer. |

## Selected design systems

### Quiz content and editorial integrity — `GAME-001` to `GAME-004`

**Player outcome:** receive fresh, fair, answerable football questions with a
clear explanation. **Entities:** `QuestionCard`, `AnswerOption`,
`AcceptedAnswerRule`, `Category`, `Era`, `CompetitionScope`, `DifficultyBand`,
`ProvenanceRecord`, `ReviewRecord`, `ContentBatch`, and `RepeatLedger`.

| Unit | Design card / rule | First-release boundary and acceptance |
| --- | --- | --- |
| GAME-001 | **Question-card grammar.** An original card has one unambiguous fact, prompt, format, category, era/competition tags, difficulty 1–3, answer rule, short explanation, and review/version state. Formats: four-option select, true/false, ordered pair, and short typed answer. | Ship only reviewed `published` cards. A card without provenance, answer rule, explanation, or two-editor approval is ineligible. Test: each sampled card adjudicates its canonical and configured accepted answers identically. |
| GAME-002 | **Catalogue batch A: “Kickoff Mix.”** 48 original cards: 12 world tournament history, 12 domestic league moments, 12 club/manager/identity, 12 players/records. Each category has 4 cards at each band, max 6 cards per competition and no single club above 4. | Finite named release package: `QB-A-01` through `QB-A-48`, authored in four 12-card editorial batches. Exact facts, wording, sources, and rights clearance remain an editorial approval gate; placeholders never ship. Test: the manifest enforces totals, distributions, unique IDs, and no unpublished card. |
| GAME-003 | **Adjudication and provenance.** Select/true-false compare canonical IDs. Ordered pair compares ordered IDs. Typed answers normalise Unicode, case, punctuation, whitespace, diacritics, and configured aliases; it never uses fuzzy matching in release one. A rejected typed answer shows the canonical answer and explanation. | Each factual assertion links to a durable permitted source or approved internal research note, with checked date, reviewer, and correction history. Conflict or contested fact ⇒ remove from eligibility until resolved. Test: alias, malformed, blank, ambiguous, and outdated-version cases have fixtures. |
| GAME-004 | **Freshness.** The repeat ledger records card ID and completion timestamp locally. A round excludes cards seen in its last two completed rounds where alternatives exist; if insufficient eligible cards exist, it discloses reuse rather than silently failing. | No renewable feed, scraping, or live refresh. Authoring flow: propose → source/provenance → factual check → accessibility/copy edit → second review → publish to a versioned batch → validate → release/rollback. Test: seeded selection is reproducible and respects the exclusion rule. |

**Visual/audio/accessibility:** cards use original broadcast-inspired category
colour families plus text labels/patterns; no colour alone encodes category or
result. Readable scalable typography, screen-reader labels, captions/text
equivalents for cues, and a reduced-motion feedback path are required. Original
cue families: prompt arrival, correct, incorrect, streak rise, and saved state;
each has a mute/volume path and no cue conveys information unavailable in text.

### Round, score, and progress rules — `GAME-005` to `GAME-008`

**Player outcome:** complete a clear, fair themed round and understand a local
milestone. **Entities:** `RoundDefinition`, `RoundRun`, `QuestionAttempt`,
`AnswerSubmission`, `ScoreEvent`, `StreakState`, `TimerState`, `ResultSummary`,
`LocalMilestone`, and `SelectionSeed`.

| Unit | Design card / rule | First-release boundary and acceptance |
| --- | --- | --- |
| GAME-005 | **Round “First Whistle.”** Tutorial round contains 5 fixed, original tutorial cards (`TUT-01`–`TUT-05`) covering selecting, typing, feedback, explanation, and pause/save. It is intentionally non-timed. | This is the complete first useful journey. Completion creates/updates local milestone `first_whistle_complete`; it cannot require account, network, purchase, or deferred content. Test: a new local profile can complete it offline and resume after app restart. |
| GAME-006 | **Round “Mixed Fixture.”** A 10-card themed round draws from one selected category or the Kickoff Mix, with no more than two adjacent cards sharing format or difficulty. The player may pause; a displayed timer mode is optional and defaults off. | First release ships one tutorial and one configurable standard round template, no ranked/daily/live/event modes. Test: deterministic seed produces ten eligible cards and valid format alternation or records the shortage. |
| GAME-007 | **Scoring and streak.** Correct = 100 points; a consecutive-correct streak of 3+ adds 25 points to each later correct answer, capped at +100. Incorrect, timeout (only if enabled), blank submission, or abandon resets the active streak; score never decreases. Explanation is available after resolution. | No paid boosts, leaderboard, social comparison, or opaque difficulty multiplier. Test: table-driven sequence proves cap, reset, and per-attempt result; a retry is a new run, not an overwrite of history. |
| GAME-008 | **Result and return.** Results show answered/correct, score, best active-session streak, category, and next action: replay, choose theme, or exit. Progress is local milestones and aggregate history only, not RPG levels. | An interrupted run persists at a safe boundary before the next unresolved question. Completed result is idempotent: reopening cannot award twice. Test: complete/reopen, abandon/resume, corrupted draft, and delete-history paths are specified. |

**Dependencies:** GAME-005 needs published tutorial cards and persistence;
GAME-006 needs GAME-001–004; GAME-007 consumes adjudication events; GAME-008
consumes score events and save/recovery. Visual family is bold category panels,
neutral answer controls, and non-colour success/error indicators; audio is
supportive, optional, and captioned.

### Accessible, recoverable multi-target experience — `GAME-009` to `GAME-012`

**Player outcome:** start, control, interrupt, recover, and return to a round
confidently on a supported surface. **Entities:** `LocalProfile`, `Settings`,
`SaveSnapshot`, `RecoveryRecord`, `ContentVersion`, `ErrorNotice`,
`InputAction`, `InstallState`, and `DiagnosticEvent`.

| Unit | Design card / rule | First-release boundary and acceptance |
| --- | --- | --- |
| GAME-009 | **Guided start.** First launch offers an accessible plain-language tutorial entry, settings access, and a local profile without sign-in. Controls map select/navigate/confirm/back/pause to touch, pointer, keyboard, and gamepad. | No mandatory account. Permission denial for optional notifications/diagnostics changes no game path and explains how to alter it later. Test: every critical action is operable with keyboard and touch, focus is visible, and gamepad has an equivalent mapping. |
| GAME-010 | **Save/recovery.** Save immutable confirmed snapshots at tutorial completion, resolved question boundaries, explicit pause, and completed results. On failed write, retain the last confirmed snapshot and show retry/continue-without-saving. On corrupt draft, offer last confirmed snapshot or discard draft; never silently overwrite. | Remote sync/conflict requires approval and is excluded. Local deletion requires confirmation, names its effect, clears local profile/history/snapshots, and returns to first launch. Test: write failure, crash/restart, corrupt draft, and deletion fixtures preserve stated invariants. |
| GAME-011 | **Offline/update/error.** The installed content batch and current snapshot remain playable offline. A new content version is staged between rounds; an incompatible cache reports recovery steps and preserves confirmed save before cache reset. Unexpected errors show a plain-language retry/return-home path and optional minimised diagnostic consent. | No background live content requirement. Test: offline launch with cached assets, update mid-round, unavailable content, and diagnostic permission-denied behaviours are covered. |
| GAME-012 | **Platform adaptation.** Shared rule/content/save semantics on responsive web, PWA, Android, and iOS. Web adds pointer/keyboard/gamepad and responsive layouts; PWA adds install/offline cache/update UX; phones add touch targets and approved portrait/landscape choice. | No target-exclusive questions or rule differences. OS/browser matrix, orientation, performance, battery, thermal, size, store/privacy declarations, crash vendor, and exact language set remain approval gates. Test: capability matrix is exercised once targets are chosen. |

Accessibility applies to all three systems: text-size and contrast settings,
reduced motion, captions/text equivalents, non-colour result encoding, focus
order, semantic labels, sufficient touch targets, and no time limit by default.
Localisation inputs are externalised prompt, answer, explanation, category, and
UI strings; only a future approved language may add translated content after
answer aliases and factual review are validated.

**Experience production package:** a finite first-release package contains the
five named tutorial cards, one settings/help copy set, input-action labels,
result/recovery/empty-state strings, category visual tokens, and five original
optional cue families. Its workflow is interaction specification → accessible
copy/caption and focus review → original art/audio production → target
adaptation → keyboard/touch/gamepad and offline/recovery acceptance checks.
It depends on the shared shell, settings, persistence, renderer, and target
adapters; it cannot depend on an account, remote service, or purchase.

## Journey and implementation-domain crosswalk

| Units | First-release journeys | Implementation domains |
| --- | --- | --- |
| GAME-001–004 | J1/J2/J4 (and J5 for versioned batch) | B content/adjudication; F delivery for batch lifecycle |
| GAME-005–008 | J1/J2/J3 | A shell/progress; C rules/score/feedback; D persistence for return |
| GAME-009–012 | J0/J1/J2/J3/J5 | D recovery, E accessibility/input/presentation, F delivery/targets |

The machine-readable `implementation_map` in the companion JSON maps every
individual `GAME-*` unit, rather than treating this grouped table as a substitute.

## Rejected and decision-gated modules

| Module | Decision | Why |
| --- | --- | --- |
| Narrative/world; characters/factions; quests/scenes/dialogue | Rejected | The brief supports themed quiz progression, not fictional story content. |
| Combat/encounters/bosses; classes/abilities/status effects | Rejected | No action, battle, party, or power-progression player activity is evidenced. |
| Units/buildings/resources; economy | Rejected | No construction, collection, or economy loop; IAP is not authorisation for an economy. |
| Levels/maps; puzzles beyond trivia | Rejected | Questions/rounds are the bounded puzzle surface; no traversal or board design is required. |
| Racing/sport rules or football match simulation | Rejected | Football is subject matter, not simulated play. |
| Multiplayer; social/safety | Decision-gated | Brief names services/safety but selects single-player and gives no mode, age, moderation, reporting, or retention policy. |
| Live content | Decision-gated/deferred | Seasons/events are deferred; editorial batches can ship without a live schedule. |
| Commerce/entitlements | Decision-gated/deferred | Purchases are named but monetisation is deferred and store/refund policy is absent. |
| Narrative content model | Not created | Narrative module is not selected; inventing premise, characters, or a script would violate scope. |

All expression is original. Functional references may inform topic breadth and
short-session goals only; they supply no copied questions, wording, assets,
layouts, audio, or interaction choreography.
