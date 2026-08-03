# Product brief — Mock Fantasy Quest 4

**Source of truth:** [`INITIAL.md`](INITIAL.md). This normalized brief supports
downstream planning; it preserves source scope and records unknowns rather than
choosing them.

## Product problem and outcome

Casual adult players need a compact, approachable fantasy RPG that delivers a
complete story without requiring a long commitment or dependable connection.
The first useful session is successful when a new player finishes a first
turn-based battle and understands how to save and resume. The release outcome
is an original short campaign that a player can complete through exploration,
dialogue, quests, combat, rewards, saving, and a short ending.

## Category, users, and core experience

| Area | Normalized first-release statement |
| --- | --- |
| Category | Deliberately small, offline-capable, 2D single-player fantasy RPG. |
| Users | Casual and adult players, including people using keyboard, mouse, touch, gamepad, captions, adjustable text, and visual settings. |
| Campaign boundary | One town, one dungeon, and one guided, short ending; no further regions or chapters are required. |
| Core loop | Explore, converse, accept or advance a quest, enter party-based turn-based combat, manage rewards/inventory, save, and continue. |
| Experience direction | Original warm hand-painted fantasy, readable silhouettes, and a restrained palette. |
| Functional reference | *Final Fantasy V* may inform only the high-level scope of a party-based turn-based adventure. |

## Selected target systems

| Target | First-release role | Input model | Delivery constraints | Out-of-scope boundary |
| --- | --- | --- | --- | --- |
| Responsive public web application | Primary browser surface for the complete game. | Keyboard, mouse, touch, and gamepad. | Responsive phone/tablet/desktop layout; browser compatibility and performance budget must be approved before implementation. | Native binaries, a separate web-only campaign, and browser-exclusive mechanics. |
| Progressive web app (PWA) | Installable delivery of the same shared game core. | Same inputs where the browser/device supports them. | Offline assets and save-data behavior; safe update/cache refresh must preserve confirmed player data. | A PWA-exclusive campaign, mandatory continuous connection, or a different ruleset. |

The product uses a shared core with platform adaptation only where necessary.
It should work on widely used devices and under feasible slow-network
conditions; exact supported browsers, device classes, storage quotas, and
network floor are open decisions.

## First-release scope and measurable success measures

Included scope: playable exploration; one town and one dungeon; narrative,
dialogue, quests, progression and a short ending; onboarding/tutorial; at least
one tutorialized turn-based battle; inventory and rewards; save/load, resume,
checkpoints, data-loss recovery; settings and accessibility; audio/visual
feedback; content/level delivery; and crash reporting with player-facing error
recovery. The source also names account/identity, multiplayer/player safety,
live-service operations, and purchase/entitlement handling, but their release
status remains contingent on the explicit conflict decision below.

The release is measurable when:

- A new player can finish the tutorial battle, create a save, reload it, and
  reach the short ending on each supported target.
- The delivered campaign contains exactly one town, one dungeon, and one short
  ending; added regions or chapters are not needed for release completion.
- Both targets meet their stated input role; the PWA is installable and each
  target has a tested offline, save, update, and error-recovery path.
- Dialogue, inventory, quest, and progression UI are readable with approved
  accessibility settings, and captions/visual settings are available where the
  corresponding feedback exists.
- An interruption, recoverable error, or safe update offers a player-facing
  recovery path and does not silently discard the last confirmed save.

## Later roadmap, non-goals, and reference boundary

Deferred roadmap: live events/seasonal content, player-created/shared content
(levels, mods, designs, stories), advanced analytics, and advanced
monetisation. They are excluded from first-release acceptance.

Non-goals: copied branding, assets, text, layouts, characters, story/lore,
audio, maps, or distinctive interactions; additional towns/dungeons/campaigns;
native apps; and platform-specific game variants. No cloud-sync, payment,
moderation, service-uptime, or backend commitment is implied before approval.

| Reference boundary | Prohibited | Permitted |
| --- | --- | --- |
| Branding and copy | Names, logos, trademarks, marketing copy, story text, dialogue, characters, and world/lore. | A high-level description of a compact party-based turn-based adventure. |
| Assets and presentation | Art, music, sound, maps, screen composition, visual language, and layouts. | Original art and UI that fulfil this brief’s own direction. |
| Interaction design | Reproducing distinctive combat screens, menus, flows, quests, or interaction choreography. | Independently designed mechanics and feedback appropriate to the requested scope. |

## Constraints and safe assumptions

Explicit constraints: web/PWA delivery, offline play, accessibility,
localisation, privacy, safe save/recovery, slow-network feasibility, and
original expression. Safe working assumptions: the offline core does not block
on a remote service; content/UI are original; local persistence is durable
enough for confirmed saves where browser storage permits; connected features,
if approved, degrade visibly; and crash diagnostics minimize personal data.
These are guardrails, not approval of a stack, vendor, backend, account model,
data-retention policy, or technical promise.

## Open decisions requiring human approval

1. **Offline versus connected scope:** Reconcile the offline single-player
   premise with required account identity, multiplayer safety, live operations,
   and purchase/entitlement handling. Classify each as release-critical,
   optional connected enhancement, or deferred.
2. **Account and data policy:** Decide whether accounts are absent, optional,
   or mandatory; then define authentication, sync/conflict behavior, retention,
   deletion, and offline/service-outage recovery.
3. **Multiplayer, commerce, and safety:** State whether multiplayer or
   real-money purchases actually ship, plus age rating, regions, moderation,
   reporting, refunds, store, and applicable legal obligations.
4. **Technical delivery baseline:** Choose engine/framework, repository and CI
   constraints, browser/device matrix, performance budget, offline-storage
   quota, update activation policy, error-reporting provider, and cost model.
5. **Production content and access:** Approve party size, encounter/quest
   counts, combat/progression balance, language set, audio scope, and the exact
   accessibility options before production planning.
