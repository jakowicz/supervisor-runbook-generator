# Product brief — football-trivia-e2e

**Source of truth:** [`INITIAL.md`](INITIAL.md). This normalized brief preserves
its scope; it records unknowns and contradictions instead of choosing them.

## Problem, category, users, and outcome

Casual adult football followers need a satisfying way to test and extend their
knowledge in a few mobile-friendly minutes. This is an original 2D,
single-player football-trivia puzzle with themed rounds, varied question
formats, answer validation, score/streak feedback, local progress, and a
curated question bank.

The first useful session succeeds when a player completes an onboarding round,
understands accepted/rejected feedback and score/streak, then saves and resumes.
This is the quiz equivalent of the source's generic “first battle” text; a
literal battle/campaign is a decision, not assumed scope.

## First-release and roadmap scope

First release: playable themed rounds; tutorial; question formats and answer
rules; accessible feedback; scoring/streaks; anti-repetition; local
progress/save/load/resume/recovery; settings/accessibility; original
audio/visual feedback; curated, reviewed, versioned question content; content
delivery; and crash/error recovery. Named account/identity, multiplayer safety,
live operations, and purchases are decision-gated, not automatic dependencies.

Success is measurable when a new player can complete onboarding, play an
authored round, get deterministic answer/score feedback, save and restore
confirmed progress, and recover from interruption or a safe update without
silent loss on every selected target. Every shipped question has category,
format, answer rule, difficulty, provenance/review record, and repeat-eligibility
metadata. Bank size, completion cadence, and performance thresholds are open.

Deferred: live/seasonal events, player-created/shared content, advanced
analytics, and advanced monetisation. Non-goals: copied branding, assets,
questions/copy, layouts, or distinctive interactions; and unapproved RPG world,
party, quest, combat, boss, or literal battle systems.

## Target systems

| Target | First-release role | Input model | Delivery constraint | Out of scope |
| --- | --- | --- | --- | --- |
| Responsive web app | Full shared game on phone, tablet, desktop. | Keyboard, mouse, touch, gamepad. | Responsive compatibility and performance budget to be approved. | Separate web ruleset/campaign. |
| PWA | Installable form of the same game. | Supported browser/device inputs. | Offline content/saves and safe cache refresh that protects confirmed progress. | Always-online dependency or PWA-only mode. |
| Android phone | Compatible packaged mobile delivery of shared core. | Touch; orientation undecided. | Battery, thermal, size, privacy, packaging, store rules. | Android-exclusive game content. |
| iPhone (iOS) | Compatible packaged mobile delivery of shared core. | Touch; orientation undecided. | Battery, thermal, size, privacy, packaging, store rules. | iOS-exclusive game content. |

Use a shared core with necessary platform adaptations only. Remote
account-linked state may use a safe local cache where approved, and must not
silently discard confirmed single-player progress.

## Constraints, assumptions, and reference boundary

Explicit constraints: accessible controls/text/captions/visual settings;
save/resume/data-loss recovery; crash reporting/player recovery; web/PWA plus
Android/iOS; feasible slow-network behaviour; localisation/privacy/platform
requirements; and original expression. Safe assumptions: independently authored
content/UI/art/audio; editorial fact review; locally available approved content
supports a basic session; outages are clear; and diagnostics minimise personal
data. No stack, vendor, backend, account, retention, or licensing choice is
approved by these assumptions.

| Reference | Allowed functional learning | Prohibited |
| --- | --- | --- |
| The Athletic | Football-topic breadth and varied quiz formats. | Brand, questions/copy, assets, layouts, editorial structure, screens, and interactions. |
| QuizUp | Broad goal of short competitive-feeling trivia sessions. | Brand, questions/copy, assets, layouts, flows, social systems, and interaction choreography. |

## Human approval decisions

1. Is generic “story/campaign” and “first battle” text real scope, or should a
   lightweight themed quiz journey replace it?
2. For account identity, multiplayer safety, live operations, and purchases:
   choose release-critical, optional connected enhancement, or deferred.
3. Decide account/authentication, sync/conflicts, retention/deletion, recovery,
   outage, safety/moderation, age/region, refund/entitlement policies if any
   connected or commerce feature ships.
4. Choose delivery approach, OS/browser/device matrix, orientation, budgets,
   update/crash provider/cost model, and Android/iOS packaging path.
5. Approve question-bank size, coverage, source/licensing/provenance, refresh,
   adjudication, languages, and exact accessibility/audio scope.
