# 00 — Domain discovery

**Sources:** [`INITIAL.md`](../INITIAL.md), [`PROJECT_BRIEF.md`](../PROJECT_BRIEF.md),
and [`01-game-identity.md`](01-game-identity.md). Labels are **explicit**
(direct request), **implied** (needed to fulfil it), **assumed** (reversible
guardrail), **deferred** (stated later scope), and **requires-decision**
(consequential unknown).

## game-design-signals and module boundary

| Signal | Classification | Brief evidence |
| --- | --- | --- |
| Archetypes | Football trivia, puzzle, turn-based/card-like quiz; 2D single-player. | Creation statement and checked characteristics. |
| Primary activity | Recall/recognise, choose or enter, confirm, review football answers. | Themed rounds, formats, validation, feedback. |
| Session model | Short mobile-friendly themed rounds with save/resume. | Quick mobile sessions and local progress. |
| Knowledge source | Curated editorial first-release question bank. | Explicit bank requirement. |
| Competitive/cooperative model | Single-player; connected multiplayer unresolved. | Checked single-player; services named separately. |
| Creative intensity | Editorial trivia/feedback high; fictional narrative/world low. | Trivia focus versus generic campaign/battle text. |

Selected candidates: question-bank/editorial QA, round/mode rules, answer
adjudication, scoring/streaks, anti-repetition, onboarding, progress/save,
accessible input/presentation, target delivery, original feedback assets,
release/content operations, and quality engineering. Rejected: RPG
world/party/boss/quest/combat/equipment; builder systems; racing or football
match simulation; platforming; and unapproved social play. Accounts,
multiplayer, live operations, and commerce are decision-gated, never selected
merely because common games include them.

## Candidate system map

| Discipline / system family | Label | Rationale | Source reference |
| --- | --- | --- | --- |
| Quiz shell, navigation, pause, lifecycle, results | implied | Quick playable rounds need entry, completion, exit, interruption. | Creation; quick mobile sessions |
| Round/theme/mode rules and local milestones | explicit | Themed rounds, playable loop, local progress. | Creation; required capabilities |
| Question schema: formats, categories, difficulty, answer rules, adjudication | explicit | Formats, validation, curated bank are direct. | Creation |
| Editorial workflow: provenance, fact review, correction, refresh | implied | Curated factual questions require accountable review/correction. | Curated question bank |
| Scores, streaks, feedback/explanations, anti-repetition | explicit | Scores/streaks/feedback named; repeat control enables variety. | Creation |
| Onboarding/tutorial and player guidance | explicit | Required capability. | Required first-release capabilities |
| Save/load/resume, persistence, migrations, data-loss recovery | explicit | Direct shared and first-release requirement. | Shared; required capabilities |
| Responsive 2D rendering, input adapters, browser performance | explicit | 2D, responsive web, keyboard/mouse/touch/gamepad. | Characteristics; web requirements |
| PWA installation, offline assets/content, cache/update safety | explicit | Direct PWA requirement. | PWA requirements |
| Android/iOS packaging, touch/orientation, mobile budgets | explicit | Both targets named. | Android/iPhone requirements |
| Accessibility: controls, text, captions, visual settings, focus/reduced motion | explicit | Direct shared requirement. | Shared requirements |
| Localisation and language-content pipeline | explicit | Localisation named; languages unknown. | Cross-platform decisions |
| Original visual/audio feedback and asset pipeline | explicit | Feedback and art direction named. | Required capabilities; art direction |
| Content delivery/versioning/validation/rollback communication | implied | Curated content and updates need controlled release. | Content delivery; PWA requirements |
| Crash diagnostics, error boundaries, recovery UI, support triage | explicit | Crash reporting and player recovery are direct. | Shared; required capabilities |
| Quality: correctness, adjudication, persistence, offline/update, accessibility, compatibility, performance | implied | Each promise needs validation beyond screens. | Targets; shared requirements |
| Privacy/security, consent, minimisation, retention/deletion | explicit | Privacy required; accounts/diagnostics may process data. | Constraints; cross-platform decisions |
| Account identity, remote sync, conflicts | requires-decision | Named but no policy or local-state relationship. | Required capabilities; data policy |
| Multiplayer safety, reporting, moderation, community operations | requires-decision | Named but conflicts with single-player and lacks mode/policy. | Characteristics; required capabilities |
| Live-service status, incident response, event tooling | requires-decision | Named while events are deferred, operating model absent. | Required/deferred capabilities |
| Purchases, catalogue, entitlements, refunds, compliance | requires-decision | Named while monetisation deferred, policy absent. | Required/deferred capabilities |
| Advanced analytics | deferred | Explicit later scope; crash diagnostics remain required. | Later capabilities |
| Seasonal/live events and player-created/shared content | deferred | Explicit later scope. | Later capabilities |
| Engine/framework, vendors, CI/CD, costs, support matrix/budgets | requires-decision | No technical/testable baseline authorized. | Constraints; target requirements |
| Campaign/story/battle content | requires-decision | Generic user outcome conflicts with specific trivia request. | Users; first useful session |

## Conclusions, assumptions, and gates

The minimal release depends on quiz shell, authored validated content,
round/adjudication/score rules, local persistence, rendering/input,
accessibility, original feedback, target delivery, recovery, release controls,
and focused QA. Editorial tooling is required as a candidate enabling discipline,
but workflow/operations cadence is not selected.

Safe assumptions: independently authored expression; shared core with adapted
inputs; locally available approved content supports a basic session; confirmed
local saves are protected where storage permits; approved remote features fail
visibly; and diagnostics minimise personal data. These do not approve a vendor,
backend, account model, retention policy, or fact-licensing arrangement.

Human approval is required for campaign/battle framing; connected/account/sync
scope; multiplayer/community safety; commerce; question sources/licensing/bank
size; languages/audio quantities; target matrices/budgets; stack/vendors;
store/legal policy; and live-operations ownership. Decision-gated systems must
not block the single-player trivia core or introduce RPG scope.

## Reference boundary

The Athletic and QuizUp may inform only football-topic breadth, varied quiz
formats, and the broad goal of short trivia sessions. They never authorize
copied brands, questions/wording, assets, layouts, screen composition, audio,
social copy, interaction choreography, or other distinctive expression. All
content, mechanics expression, UI, visual, and audio work must be original.
