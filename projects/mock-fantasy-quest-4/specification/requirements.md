# Canonical requirements register

**Source precedence:** [`INITIAL.md`](../INITIAL.md), then the F001–F010 discovery/specification/planning records cited below. **Status meanings:** `accepted` is P0; `proposed` needs the named decision; `deferred` is outside P0; `hold` is a contradictory requested connected capability. Priority is P0 (release-critical), P1 (required but approval-gated), or Deferred.

| ID | Requirement | Pri. | Source / rationale | Targets | Verify | Status |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-0001 | Deliver an original small 2D single-player fantasy RPG campaign. | P0 | Brief: creation/category; bounded release | Shared | playthrough + provenance review | accepted |
| REQ-0002 | Provide exactly one town, one dungeon, exploration, dialogue, quests, progression and a short ending. | P0 | Brief: creation/capabilities | Shared | content reachability/playthrough | accepted |
| REQ-0003 | Provide party-based turn combat with legal actions, visible resolution, rewards and defeat recovery. | P0 | Brief/reference scope; feature model J2 | Shared | deterministic combat tests/J2 | accepted |
| REQ-0004 | Provide inventory with inspect/use/equip rules, protected quest items, and safe empty/invalid states. | P0 | Brief; J4 | Shared | inventory tests/J4 | accepted |
| REQ-0005 | Onboard a new player so they finish a first battle and understand saving. | P0 | Brief: first useful session | Shared | J1–J2 browser/manual evidence | accepted |
| REQ-0006 | Save, load, resume, checkpoint, delete-confirm, and recover confirmed local progress. | P0 | Brief: shared requirements; J5 | Shared | fault/migration/recovery tests | accepted |
| REQ-0007 | Provide settings for accessible controls, readable text/UI, captions, visual options and audio/visual feedback. | P0 | Brief: shared/capabilities | Shared | accessibility/settings journey | accepted |
| REQ-0008 | Deliver original authored levels, narrative, items, encounters, assets and base locale with validation/provenance. | P0 | Brief art/content delivery | Shared | validator + creative review | accepted |
| REQ-0009 | Offer keyboard, mouse, touch and feature-detected gamepad through the same semantic actions. | P0 | Web requirements | Web, PWA | adapter + browser input tests | accepted |
| REQ-0010 | Reflow usable game/UI across phone, tablet and desktop viewports. | P0 | Web requirements | Web, PWA | responsive browser/manual matrix | accepted |
| REQ-0011 | Be installable as a PWA, run cached assets offline, and update only at a safe save boundary. | P0 | PWA requirements | PWA | lifecycle/cache tests | accepted |
| REQ-0012 | Recover player-facingly from crashes, storage/content/cache errors without silently losing confirmed state. | P0 | Brief; J7 | Shared, PWA | injected-fault evidence | accepted |
| REQ-0013 | Do not make account, identity, remote sync, multiplayer, player safety, live service, purchases or entitlements a P0 dependency. | P0 | Brief conflict; discovery | Shared | scope/architecture audit | accepted |
| REQ-0014 | If account-linked remote state is approved, provide explicit local/remote conflict choice and no silent overwrite. | P1 | Brief cross-platform policy; J5 | Web, PWA | approved future contract | proposed |
| REQ-0015 | If multiplayer/safety, live operations, or commerce is approved, define privacy/security/operations/failure modes first. | P1 | Brief required capabilities conflict | Shared | approved future contract | hold |
| NFR-0001 | The campaign works offline after successful initial asset availability; uncached launch explains its requirement. | P0 | PWA/J1 | Web, PWA | offline lifecycle test | accepted |
| NFR-0002 | Saves are versioned, validated, atomic, recoverable, and never restore a half-turn/reward. | P0 | J5; technical contract | Shared | persistence fault tests | accepted |
| NFR-0003 | Preserve previous confirmed save/cache on failed write, migration, or refresh; quarantine invalid candidates. | P0 | J5/J7 | Shared, PWA | fault tests/rollback dry run | accepted |
| NFR-0004 | Use semantic UI, keyboard/focus-safe navigation, readable reflow, non-colour cues, captions, text/spacing and reduced-motion adaptations. | P0 | Experience contract | Web, PWA | automated/manual accessibility evidence | accepted |
| NFR-0005 | Persist preferences separately; a persistence failure leaves the current session usable and explains non-persistence. | P0 | J6 | Shared | settings failure test | accepted |
| NFR-0006 | Keep diagnostics minimal, consent-gated where required, redact save/dialogue payloads, and permit local diagnostic deletion. | P0 | Brief privacy; QOR-02 | Web, PWA | redaction/consent test | accepted |
| NFR-0007 | Apply content reference/reachability/localisation validation before release packaging. | P0 | Feature/technical contracts | Shared | content validator | accepted |
| NFR-0008 | Maintain original-design provenance and prohibit copied reference expression in content and UI. | P0 | Brief non-goal/reference boundary | Shared | provenance/manual review | accepted |
| NFR-0009 | Measure web compatibility, load/cache size, startup, interaction and slow-network behaviour against an approved numeric matrix/budget. | P1 | Web requirements; QOR-05 | Web, PWA | approved-matrix measurement | proposed |
| NFR-0010 | Use a shared core and isolate only necessary web/PWA adapters; no target changes campaign rules. | P0 | Cross-platform decision | Shared, Web, PWA | architecture/contract review | accepted |
| NFR-0011 | Build/release artifacts identify version and compatibility; cache rollout/rollback retain a known-good path. | P1 | PWA/release requirements | Web, PWA | release/rollback evidence | proposed |
| NFR-0012 | Select no framework, vendor, host, storage quota, retention policy, legal/store policy, or support promise without approval. | P0 | Brief constraints; handoff | Shared | decision-log audit | accepted |

## Release gates and risks

| ID | Record | State / linked decision |
| --- | --- | --- |
| GATE-0001 | Framework, package manager and CI baseline selected | blocked — DEC-0001 |
| GATE-0002 | Browser/device/assistive-tech matrix, network profiles and numeric budgets approved | blocked — DEC-0002 |
| GATE-0003 | Storage API/quota, schema support window and recovery/export support policy approved | blocked — DEC-0003 |
| GATE-0004 | Content quantities, party size, balance, locale, audio/remapping, font/contrast targets approved | blocked — DEC-0004 |
| GATE-0005 | Hosting/CDN, PWA rollout/rollback, diagnostics transport/retention and support owner approved | blocked — DEC-0005 |
| GATE-0006 | Identity/sync, multiplayer/safety, live operations and commerce either excluded or newly approved with full contracts | blocked — DEC-0006 |
| GATE-0007 | Ratings/age/region/legal/store/certification policy determined if applicable | blocked — DEC-0007 |

| ID | Risk / treatment | Status |
| --- | --- | --- |
| RISK-0001 | Connected-service list conflicts with offline P0; preserve exclusion boundary until GATE-0006. | open |
| RISK-0002 | Storage, migration and cache failures can lose progress; atomic/quarantine/known-good rules and GATE-0003. | mitigated by requirements; gate open |
| RISK-0003 | Unapproved compatibility and performance claims can overpromise; measure only after GATE-0002. | open |
| RISK-0004 | Unoriginal content/reference copying harms delivery; provenance plus human creative review. | open |
| RISK-0005 | PWA update/rollback can mismatch content and saves; version compatibility and GATE-0005. | open |
