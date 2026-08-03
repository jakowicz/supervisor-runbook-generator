# 08 — Quality, operations, and release authoring contracts

**Inputs:** [delivery map](05-delivery-map.md), [foundation and domain
contracts](06-foundation-domain-contracts.md), [feature and experience
contracts](07-feature-experience-contracts.md), and the
[technical contract](../specification/03-technical-contract.md).

## Purpose and operating boundary

These records turn the approved P0 trust, quality, recovery, and release
requirements into implementation contracts. They apply to the static,
client-side, offline single-player web/PWA release. They do **not** authorise
a server, account identity, remote saves, multiplayer, moderation, live
operations, analytics, purchases, entitlements, or an external crash-reporting
service.

`Evidence` means a reviewable artifact produced by the named check or a human
record with its date, release candidate version, executor, outcome, and any
exception. A generated report, screenshot, or command transcript may not be
invented, backdated, reused for a different candidate, or marked passing when
the underlying action did not run. Manual, external, paid, privileged, or
production actions remain `not run` until a named authorised person supplies
real evidence.

Paths are planned implementation paths until the framework and tooling are
approved. A later runbook must cite the applicable contract IDs and must stop
at an unresolved decision gate rather than silently selecting a provider,
browser matrix, budget, retention period, or production process.

## Shared evidence record

Each record used for a release has this minimum metadata:

| Field | Required content |
| --- | --- |
| Candidate | Immutable build/version identifier and content/save-schema compatibility declaration. |
| Requirement | Contract ID and exact requirement or check being evidenced. |
| Method | Command, test name, manual procedure, or approved external system used. |
| Result | Pass, fail, blocked, or not run; failures link to an issue or explicit hold. |
| Evidence location | Immutable log/report/artifact path or authorised reviewer record. |
| Executor and time | Person or CI identity and actual completion timestamp. |
| Exceptions | Approver, expiry, risk, mitigation, and rollback trigger; empty when none. |

No release gate may infer a pass from missing fields. CI may attest only to the
checks it actually executed. An agent may prepare commands, templates, and
evidence tables, but may not claim a production deployment, payment,
third-party scan, account action, manual device test, legal review, or approval.

## Trust and privacy contracts

### QOR-01 — Secret, configuration, and authorization boundary

- **Scope / owns:** Build configuration schema, example configuration,
  release-time secret scan, and security documentation; initial paths are root
  configuration, `.secrets.env.example`, `scripts/release-check.*`, and
  `docs/security-and-provenance.md`.
- **Contract:** Client artifacts contain only public, validated release
  metadata. Required configuration fails closed when absent or malformed.
  Credentials, private keys, tokens, service credentials, and `.secrets.env`
  are never committed, bundled, logged, copied into examples, or supplied to
  test fixtures. Secret-like findings block release until removed, revoked if
  exposure is confirmed, and rescanned; an agent cannot perform revocation or
  assert it occurred.
- **Authorization:** P0 has no server resource or identity boundary and hence
  has no application roles to implement. Browser-profile access is not an
  authorization guarantee. Any future endpoint, remote state, diagnostic
  transport, or privileged operation is prohibited until a separate approved
  contract specifies authenticated per-request authorization, least privilege,
  rate limiting, audit events, consent, deletion/retention, incident owner,
  outage behaviour, and real production evidence.
- **Verification / evidence:** Positive and negative configuration tests;
  client artifact secret scan; dependency/lockfile review; CSP/static-header
  configuration review after a host is approved. Store command output and the
  scanned candidate identifier. A host header capture is `not run` before an
  authorised deployment exists.
- **Decision gates:** Engine/build tool, hosting/CDN, CSP/header mechanism,
  dependency policy, and any connected service.

### QOR-02 — Privacy, diagnostics, and safe input handling

- **Scope / owns:** Local diagnostics policy and redaction tests in
  `src/{app/recovery,platform/web/diagnostics}`, plus
  `docs/privacy-and-recovery.md`.
- **Contract:** P0 persists only local campaign state, preferences, bounded
  recovery metadata, and a player-controlled bounded diagnostic record. It
  does not collect names, contact data, precise location, advertising IDs,
  account identifiers, payment data, or gameplay analytics. Diagnostics have
  no network transport in P0, are off where consent is required, state their
  fields/purpose/retention/deletion locally, and exclude credentials, complete
  saves, free-text dialogue, and player-entered content.
- **Input trust:** Content packages, save imports if later approved, URL
  parameters, browser events, service-worker messages, and persisted bytes are
  untrusted. Bound size before parse, validate schema/references/checksum, do
  not execute authored data as code, and never render dialogue through unsafe
  HTML. Invalid input fails safely without overwriting a confirmed save.
- **Verification / evidence:** Consent-default, redaction, clear-record,
  hostile/malformed payload, size-bound, and unsafe-rendering tests. A manual
  privacy-copy review records the candidate and reviewer. Any external privacy
  review, legal assessment, data export, or transport test is `not run` unless
  separately approved and evidenced by its authorised owner.
- **Decision gates:** Retention period, legal/age/regional policy, export
  workflow, and every non-local diagnostic capability.

## Operations and resilience contracts

### QOR-03 — Local observability, health, and player recovery

- **Scope / owns:** Development structured logs, release/version/cache status,
  error boundary, and local fault records; initial paths
  `src/{app/recovery,platform/web/diagnostics,platform/web/pwa}` and support
  UI/help copy.
- **Contract:** Observability is local and player-respecting: development
  console/build logs, visible release/version/cache state, and optional bounded
  local diagnostics. Production P0 has no remote health endpoint, telemetry
  dashboard, pager, or monitoring dependency. The health signal is therefore
  a reproducible client verification, not a claim that a deployed service is
  healthy.
- **Recovery behaviour:** An unexpected fault presents `Retry`, `Return to
  title`, and `Safe recovery`, places focus on the actionable summary, avoids
  replaying a stale destructive command, preserves confirmed progress, and
  keeps quarantined data untouched absent confirmed deletion. Every error,
  storage, cache, or content failure has a player-facing path and a test for
  retained save/cache behaviour.
- **Verification / evidence:** Fault-injection and recovery state-machine
  tests; browser evidence for the injected-fault flow; a recorded inspection
  of version/cache/support status. Before a production host is approved,
  production availability monitoring and incident response exercises are
  explicitly `not run`.
- **Decision gates:** Hosting, support owner/response expectation, external
  monitoring, and diagnostics transport.

### QOR-04 — Save integrity, migration, rollback, and recovery

- **Scope / owns:** Save protocol, migration runner, cache-release rollback
  procedure, and recovery documentation; initial paths
  `src/{core/save,core/session,platform/web/persistence}`, `docs/rollback.md`,
  and `docs/release-runbook.md`.
- **Migration contract:** Save and content schemas declare explicit versions
  and supported predecessor ranges. Migrations are ordered, pure, and promote
  only a validated candidate; each supported predecessor fixture migrates once.
  A failed or unsupported migration preserves original bytes in quarantine and
  offers a clear fallback/new-game path. No agent may alter a real player save
  to prove migration or recovery.
- **Rollback contract:** A rollback selects a previously verified, immutable
  known-good release compatible with the declared save/content ranges. It must
  not delete, rewrite, migrate, synchronise, or claim to restore player saves.
  Service-worker activation remains at title or paused menu after a confirmed
  save; failed refresh retains the known-good cache. Rollback is held if
  compatibility, cache retention, or recovery evidence is absent.
- **Verification / evidence:** Fault-injection tests for interrupted write,
  malformed snapshot, quota/permission failure, quarantine, deletion, and
  migration; dry run against a synthetic fixture profile; recorded prior-build
  identifier, compatibility declaration, procedure output, and reviewer.
  A production rollback is never simulated or claimed without deployment
  authority and independently captured evidence.
- **Decision gates:** Storage API/quota, support retention policy, service
  worker rollout, hosting rollback mechanism, and supported schema window.

### QOR-05 — Performance and environment measurement contract

- **Scope / owns:** Performance harness/configuration, size reports, and test
  matrix documentation; initial paths `scripts/release-check.*`, test config,
  `docs/{quality-plan,test-matrix}.md`.
- **Environment contract:** Configuration distinguishes public build metadata
  from development-only values, is typed and validated, and produces immutable
  candidate/version metadata. Development, test, and release procedures must
  identify the resolved non-secret configuration and toolchain version without
  printing secret values.
- **Performance contract:** Measure initial load, bundle/cache size, warm and
  offline startup, interaction/frame-time behaviour, memory, and feasible
  slow-network behaviour only against an approved browser/device/network
  matrix and numeric budget. Until that approval, collect measurements as
  informational evidence only; do not label them budget passes or make public
  performance promises.
- **Verification / evidence:** Configuration positive/negative tests, artifact
  hash and size report, and measurement transcript tied to the candidate,
  browser/device/network profile, cache state, and method. Real-device,
  lab, paid-provider, or production measurements require the authorised
  executor's evidence and remain `not run` when unavailable.
- **Decision gates:** Exact browser/device matrix, network profiles, numeric
  budgets, test hardware, runner/provider, and release performance threshold.

## Documentation and quality contracts

### QOR-06 — Player, operator, and authoring documentation

- **Scope / owns:** `docs/{player-guide,accessibility,privacy-and-recovery,
  security-and-provenance,quality-plan,test-matrix,release-runbook,rollback,
  content-authoring}.md` and corresponding in-app Help/Status copy.
- **Contract:** Player documentation explains controls, keyboard/touch/gamepad
  alternatives, saving/resume/delete/recovery, offline/first-install limits,
  update/cache status, accessibility settings, privacy/diagnostics choices,
  version/support path, and known limitations. Operator documentation defines
  release evidence, hold conditions, rollback, issue ownership, and
  compatibility declarations. Content guidance requires original-asset/text
  provenance and validation before bundling. Documentation must state
  unresolved browser, locale, assistive technology, performance, and support
  decisions instead of promising them.
- **Verification / evidence:** Contract-to-document review checklist with
  candidate ID and reviewer; link checks; help/status UI review; provenance
  inventory review. Legal, accessibility, rating, store, translation, or
  support approval is not implied by a documentation check and requires its
  authorised reviewer record.

### QOR-07 — Quality review and issue disposition

- **Scope / owns:** Deterministic/unit/content/persistence integration suite,
  browser evidence, manual matrix, release evidence register, and issue
  disposition template.
- **Contract:** Quality evidence maps every release requirement to a method,
  candidate, result, artifact, and owner. Required layers are: deterministic
  core/content tests; persistence/migration/recovery fault injection;
  app/integration tests; supported-browser automated smoke for start, first
  battle, save/resume, recovery and PWA lifecycle where applicable; and manual
  responsive/accessibility/offline/storage checks after the matrix is approved.
  Test fixtures use isolated synthetic storage and never modify player data.
- **Issue rules:** A failing, blocked, missing, stale-candidate, or unverifiable
  required check is a release hold. Each known issue records severity, player
  impact, affected target, reproduction, mitigation, owner, and release
  decision. Only an explicitly authorised risk acceptance may waive a
  non-critical issue; it records approver, expiry, rationale, mitigation, and
  rollback trigger. Critical security, data-loss, save-corruption, privacy,
  or unbounded execution findings cannot be waived by this contract.
- **Verification / evidence:** CI-equivalent transcript; browser report;
  completed manual matrix; issue register; and an evidence freshness review
  confirming artifacts belong to the release candidate. Missing approvals or
  unavailable targets are recorded as holds, not manufactured passes.

## Release readiness gate

### QOR-08 — Evidence-based release or hold decision

The release owner completes this gate for one immutable candidate. This record
does not grant deployment authority; it determines whether the candidate is
ready to be presented for an authorised release decision.

| Gate | Required evidence | Hold when |
| --- | --- | --- |
| Candidate identity and compatibility | Version/build hash; content/save schema versions and supported ranges; known-good rollback target | Identity, hash, compatibility, or rollback target is missing or incompatible. |
| Trust and privacy | QOR-01 artifact secret scan/configuration result; QOR-02 consent/redaction/input-safety results; provenance/dependency review | A secret finding, unsafe parser/rendering result, missing consent/redaction evidence, or unresolved provenance/dependency risk exists. |
| Health and recovery | QOR-03 recovery evidence; QOR-04 save/migration/quarantine/cache-retention tests and rollback dry run | A fault lacks a safe path, save/recovery test fails, or rollback/recovery evidence is absent. |
| Quality and accessibility | QOR-07 CI/browser/manual evidence, with approved target matrix and all required contract mappings | A required check is fail, blocked, not run, stale, or lacks reviewable evidence. |
| Performance and environment | QOR-05 validated configuration, hash/size report, and approved-matrix measurement against approved budget | Required environment/budget/matrix evidence is unapproved, absent, or over budget without authorised disposition. |
| Documentation and known issues | QOR-06 review; player/operator material; issue register and any authorised, unexpired exception | Documentation is inaccurate/missing, an issue is undisposed, an exception is expired/unauthorised, or a non-waivable issue exists. |
| Authorised decision | Named release authority records `release` or `hold`, time, candidate, evidence links, and rationale | No authorised decision exists. An agent or automated check cannot substitute for this record. |

**Decision algorithm:** Record `HOLD` if any gate is held, any required evidence
is not real and candidate-specific, or an unresolved decision gate affects the
release claim. Record `READY FOR AUTHORISED RELEASE DECISION` only when every
applicable gate has passing evidence and no unwaivable issue. The authorised
release authority then records either `RELEASE` or `HOLD`; absent that record,
the outcome remains `HOLD / awaiting authority`.

## Retained decisions and excluded actions

1. Engine/framework, package manager, CI runtime, storage API/quota, host/CDN,
   service-worker rollout, browser/device/assistive-technology matrix,
   performance budgets, locales, retention policy, legal/age/regional policy,
   and support ownership require approval.
2. Production hosting, deployment, rollback execution, external scans, paid
   test services, real-device labs, store submission, legal review, and any
   account action require separately granted authority and real evidence.
3. Account identity, cloud sync, multiplayer/player safety, live-service
   operations, analytics, commerce, and entitlements remain excluded. They
   need new product, privacy, security, operational, cost, and failure-mode
   contracts before implementation or release claims.
