# 02 — Feature model and release slices

**Inputs:** [domain discovery](00-domain-discovery.md) and the canonical
[project brief](../PROJECT_BRIEF.md). This document turns only the accepted
offline-game scope into a model. It records connected and commercial requests
as approval gates; it does not silently turn them into a first-release
dependency.

## Product outcome and personas

The first release is successful when a casual or adult player can start the
original 2D fantasy adventure, complete an understandable first battle, save,
return later without losing confirmed progress, finish the single town and
dungeon story, and reach its short ending offline after installation or a
successful first asset download.

| Persona | Job to be done | Success signal | Relevant journeys |
| --- | --- | --- | --- |
| Casual story player | When I have a short session, help me understand what to do and make visible story progress without complex controls. | Starts, wins the tutorial battle, saves, and resumes a quest. | J1–J4 |
| Adult returning player | When I resume after interruption or a long gap, help me recover safely and understand my current objective. | Restored checkpoint is clear; no confirmed progress is silently lost. | J3, J5 |
| Player with access needs | When I play on my chosen device, let me read, hear, see, and control the game in a comfortable way. | Can change supported text, caption, visual, and control options before or during play. | J1, J6 |
| Offline PWA player | When connectivity changes or an update is available, let me keep playing the installed game without corrupting saves. | Cached release runs offline; update waits for a safe boundary. | J1, J5, J7 |

## Core journeys

| ID | Journey and outcome | Normal path | Empty / invalid / denied / offline / conflict / recovery / deletion handling |
| --- | --- | --- | --- |
| J1 | Start, orient, and configure: player reaches the town and knows the tutorial goal. | Open web game or installed PWA → choose new game → optional settings → readable dialogue and input hints → town. | No prior save shows New Game; unavailable gamepad falls back to listed keyboard/mouse/touch controls; unsupported input shows a non-blocking message. Offline launch is allowed only when the current assets are cached; otherwise explain that an initial download is needed. Declining optional diagnostics does not block play. |
| J2 | Learn and win first combat: player understands the turn loop. | Accept first encounter → choose a legal party action → resolve enemy turn → win → receive reward and quest update. | Empty inventory/action lists show explanation; invalid/stale target or unavailable item is rejected without consuming a turn; defeated party reloads the latest safe checkpoint and explains the consequence. No network permission is needed. |
| J3 | Explore and advance the campaign: player finishes town, dungeon, and ending. | Talk to characters → accept quest → traverse town/dungeon → resolve required encounter and objective → claim reward → see ending. | Locked exits state the missing quest condition; exhausted dialogue has a safe closing line; missing authored reference fails content validation and shows recoverable error rather than breaking state; optional reward absence never blocks completion. |
| J4 | Manage items and progression: player can use earned resources correctly. | Open inventory → inspect item → use/equip only where legal → see immediate feedback → close back to play. | Empty inventory has an explicit empty state; invalid use, full/limited capacity (if authored), or ineligible target preserves inventory; quest items cannot be discarded if that would make a required path impossible. Deletion/discard is not a first-release capability unless an authored safe rule is later approved. |
| J5 | Save, load, and recover: player can leave and return safely. | Manual save or checkpoint completes atomically → resume chooses latest valid save → state restores at a safe scene boundary. | No save slot shows explanation; corrupt/incompatible candidate is quarantined, never overwritten, and falls back to the last valid checkpoint or new game; storage denial/quota exposes retry and export/support guidance where feasible; interrupted write keeps prior confirmed save. Local cache and any future remote copy conflict resolve only with explicit player choice; remote sync is not first release. Deleting a save requires confirmation and removes only that selected local save. |
| J6 | Adjust accessibility and feedback: player can make the game usable. | Open settings → preview/change text, captions, visual and input options → apply → preferences persist. | Unsupported option/device is labelled unavailable; reset asks confirmation; settings storage failure leaves current-session setting active and explains it may not persist. No permission denial is required for these settings. |
| J7 | Install, update, and recover from a fault: player retains a coherent playable version. | Install when browser allows → cache approved release → play offline → accept update at launch/menu after save boundary. | Installation prompt may be unavailable/declined without blocking web play; offline uncached assets state the requirement; cache refresh failure retains known-good cache; crash/error boundary offers retry, return to title, and safe recovery. Diagnostics are minimal and consent-gated where required; a player can decline or delete local diagnostic data without losing play. |

## Domain vocabulary and state ownership

| Term | Meaning / owner |
| --- | --- |
| Campaign | The fixed first-release sequence from new game through ending; owns completion state. |
| Scene | One authored playable location: town or dungeon; owns exits, encounter zones, and presentation references. |
| Quest | Authored objective and state machine that gates campaign progress and rewards. |
| Party | Player-controlled combat group; owns members' current combat-ready values and progression. Exact party size is an authoring decision. |
| Encounter | A combat instance created from an authored encounter definition; never persists mid-turn. |
| Item | Authored definition; an inventory stack/reference is the player-owned instance/count. |
| Save snapshot | Versioned, validated, atomic representation of durable player state at a safe boundary. |
| Checkpoint | Authored or system-selected safe snapshot point; it is not a promise to restore arbitrary moment-to-moment state. |
| Content package | Versioned original scenes, dialogue, quests, encounters, items, translations, and audiovisual assets delivered together. |

## System relationship map

```text
Content package ──validates/defines──> Scene ──starts──> Encounter
      │                                  │                  │
      ├──defines──> Dialogue ──updates──> Quest <──rewards───┘
      │                                  │       │
      └──defines──> Items ──held by──> Inventory │
                                                 │
Input + accessibility ──drives──> Game shell ──> exploration / UI
                                                 │
Quest + inventory + party + scene ──snapshot──> Save / checkpoint
Save version <──compatible-with── Content package / PWA release
PWA cache + release workflow ──protect──> runnable assets and save boundary
Error recovery + minimal diagnostics ──observe──> shell, persistence, cache
```

**Cross-domain invariants and lifecycle boundaries**

- A quest transition, reward grant, and save snapshot are ordered: validate
  transition, apply reward once, then checkpoint; retrying cannot duplicate a
  reward.
- An encounter may read party, item, and quest state but changes durable state
  only after a resolved turn/encounter safe boundary. A crash cannot restore a
  half-consumed item or half-applied reward.
- A scene exit is available only when its authored quest predicate is true.
  Content validation ensures every required predicate, target, reward, and
  localisation key exists.
- Settings affect presentation/input immediately but never campaign rules.
  The same semantic action must be available through supported keyboard,
  mouse, touch, and gamepad adaptations.
- Save snapshots record content/schema version and are written atomically.
  Cache replacement and application migration happen only outside combat and
  only while a valid fallback save remains intact.
- The local offline campaign neither needs identity nor sends player state.
  Any later account is an optional replication boundary, not campaign truth.

## Accepted domain chapters

### 1. Game shell, session, input, and responsive presentation

**Entities/lifecycle:** `Session` moves `launching → title → new-or-resume →
playing ↔ paused → ending → title`; `InputAction` is mapped per supported input
method; `ViewportProfile` selects responsive layout. Authoring inputs are title
copy, control hints, menu routes, and UI layouts. Rules: pause blocks world and
combat advancement; focus loss pauses or reaches a safe state; UI action labels
remain readable and semantic across screen sizes. Dependencies are accessibility,
rendering, persistence, and content. Outcome is an understandable, controllable
start and return path. Edge cases are no existing save, focus loss, rotation,
unavailable gamepad, unsupported browser feature, and input remap conflict.
**First-release boundary:** web/PWA keyboard, mouse, touch, and gamepad
adaptation; one shared game core. No native-client shell or arbitrary controller
configuration guarantee.

### 2. Exploration, town, dungeon, and campaign content

**Entities/lifecycle:** `Scene` is `unloaded → entered → active → exited`;
`Exit` is `locked | available | used`; `Interactable` is `available → used` or
reusable as authored. Inputs are original tile/layout data, collision shapes,
spawn points, NPCs, exits, encounter zones, dialogue, and asset references.
Rules: exactly one town and one dungeon form the first campaign; collision and
gates must leave a completable route. Dependencies are narrative, quests,
combat, rendering, and saves. Outcome is readable navigation to the ending.
Edge cases: blocked exit, empty interaction, absent optional item, and invalid
content reference. **Boundary:** no extra regions, procedural worlds, or shared
levels.

### 3. Narrative, quests, onboarding, and ending

**Entities/lifecycle:** `Dialogue` is `available → shown → acknowledged`;
`Quest` is `unavailable → available → accepted → objective-complete →
claimed → completed` (or `failed` only where authored); `TutorialStep` is
`pending → presented → understood`; `Campaign` is `not-started → active →
completed`. Inputs are original characters, text, localisation keys, objective
predicates, rewards, and ending sequence. Rules: tutorial teaches a battle and
saving before unrestricted progression; required quests cannot be abandoned;
completion is idempotent. Dependencies are scenes, combat, inventory, UI, and
saves. Outcomes are clear objectives and a short finish. Edge cases: repeated
NPC talk, dialogue after completion, missing translation, and an invalid quest
predicate. **Boundary:** one authored story path; no branching campaign,
seasonal narrative, or user-authored stories.

### 4. Party combat, encounters, rewards, and balance

**Entities/lifecycle:** `Encounter` is `pending → active → player-turn →
resolution → won | lost | escaped-if-authored`; `Combatant` is `ready → acting
→ resolved → defeated`; `Reward` is `pending → granted`. Inputs are party and
enemy definitions, actions, targeting, encounter placement, reward tables, and
balance values. Rules: only legal actions/targets resolve; turn order is visible;
reward grants once; defeat returns to a safe checkpoint. Dependencies are party,
inventory, quest transitions, audiovisual feedback, and saves. Outcome is a
learnable turn-based first battle and reliable progress. Edge cases: no legal
target, empty item list, invalid action request, pause/focus loss, crash during
resolution, and stale UI selection. **Boundary:** authored encounters only; no
multiplayer, ranked modes, live balance changes, or mid-combat save guarantee.

### 5. Inventory, party progression, and economy

**Entities/lifecycle:** `InventoryEntry` is `absent → acquired → usable |
equipped → consumed-if-applicable`; `PartyMember` progresses through authored
states; `RewardGrant` is `unclaimed → applied`. Inputs are item definitions,
descriptions, icons, use/equip restrictions, and rewards. Rules: use validates
target and eligibility before mutation; required quest items remain protected;
duplicate grants are ignored by stable reward ID. Dependencies are combat,
quests, UI, content validation, and saves. Outcome is meaningful reward use
without dead ends. Edge cases: empty inventory, ineligible target, capacity
limit if selected, duplicate reward, and missing item definition. **Boundary:**
small authored set; no crafting, trading, loot boxes, purchases, or destructive
discard flow without approval.

### 6. Save, recovery, and offline persistence

**Entities/lifecycle:** `SaveSlot` is `empty → writing → valid → loading` or
`quarantined`; `Checkpoint` is `eligible → committed`; recovery is `detect →
preserve → offer-fallback → restored | new-game`. Inputs are schema version,
campaign/quest/party/inventory/settings state, checkpoint triggers, and
migration rules. Rules: validate before replace; retain last known-good data;
never overwrite corruption; loading restores only safe scene boundaries; delete
requires explicit confirmation. Dependencies are every durable domain, PWA
storage, error UX, and release versioning. Outcome is confidence to stop and
resume. Edge cases: quota/permission denial, malformed data, interrupted write,
old schema, unavailable local storage, offline launch, and later remote conflict.
**Boundary:** local durable saves and recovery; remote accounts, sync, cross-
device merge, and cloud deletion policy await approval.

### 7. Accessibility, localisation, and audiovisual feedback

**Entities/lifecycle:** `Preference` is `default → previewed → applied →
persisted`; `LocalePack` is `validated → packaged → active`; `FeedbackEvent`
is emitted by action/scene/combat state. Inputs are accessible labels, text
styles, captions, visual settings, translations, original art/audio, and event
bindings. Rules: settings are understandable and reversible; captions/text do
not convey essential information only through sound/colour; missing translation
falls back to the approved base language and is logged for content repair.
Dependencies are UI, content packaging, input, and storage. Outcome is readable,
controllable play with clear feedback. Edge cases: unsupported preference,
storage failure, missing locale key, muted audio, contrast conflict, and narrow
viewport. **Boundary:** the settings categories named in the brief and a
language-content pipeline; exact languages, remapping depth, ratings, and audio
production scope remain decisions.

### 8. PWA delivery, release safety, diagnostics, and quality operations

**Entities/lifecycle:** `Release` is `built → validated → published → cached →
superseded`; `Cache` is `installing → ready → retained | replaced`; `Fault` is
`caught → player-recovered → optionally-reported`. Inputs are asset manifests,
content/save compatibility declarations, service-worker policy, error messages,
minimal diagnostic schema, and test matrices. Rules: an update activates at a
title/menu safe boundary after a confirmed save; failed refresh retains a
known-good cache; diagnostics minimise data and respect consent; supported
browser/device/network and performance thresholds must be agreed before release
acceptance. Dependencies are all packaged content, persistence, shell, privacy,
and quality checks. Outcome is safe installation, offline continuation, update,
and error recovery. Edge cases: declined install, first offline visit, stale
cache, asset fetch failure, crash loop, diagnostics denial/deletion, and storage
pressure. **Boundary:** installable web/PWA and minimal crash recovery only; no
live event operation, account support desk, analytics programme, or paid-service
SLO until approved.

## Capability parity and intentional differences

| Capability | Responsive web | Installed PWA | Shared rule |
| --- | --- | --- | --- |
| Campaign, combat, inventory, quests, settings, saves | Required | Required | Same content, rules, save schema, and accessible semantic actions. |
| Input | Keyboard, mouse, touch, gamepad | Same where device/browser exposes it | Input adapters map to one action vocabulary. |
| Responsive presentation | Required on phone, tablet, desktop | Required on phone, tablet, desktop | Layout adapts; no gameplay advantage by surface. |
| Offline play/assets | May work once cached | Primary expected offline route once cached | First visit needs assets; saves remain local and recoverable. |
| Installation | Browser page can offer it where supported | Installable experience | Declining/unavailable install never blocks web play. |
| Updates | Cache refresh at safe boundary | Cache refresh at safe boundary | Never swap content/version during unresolved combat or save write. |

## Prioritised feature catalogue and slices

| Priority | Feature | User outcome / journey | Slice |
| --- | --- | --- | --- |
| P0 | Shell, title/new game, pause, responsive input/presentation | Start and control the game (J1). | First release |
| P0 | One town, one dungeon, original content packaging and validation | Traverse one completable campaign (J3). | First release |
| P0 | Dialogue, quest state, onboarding, short ending | Understand and complete story progress (J1–J3). | First release |
| P0 | Party turn-based combat, tutorial encounter, rewards | Finish first battle and understand the loop (J2). | First release |
| P0 | Inventory/progression UI and safe item rules | Use earned rewards without dead ends (J4). | First release |
| P0 | Atomic local save/load, checkpoints, corruption recovery, save deletion | Stop, resume, and recover confirmed progress (J5). | First release |
| P0 | Settings: accessible controls/text/captions/visuals; localisation pipeline | Play comfortably and read core UI (J1, J6). | First release |
| P0 | Web/PWA caching, install path, update safety, error recovery | Keep a stable offline-capable version (J7). | First release |
| P0 | Original art/audio feedback and quality validation | Receive clear, original feedback on supported targets (J2, J6). | First release |
| P1 | Additional locales, refined remapping, content expansion | Broader comfort and longer campaign. | Later, after languages/content scope is approved |
| P1 | Optional account-linked backup/sync | Recover across devices with explicit conflict choices. | Later, approval required |
| P1 | Multiplayer, player safety, moderation, support and live operations | Play safely with others. | Later, approval required; not implied by single-player game |
| P2 | Live events/seasonal content; player-created/shared content | Receive or create continuing content. | Deferred |
| P2 | Advanced analytics/monetisation, purchases, catalogue, entitlements/refunds | Optional commercial/personalised experience. | Deferred; commerce approval required |

The P0 set deliberately forms a complete useful journey: J1 starts and teaches,
J2 proves the core loop, J3 reaches the ending, J4 supports rewards, J5 makes
progress durable, and J6–J7 keep it usable and safe on both targets. None
depends on identity, remote services, multiplayer, commerce, or deferred
content.

## Approval gates and unanswered questions

- Select technology, repository, engine/framework, vendors, CI/CD, cost model,
  browser/device/network matrix, storage quota, and performance budget.
- Decide whether the apparently contradictory account, multiplayer, safety,
  live-service, and commerce requirements are cancelled, later scope, or a
  separately funded product. Define ownership, consent, retention/deletion,
  support, and degraded modes before implementation.
- Set exact party/content quantities, languages, audio scope, accessibility
  configuration depth, age/parental/legal regions, and certification/store
  obligations. These are not inferred from the functional reference.
