# 05 — Delivery map

**Inputs:** discovery, game identity/bible, creative/asset/audio direction,
technical contract, and [production inventory](game-production-inventory.md).
The repository currently contains specifications and Supervisor tooling, not an
application source tree. Paths below are deliberate future ownership boundaries,
not claims that code already exists. Complete the gated G design collection
before F006; never substitute placeholders for `GPI-*` content or creative IDs.

## Planned layout and dependency rule

```text
src/core/       deterministic quiz, content, scoring, lifecycle and save rules
src/content/    authored QB/TUT sources, schemas, provenance and validators
src/platform/   web/PWA and native-wrapper input, storage, cache, audio adapters
src/app/        accessible responsive shell, views, settings, feedback
assets/         original visual/audio source, manifests and reviewed renders
tests/          core, content, platform, app and release evidence
docs/           editorial, accessibility, privacy, support and release evidence
```

Each `PW-*` path is reserved exclusively for its row. Target budgets, framework,
store accounts, signing, and service vendors remain approval gates; the shared
offline client may proceed without inventing them.

## Shared foundations and real creative inputs

| ID | Bounded outcome | Depends on | Owns files/data | Verification |
| --- | --- | --- | --- | --- |
| DM-01 | Bootstrap selected client framework, deterministic tests, lint/format, and directory boundaries. | stack approval | root config; `src/`; `tests/`; `docs/development.md` | Clean bootstrap and sample pure-core test. |
| DM-02 | Implement immutable commands/events/state, revisions, interaction IDs, seeded RNG, and invariants without platform imports. | DM-01 | `src/core/{state,commands,events,invariants,rng}` | Unit tests reject stale/illegal commands without mutation. |
| DM-03 | Implement versioned content schema/import validator and immutable package manifest. | DM-01–02; GPI-001 | `src/content/{schema,validator,registry}`; `content/`; `tests/content/` | Valid minimal package passes; one negative fixture per reference/status failure fails. |
| DM-04 | Produce and validate GPI-001 plus all four named Kickoff Mix batches GPI-002–005, including two-review and rights/source records. | DM-03; accepted G evidence | `content/cards/`; `content/provenance/`; `tests/content/editorial.*` | 48-card quota/cap/source/review/locale validator report. |
| DM-05 | Produce and validate TUT-01–05, GPI-008, as a fixed accessible offline tutorial package. | DM-03–04; accepted G evidence | `content/tutorial/`; tutorial fixtures | Every named card resolves and tutorial fixture completes once. |
| DM-06 | Implement GPI-006 adjudication and GPI-007 eligibility/anti-repeat policy. | DM-02–04; accepted G evidence | `src/core/{answer,selection}`; fixtures | Alias/blank/ambiguous/withdrawn and seeded-shortage tests. |
| DM-07 | Create original P0 visual sources for `ASSET-SHL/QZ/UI/FBK/SYS-001` families, variants, alt/meaning records, checksums, and review ledger. | DM-03; GPI-001, 008–014 | `assets/visual/`; `assets/manifest.*`; `tests/content/assets.*` | Provenance, contrast, 200%/high-contrast/reduced-motion and missing-asset checks. |
| DM-08 | Generate/select original P0 `AUDIO-*` cues, captions/descriptions, manifests, accessibility fallbacks, and provenance/review records. | DM-03; accepted G evidence | `assets/audio/`; `assets/audio-manifest.*`; `tests/content/audio.*` | Trigger/caption/mute/duration/checksum/licence validation; no audio-only meaning. |
| DM-09 | Implement content/asset/audio registry resolving only reviewed manifest IDs and safe optional-media fallback. | DM-03–08 | `src/content/{assets,audio,package}`; integration fixtures | Missing optional media falls back; missing required/package-invalid media rejects new round. |
| DM-10 | Implement revisioned confirmed local snapshot repository, migration runner, quarantine/delete, and local consent-gated diagnostics. | DM-02–03 | `src/core/save/`; `src/platform/storage/`; `tests/{core,platform}/save.*` | Fault injection preserves last confirmed save and excludes prompt/answer payloads. |

## Core quiz features and UI/input integration

| ID | Bounded outcome | Depends on | Owns files/data | Verification |
| --- | --- | --- | --- | --- |
| DM-11 | Implement First Whistle lifecycle and one-time local milestone from GPI-008. | DM-02, 05–06, 10 | `src/core/tutorial/`; `tests/core/tutorial.*` | Offline start, resolve, restart, and idempotent milestone tests. |
| DM-12 | Implement Mixed Fixture lifecycle and GPI-009 deterministic eligible 10-card selection. | DM-02, 04, 06, 10 | `src/core/round/`; `tests/core/round.*` | Seeded selection, optional timer, pause, shortage and safe-boundary tests. |
| DM-13 | Implement GPI-010 score/streak and GPI-011 result events with explainable feedback. | DM-06, 12 | `src/core/{score,results}`; fixtures | Cap/reset/blank/abandon/non-decreasing/idempotent-complete tests. |
| DM-14 | Build responsive semantic shell: profile, home, tutorial/round entry, pause, results, error boundary, and focus/visibility state. | DM-01, 10–13 | `src/app/{shell,navigation,recovery}`; `PW-14-shell.spec.*` | App tests; `supervisor/browser/tests/changes/pw-14-shell.spec.*` covers no-save, resume, reflow and focus return. |
| DM-15 | Build card, choice, typed-answer, confirm, explanation, score/streak, and result surfaces wired to real GPI content and media IDs. | DM-07–09, 11–14 | `src/app/{quiz,feedback,results}`; `PW-15-round.spec.*` | State-driven tests; `PW-15` completes tutorial and standard round with media unavailable. |
| DM-16 | Map touch, pointer, keyboard, and feature-detected gamepad to one semantic action vocabulary. | DM-02, 14 | `src/platform/input/`; `src/app/controls/`; `PW-16-input.spec.*` | Adapter fixtures; `PW-16` checks keyboard-only, touch, pointer and unavailable gamepad. |
| DM-17 | Implement GPI-012 settings/accessibility: scale/spacing/contrast, captions, reduced motion/sensory feedback, visible focus, labels, dialogs and locale fallback. | DM-08, 12, 14–16 | `src/app/{settings,accessibility,i18n}`; `PW-17-accessibility.spec.*` | Automated scan plus `PW-17` 200% reflow, caption/mute, contrast, reduced-motion and focus tests. |
| DM-18 | Integrate GPI-013 recovery panels and snapshot coordination at resolved, pause, and result boundaries. | DM-10–15 | `src/app/recovery/`; `src/core/session/`; `PW-18-recovery.spec.*` | Fault tests; `PW-18` shows write-failure, corruption and confirmed-delete choices. |

## Target adapters, operations, trust, release, and evidence

| ID | Bounded outcome | Depends on | Owns files/data | Verification |
| --- | --- | --- | --- | --- |
| DM-19 | Implement responsive-web/PWA adapter: manifest, install, cache, offline status, known-good retention, and between-round update gate. | DM-04, 09–10, 14–18 | `public/`; `src/platform/{web,pwa}`; `PW-19-pwa.spec.*` | `PW-19` covers uncached explanation, cached play, install unavailable, deferred update and failed refresh retention. |
| DM-20 | Implement Android/iOS wrapper adapters only after packaging/orientation/budget/store approval; preserve shared-core parity from GPI-015. | DM-15–19; mobile approvals | `src/platform/{android,ios}`; `docs/target-matrix.md` | Device matrix demonstrates rule/content/save parity and explicit adaptations. |
| DM-21 | Integrate visual/audio loading, trigger routing, volume/mute/audio-focus, captions, reduced feedback, and platform interruption behaviour. | DM-07–09, 15–17, 20 as applicable | `src/platform/audio/`; `src/app/media/`; `PW-21-media.spec.*` | `PW-21` checks triggers once, mute/caption equivalence, unavailable audio, reduced feedback and cache fallback. |
| DM-22 | Add privacy/trust/release checks: provenance, licences, dependency scan, asset/package hashes, parser/size limits, CSP/static headers, no-secret check. | DM-03–10, 19 | `scripts/release-check.*`; `docs/{privacy,provenance,security}.md`; `tests/security/` | Release check rejects hostile content/save and incomplete creative record. |
| DM-23 | Create editorial operations, correction/withdrawal/rollback and player-support documentation. | DM-04–10, 18–22 | `docs/{editorial,content-release,player-guide,recovery}.md` | Tabletop correction and known-good rollback preserve active round/save. |
| DM-24 | Assemble quality evidence: core/content/persistence, accessibility, browser/device/offline/update, visual and audio review, performance and store-certification checklist. | DM-01–23; approved targets/budgets | test config; `docs/{quality-plan,test-matrix,release-runbook}.md`; `PW-24-release.spec.*` | CI-equivalent suite; `PW-24` primary start/save/resume path; manual matrix records approved gates. |

## Dependency summary

```text
G design acceptance → DM-03 → DM-04/05 → DM-06 → DM-11/12 → DM-13 → DM-14 → DM-15/16/17 → DM-18
                     ├→ DM-07 → DM-09 ────────────────────────────────────────────────┐
                     └→ DM-08 ─────────────────────────────────────────────────────────┼→ DM-21 → DM-22 → DM-23 → DM-24
DM-10 ───────────────────────────────────────────────────────────────────────────────────┘
DM-19 (PWA) follows DM-14–18; DM-20 follows explicit mobile approval and DM-19.
```

Account identity/remote sync, multiplayer/safety, live operations, purchases,
and seasonal content are excluded pending explicit product, privacy, safety,
cost, and operations decisions. No future task may copy or imitate reference
questions, branding, layouts, visual assets, or audio.
