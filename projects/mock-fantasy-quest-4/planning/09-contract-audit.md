# 09 — Implementation-contract catalogue audit

**Audited inputs:** [product brief](../specification/01-product-brief.md),
[feature model](../specification/02-feature-model.md), [technical contract](../specification/03-technical-contract.md), [experience contract](../specification/04-experience-contract.md), [delivery map](05-delivery-map.md), [foundation and domain contracts](06-foundation-domain-contracts.md), [feature and experience contracts](07-feature-experience-contracts.md), and [quality, operations, and release contracts](08-quality-operations-contracts.md).

## Audit result and correction

The catalogue contains stable, unique IDs in three namespaces: `FDN-01` to
`FDN-09`, `FEX-01` to `FEX-14`, and `QOR-01` to `QOR-08`. Their authoring
sequence is foundation first, feature/experience next, and quality/release
evidence throughout and at the release gate. `05-delivery-map.md` supplies the
implementation sequence (`DM-01` to `DM-20`) and closure for the planned code
boundaries; its numbered order must not be treated as permission to bypass a
listed approval gate.

One metadata gap was corrected in this audit: FEX-09 had browser-facing
feedback assertions but delegated them to three other feature specs. That
violated the unique browser-spec ownership convention in 07. FEX-09 now owns
`supervisor/browser/tests/changes/fex-09-feedback.spec.*`; no implementation
spec exists yet because this repository is still planning-only.

## Requirement-to-runbook traceability

| Brief / contract requirement | Primary implementation-contract owners | Evidence owner |
| --- | --- | --- |
| Small offline single-player 2D RPG: one town, one dungeon, battle, short ending | FDN-03, FDN-05; FEX-02–FEX-05, FEX-13 | FEX-13 validation/reachability; FEX-02–FEX-05 core and browser evidence |
| First useful session: first battle and saving understood | FEX-01, FEX-04, FEX-10 | FEX-01 Playwright/tutorial and FEX-04 combat tests |
| Onboarding, quest/campaign progression, inventory, rewards | FEX-01–FEX-05, FEX-13 | Feature core/app tests; FEX-01–FEX-05 unique browser specs |
| Save/load, migration, data-loss prevention, long-session recovery | FDN-06; FEX-10, FEX-11; QOR-04 | Persistence fault/migration tests and FEX-10/FEX-11 browser specs |
| Settings, readable UI, accessible controls/captions/visual settings/localisation | FDN-04; FEX-06–FEX-09 | Accessibility, adapter and status tests; FEX-06–FEX-09 browser specs |
| Keyboard, mouse, touch, gamepad and responsive web surfaces | FEX-06, FEX-07 | FEX-06/FEX-07 Playwright and adapter tests |
| Installable PWA, offline assets/save separation, safe update/cache refresh | FEX-12; QOR-03–QOR-05 | FEX-12 lifecycle browser spec and QOR-04 cache/recovery evidence |
| Original warm hand-painted direction and no copied creative work | FDN-04; FEX-09, FEX-13; QOR-06 | Token/provenance validation and manual original-design review |
| Crash/error recovery, privacy-safe diagnostics, player-facing error paths | FDN-06; FEX-10, FEX-11; QOR-02–QOR-04 | Recovery/redaction/fault tests and FEX-11 browser spec |
| Release safety, documentation, quality evidence, rollback | FEX-14; QOR-01–QOR-08 | QOR evidence register, release gate, FEX-14 release-evidence spec |
| Brief-required connected capabilities (identity, multiplayer/safety, live service, IAP/entitlements) | FDN-07, FDN-08; QOR-01; 05 delivery-map exclusions | Explicit P0 exclusion and separate-approval hold; no false implementation claim |

## Dependency, lifecycle, and ownership audit

| Audit area | Validation result | Record of closure / owner |
| --- | --- | --- |
| Foundation order | Pass | FDN-01 gates tooling; FDN-02/03 establish configuration and seams; FDN-04/05 establish presentation/domain; FDN-06/09 require those seams. FDN-07/08 are exclusion records and cannot unlock connected work. |
| Feature dependency closure | Pass with decision gates retained | DM-01–DM-20 gives the executable dependency order. FEX-01–FEX-05 and FEX-10–FEX-13 consume FDN-03/05/06 and validated content; FEX-06–FEX-09 consume the shell/tokens/input settings boundaries; FEX-14 consumes feature evidence. Unapproved framework, storage, content quantities, locale, audio/remapping, browser/device, and rollout decisions remain blockers where named. |
| Quality/release dependency closure | Pass | QOR-01–QOR-07 define evidence by trust, recovery, environment, documentation, and quality area. QOR-08 cannot become release authority and holds if candidate-specific evidence, compatibility, or approval is absent. |
| Browser-spec ownership | Pass after FEX-09 correction | FEX-01–FEX-12 and FEX-14 each own unique `fex-*.spec.*` paths; FEX-09 now owns `fex-09-feedback.spec.*`. FEX-13 is content-only and explicitly has no browser spec until rendered by its consuming journeys. QOR browser evidence is release-level evidence owned by FEX-11/FEX-12/FEX-14, so it does not duplicate feature-spec ownership. |
| Durable-data lifecycle | Pass | FDN-05 owns immutable state/commands; FDN-06 owns snapshots, migration and quarantine; FEX-10 owns player save UI; FEX-11 owns recovery diagnostics; FEX-12 owns cache lifecycle without owning saves; QOR-04 owns rollback compatibility. |
| Test ownership | Pass | FDN-09 owns runner/fixtures and test conventions; each FDN/FEX record names its acceptance evidence; QOR-07 owns the cross-contract evidence register and issue disposition; QOR-08 owns the release/hold decision record. |

## Remaining decisions, external gates, and risks

These are real holds, not missing implementation contracts:

1. Approve engine/framework, package manager, CI runtime, browser storage API
   and quota, host/CDN, service-worker rollout, browser/device/assistive-tech
   matrix, network profiles, and numeric performance budget.
2. Approve content quantities and party size, final fonts/contrast targets,
   locales, audio scope, control-remapping depth, retention, legal/age/regional
   policy, and support ownership before implementation makes final promises.
3. The brief names account-linked state, identity, multiplayer/player safety,
   live operations, purchases, and entitlements, but the scoped P0 is an
   offline local campaign. These remain intentionally excluded and require a
   new approved product, privacy, security, operational, cost, and failure-mode
   contract before implementation.
4. No application source, selected framework, generated Playwright specs, or
   candidate-specific test evidence exists in this planning workspace. The
   planned paths establish ownership only; they are not implementation proof.
