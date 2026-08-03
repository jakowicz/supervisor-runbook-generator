# 06 — Foundation and domain authoring contracts

**Inputs:** [delivery map](05-delivery-map.md), [technical contract](../specification/03-technical-contract.md), [feature model](../specification/02-feature-model.md), and [experience contract](../specification/04-experience-contract.md).

## Purpose and use

This is the authoring input for later implementation runbooks. Each record is
an atomic, independently reviewable outcome; it is not authority to choose an
engine, vendor, remote service, or production browser matrix. A later runbook
must name its contract ID, preserve its ownership boundary, and either resolve
the listed decision gate or stop before work that depends on it.

The P0 product remains a client-side, offline, single-player web/PWA campaign.
`Shared` denotes work used by both responsive web and installed PWA. `Web`
denotes browser-only work; `PWA` denotes a service-worker/install adaptation.
No contract below creates account, sync, multiplayer, commerce, analytics, or
live-service functionality.

## Contract record conventions

- **Implementation ID** is stable and must be cited by dependent runbooks.
- **Owns** gives the sole initial owner of files and durable data. Paths are
  planned paths until FDN-01 has an approved framework.
- **Does not own** prevents adjacent work from being pulled forward.
- **Acceptance evidence** is the artifact a supervisor can inspect after the
  stated verification passes.
- A decision gate is a blocking approval, not a default that an author may
  silently select.

## Foundation contracts

### FDN-01 — Bootstrap the reproducible project baseline

- **Scope / target:** Shared build and test baseline for responsive web and
  PWA; no gameplay or PWA cache implementation.
- **Bounded outcome:** An approved engine/framework project skeleton has one
  documented bootstrap command, deterministic test command, lint/format
  commands, and the planned source/test directory boundaries.
- **Dependencies:** Approved engine/framework, package manager, and CI runtime.
- **Owns:** Root build/tooling configuration; `src/{core,content,platform/web,app}/`;
  `tests/{core,content,platform,app}/`; `docs/development.md`.
- **Does not own:** Domain rules, content, persistence implementation, UI,
  service worker, hosting, or a browser support promise.
- **Verification:** Clean checkout/bootstrap succeeds in the approved runtime;
  formatting and lint commands pass; a deterministic core sample test runs.
- **Acceptance evidence:** Pinned toolchain/version declaration, documented
  command transcript, and CI-equivalent check output.

### FDN-02 — Declare configuration and environment boundaries

- **Scope / target:** Shared release configuration with Web/PWA build inputs;
  no remote runtime configuration or secrets.
- **Bounded outcome:** Typed, validated build configuration separates public
  release metadata from development-only settings, fails closed for absent or
  malformed required values, and prevents client-secret inclusion.
- **Dependencies:** FDN-01; approved release/versioning and hosting inputs.
- **Owns:** Root configuration schema/loader; checked-in example configuration;
  build-time environment documentation; release metadata interface.
- **Does not own:** Account credentials, telemetry endpoints, feature flags for
  unapproved services, or values for undecided vendors/hosts.
- **Verification:** Valid sample configuration builds; missing/invalid required
  value fails with actionable output; release artifact scan finds no secret-like
  configured value.
- **Acceptance evidence:** Configuration contract, sample file, negative-test
  fixtures, and an artifact-scan report.

### FDN-03 — Establish architecture seams and dependency rules

- **Scope / target:** Shared core/content/application boundaries plus Web and
  PWA adapter boundaries.
- **Bounded outcome:** Enforced imports/interfaces ensure the deterministic
  core has no browser, renderer, timer, or network dependency; UI and input
  submit commands only; persistence serializes confirmed core state only.
- **Dependencies:** FDN-01; FDN-02 for build-time enforcement configuration.
- **Owns:** `src/core/` public command/state/event interfaces; boundary/lint
  rules; adapter interface definitions; architecture decision documentation.
- **Does not own:** Concrete combat, exploration, UI panels, storage driver,
  service worker, or content package data.
- **Verification:** Dependency-rule test rejects forbidden core imports; a
  fixture adapter can submit an action and render returned state/events without
  direct state mutation.
- **Acceptance evidence:** Dependency graph/check output, public-interface
  inventory, and passing adapter fixture test.

### FDN-04 — Define semantic design-token contracts

- **Scope / target:** Shared visual/accessibility semantics, with responsive
  Web layout use and PWA inheriting the same tokens.
- **Bounded outcome:** Original, named tokens cover restrained warm-fantasy
  colour roles, typography scale, spacing, radii, elevation, focus, motion,
  touch target, status, and non-colour state cues; tokens support text scaling,
  contrast modes, reduced motion, and captions without asserting final art.
- **Dependencies:** FDN-01; accessibility acceptance criteria; final font and
  contrast targets remain approval gates.
- **Owns:** `src/app/design/tokens/`; token documentation; token validation or
  preview fixtures.
- **Does not own:** Screens, maps, copied reference styling, art/audio assets,
  final responsive breakpoints, or gameplay UI implementation.
- **Verification:** Token build/type validation passes; sample semantic states
  retain a text label and non-colour cue; reduced-motion values remove or bound
  non-essential animation.
- **Acceptance evidence:** Token inventory with role rationale, original-style
  provenance note, and automated validation/sample capture.

### FDN-05 — Model deterministic campaign data and commands

- **Scope / target:** Shared, browser-free domain model for both delivery
  surfaces.
- **Bounded outcome:** Immutable campaign state, typed commands/results/events,
  revisions, interaction IDs, deterministic RNG state, and invariant helpers
  define legal transitions without implementing later feature state machines.
- **Dependencies:** FDN-01 and FDN-03; party size and content quantities are
  approval gates for any concrete shape beyond the minimum contract.
- **Owns:** `src/core/{state,commands,events,invariants,rng}/` and
  `tests/core/contract.*`.
- **Does not own:** Authored content values, inventory/combat/quest algorithms,
  save storage, UI selection state, account profiles, or network state.
- **Verification:** Unit tests show invalid commands do not mutate state,
  expected-revision mismatch rejects stale intent, and repeated interaction IDs
  do not produce an extra durable transition.
- **Acceptance evidence:** Versioned type/interface reference, invariant-test
  report, and rejection/idempotency fixtures.

### FDN-06 — Define the local persistence and recovery protocol

- **Scope / target:** Shared save schema/protocol with a Web local-storage
  adapter; installed PWA uses the same browser-origin data independently of
  cache lifecycle.
- **Bounded outcome:** A schema contract specifies immutable revisions,
  checksums, validated current pointer, last-known-good retention, quarantine,
  settings separation, deletion confirmation, and pure ordered migrations.
- **Dependencies:** FDN-03 and FDN-05; approved browser storage API/quota and
  save-support retention policy.
- **Owns:** `src/core/save/{schema,compatibility,migrations}/`;
  `src/platform/web/persistence/`; `tests/{core,platform}/**/*save*`; save and
  recovery documentation.
- **Does not own:** Cloud sync, account-linked saves, content import/export,
  PWA cache records, or a guarantee after user/browser storage eviction.
- **Verification:** Fault-injection fixtures cover interrupted write, checksum
  failure, malformed/unsupported migration, quota/permission failure,
  quarantine, retry, and selected-slot deletion; every supported predecessor
  fixture migrates once without modifying its original bytes.
- **Acceptance evidence:** Save-state diagram, schema compatibility table,
  fixtures, and passing fault/migration report showing retained valid revision.

### FDN-07 — Bound the deferred identity contract

- **Scope / target:** Explicit P0 exclusion shared by Web and PWA; no identity
  adapter is built.
- **Bounded outcome:** The domain and storage interfaces prove no player
  account identifier, authentication token, remote profile, or sync authority
  is needed for an offline campaign; future identity integration requirements
  are recorded as a decision gate.
- **Dependencies:** FDN-03, FDN-05; explicit product/privacy/security/vendor
  approval before any connected identity work.
- **Owns:** Architecture/privacy decision record and contract tests asserting
  local-save interfaces require only local slot identity.
- **Does not own:** Sign-up, sign-in, guest accounts, OAuth, session handling,
  cloud sync, remote deletion, or support identity lookups.
- **Verification:** Static/dependency scan finds no account/token fields or
  network identity client in P0 foundation modules; local campaign start/save/
  resume fixture runs with no identity input.
- **Acceptance evidence:** Recorded P0 exclusion, future-approval checklist
  (identity provider, consent, outage, retention/deletion, support, conflict),
  and scan/test output.

### FDN-08 — Bound the deferred authorization contract

- **Scope / target:** Explicit P0 exclusion shared by Web and PWA; browser
  profile control is not presented as authorization.
- **Bounded outcome:** The contracts state that P0 has no server resource or
  role boundary; future authorization must be server-enforced, least-privilege,
  authenticated per request, auditable, rate-limited, and resilient to outage.
- **Dependencies:** FDN-07 and explicit approval for a server resource and
  identity policy.
- **Owns:** Security/architecture decision record and negative contract tests
  that domain commands do not accept client-asserted role/permission fields.
- **Does not own:** Roles, permissions, administration, moderation, player
  safety, purchase entitlement, server APIs, or client-side permission checks.
- **Verification:** Type/interface scan confirms no authorization fields in
  P0 commands/snapshots; negative fixture rejects or cannot construct a
  client-supplied privilege claim.
- **Acceptance evidence:** P0 authorization-exclusion statement, future
  service authorization checklist, and passing negative test/scan report.

### FDN-09 — Build the layered deterministic test harness

- **Scope / target:** Shared unit/content/integration harness; Web adapter
  checks; PWA lifecycle browser tests only after service-worker work exists.
- **Bounded outcome:** Test conventions and fixtures make deterministic domain,
  content validation, persistence fault injection, application integration,
  and browser-change coverage independently runnable with isolated data and no
  real services.
- **Dependencies:** FDN-01–FDN-06; FDN-07–FDN-08 exclusion fixtures; approved
  browser/device matrix and performance budgets for final target claims.
- **Owns:** Test-runner configuration; fixture factories; deterministic RNG/
  clock controls; `tests/{core,content,platform,app}/`; test guidance; reserved
  `supervisor/browser/tests/changes/` conventions.
- **Does not own:** Final game feature assertions, production telemetry,
  performance-budget values, or a smoke spec before a browser-facing feature
  has an implemented surface.
- **Verification:** One command runs each test layer; a deliberately failing
  fixture is detected; fixtures cannot write to a real player slot; repeated
  run produces identical core result/event data.
- **Acceptance evidence:** Test command matrix, fixture-isolation proof,
  deterministic-run comparison, and documented mapping from later contract IDs
  to their unit/integration/browser evidence.

## Authoring order and cross-target allocation

| Order | Contract | Later runbook may start when | Target allocation |
| --- | --- | --- | --- |
| 1 | FDN-01 | Framework/toolchain approval exists. | Shared baseline |
| 2 | FDN-02, FDN-03 | FDN-01 is verified. | Shared; Web/PWA build boundaries |
| 3 | FDN-04, FDN-05 | Architecture seams are verified. | Shared; Web token consumption |
| 4 | FDN-06, FDN-09 | Core contract and storage decision are approved. | Shared schema, Web adapter, PWA inherits saves |
| Gate only | FDN-07, FDN-08 | A connected product decision is explicitly approved. | No P0 implementation on either target |

## Unresolved decisions to carry forward

1. Engine/framework, package manager, CI runtime, browser storage API/quota,
   and release host remain unselected.
2. Browser/device/assistive-technology support matrix, performance budgets,
   final font, contrast thresholds, locales, party size, and content quantities
   require approval before final claims or fixtures use concrete values.
3. Account/sync, multiplayer/safety, live operations, analytics, commerce, and
   entitlements remain excluded from P0. They must receive separate product,
   privacy, security, cost, support, and failure-mode contracts before work.
