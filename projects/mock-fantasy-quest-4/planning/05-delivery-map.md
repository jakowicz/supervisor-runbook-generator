# 05 — Delivery map

**Inputs:** [product brief](../specification/01-product-brief.md), [feature model](../specification/02-feature-model.md), [technical contract](../specification/03-technical-contract.md), and [experience contract](../specification/04-experience-contract.md).

## Purpose and ordering

This is the implementation dependency map for the offline P0 campaign.  The
project workspace currently contains specification artefacts only; it has no
application source tree or selected framework.  Accordingly, the paths below
are *initial ownership boundaries* for the implementation repository rather
than claims about existing code.  Select the engine/framework, content format,
and final browser/device/performance matrix before their dependent work starts.

Tasks are deliberately small, reviewable increments.  Complete them in numeric
order unless their dependencies show that parallel work is safe.  `PW-*` paths
are reserved future Playwright paths; each browser-impacting task owns one
unique path and may not reuse another task's specification.

### Planned implementation layout

```text
src/core/                 deterministic, browser-free rules and state
src/content/              authored package types, source data, validation
src/platform/web/         storage, input, browser capability adapters
src/app/                  semantic shell, renderer integration, UI panels
public/                   manifest, icons, service-worker assets
tests/core/ tests/content/ tests/platform/ tests/app/
supervisor/browser/tests/changes/
docs/                     support, privacy, release, and authoring guidance
```

## Shared foundations

| ID | Bounded outcome | Depends on | Owns files / data | Verification |
| --- | --- | --- | --- | --- |
| DM-01 | Create the selected-framework project skeleton, deterministic test runner, lint/format commands, and the source/test directories above. | Approval of engine/framework | Root build/config files; `src/`; `tests/`; `docs/development.md` | Clean bootstrap; lint/format; one deterministic sample-core test. |
| DM-02 | Define immutable domain state, typed commands/results/events, revisions, interaction IDs, deterministic RNG state, and invariant helpers with no browser imports. | DM-01 | `src/core/{state,commands,events,invariants,rng}`; `tests/core/contract.*` | Unit tests prove command rejection is non-mutating and expected-revision checks reject stale requests. |
| DM-03 | Implement the versioned content-package types and build-time validator for IDs, references, localisation, asset manifest, quest predicates, rewards, and campaign reachability. | DM-01, DM-02; content-format approval | `src/content/{schema,validator,registry}`; `content/`; `tests/content/validation.*` | Valid-minimum package passes; one fixture per invalid reference class fails; graph test proves opening-to-ending reachability. |
| DM-04 | Author the original minimal Larkspur Reach / Glassroot Hollow content package: town, dungeon, dialogue, tutorial, quests, encounters, items, rewards, ending, base locale, and provenance records. | DM-03; content quantities/party-size approval | `content/base/`; `assets/source-manifest.*`; `docs/content-authoring.md` | Content validation passes; review confirms original provenance and one complete campaign path. |
| DM-05 | Implement atomic local snapshot repository: checksummed immutable revisions, current pointer, last-known-good retention, quarantine, delete semantics, and separately persisted preferences. | DM-02; storage-API/quota approval | `src/platform/web/persistence/`; `src/core/save/`; `tests/platform/persistence.*` | Fault-injection tests cover interrupted write, malformed snapshot, quota/permission failure, quarantine, and selected-slot deletion. |
| DM-06 | Implement save schema compatibility declarations and pure, ordered migration runner that promotes only validated candidates. | DM-03, DM-05 | `src/core/save/{schema,migrations,compatibility}`; migration fixtures in `tests/core/save/` | Every supported predecessor fixture migrates once; failed/unsupported migration preserves original quarantine data. |
| DM-07 | Establish error boundary, player recovery model, bounded local diagnostic record, consent/clear controls, and no-network guardrails. | DM-01, DM-05 | `src/app/recovery/`; `src/platform/web/diagnostics/`; `docs/privacy-and-recovery.md`; `tests/app/recovery.*` | Tests show retry/title/safe-recovery keep confirmed progress; diagnostics are absent without consent and exclude save/dialogue payloads. |

## Domain and campaign features

| ID | Bounded outcome | Depends on | Owns files / data | Verification |
| --- | --- | --- | --- | --- |
| DM-08 | Implement quest, dialogue, campaign, and tutorial state machines, including idempotent objective/reward/checkpoint ordering and ending completion. | DM-02, DM-03, DM-04, DM-05 | `src/core/{quest,dialogue,campaign,tutorial}`; `tests/core/campaign.*` | Tests cover repeated interaction, locked predicates, one-time rewards, tutorial progression, and ending transition. |
| DM-09 | Implement party, legal turn-based encounter resolution, visible turn events, defeat-to-checkpoint rule, and deterministic combat fixtures. | DM-02, DM-03, DM-05, DM-08 | `src/core/combat/`; `tests/core/combat.*` | Tests reject stale/illegal action or target without consuming a turn; deterministic win/loss and reward-once fixtures pass. |
| DM-10 | Implement inventory and authored party progression mutations: acquire, inspect, use/equip eligibility, quest-item protection, and duplicate-grant ledger behaviour. | DM-02, DM-03, DM-08, DM-09 | `src/core/{inventory,party,rewards}`; `tests/core/inventory.*` | Tests cover empty inventory, illegal use, protected quest items, ineligible targets, and duplicate grant rejection. |
| DM-11 | Implement scene exploration rules for collision, interactions, exits, encounter zones, and safe scene boundaries across exactly one town and one dungeon. | DM-02, DM-03, DM-04, DM-08, DM-09 | `src/core/exploration/`; `tests/core/exploration.*` | Scripted route traverses town to dungeon to ending; locked exit and missing/invalid content states fail safely. |
| DM-12 | Integrate core commands with the save/checkpoint coordinator so manual saves, authored checkpoints, rewards, scene exits, and recovery obey one safe-boundary policy. | DM-05, DM-06, DM-08–DM-11 | `src/core/session/`; `src/app/session/`; `tests/{core,app}/checkpoint.*` | Integration tests prove no unresolved combat is persisted, prior confirmed snapshot survives failed save, and resume restores a safe scene. |

## Web adapters, UI, input, and accessibility

| ID | Bounded outcome | Depends on | Owns files / data | Verification |
| --- | --- | --- | --- | --- |
| DM-13 | Build the responsive semantic application shell: title/new/continue/load navigation, pause/focus/visibility behaviour, game stage, panels, status messages, and error-boundary entry points. | DM-01, DM-07, DM-12 | `src/app/{shell,navigation,status}`; `tests/app/shell.*`; `supervisor/browser/tests/changes/dm-13-shell-navigation.spec.*` | App integration tests; Playwright covers no-save title state, panel return target, focus-loss pause, and phone/tablet/desktop shell reflow. |
| DM-14 | Deliver exploration, dialogue, quest, party, inventory, combat, and ending presentation bound only to core state/events, with readable empty/locked/invalid feedback. | DM-04, DM-08–DM-13 | `src/app/{game,panels,combat,dialogue}`; `tests/app/gameplay-ui.*`; `supervisor/browser/tests/changes/dm-14-gameplay-ui.spec.*` | State-driven UI tests; Playwright completes the tutorial battle and verifies empty inventory, locked exit, visible objective, and ending path. |
| DM-15 | Implement web input adapters for keyboard, mouse, touch, and feature-detected gamepad, all mapping to one action vocabulary with focus-safe repeat/debounce handling. | DM-02, DM-13 | `src/platform/web/input/`; `src/app/controls/`; `tests/platform/input.*`; `supervisor/browser/tests/changes/dm-15-input-adapters.spec.*` | Unit tests map each adapter to semantic actions; Playwright validates keyboard-only navigation, touch targets, pointer equivalence, and unavailable-gamepad fallback. |
| DM-16 | Implement settings and accessibility adaptations: text/spacing, contrast/non-colour cues, captions, audio, reduced motion, on-screen controls, locale fallback, semantic landmarks, accessible names, dialogs, and focus restoration. | DM-05, DM-13–DM-15; language/control-remapping/audio approvals as applicable | `src/app/{settings,accessibility,i18n}`; `tests/app/accessibility.*`; `supervisor/browser/tests/changes/dm-16-accessibility-settings.spec.*` | Automated accessibility scan plus keyboard/focus assertions; Playwright verifies settings persistence failure notice, 200% text/reflow, reduced motion, dialog Cancel default, and captions/contrast settings. |

## Distribution, trust, operations, documentation, QA, and release

| ID | Bounded outcome | Depends on | Owns files / data | Verification |
| --- | --- | --- | --- | --- |
| DM-17 | Add PWA manifest, install affordance, asset manifest/precache, offline status, known-good cache retention, and safe-boundary update activation independent from saves. | DM-04–DM-07, DM-12–DM-16; service-worker rollout approval | `public/{manifest,icons}`; `src/platform/web/pwa/`; service-worker/build config; `tests/platform/pwa.*`; `supervisor/browser/tests/changes/dm-17-pwa-lifecycle.spec.*` | Browser test covers uncached offline explanation, cached offline reload, declined/unavailable install, refresh failure retention, and update deferred until title/pause after confirmed save. |
| DM-18 | Add release hardening: build asset hashes, CSP/static-host headers, dependency/license/provenance review, parser/size bounds, and client secret scan. | DM-01, DM-03, DM-04, DM-17; hosting approval | Build/host config; `scripts/release-check.*`; `docs/security-and-provenance.md`; `tests/security/` | Release check verifies hashed manifest, CSP/header policy, no secret findings, dependency/provenance inventory, and hostile content/save payload rejection. |
| DM-19 | Define and automate quality evidence: core/content/persistence integration suite, target-browser matrix runner, responsive/accessibility manual checklist, offline/storage cases, and approval-gated performance measurement. | DM-01–DM-18; browser/device/budget approval | Test configuration; `docs/quality-plan.md`; `docs/test-matrix.md`; `supervisor/browser/tests/changes/dm-19-release-evidence.spec.*` | CI-equivalent local suite is green; Playwright smoke verifies primary start/save/resume path; documented manual matrix has evidence fields and clearly marks unapproved targets/budgets. |
| DM-20 | Produce player and operator release material: controls/help, save/recovery and privacy guidance, accessibility statement, support/version/cache status, content authoring/release checklist, rollback procedure, and release compatibility declaration. | DM-04–DM-19 | `docs/{player-guide,accessibility,privacy-and-recovery,release-runbook,rollback,content-authoring}.md`; in-app Help/Status copy | Documentation review against contracts; dry-run release/rollback using a known-good build without changing player saves. |

## Dependency summary

```text
DM-01 → DM-02 → DM-03 → DM-04
                  ├→ DM-05 → DM-06 → DM-12 → DM-13 → DM-14 → DM-15 → DM-16
                  ├→ DM-08 → DM-09 → DM-10 ─┐                         │
                  └→ DM-11 ─────────────────┘                         │
DM-05 → DM-07 → DM-13                                             DM-17 → DM-18 → DM-19 → DM-20
```

## Explicitly excluded or approval-gated work

The delivery map does **not** create account identity, remote saves/sync,
multiplayer, moderation/player safety services, live operations, analytics,
purchases, or entitlements.  These requests contradict the P0 offline local
campaign and require separate product, privacy, security, cost, support, and
failure-mode approval.  Exact engine, storage API, host/CDN, diagnostics
transport, content-editor format, languages, ratings/parental/regional policy,
supported browsers/devices/assistive technology, performance budgets, and
service-worker rollout policy remain decision gates—not invented requirements.
