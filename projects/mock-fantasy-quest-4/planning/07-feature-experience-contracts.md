# 07 — Feature and experience authoring contracts

**Inputs:** [delivery map](05-delivery-map.md), [foundation and domain contracts](06-foundation-domain-contracts.md), [feature model](../specification/02-feature-model.md), and [experience contract](../specification/04-experience-contract.md).

## Purpose and record rules

These are atomic implementation contracts for the first-release, offline,
single-player campaign.  A record may be implemented only after its listed
dependencies and decision gates are satisfied. `Shared` behaviour is identical
in the responsive web app and installed PWA unless the record names an
adaptation. No record authorises accounts, remote sync, multiplayer, safety
services, live operations, analytics, purchases, entitlements, copied assets,
or copied interaction/layout patterns.

Every browser record owns its stated Playwright path and must provide both the
specified automated evidence and an accessible, visible UI result. Paths are
planned paths until the framework decision is approved.

## Campaign and progression contracts

### FEX-01 — Start, resume, and tutorial journey

- **Target / ownership:** Shared game shell; `src/app/{shell,navigation,tutorial}` and `src/core/tutorial`; browser evidence `supervisor/browser/tests/changes/fex-01-start-tutorial.spec.*`.
- **Player-visible behaviour:** Title shows `New game`, settings, help, save data and privacy/diagnostic entry points. `Continue` and `Load` are absent or explained as unavailable when no valid save exists. New game offers a skippable accessibility quick setup, then teaches move/interact, one legal combat action and target, result, and save in that order before town exploration.
- **Invariants / validation:** A tutorial step cannot be skipped by an unrelated action; repeated input cannot award progress twice. New game never replaces an active slot without an explicit named-slot confirmation or a separate slot. Essential text never auto-advances.
- **Persistence / recovery:** Confirmed tutorial milestones and the first safe checkpoint are durable; a reload resumes only from a confirmed safe boundary. Failure to save leaves the current session usable and explains that persistence did not complete.
- **Permissions / boundaries:** No identity, network, telemetry, or notification permission is requested. Accessibility choices are available before play and persist separately where possible.
- **Acceptance evidence:** Core tutorial transition/idempotency tests; app test for title availability and replacement confirmation; Playwright completes the first battle and confirms the save explanation.

### FEX-02 — Town-to-dungeon exploration journey

- **Target / ownership:** Shared campaign/exploration; `src/core/{exploration,campaign}` and `src/app/game`; browser evidence `supervisor/browser/tests/changes/fex-02-exploration.spec.*`.
- **Player-visible behaviour:** The player explores exactly Larkspur Reach and Glassroot Hollow through labelled interaction prompts, collision-safe movement, authored exits, encounter zones, and a visible current objective. The town request leads to the dungeon and the dungeon path leads to the beacon ending.
- **Invariants / validation:** Scene IDs, exits, interaction targets, and predicates must resolve in validated content. Movement cannot cross collision or a locked exit; a locked route names its unmet requirement. Invalid/missing content fails safely without corrupting campaign state.
- **Persistence / recovery:** Scene exits and authored checkpoints request persistence only at safe boundaries; an interrupted write retains the previous confirmed location. Resume restores a safe scene, never an unresolved traversal action.
- **Responsive / accessibility:** Keyboard, touch, mouse, and detected gamepad invoke the same move/interact actions. Canvas/world interaction has adjacent labelled action routes and textual state; no required route depends on hover, drag, or tiny targets.
- **Acceptance evidence:** Scripted core route reaches ending; negative fixtures reject unresolved exits; Playwright verifies town-to-dungeon progression, locked-exit explanation, and narrow/wide interaction controls.

### FEX-03 — Dialogue, quest, and ending journey

- **Target / ownership:** Shared narrative state and panels; `src/core/{dialogue,quest,campaign}` and `src/app/{dialogue,panels}`; browser evidence `supervisor/browser/tests/changes/fex-03-quest-ending.spec.*`.
- **Player-visible behaviour:** Dialogue shows speaker, a short readable turn, and explicit continue/response choices. Quest UI states what happened, next action, and destination. Objective updates are visible near the objective and in the quest panel. Completing the beacon sequence returns the player to town, marks the campaign complete, and presents the short ending.
- **Invariants / validation:** Locked dialogue/quest predicates do not mutate state; an interaction ID can complete an objective or grant a reward once only. Ending cannot trigger before its authored predicates and cannot duplicate completion on reload.
- **Persistence /recovery:** Quest and ending state are saved only after a complete transition; a crash or failed save resumes the last confirmed objective/checkpoint. Current dialogue is never included in diagnostics.
- **Accessibility / scope:** Speaker and essential dialogue are available as text; captions can be enabled; no copied setting, narrative, names, layouts, or choreography from a reference is permitted.
- **Acceptance evidence:** Predicate, repeated-interaction, one-time-reward, and ending-transition tests; Playwright verifies visible objective and ending path.

### FEX-04 — Turn-based combat and defeat recovery

- **Target / ownership:** Shared combat rules and presentation; `src/core/combat`, `src/app/combat`; browser evidence `supervisor/browser/tests/changes/fex-04-combat.spec.*`.
- **Player-visible behaviour:** Combat announces the active turn, exposes only legal actions, requires an explicit target where needed, displays the outcome, and returns to the next decision. Illegal/unavailable choices state why without consuming a turn. Victory gives the authored reward once. Defeat offers recovery at the prior confirmed checkpoint.
- **Invariants / validation:** Commands require current revision and legal actor/action/target; stale, repeated, or invalid commands are non-mutating and do not advance RNG or turn state. Encounter resolution and reward ledgers are deterministic for a fixture seed.
- **Persistence / recovery:** No unresolved combat, selected target, or mid-resolution animation is persisted. Save/checkpoint happens only after a stable outcome; defeat reloads the last confirmed checkpoint rather than deleting progress.
- **Accessibility / responsive:** Turn, action, target, health values, intent, and result have text equivalents. On phone actions stack or sequence; tablet/desktop may show actions and targets together. Reduced motion does not hide outcome meaning or delay input.
- **Acceptance evidence:** Deterministic win/loss, legal-action, stale-action, reward-once, and defeat-checkpoint tests; Playwright completes the tutorial battle using keyboard only and verifies phone action layout.

### FEX-05 — Inventory and party progression journey

- **Target / ownership:** Shared inventory/party rules and panels; `src/core/{inventory,party,rewards}`, `src/app/panels`; browser evidence `supervisor/browser/tests/changes/fex-05-inventory-party.spec.*`.
- **Player-visible behaviour:** Bag and Party panels show item/character names, usable eligibility, effects, and clear empty state. Players may inspect and use/equip valid items on valid targets. Quest items are visibly protected. Rewards visibly confirm acquisition.
- **Invariants / validation:** Item IDs, effects, target eligibility, capacity/equipment rules, and reward ledger are content-validated. Invalid use, ineligible target, protected quest-item removal, and duplicate reward grant leave state unchanged and explain the reason.
- **Persistence / recovery:** Inventory and party mutations join the same confirmed checkpoint policy as rewards; failed saves retain the last confirmed snapshot and never claim completion.
- **Accessibility / responsive:** Empty/locked feedback names a next useful action. Panels are labelled dialogs/pages with focus restored to the opener; full-screen compact panels and two-column desktop inspection preserve all actions at 200% text.
- **Acceptance evidence:** Unit tests for empty, invalid, protected, ineligible, and duplicate cases; Playwright verifies empty bag, item inspection, focus return, and 200% reflow.

## Shell, input, and responsive contracts

### FEX-06 — Semantic shell, panels, and focus-safe navigation

- **Target / ownership:** Web shell; `src/app/{shell,navigation,status}`; browser evidence `supervisor/browser/tests/changes/fex-06-shell-navigation.spec.*`.
- **Player-visible behaviour:** The primary game workspace has landmarked title/navigation, main controls, objective/status, and temporary titled panels. Pause is available via visible control, Escape, and mapped gamepad action at safe playable states. Focus loss/hidden tab pauses once per session with an explanation.
- **Invariants / validation:** Closing a panel returns to its known invoking control and preserves prior selection/scroll where feasible. Browser Back closes a transient panel before it can leave play. Blocking dialogs identify consequence and use `Cancel` as initial focus; no dialog times out.
- **Responsive:** Phone uses safe-area-aware world view, compact objective, reachable bottom controls and full-screen panels; tablet uses contextual side/bottom panels; desktop uses a collapsible status rail. Resize, rotation, zoom, virtual keyboard, and display-mode changes preserve state/selection or move focus to the panel heading with a status message.
- **Acceptance evidence:** App navigation/focus tests; Playwright covers no-save title state, return target, focus-loss pause, Back behaviour, and phone/tablet/desktop reflow.

### FEX-07 — Unified input and control adaptation

- **Target / ownership:** Web input adapters and controls; `src/platform/web/input`, `src/app/controls`; browser evidence `supervisor/browser/tests/changes/fex-07-input-adapters.spec.*`.
- **Player-visible behaviour:** Keyboard, pointer, touch, on-screen controls, and feature-detected gamepad map to move, interact, confirm, cancel/pause, panels, and legal combat choices. Help describes the active input vocabulary; unavailable/disconnected gamepad leaves keyboard/mouse/touch alternatives available.
- **Invariants / validation:** All adapters dispatch the same semantic commands. Repeat/debounce cannot confirm a destructive dialog, consume multiple turn actions, or replay a completed interaction. Mapping conflicts are explained before a remap is persisted if remapping is approved.
- **Accessibility / responsive:** Tab order follows visual reading order; early shell skip link reaches game controls. Targets are at least 44 by 44 CSS px with separation; no core journey requires precision pointer, multi-touch, swipe-only, drag, long press, or a time limit.
- **Acceptance evidence:** Adapter equivalence and repeat/debounce unit tests; Playwright keyboard-only navigation, touch target sizing, pointer equivalence, and unavailable-gamepad fallback.

### FEX-08 — Settings, localisation, and accessibility preferences

- **Target / ownership:** Web settings/accessibility/i18n; `src/app/{settings,accessibility,i18n}`; browser evidence `supervisor/browser/tests/changes/fex-08-accessibility-settings.spec.*`.
- **Player-visible behaviour:** Before new game and while paused, players can reach text size/spacing, contrast/non-colour cues, captions, master/music/effects audio, reduced motion, on-screen controls, language when supplied, help, privacy, and reset controls. Changes take effect in-session immediately.
- **Invariants / validation:** Focus indicator is at least 3 CSS px and 3:1 against adjacent colours; essential text is 4.5:1, targets are 44 CSS px minimum, and 200% text has no clipped/lost action or horizontal page scroll. Essential state always has text and non-colour cues. Reset describes affected preferences, confirms, and never alters campaign state.
- **Persistence / recovery:** Preferences persist separately from campaign saves where possible. A settings write failure retains the in-session setting, announces it will not persist, and preserves a usable default. Missing locale content falls back visibly to the base locale rather than showing an unresolved key.
- **Acceptance evidence:** Automated accessibility scan plus focus/name/dialog assertions; Playwright verifies persistence failure notice, 200% reflow, reduced motion, captions/contrast, locale fallback, and Cancel-default reset dialog.

### FEX-09 — Audio, visual, and status feedback

- **Target / ownership:** Shared feedback semantics; `src/app/{status,feedback,design}` and content manifests; browser evidence `supervisor/browser/tests/changes/fex-09-feedback.spec.*`.
- **Player-visible behaviour:** Victory, item gained, blocked route, invalid action, save result, update readiness, and recovery use concise text plus icon/shape, optional supported audio/haptic feedback, and non-blocking visual change. Status history remains reviewable in the objective/status panel.
- **Invariants / validation:** Colour, sound, animation, and vibration are never the sole carrier of meaning. Notifications are deduplicated, do not flood assistive announcements, and decorative animation frames are not announced. No flash exceeds three flashes per second.
- **Scope / originality:** Art, audio, names, UI composition, timing, and feedback choreography are independently authored; functional references provide no reusable creative material.
- **Acceptance evidence:** Status deduplication/review tests, non-colour semantic-state fixture, reduced-motion fixture, and Playwright verifies that blocked, save, recovery, and reward feedback retain a text/non-colour meaning with captions or reduced motion enabled.

## Save, recovery, and PWA contracts

### FEX-10 — Save, load, delete, and migration journey

- **Target / ownership:** Web persistence UI and shared save coordinator; `src/{core/save,core/session,platform/web/persistence,app/session}`; browser evidence `supervisor/browser/tests/changes/fex-10-save-recovery.spec.*`.
- **Player-visible behaviour:** Save data exposes valid slots, load, selected-slot deletion, recovery status, and clear explanations for no saves, corrupt saves, interrupted writes, quota/permission failures, and unsupported saves. Save success is stated only after confirmation.
- **Invariants / validation:** Snapshots are immutable checksummed revisions with validated current pointer and last-known-good retention. Ordered pure migrations promote only valid candidates. Delete names the slot/progress/time, has initial `Cancel` focus, rejects stale/repeated input, and removes only the selected slot plus its recovery metadata.
- **Recovery:** Malformed/unsupported candidates are quarantined, preserved, and described without blame. Retry, title, safe-recovery, and new-game paths retain confirmed progress. Failed migration or write does not overwrite the previous snapshot.
- **Acceptance evidence:** Fault injection for interrupted/malformed/quota/permission/delete cases, migration fixtures, and Playwright for save/resume, deletion confirmation, quarantine, and recovery choices.

### FEX-11 — Crash boundary and privacy-safe diagnostics

- **Target / ownership:** Web error boundary and diagnostics; `src/{app/recovery,platform/web/diagnostics}`; browser evidence `supervisor/browser/tests/changes/fex-11-crash-recovery.spec.*`.
- **Player-visible behaviour:** An unexpected fault shows plain-language `Retry`, `Return to title`, and `Safe recovery` actions. Recovery is separate from optional diagnostics; clear diagnostics states its local-only effect.
- **Invariants / permissions:** Confirmed progress survives recovery attempts. P0 sends no telemetry and creates/exports no diagnostic record without explicit consent. Diagnostic records are bounded and exclude save payloads, dialogue, credentials, account data, and player-entered content.
- **Recovery:** Error focus goes to an actionable summary; retry cannot replay a stale destructive command. If recovery cannot restore a valid slot, new game remains available and quarantined data remains untouched unless the player confirms deletion.
- **Acceptance evidence:** Recovery state-machine and redaction/consent/clear tests; Playwright injected-fault flow verifies all recovery paths and no diagnostics before consent.

### FEX-12 — PWA installation, offline, and update journey

- **Target / ownership:** PWA adapter/status; `src/platform/web/pwa`, `public/{manifest,icons}`, service-worker config; browser evidence `supervisor/browser/tests/changes/fex-12-pwa-lifecycle.spec.*`.
- **Player-visible behaviour:** Installation is optional and its unavailable/declined state is non-blocking. An uncached first offline visit explains that assets must download before play; a known-good cached version remains playable offline. PWA status distinguishes asset/cache state from save data.
- **Invariants / validation:** A failed refresh retains known-good cache. Update notice appears only at title or paused menu after a confirmed save; it offers `Update now` and `Later` and never reloads during combat, save write, modal choice, or essential dialogue. Cache activation cannot delete, migrate, or imply synchronisation of saves.
- **Permissions / recovery:** Install prompt is requested only through a player-visible action where browser policy permits. Update/install decline does not block valid current/cached play; offline failure has a title/retry path.
- **Acceptance evidence:** Browser scenarios for uncached offline explanation, cached offline reload, install declined/unavailable, refresh retention, and deferred safe-boundary activation.

## Content, trust, and release-quality contracts

### FEX-13 — Original minimal content package and authoring validation

- **Target / ownership:** Shared content; `content/base`, `src/content/{schema,validator,registry}`, `assets/source-manifest.*`; no browser spec until rendered by FEX-02–FEX-05.
- **Player-visible behaviour:** The complete first-release route is original Larkspur Reach → Glassroot Hollow → restored beacon ending, with authored dialogue, tutorial, quests, encounters, items, rewards, base locale, and provenance records.
- **Invariants / validation:** Package version, IDs, references, localisation keys, assets, predicates, rewards, and reachability validate before release. The opening-to-ending graph must be reachable; invalid/missing asset or reference fixtures fail without shipping. Provenance records identify original creation/source status.
- **Scope boundary:** Exactly one town, one dungeon, short ending, and offline campaign. No imported branded material, expansion areas, live events, player-created content, or unapproved monetisation/analytics.
- **Acceptance evidence:** Valid minimum package, invalid-reference fixtures, reachability test, authored provenance review, and manual original-design checklist.

### FEX-14 — Release safety and quality evidence

- **Target / ownership:** Shared release/QA documentation and checks; `scripts/release-check.*`, `docs/{quality-plan,test-matrix,security-and-provenance,player-guide,accessibility,privacy-and-recovery,release-runbook,rollback,content-authoring}.md`; browser evidence `supervisor/browser/tests/changes/fex-14-release-evidence.spec.*`.
- **Player-visible behaviour:** Help explains controls, save/recovery, accessibility, privacy, version/cache status, and support paths. Release copy makes no promise beyond approved browser/device, performance, localisation, or assistive-technology decisions.
- **Invariants / validation:** Build assets are hashed; CSP/static host headers, parser/size bounds, dependency/license/provenance review, and client-secret scan pass. Quality evidence maps every contract to deterministic, integration, browser, and required manual checks; fixtures never write player data.
- **Recovery / rollback:** A known-good build can be restored through the documented rollback procedure without changing player saves. Unsupported/corrupt hostile content and save payloads fail safely.
- **Acceptance evidence:** CI-equivalent command transcript, release/security reports, browser smoke start/save/resume evidence, completed manual matrix fields, and known-good rollback dry run.

## Decision gates retained for later runbooks

1. Engine/framework, package manager, CI runtime, storage API/quota, host/CDN,
   service-worker rollout, and browser/device/performance matrix require approval.
2. Party size, content quantities, final fonts, locales, audio scope, control
   remapping depth, legal/age/regional policy, and assistive-technology matrix
   remain unresolved; implementations must not invent them.
3. Connected identity/sync, multiplayer/safety, live operations, analytics,
   commerce, and entitlements are excluded from this release and require new
   approved contracts before any UI, storage, or integration work begins.
