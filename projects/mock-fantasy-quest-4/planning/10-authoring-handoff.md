# 10 — Specification-to-runbook authoring handoff

**Purpose:** hand the audited planning catalogue to F011–F016 without starting
product implementation, testing, deployment, or release activity. This file is
an authoring control record, not an implementation plan that overrides the
[source brief](../INITIAL.md).

## Authoritative inputs and evidence locations

Read these in order. If sources conflict, preserve the source brief, record the
conflict in the F011 decision log, and stop the affected allocation rather than
inventing a resolution.

1. [INITIAL.md](../INITIAL.md) is the original source of truth; the normalized
   [product brief](../specification/01-product-brief.md) preserves its scope.
2. [Domain discovery](../specification/00-domain-discovery.md), the feature,
   technical, and experience contracts (`02`–`04`) define the discovered
   product and target constraints.
3. [Delivery map](05-delivery-map.md) provides the dependency order DM-01 to
   DM-20. [Foundation](06-foundation-domain-contracts.md),
   [feature](07-feature-experience-contracts.md), and
   [quality](08-quality-operations-contracts.md) define FDN-01–09,
   FEX-01–14, and QOR-01–08 ownership and acceptance evidence.
4. [Contract audit](09-contract-audit.md) is the current closure evidence,
   including browser-spec ownership and retained decisions.

F011 writes canonical specification and traceability evidence under
`specification/` (including `requirements.md`, `requirements.json`, a
traceability matrix, decision log, platform appendix, and specification index).
F012 writes the implementation catalogue and graph under `planning/`; F013
writes the batch manifest there; F014 writes B-series authoring runbooks under
`authoring-runbooks/` and their registration records; F015 writes structural
quality-gate evidence; and F016 writes the project README and durable resume
handoff. Generated R-series instructions and their evidence belong in
`runbooks/` and the locations named by their final contracts. Planned test and
browser paths are ownership reservations only until a later implementation task
creates executable code and independent evidence.

## Scope boundary and original-design rule

The P0 to author is an original, offline-capable 2D, single-player fantasy RPG:
one town, one dungeon, a guided short campaign ending, exploration, dialogue,
quests, party-based turn-based combat, inventory/rewards, onboarding, local
save/load/checkpoints/recovery, settings/accessibility, responsive web, and an
installable PWA with safe offline/update behaviour. It uses a shared core with
only necessary web/PWA adaptations.

Do not author implementation work for additional regions, chapters, native
apps, PWA-exclusive rules, live events, player-created/shared content, advanced
analytics/monetisation, cloud sync, payment flows, accounts/identity,
multiplayer, moderation, player-safety services, live operations, or
entitlements. The brief mentions several connected capabilities, but their
conflict with the offline P0 remains an explicit hold; no author may recast
that hold as approved scope.

The Final Fantasy V reference permits only high-level party-based turn-based
adventure scope. Never reproduce or request copied names, branding, assets,
story/lore, dialogue, maps, music, layouts, menus, combat screens, interaction
choreography, or distinctive presentation. All planned content and assets must
be independently original, warm hand-painted fantasy with readable silhouettes
and a restrained palette, supported by provenance records and later human
review.

## Execution order and dependencies

| Stage | Required outcome | Inputs / dependency | Cannot proceed without |
| --- | --- | --- | --- |
| F011 | Canonical `REQ-*`, `NFR-*`, `DEC-*`, `RISK-*`, `GATE-*` system and traceability | This handoff and all specifications/planning 05–09 | Recording, not deciding, open choices |
| F012 | Bounded `IMP-*` catalogue, ownership, and acyclic graph | Completed F011 | Requirement traceability and named domain shards |
| F013 | Persistent B/R allocation ledger and context packets | Completed F012 | Unique immutable IDs and dependency-safe batches of at most seven R contracts |
| F014 | Bootstrap B-series/dispatcher collection and child registrations | Completed F013 | Valid manifest, bounded wave, and existing-ID collision checks |
| F015 | Structural/traceability quality gate and recovery procedure | F014 output plus manifest | Passing ownership, metadata, dependency, asset, and browser-path checks |
| F016 | Project README, registrations, evidence map, and resume handoff | F015 quality evidence | Explicit holds and safe resume points retained |

Within later implementation contracts, preserve the DM order: select and
bootstrap the framework before core/state/content; establish persistence and
recovery before session/UI; complete campaign rules before their UI; then input
and accessibility, PWA lifecycle, release hardening, quality evidence, and
documentation. Parallel authoring is allowed only for contracts whose declared
dependencies are already satisfied and whose files/data/browser paths do not
overlap.

## Decision gates, approvals, and stop conditions

The following gates require a human or responsible external owner before a
dependent contract is allocated as ready: engine/framework and package manager;
CI runtime; browser storage API/quota; browser/device/assistive-tech and
network matrix; numeric performance budget; host/CDN and service-worker rollout;
content quantities, party size, balance, locale, audio and remapping scope;
font/contrast targets; diagnostics provider/transport, retention and privacy;
and ratings, age, regional, legal, support, store, or certification policy.

Stop the batch authoring system and mark the item blocked—not failed or
implicitly approved—when any of these occurs:

- an open decision changes scope, privacy/security, cost, legal obligations,
  connected services, or delivery commitments;
- a requirement lacks a source, owner, verification approach, or safe bounded
  contract; a dependency is cyclic or ownership conflicts;
- an R/B/asset ID, output path, browser test path, or accepted contract would
  be overwritten, renumbered, duplicated, or ambiguously owned;
- a request entails credentials, paid services, account creation, store action,
  deployment, publishing, release approval, or real-device/certification access;
- evidence would require claiming that planned paths, generated runbooks, or
  structural validation prove product implementation or release readiness.

## Safe authoring-agent configuration

Use a workspace-scoped authoring agent with no secrets, deployments, payments,
publishing, external account actions, or authority to approve gates. Give each
agent only its manifest context packet, the source documents it cites, its
assigned immutable IDs, and its declared output paths. It may create Markdown,
JSON manifests, validation instructions, and child-registration files only in
this project workspace; it must not create product source, generated game
assets, tests that purport to validate a product, or release artefacts in this
F011–F016 phase.

Every authoring task records source links, requirement/contract IDs,
dependencies, owned outputs, unresolved questions, gate status, and structural
evidence. It checkpoints after each bounded batch, retains accepted IDs and
manifest counters, and resumes from the next unaccepted item. F015 is the
structural evidence gate: it validates metadata, traceability, dependency
closure, output ownership, asset assessment, and browser-path uniqueness. Any
later executable test, browser result, visual review, accessibility assessment,
or release evidence must be stored at the paths named by its implementation
contract and remains outside this authoring handoff.

## Assumptions and risks carried forward

Safe assumptions are limited to an offline-first local campaign, original
content/UI, shared core with necessary target adaptations, local durable saves
where browser storage allows, visibly degraded connected features if ever
approved, and privacy-minimised diagnostics. They are guardrails, not stack,
vendor, backend, account, retention, performance, accessibility, or support
promises.

Key risks are unresolved connected-scope conflict; storage/quota and update
loss hazards; unsupported browser/device or assistive-tech assumptions;
unapproved performance targets; original-design/provenance failure; and
manifest/ID drift across resumed authoring waves. Mitigate each by retaining
the named gate, keeping save/cache responsibilities separated, requiring
provenance and human creative review, and using the F013 ledger plus F015
quality gate before dispatching further work.

## Readiness statement

The catalogue is ready for **batch authoring only**: audited inputs identify
the P0 boundary, contract namespaces, delivery dependencies, evidence owners,
and unresolved decision gates. F011–F016 may now formalise, shard, allocate,
validate, and hand off implementation instructions. This statement does not
select a technology, authorize any gate, create implementation or release
work, or assert that the game has been built, tested, or approved for release.
