# 03 — Technical, data, trust, and quality contract

**Inputs:** [`INITIAL.md`](../INITIAL.md), [domain discovery](00-domain-discovery.md),
[game identity](01-game-identity.md), [creative direction](01-creative-direction.md),
[feature model](02-feature-model.md), and [game design bible](02-game-design-bible.md).

This contract implements the bounded first-release football-trivia game. It
does not turn the brief's approval-gated account, multiplayer, live-service,
commerce, or remote-sync requests into production scope. It specifies a
vendor-neutral architecture so those systems can be added only after their
identity, cost, safety, retention, and outage decisions are approved.

## Production architecture and boundaries

The release is an offline-capable 2D client game with one shared deterministic
domain core, immutable validated content packages, platform adapters, and local
durable storage. The initial web/PWA and Android/iOS outputs package the same
core and content; a platform adapter may render, persist, cache, map inputs,
report a fault locally, or obtain an approved release, but cannot adjudicate an
answer or alter a score. The core has no renderer, platform API, clock, network,
or third-party-service dependency.

| Component / owned boundary | Product or quality requirement traced | Contract |
| --- | --- | --- |
| Quiz application shell | GAME-005/008/009; J0–J3 | Owns routes, focus, pause/visibility prompts, ephemeral UI and accessible rendering. Sends intents to the core and never mutates a run directly. |
| Input and accessibility adapters | GAME-009/012; responsive web and phones | Map touch, pointer, keyboard, and gamepad to semantic actions (`navigate`, `select`, `submit`, `back`, `pause`). Apply text/contrast/reduced-motion/caption settings; unsupported hardware has a visible equivalent. |
| Deterministic quiz core | GAME-001, 003, 005–008 | Owns selection, normalisation/adjudication, score/streak, milestones, legal lifecycle transitions, and versioned rule calculations. Explicit seed and rule version make selection/results reproducible. |
| Content registry and validator | GAME-001–004; curated original bank | Resolves immutable published packages by stable ID and refuses invalid or withdrawn content before it can enter a new round. Runtime reads only validated data. |
| Save/recovery repository | GAME-008/010; J3 | Owns revisioned snapshots, checksum/validation, atomic promotion, rollback, migration, quarantine, export only if later approved, and confirmed deletion. |
| Release/cache manager | GAME-011/012; PWA/mobile offline delivery | Stages signed/hashed approved package and assets; activates only between rounds and never during a save commit. It retains a known-good compatible package on update failure. |
| Error boundary and diagnostics | crash recovery and privacy | Owns plain-language retry, return-home, and recovery choices. P0 diagnostics are local and consent-gated; no telemetry transport is assumed. |
| Editorial build tooling | J4/J5; factual/release integrity | Imports author-controlled source files, runs schema/relationship/provenance checks, and emits a content manifest. It has no runtime authoring or publishing endpoint. |

```text
authored content ─> build validator ─> immutable ContentPackage ─┐
                                                               ├─> deterministic quiz core <─ semantic input actions
platform renderer/accessibility <─ state + events ─────────────┘             │
             │                                                               ├─> save/recovery repository
             └─> release/cache manager (safe boundary only) ─────────────────┴─> local error/diagnostic record
```

Only the core creates durable game facts. The shell owns transient selection,
focus, animation and open-panel state. The repository owns serialized records,
not gameplay. Content/cache, diagnostics, and UI must not be prerequisites for
a legal answer, score, or completed tutorial.

## Data, editorial content, and lifecycle contracts

| Data class | Owner and lifecycle | Local persistence/retention | Access, recovery, and authorization |
| --- | --- | --- | --- |
| `ContentPackage` | Editorial owner: draft → review → published → staged → active → superseded/rolled back/withdrawn | Bundled or cached immutable release artifact; current compatible and last-known-good package follow platform cache policy | Player runtime reads only published package. No content write API, account role, or remote publish service exists in P0. |
| `LocalProfile`, settings | Player: new → active → deletion-pending → deleted; settings valid → applied → reset | Separate local records; retained until explicit profile deletion | Browser/device profile controls local access. Failed setting write retains the applied session value and explains it. |
| `RoundRun`, attempts, results, milestones | Core: created → active/paused → complete, abandoned, or recoverable; attempts presented → draft → submitted → resolved | Valid confirmed snapshots plus prior known-good revision; unresolved draft is disposable | Immutable resolved attempts reference exact content/rule versions. A player may recover/discard only their local state. |
| `SaveSnapshot`/recovery record | Repository: candidate → validated → confirmed → superseded/quarantined → deleted | Current confirmed revision and prior valid revision; recovery metadata is bounded and deleted with profile | No overwrite of a valid revision by a malformed candidate. Corruption/migration failure offers last valid snapshot or new game. |
| Original visual/audio assets and strings | Creative/content owner: source → provenance/review → manifest reference → packaged → superseded | Versioned content package references; source provenance retained in repository/release records | Runtime may resolve only manifest IDs. Missing optional cue gives text feedback; missing required asset rejects release. |
| Diagnostic record | Player-controlled: fault → local bounded record → cleared/exported only if later approved | Default no transport; bounded local retention and clear control | Excludes prompts, typed answers, profile identifiers and save content. Consent is required before recording any optional diagnostic. |

### Versioned question, feedback, and asset schema

High-volume creative content is a first-class build input. Generated packages
are never hand-edited, and stable IDs are never reused for a different fact.

```text
ContentPackage {
  packageId, semanticVersion, schemaVersion, defaultLocale, ruleVersion,
  cards[], roundDefinitions[], categories[], strings[], visualAssets[], audioCues[],
  provenanceRecords[], reviewRecords[], manifestHash, compatibility
}
QuestionCard {
  id, revision, status, format, promptKey, answerRule, explanationKey,
  categoryId, era, competitionScopes[], difficultyBand, tags[], provenanceId,
  reviewIds[], visualAssetIds[], audioCueIds[], localeCoverage
}
AnswerRule { canonicalIds[] | canonicalBoolean | orderedIds[] | typedAliases[] }
AudioCue { id, revision, trigger, captionKey, durationClass, provenanceId, optional }
VisualAsset { id, revision, kind, sourceHash, altKey, provenanceId }
SaveSnapshot {
  schemaVersion, contentPackageId, contentVersion, ruleVersion, profileId,
  revision, status, selectionSeed, roundRun, attempts[], scoreState,
  milestones, repeatLedger, settingsRef, checksum, committedAt
}
```

`QB-A-01…48` and `TUT-01…05` are reserved stable card IDs; a correction creates
a new card revision and correction history rather than silently changing an
old run. Prompts, options, canonical answer labels, explanations, categories,
captions, cue descriptions, asset alt text, and UI copy are localisation keys.
An offered locale must supply reviewed strings and valid typed-answer aliases;
otherwise it is unavailable, not partially substituted. Audio trigger names
(`prompt_arrival`, `correct`, `incorrect`, `streak_rise`, `saved`, `results`)
are data IDs, with caption/text equivalents and mute/volume behaviour; audio
never carries essential information alone.

### Editorial ownership, validation, import/export, and reference integrity

- The designated editorial owner creates original card sources; factual source
  and rights/provenance record, checked date, accessibility/copy review, and
  two reviewer IDs are required to publish. Uncertain rights or disputed facts
  block the card. No scraping, copied question, unreviewed AI fact, or runtime
  authoring/import is allowed.
- The build import path is repository-controlled structured source → validator
  → immutable package/manifest. A future editor may produce that source only if
  it preserves schemas, stable IDs, review/provenance, deterministic export,
  and the same validator. Player save export/import is not a P0 feature; any
  later import must use a versioned envelope, size bounds, parse-before-write,
  confirmation, and preserve the valid save on failure.
- Validation rejects duplicate IDs/aliases, unpublished/withdrawn cards,
  absent review/provenance/localisation keys, invalid format-specific answer
  rules, missing assets/captions, unsupported cue trigger, invalid references,
  incomplete compatibility declaration, and package hash mismatch. It enforces
  GAME-002 totals/distribution/caps and GAME-006 format/difficulty adjacency
  capability before release.
- Relationship tests prove every round references eligible cards, every card
  resolves its answer/explanation/category/assets/cues/provenance/reviews, each
  alias has one intended canonical answer within a locale, and withdrawn cards
  cannot appear in new selection. Fixed fixtures cover TUT-01…05, representative
  cards of each format, aliases/diacritics/blanks/ambiguity, shortages, a bad
  reference of every class, and a corrected old-content run.
- Package compatibility declares supported save-schema, content-schema, and
  rule-version ranges. An old snapshot continues to display its referenced
  explanation where its package is retained; unsupported data is quarantined,
  never guessed or rewritten. Content can activate only between rounds.

## Commands, validation, idempotency, and concurrency

The core accepts typed intents: `CreateProfile`, `StartTutorial`, `StartRound`,
`SelectAnswer`, `EnterTypedAnswer`, `ConfirmBlank`, `SubmitAnswer`, `Pause`,
`Resume`, `CompleteRound`, `CommitSnapshot`, `RecoverSnapshot`, `DeleteProfile`,
and `ApplySettings`. Each state-changing intent carries `expectedRevision` and
a unique `interactionId`, and returns a typed rejection or ordered state/events
with a new revision.

- Before mutation validate command shape/size, active lifecycle state,
  expected revision, content/rule compatibility, card eligibility, selected
  option or typed-answer normalisation, and required safe-boundary condition.
  Treat UI events, deep links, cached content and persisted bytes as untrusted.
- Typed answers use the GAME-003 deterministic Unicode/case/punctuation/
  whitespace/diacritic normalisation and configured aliases only—never fuzzy
  matching. Blank needs explicit confirmation; a resolved submission is
  immutable and shows canonical answer/explanation.
- `interactionId`, completed-run ID, milestone key and snapshot revision form
  idempotency keys. Retried submission/complete/snapshot returns its recorded
  result; it never adds score, streak, milestone, or history twice. A replay is
  a new run with a new selection seed.
- Process one intent per local profile/run. Disable/debounce submit while it is
  pending and reject an old revision after asynchronous persistence completes.
  A second browser tab or resumed process acquires a local lease or becomes
  read-only; a stale writer cannot replace the latest confirmed revision.
- Selection uses an explicit deterministic seed with content/rule version and
  local repeat ledger recorded in the snapshot. The last two completed rounds
  are excluded where possible; a shortage is a disclosed deterministic result,
  not a hidden reroll.

## Persistence, migrations, and failure semantics

At tutorial completion, every resolved-question boundary, explicit pause, and
completed result, save by: serialize a candidate → validate schema/checksum/
invariants → write immutable revision → read back/validate → atomically promote
current pointer → retain prior known-good revision. Storage must provide an
atomic final pointer or emulate one with revision records. It must never clear
the previous confirmed snapshot before promotion succeeds.

| Condition | Required player-safe behaviour |
| --- | --- |
| Quota, permission denial, unavailable storage | Keep round playable, retain previous confirmed snapshot, state that saving failed, and offer retry/continue without saving. |
| Process death/interrupted write | Ignore incomplete candidate; load prior confirmed revision and offer the normal resume state. |
| Corrupt/checksum-invalid draft or snapshot | Quarantine bytes/metadata without overwrite; offer last known-good snapshot, discard draft, or new local profile. |
| Unsupported schema or migration failure | Preserve original candidate, fail closed into quarantine, and offer explicit recovery/new-game path. |
| Invalid/partial content/cache update | Keep compatible active package and save; block affected new-round route with retry/home explanation. Never activate it mid-round. |
| First offline visit/no cached package | Explain that initial approved download is needed; never misrepresent an uncached game as offline-ready. |
| Fault/crash loop | Error boundary offers retry, return home, and recovery; optional local diagnostics do not block either action. |
| Explicit deletion | Confirm scope, then remove profile/settings/history/snapshots/recovery records/local diagnostics and return to first launch. |

Migrations are pure, ordered `fromSchema → toSchema` transformations with
fixtures for each supported predecessor. They run into a new candidate,
validate before promotion, and are idempotent or record source version so a
retry cannot apply one twice. A migration cannot reinterpret old answer facts,
grant new score/milestones, or change a completed run's content/rule reference.

## Trust, privacy, security, and authorization

- P0 has no server-owned resource and no player account: there is therefore no
  remote authorization role. A device/browser-profile owner can alter local
  data; local persistence is integrity/recovery protection, not anti-cheat.
  Editorial publication is an offline repository/release responsibility, not a
  client role. Any future server requires authenticated least-privilege roles,
  authorization on every request, rate limits, audit records, support owner,
  deletion/retention and outage/conflict policy before implementation.
- Persist only necessary local profile, game state, preferences, compatible
  content/cache and bounded recovery data. Do not collect names, contact data,
  precise location, ad IDs, payment data, account IDs, raw typed answers, or
  gameplay analytics. A diagnostic excludes question text, answer text, save
  payload and unique identity; consent describes fields, purpose, retention,
  deletion, and any approved transport.
- Validate and size-bound package, save, import, URL, platform event and
  service-worker message before parsing. Render authored text as text, never
  executable/unsafe HTML. Pin/review dependencies, scan generated release for
  secrets, use HTTPS and restrictive CSP/no third-party scripts for web builds,
  hash assets/manifests, and never embed credentials.
- All writing, art, visual asset and audio cue records carry provenance. The
  pipeline rejects copied reference expression and preserves source hash or
  original-work record. Functional references inform breadth/session goals only.

## Target-platform matrix

Exact minimum OS/browser, orientation, budgets, store metadata and distribution
providers remain release-approval gates. The following is the required target
contract, not a claim that each platform capability is universally available.

| Contract | Responsive public web | PWA | Android phone | iPhone (iOS) |
| --- | --- | --- | --- | --- |
| Shared code/data boundary | Shared core, schemas, package, actions, save semantics; web renderer/layout adapter only. | Same shared core/data; install/service-worker/cache adapter only. | Same shared core/data; native/web-runtime packaging, touch/accessibility/storage adapter only. | Same shared core/data; iOS packaging, touch/accessibility/storage adapter only. |
| Inputs/device capabilities | Keyboard, mouse, touch, gamepad when exposed; resize/visibility; feature-detect all. | Same; install/notification/storage prompts optional and non-blocking. | Touch first; orientation choice TBD; respect system text, contrast, motion, audio and focus affordances. | Touch first; orientation choice TBD; respect system text, contrast, motion, audio and focus affordances. |
| Offline and recovery | Offline only after assets/package cached; first uncached visit explains network need. Local save is independent of cache. | Installable offline route after successful cache; known-good cache survives refresh failure; safe update notice. | Packaged/cache-approved content and independent local save; offline core works after first installation; update only safe boundary. | Same as Android, subject to platform storage/cache behaviour; retain confirmed save across package/content update. |
| Build and test | Hashed static bundle/manifest; core/content/save unit tests; browser layout, keyboard/mouse/touch/gamepad, slow-network and error checks. | Adds manifest/service worker; test install, offline reload, cache rollback, update-safe-boundary, cache/storage pressure. | Signed store-compatible build after approval; test physical/emulated representative touch, interrupt/resume, storage pressure, accessibility, battery/thermal/size budget. | Signed store-compatible build after approval; test representative devices, interrupt/resume, storage pressure, accessibility, battery/thermal/size budget. |
| Accessibility/performance | Semantic labels, focus, text scaling, contrast, captions/non-colour cues; measure approved load/frame/memory/bundle budgets across phone/tablet/desktop. | Same plus offline/update/install state is fully operable; measure cold/warm/offline startup and cache size. | Touch target, screen reader, text scaling, reduced motion/captions; measure startup/frame/memory/download/battery/thermal against approved thresholds. | Equivalent outcome using platform assistive tech; measure same approved mobile budgets and interrupted-state recovery. |
| Release channel/policy | Approved immutable static host; selected staged rollout/rollback; publish browser support, privacy and recovery notes. | Browser-mediated install/update; safe prompt, manifest/icon/display requirements, rollback retains runnable cache. | Approved Android distribution/store channel; complete privacy/data-safety, signing, age/content, accessibility and release-note requirements before submission. | Approved App Store/TestFlight channel; complete privacy nutrition label, signing, age/content, accessibility and review requirements before submission. |

The shared game is capability-tested on current and previous agreed browser/OS
releases and representative phone, tablet and desktop classes. If an agreed
target lacks a capability, the app provides an understandable fallback or is
excluded by the approved support matrix—never silently weakens a core rule.

## Observability, quality evidence, and release verification

P0 observability is local and supportable: structured development/build logs,
visible package/save/cache version status, and optional minimal local fault
record. Every fault must have player-facing recovery and evidence that save or
cache protection held. External crash, analytics, account, commerce, live-op,
multiplayer/moderation, notification, and sync providers remain optional and
unintegrated until credentials, cost, data use, reliability and failure
behaviour receive approval.

| Evidence layer | Required evidence before release |
| --- | --- |
| Rules/content | Unit/property fixtures for formats/normalisation, illegal lifecycle commands, scoring cap/reset, deterministic seeds/repeat exclusion, immutable results/idempotency, card schema/provenance/review/distribution/reference/localisation/asset/cue validation. |
| Save/recovery | Encode/decode/checksum, atomic-promotion sequence, concurrent/stale revision, write/quota failure, crash restart, corrupt draft, every migration predecessor, content compatibility, delete-profile and no-double-completion fixtures. |
| Integration | Shell-to-core action mapping; tutorial offline completion; focus/pause/resume; missing audio/input fallback; settings persistence failure; package update between rounds; cache/save independence; error retry/home paths. |
| Targets/accessibility | Matrix checks for responsive viewport, keyboard/mouse/touch/gamepad paths, PWA install/offline/update, Android/iOS touch/interruption/storage, semantic/focus/manual assistive-technology checks, text/contrast/reduced-motion/captions. |
| Performance/security | Measured approved initial/warm/offline load, frame, memory, cache/download, slow-network, battery and thermal budgets; dependency/license/provenance/secrets review; CSP/HTTPS/manifest hash checks; parser bounds/fuzz tests. |
| Release gate | Clean content validation; compatibility declaration; migration/recovery suite; target build/install evidence; PWA rollback/offline check; accessibility/performance results; store/privacy copy; known-good content and app rollback rehearsal. |

Release is blocked if a package can select unpublished/ambiguous content, a
save can replace the last valid snapshot, an update can switch mid-round or
mid-write, core play lacks an accessible fallback, or a required approved
matrix/budget/policy evidence item is absent.

## Approval-gated decisions

This contract deliberately does not select engine/framework, rendering library,
storage implementation, static host/CDN, CI, signing/distribution tooling,
diagnostic vendor/transport, content editor, exact support matrix/orientation,
performance/download/battery/thermal budgets, languages, audio count, or
regional/age/store policy. Account/identity, remote sync and conflict handling,
multiplayer safety, live operations, analytics, IAP/entitlements, seasonal
content and player-created/shared content require separate product, security,
privacy, cost, operational ownership and failure-semantics approval. Until
then they cannot be implicit dependencies of the playable offline release.
