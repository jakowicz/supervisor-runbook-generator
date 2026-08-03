# 01 — Game identity

**Status:** first-release game layer, before genre-specific content planning.

## Pillars and stable design units

| ID | Unit | Commitment |
| --- | --- | --- |
| GAME-001 | Fast football knowledge | Enter a themed trivia round and make repeated answer decisions in a quick mobile-friendly session. |
| GAME-002 | Fair, legible adjudication | Every question has an answer rule and communicates result, score change, and feedback accessibly. |
| GAME-003 | Momentum without punishment | Scores/streaks create tension; wrong answers are recoverable and results are understandable. |
| GAME-004 | Curated variety | Authored categories, formats, difficulty, and anti-repetition make short sessions fresh. |
| GAME-005 | Trustworthy return play | Local progress, save/resume, approved offline content, settings, and recovery support safe return. |

## Fantasy, loop, sessions, and progression

Player fantasy: be the person who spots the football answer before the clock,
builds a run of confident calls, and improves their knowledge. Verbs: **read or
listen**, **recall**, **select or enter**, **confirm**, **review**, **continue**.
Loop: choose/receive theme → consume prompt → submit → adjudication and
accessible feedback → update score/streak/progress → next suitable prompt →
finish or safely resume. Sessions are short, interruptible rounds with
onboarding first, an objective, question sequence, results, and saved return
state. Progression promises broader knowledge and local milestones, not levels,
equipment, traversal, or combat power.

The emotional arc is curiosity, competence, mounting stakes, then celebration
or useful recovery. Audience: casual adult football-interested players using
touch, keyboard, mouse, gamepad, captions, adjustable text, and visual settings.

## game-design-signals

| Signal | Classification and evidence | Design consequence |
| --- | --- | --- |
| Archetype | Football trivia/puzzle/turn-based card-like quiz; source names trivia, formats, and checked puzzle/card/board/turn-based. | Questions, rounds, answers, and results—not action/adventure content. |
| Primary activity | Recall/recognise and answer; source names validation and feedback. | Input, adjudication, explanations, and score rules. |
| Session model | Quick mobile sessions with local progress/save. | Short lifecycle and interruption-safe state. |
| Knowledge source | Curated editorial football bank. | Provenance, review, categories, difficulty, refresh. |
| Social model | Single-player; multiplayer is undefined. | No opponents, matchmaking, chat, co-op, rankings, or social graph in core. |
| Creative intensity | Editorial questions/feedback high; fictional narrative low. | Question tooling, not lore/character pipeline. |

## Candidate module decision record

| Module | Decision | Rationale |
| --- | --- | --- |
| Question provenance/categories/formats/difficulty/answers/explanations | Selected | Necessary for curated themed trivia and validation. |
| Round/mode rules, scoring/streaks, results, anti-repetition, milestones | Selected | Named or necessary for replayable short sessions. |
| Onboarding, accessibility, input, save/recovery, web/PWA/mobile delivery | Selected | Explicit shared and target requirements. |
| Editorial refresh and validation tooling | Selected candidate | Factual curated content needs correction and quality controls; cadence awaits approval. |
| Accounts/sync, multiplayer safety, live ops, commerce | Requires decision | Named but conflicts with core and lacks policy. |
| RPG world/party/quests/combat/jobs/enemies/bosses/equipment/locations | Rejected | Not evidenced; generic campaign/battle wording is a decision, not scope. |
| Builder economy/construction; racing physics; match simulation; platforming | Rejected | No player-activity evidence. |

Completion is an accessible results state with score, streak outcome, and next
step; an interruption becomes safe resumable state where supported. Narrative,
competitive-rank, and seasonal completion are outside first release unless an
approval decision changes this identity.
