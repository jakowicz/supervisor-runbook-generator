# 03 — Technical, data, trust, and quality contract

**Inputs:** [`INITIAL.md`](../INITIAL.md), [product brief](01-product-brief.md),
and [feature model](02-feature-model.md). This contract makes the P0 offline
single-player release implementable without selecting a vendor or creating a
dependency on the contradictory connected-service requests. It is a design
contract, not permission to collect data or operate services.

## Architecture and requirement traceability

The production architecture is a static, client-side 2D web game: a shared
deterministic domain core, browser presentation/input adapters, versioned
authored content, and local durable storage. The web host may deliver a signed
release bundle and service worker, but it is not a campaign authority. The
core must have no browser APIs, timers, network calls, or renderer dependencies.

| Component / boundary | Requirement served | Contract |
| --- | --- | --- |
| Game shell and responsive renderer | J1, J3, J6; readable mobile-to-desktop play | Owns navigation, focus/visibility pause, semantic UI, visual settings, and rendering only. It requests domain commands and renders returned state/events. |
| Input adapters | Keyboard, mouse, touch, gamepad accessibility | Convert platform events into a shared, remappable `InputAction` vocabulary; unavailable hardware is non-fatal. No adapter may mutate campaign state directly. |
| Deterministic rules core | Tutorial combat, quests, inventory, progression | Owns legal state transitions, seeded/randomness policy, combat resolution, reward ledger, and invariants. Command validation precedes every mutation. |
| Content registry and validator | One town/dungeon, original content, localisation | Loads the active versioned content package; resolves IDs/keys and rejects invalid packages before play. It is read-only at runtime. |
| Save/recovery repository | J5, long-session recovery | Owns atomic local snapshot writes, validation, quarantine, migration, retention, export/import when approved, and explicit deletion. |
| PWA release manager | J7, install/offline/update safety | Owns precache manifest, cache integrity, install affordance, and safe-boundary activation. It never replaces a running release or a pending save write. |
| Error boundary and consent-gated diagnostics | Crash/error recovery and privacy | Shows retry/title/recovery actions. Local diagnostic records are minimal and removable; no telemetry transport exists in P0. |

### Dependency direction and state rules

```text
authored content ──> content validator ──> deterministic rules core <── input actions
                                            │
web/PWA shell + renderer <── state/events ─┼──> save/recovery repository
        │                                   │
        └──────────> PWA release manager ──┴──> error boundary / local diagnostics
```

Only the rules core can produce durable campaign state. The shell owns
ephemeral UI state (open panels, selection, animation), while the repository
owns only serialized snapshots and recovery metadata. Rendering, input,
caching, and diagnostics must not be required to make a legal game decision.

## Data contract

### Ownership, lifecycle, and retention

| Data class | Owner and lifecycle | Persistence / retention | Access and recovery |
| --- | --- | --- | --- |
| Content package | Build/content owner: authored → schema-validated → bundled → immutable release artifact → superseded | Public static assets; current and previous known-good cache retained per cache policy | Read by client only; invalid references reject package before gameplay. |
| Campaign snapshot | Player; new game → checkpoint/manual save → valid, migrated, quarantined, or explicitly deleted | Browser-origin local storage appropriate for structured durable data (implementation selects IndexedDB or equivalent); retain current valid slot plus last-known-good checkpoint | Same browser origin only in P0; player may load, delete after confirmation, and receive export/support guidance where feasible. |
| Settings | Player; default → previewed → applied → persisted/reset | Separate local preference record; current session remains active if persistence fails | Read/write only by local game; reset requires confirmation. |
| Recovery metadata | Client; write attempt/failure → recovery offer → resolved | Local, bounded and tied to save slot; remove with slot/delete-local-data action | Never overwrites valid snapshot; aids quarantine and fallback. |
| Diagnostic record | Player-controlled, consent-gated; fault → local record → optional future export/delete | Bounded local record, no identifiers, no campaign dialogue, and no network sending in P0 | Player can decline, clear, or export only after a future approved workflow. |

The local campaign is the P0 source of truth. There is no account, remote
profile, analytics stream, purchase ledger, match state, or cloud backup.
Remote account-linked replication is a later optional mirror—not campaign truth
until approval defines identity, vendor, consent, cost, retention, deletion,
support, conflict UX, and outage behaviour.

### Versioned content and save schemas

All high-volume authored data uses a versioned, machine-validated package:

```text
ContentPackage { packageId, semanticVersion, schemaVersion, localeDefault,
  scenes[], exits[], dialogues[], quests[], encounters[], enemyDefinitions[],
  itemDefinitions[], rewards[], localisation[], assetManifest[] }
SaveSnapshot { schemaVersion, contentPackageId, contentVersion, slotId,
  revision, checkpointId, campaign, quests, party, inventory, rewardLedger,
  settingsReference?, checksum, committedAt }
```

- **Ownership and authoring:** designated game/content owners maintain source
  data in repository-controlled files and original asset references. The exact
  editor/format is an implementation choice; generated bundles are derived,
  never hand-edited.
- **Validation:** CI validates JSON/schema shape, unique stable IDs, required
  fields, asset and localisation-key existence, valid quest predicates,
  scene/spawn/exit targets, legal reward/item/enemy references, no duplicate
  reward IDs, and reachability from opening scene to ending. It also rejects
  missing required translations in any release locale and unsafe quest-item
  removal paths.
- **Relationship rules:** every required quest path has a reachable transition;
  each locked exit predicate refers to an existing quest state; each encounter
  has legal targets/actions and a completion path; all rewards resolve to
  extant definitions. Tests include valid minimal package, each broken
  reference class, and a graph traversal proving the authored campaign is
  completable.
- **Import/export:** P0 imports content only at build time through the
  validator and packages it into the release. Player save export/import is not
  promised; if added, it must use a versioned envelope, parse/validate before
  write, never replace a valid save until confirmation, and reject untrusted
  payloads safely.
- **Compatibility:** each release declares supported content and save schema
  ranges. Incompatible saves are quarantined with their original bytes and a
  clear fallback/new-game action; a migration must create a new candidate and
  validate it before promotion.

## Commands, validation, idempotency, and concurrency

The core exposes typed intent commands such as `StartCampaign`,
`ChooseAction`, `UseItem`, `Talk`, `AcceptQuest`, `ClaimReward`,
`EnterExit`, `CommitCheckpoint`, `LoadSlot`, and `ApplySettings`. A command
contains an expected campaign revision and an interaction/action ID. The core
returns either a typed rejection without mutation or an ordered state/event
result with a new revision.

- Validate session state, command shape, actor/target existence, availability,
  eligibility, quest predicate, and expected revision before mutation. UI
  selections are untrusted/stale inputs even though all execution is local.
- Use stable `rewardId`/`grantId` ledger entries and interaction IDs. Retrying
  an acknowledged reward, quest completion, or checkpoint returns the prior
  result rather than granting twice.
- One command is processed at a time per active campaign. Disable/debounce
  duplicate controls while pending; compare expected revision on completion.
  Visibility changes, gamepad repeats, and multiple tabs cannot interleave
  transitions. A second tab must be warned/read-only or acquire an explicit
  local slot lease; stale writers fail without replacing the latest revision.
- Combat resolution uses an explicit deterministic seed/state recorded at
  safe boundaries. It never persists an unresolved turn; a crash restores the
  prior checkpoint, avoiding half-consumed items, half-applied damage, or
  duplicate rewards.

## Persistence, migration, and failure semantics

Save commit is a write-ahead replacement protocol: serialize a complete
snapshot → validate checksum/schema/invariants → write candidate under a new
revision → verify read-back → mark current → retain prior known-good snapshot.
Implementations must use browser storage semantics that make the final pointer
switch atomic, or emulate it with immutable revision records and a validated
current pointer. Never clear the prior save before the new pointer is valid.

| Condition | Required behaviour |
| --- | --- |
| Storage quota, permission, or unavailable local storage | Keep session playable; show non-blocking save failure and retry guidance; do not claim persistence succeeded. |
| Interrupted/crashed write | Ignore incomplete candidate, retain/reload prior confirmed snapshot, and show recovery state at next launch. |
| Malformed/checksum-invalid save | Quarantine bytes and metadata; do not overwrite; offer last valid checkpoint/new game and support/export guidance where feasible. |
| Migration failure or unsupported version | Preserve original, fail closed into quarantine, and offer clear version/fallback choices. |
| Bad content package/reference | Fail build/CI; if discovered at runtime, stop the affected route, retain save, and offer title/retry rather than corrupting campaign state. |
| Cache/network refresh failure | Continue with known-good cached release; explain first-install offline limitation without pretending an uncached release is playable. |
| Application fault/crash loop | Error boundary offers retry, title, and safe recovery; diagnostics remain local unless explicitly consented and a future transport is approved. |

Migration functions are ordered, pure transformations from one explicit schema
version to the next, with fixtures for every supported predecessor. They must
be idempotent or record the source version so a retry cannot apply a migration
twice. A release may remove old migrations only after a separately approved
support/retention decision.

## Trust, privacy, and security

- Treat content, imported saves, URL parameters, browser events, service-worker
  messages, and persisted bytes as untrusted. Validate and bound sizes before
  parsing; never execute content as code or render dialogue via unsafe HTML.
- Serve production assets over HTTPS with a restrictive content security policy,
  no third-party scripts by default, dependency lock/review, and build-time
  asset integrity/hash manifest. Do not embed credentials in the client.
- Use same-origin storage isolation; minimise persisted data to game state and
  chosen preferences. Do not collect names, contact data, precise location,
  advertising IDs, account identifiers, payment data, or gameplay analytics in
  P0.
- Diagnostics default off where consent is required and must state fields,
  purpose, retention, deletion, and transport before collection. A local
  diagnostic record excludes free-text dialogue and complete save contents.
- There is no authorization role in P0 because there is no server resource or
  identity boundary. Locally, a player controls their browser profile; this is
  not a security guarantee against a device owner. Any server feature requires
  explicit least-privilege roles, authenticated authorization on every request,
  rate limits, audit events, deletion/retention policy, incident ownership, and
  documented offline/outage behaviour before implementation.
- No copied branding, assets, text, layouts, or distinctive interaction
  sequences enter the content pipeline. Provenance/review is required for
  shipped art, audio, writing, and dependencies.

## Target-platform matrix

| Contract area | Responsive public web application | Installable PWA |
| --- | --- | --- |
| Shared code/data boundary | Same rules core, content package, save schema, semantic actions, accessibility settings, and release compatibility rules. Browser adapter owns viewport/input differences. | Same shared core/data. Service worker, installation, cache lifecycle, and platform install affordance are PWA adapters. |
| Input and device capability | Keyboard, mouse, touch, and gamepad where exposed; feature-detect and show available mappings. Handle resize, rotation, focus/visibility, reduced-motion/contrast settings where available. | Same inputs and feature detection; no assumed hardware merely because installed. Installation, notifications, or storage-persistence prompts are optional and must not block play. |
| Offline and recovery | May play offline only after relevant assets are cached. First uncached visit tells player an initial download/network is required. Local save protocol applies. | Primary offline route after successful install/cache. Precaches approved shell/content, retains known-good cache on refresh failure, and keeps saves independent of cache eviction. |
| Build and test | Produce hashed static assets, manifest, and browser-compatible bundle. Test core/unit/content validation, responsive layouts, input adaptations, save corruption/migration, error states, and supported browser/device/network matrix. | Build includes service worker and install manifest. Test installability, offline reload, cache rollback/update-at-safe-boundary, storage pressure, and all shared checks. |
| Accessibility and performance | Keyboard-operable menus, semantic labels, visible focus, readable scalable text, captions, non-colour cues, settings persistence, responsive phone/tablet/desktop checks. Establish approval-gated performance budgets for initial load, interaction frame time, memory, bundle/cache size, and slow-network behaviour before release. | Same accessibility/performance requirements, plus offline messaging, update state, install prompt alternatives, and no inaccessible full-screen/install-only path. Measure cold/warm/offline startup and cache size. |
| Release channel and policy | Immutable versioned static release to approved web hosting; staged/canary and rollback process must be selected before launch. Publish supported-browser matrix, privacy notice if diagnostics changes, and recovery notes. | Browser-mediated install/update channel; manifest/icon/display policy and service-worker behaviour must meet supported browser/platform rules. Prompt only at safe boundaries; release notes and rollback retain prior runnable cache. |

Support targets are expressed as capability tests rather than invented minimum
OS versions: current and previous major releases of agreed evergreen browsers
on representative phone, tablet, and desktop classes; exact versions/devices,
browser engine exclusions, storage quota, and slow-network thresholds remain a
release approval gate.

## Observability, quality evidence, and release verification

P0 observability is local and player-respecting: structured console/build logs
in development, release/version/cache status visible in support UI, and an
optional bounded local fault record. It has no remote monitoring dependency.
Every fault has a player-facing recovery path and a test that asserts retained
save/cache behaviour as applicable.

| Evidence layer | Required checks |
| --- | --- |
| Rules and data | Unit/property tests for legal/illegal commands, revision rejection, idempotent grants, deterministic combat fixtures, save encode/decode/checksum, migration fixtures, recovery/quarantine, and content schema/reachability/reference validation. |
| Integration | Test shell-to-core action mapping, checkpoint ordering, focus/pause, unavailable input fallback, settings persistence failure, cache/save independence, and PWA safe update behaviour. |
| Target/browser | Run agreed browser/device matrix for keyboard/mouse/touch/gamepad-adapted paths, responsive viewport checks, offline first/repeat visit, install flow where supported, storage failure, and browser accessibility audit/manual assistive-technology checks. |
| Performance/security | Capture approved load/frame/memory/cache budgets on representative low-capability and slow-network profiles; dependency/license/provenance review, CSP/header check, no-secret scan, and import/parser fuzz/bounds tests. |
| Release gate | Versioned content/save compatibility declaration, clean content validation, migration/recovery suite, PWA offline/update/rollback check, accessibility and performance results, privacy/diagnostic confirmation, and tested rollback to a known-good release. |

Release is blocked when validation cannot prove campaign reachability, a save
could overwrite the last known-good state, an update can activate mid-combat or
mid-write, an unsupported capability blocks the core path without explanation,
or any mandatory quality budget/matrix remains unapproved or unmeasured.

## Decisions deferred for approval

These are intentionally not selected by this contract: game engine/framework,
rendering library, static host/CDN, CI provider, diagnostics vendor/transport,
exact storage API/quota, browser/OS/device minimums, performance thresholds,
languages, age/parental/regional obligations, service-worker rollout policy,
and content editor format. Account identity, remote save replication,
multiplayer/player safety, live operations, analytics, purchases, and
entitlements require separate product, security, privacy, cost, failure-mode,
and support approval before they are allowed to alter this architecture.
