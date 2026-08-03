# 02 — Feature model, domains, journeys, and release slices

**Inputs:** `INITIAL.md`, `PROJECT_BRIEF.md`, F001 discovery, and game identity.
This model resolves the generic story/battle wording as a bounded themed quiz
journey; it does not authorise an RPG campaign. Product decisions still marked
approval-gated remain outside a complete first release.

## Personas, jobs, and first-release promise

| Persona | Job / outcome | Journey supported |
| --- | --- | --- |
| Casual adult player | In a few minutes, test football knowledge and get a fair, satisfying result. | J1 start-to-results; J2 replay. |
| Returning player | Resume safely after interruption and see local improvement without redoing confirmed work. | J3 pause/recover/return. |
| Accessibility-settings user | Read, operate, and understand every answer/result with their preferred presentation and input. | J0 configure; J1. |
| Editorial contributor/reviewer | Produce original, factual, consistently adjudicated cards that are safe to release or correct. | J4 author-to-publish. |
| Release/support operator | Stage a content update or explain recovery without losing confirmed player state. | J5 update/recovery. |

**Complete first-release journey (J1):** launch → optionally configure → enter
the five-card `First Whistle` tutorial → answer/receive text-plus-audio/visual
feedback → pause at a safe boundary if needed → finish results → create a
confirmed local milestone/snapshot → exit and resume. It works with packaged
content offline and no account, multiplayer, purchase, live event, or deferred
dependency.

## Core journeys and edge paths

| ID | Normal flow | Empty / invalid / denied / offline / conflict / recovery / deletion behaviour |
| --- | --- | --- |
| J0 Settings and consent | Open settings before/during a round; changes apply immediately or next safe boundary and persist locally. | Invalid value restores last valid value with explanation. Optional diagnostic/notification denial leaves all play enabled. Reset settings confirms scope. |
| J1 First Whistle | New local profile → tutorial → submit each answer → adjudication/explanation → results/snapshot. | Blank typed input cannot submit until explicitly confirm blank; malformed typed input resolves via normalisation then gives correction. No network is needed. Failure before a confirmed boundary offers retry/return home. |
| J2 Standard round/replay | Choose available theme → deterministic 10-card selection → resolve → results → replay/choose/exit. | Empty eligible pool shows unavailable category and a different eligible choice; repeat shortage is disclosed. Invalid/stale content is ineligible. No ranked or remote conflict exists. |
| J3 Pause, resume, recovery, deletion | Pause or interrupt → save confirmed snapshot → reopen → resume before next unresolved card. | Write failure preserves previous confirmed snapshot and offers retry/continue unsaved. Corrupt draft offers last confirmed snapshot/discard. Delete profile explicitly confirms and removes local history/snapshots/settings then returns to first launch. Remote conflict is not applicable: sync is excluded. |
| J4 Editorial publish/correct | Propose → provenance → fact check → accessibility/copy edit → second review → versioned publish → validate → stage/release or rollback. | Missing provenance, ambiguous answer, failed validation, or reviewer rejection blocks publish. Rights/source uncertainty is escalated, not guessed. Offline authoring cannot publish. |
| J5 Update/error support | Download/stage approved batch → apply between rounds → retain confirmed save → record minimum diagnostic only with consent. | Offline stays on cached compatible batch. Incompatible cache explains reset after save protection. Permission-denied diagnostics are skipped. Failed update rolls back/stays current; no mid-round replacement. |

## Domain relationship map and invariants

```text
Editorial content ─publishes→ Content version ─selects→ Round run
     │ provenance/review                      │             │ attempts
     └── blocks invalid cards                  │             ├─→ Adjudication ─→ Score/streak ─→ Results/milestone
                                               │             │                         │
Platform/cache ─provides→ input/rendering ─────┘             └─→ Save snapshot ─→ Recovery/delete
     │                                                                        │
Accessibility/settings ─applies to all player-facing nodes ──────────────────┘
Release/diagnostics ─stages/observes versions and errors; never changes a live round
Decision-gated identity/sync/safety/commerce have no first-release runtime edge.
```

Cross-domain invariants: a resolved attempt references immutable card/version
and rule version; only published/reviewed cards may enter a round; score is a
deterministic projection of attempts; confirmed snapshots are append/replace
only after validation; content updates occur between rounds; local deletion
removes all local profile-linked records; accessibility settings affect every
path; diagnostics contain no answer text, typed answer, or unnecessary identity
data. Lifecycle boundaries are content publish/rollback, round start/resolution/
complete/abandon, snapshot confirmation/recovery/deletion, and cache stage/apply.

## Domain chapters

### A. Quiz shell, workflows, and player progress

**Entities/lifecycle:** `LocalProfile` (new → active → deletion-pending →
deleted), `RoundRun` (created → active ↔ paused → completed | abandoned |
recoverable), `QuestionAttempt` (presented → draft → submitted → resolved),
and `ResultSummary` (computed → viewed → archived). **Rules:** one unresolved
card at a time; a submission is immutable after resolution; results are
idempotent; replay creates a new run. **Inputs/dependencies:** content version,
selection seed, settings, persistence, input/rendering. **Outcome:** an
understandable quick session. **Edge cases:** back during draft asks whether to
discard; unavailable theme has an explanatory empty state; interruption creates
recoverable state only at safe boundaries. **Boundary:** tutorial plus one
standard template; no campaign, ranks, or social comparison.

### B. Question content, adjudication, and editorial production

**Entities/lifecycle:** cards/batches and review/provenance records are draft →
review → published → superseded/withdrawn; a withdrawn card never enters a new
round. **Rules:** schema, normalisation, quotas, provenance, two-editor review,
and anti-repeat policy are GAME-001–004. **Authoring:** bounded `QB-A-01…48`
and `TUT-01…05` cards with source/review fields; validators reject holes and
distribution violations. **Dependencies:** editorial workflow, release/version,
local repeat ledger. **Outcome:** fair topic breadth. **Edge cases:** disputed
fact/rights uncertainty blocks release; answer alias collision requires rewrite;
old run retains its referenced content version for explanation. **Boundary:**
no scraping, AI-generated unreviewed facts, live feed, or unbounded catalogue.

### C. Round rules, score, streaks, and feedback

**Entities/lifecycle:** definitions are versioned; run/attempt/score events
are created → resolved → summarised; streak resets per GAME-007. **Rules:**
five fixed tutorial cards, ten standard cards, 100 base points and capped streak
bonus; timer disabled by default. **Authoring inputs:** template, category,
seed, feedback strings/cues. **Dependencies:** eligible cards, adjudication,
save and accessibility. **Outcome:** transparent momentum, not punishment.
**Edge cases:** blank/malformed/timeout/abandon reset streak; no eligible card
creates empty state; versioned calculation prevents changed rules rewriting old
results. **Boundary:** no paid boosts, daily competition, leaderboard, event,
or difficulty multiplier.

### D. Persistence, offline cache, recovery, and privacy

**Entities/lifecycle:** snapshots draft → validated/confirmed → superseded →
deleted; cache staged → active → obsolete/reset; `RecoveryRecord` is open →
resolved. **Rules:** save only confirmed state at listed safe boundaries;
preserve prior confirmed state on failure; deletion is confirmed and complete.
**Inputs/dependencies:** platform storage, content version, optional diagnostic
consent. **Outcome:** trustworthy return play. **Edge cases:** quota/write
failure, process death, corrupt draft, cache mismatch, offline start, optional
permission denial, and local deletion are J3/J5. **Boundary:** local-only
profile/saves; remote identity/sync/conflict/retention is approval-gated.

### E. Presentation, input, accessibility, localisation, and original media

**Entities/lifecycle:** `Settings` is valid → applied → persisted/reset;
`InputAction` is mapped → invoked; media cue is available/muted/unavailable.
**Rules:** all critical actions have touch/pointer/keyboard/gamepad equivalent;
semantic focus/labels and non-colour outcomes are mandatory; visual settings,
text scaling, captions/text cues and reduced motion apply globally. **Authoring
inputs:** original category visual tokens, localisable string keys, captions,
cue metadata. **Dependencies:** shell, rendering/input adapters, settings.
**Outcome:** equitable readable play. **Edge cases:** unsupported gamepad falls
back visibly; missing audio leaves full text feedback; untranslated content is
not offered as a language. **Boundary:** original broadcast-inspired system
only; languages and exact audio asset count await approval.

### F. Delivery, targets, quality, and operations

**Entities/lifecycle:** `ContentVersion` draft → validated → staged → active →
rolled-back; `DiagnosticEvent` queued → consented/withheld → sent/discarded.
**Rules:** version switch only between rounds; cache refresh protects confirmed
save; errors offer retry/home; diagnostics minimise data. **Authoring inputs:**
release manifest, compatibility declaration, test evidence, privacy/store copy.
**Dependencies:** platform packaging/PWA cache, content, recovery. **Outcome:**
safe delivery on feasible networks. **Edge cases:** failed/partial update,
offline cache, compatibility failure, error-report denial, and rollback are J5.
**Boundary:** provider/CI/OS/browser matrix/performance and store policies await
approval; no live event operation.

## Target parity and adaptation

| Capability | Responsive web | PWA | Android / iOS | Invariant |
| --- | --- | --- | --- | --- |
| Quiz rules, cards, score, save semantics | Full shared core | Same | Same | No target-exclusive content or rule. |
| Input/layout | keyboard, mouse, touch, gamepad; responsive phone/tablet/desktop | browser-supported subset | touch; orientation TBD | Every action has an accessible equivalent. |
| Offline/update | browser cache subject to approved support | install, explicit offline/cache-refresh UX | packaged/cache path subject to delivery choice | Cached compatible content and confirmed save survive offline/update. |
| Accessibility/localisation | semantic web controls | same shared settings | platform accessibility integrations | Same outcome; platform affordance may differ. |
| Packaging/diagnostics | web compatibility/consent | install/cache safety | store/privacy/thermal/battery/size requirements | Exact matrices/budgets/vendors are gated, never silently weakened. |

## Prioritised feature catalogue and slices

| Priority / slice | Features | User outcome / journeys | Dependencies |
| --- | --- | --- | --- |
| P0 — first release | GAME-001–012; 53 bounded original cards; tutorial + standard round; adjudication, score/streak, feedback; settings/accessibility; local save/recovery/delete; offline cached play; original feedback; versioned delivery/error UI | Complete J0–J5 core; J1 has no deferred dependency. | Approved factual sources/bank size, target and packaging decisions where required. |
| P1 — later, approval required | Account identity, remote sync/conflict resolution, account deletion/retention, optional connected status | Cross-device return only after policy and backend approval. | Identity, privacy, security, outage and conflict policy. |
| P2 — deferred | Seasonal/live events, player-created/shared content, advanced analytics, advanced monetisation, purchases/entitlements, multiplayer/social features | New content/community/commercial outcomes, not core completion. | Operations, moderation/safety, store/refund, rights, and cost decisions. |
| Excluded | RPG campaign/battle/party; match simulation; copied reference expression | None; incompatible with discovered game identity. | None. |

## Open decisions retained for approval

Approve factual source/licensing policy and exact catalogue size; supported
OS/browser/device matrix, orientation, performance/battery/thermal/download
budgets; implementation/packaging stack and crash provider; language list and
audio quantity; account/sync/safety/commerce/live-operation policies. These
gates do not prevent an offline local first tutorial once its original reviewed
content and selected platform implementation exist.
