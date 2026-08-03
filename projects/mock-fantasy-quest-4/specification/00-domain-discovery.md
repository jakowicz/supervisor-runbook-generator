# 00 — Domain discovery

**Sources:** [`INITIAL.md`](../INITIAL.md) and the normalized
[`PROJECT_BRIEF.md`](../PROJECT_BRIEF.md). This is a candidate system map, not
an implementation commitment. Labels mean: **explicit** (directly requested),
**implied** (necessary to fulfill a direct request), **assumed** (safe temporary
guardrail), **deferred** (later scope), and **requires-decision** (not safely
selectable from the source).

## Candidate system map

| Discipline / system family | Label | Rationale | Source reference |
| --- | --- | --- | --- |
| Game shell, lifecycle, pause, navigation, and session recovery | implied | A playable web/PWA game needs safe entry, pause, resume, and return from interruption. | What are we creating?; selected targets |
| Exploration, traversal, collision, town and dungeon scenes | explicit | Exploration and exactly one town and one dungeon are named. | What are we creating? |
| Narrative, characters, dialogue, quest text, and short ending | explicit | Story/campaign progress, readable dialogue, quests, and a short ending are direct. | Users; shared requirements; creation scope |
| Quest state, progression, rewards, and onboarding/tutorial | explicit | Quests, progression, and onboarding are required; first session teaches battle and saving. | Required capabilities; first useful session |
| Party combat, encounters, turn resolution, rewards, and balancing | explicit | Turn-based combat is named; party scope comes only from the functional reference. Balancing is necessary for a learnable loop. | Creation scope; functional reference |
| Inventory, item definitions, equipment/use rules, and reward economy | explicit | Inventory is named and needs authored items/rewards. | Creation scope; shared UI requirements |
| Save/load, checkpoints, migrations, data-loss recovery, and local persistence | explicit | Save/load, long-session checkpoints, recovery, and offline PWA save behavior are direct. | Shared requirements; PWA requirements |
| Rendering, responsive layout, input adapter, and browser performance | explicit | Web target demands responsive layout, keyboard/mouse/touch/gamepad, compatibility, and performance budget. | Responsive web requirements |
| PWA installability, service worker, cache lifecycle, offline asset delivery, and update safety | explicit | Installability, offline assets/save behavior, and safe cache refresh are direct. | PWA requirements |
| Accessibility: remappable/accessible controls, text, captions, visual settings, and readable UI | explicit | Accessibility and readability are named across controls and core game interfaces. | Shared requirements |
| Localisation and language-content pipeline | explicit | Localisation is required, though languages are unknown. | Cross-platform decisions |
| Audio/visual feedback and original art asset pipeline | explicit | Feedback and original warm hand-painted direction are requested. | Required capabilities; art direction |
| Content authoring, validation, packaging, and level delivery | implied | Town, dungeon, dialogue, quests, items, and level delivery require controlled authored content and validation. | Content/level delivery; explicit scope |
| Build, release, versioning, cache/update communication, and rollback policy | implied | Safe web/PWA refresh cannot be delivered without release discipline. | PWA requirements |
| Crash diagnostics, error boundaries, player recovery UI, and support triage | explicit | Crash reporting and player-facing error recovery are direct. | Shared requirements; required capabilities |
| Quality engineering: gameplay, compatibility, offline/update, persistence/recovery, accessibility, and performance testing | implied | Every target and recovery promise needs validation beyond individual screens. | Per-target and shared requirements |
| Privacy, security, consent, data minimisation, retention/deletion | explicit | Privacy is required and accounts/diagnostics may process player data. | Constraints; cross-platform decisions |
| Account identity, authentication, remote state sync, and conflict handling | requires-decision | Named as required but no account/sync policy exists and it conflicts with offline scope. | Required capabilities; cross-platform data policy |
| Multiplayer, player safety, moderation/reporting, and community operations | requires-decision | Named as required but inconsistent with the single-player framing and lacks mode/safety policy. | Game characteristics; required capabilities |
| Live-service operations, status, support, incident response, and event tooling | requires-decision | Named as required but conflicts with a deliberately small offline release. | Required capabilities; creation scope |
| Purchases, catalogue, entitlements, refunds, and compliance | requires-decision | Named as required while monetisation is deferred and no payment/platform policy is given. | Required and deferred capabilities |
| Analytics and telemetry | deferred | Advanced analytics is explicitly later; minimum crash diagnostics remain separately required. | Later/deferred capabilities |
| Seasonal/live events and player-created/shared content | deferred | These are explicitly listed as later scope. | Later/deferred capabilities |
| Repository, engine/framework, backend/vendors, CI/CD, and cost model | requires-decision | The source says to determine constraints but authorizes no selection. | Constraints and non-goals |
| Browser/device matrix, storage quota, network floor, and performance budget | requires-decision | “Widely used” and “feasible slow-network” are not testable thresholds. | Cross-platform decisions; web requirements |
| Age rating, parental controls, regions, store/certification, and legal policy | requires-decision | Applicable requirements are named but audience detail, regions, and commerce/service scope are unknown. | Cross-platform decisions |

## Scope and dependency conclusions

The minimal offline campaign depends on the shell, exploration, narrative,
quests/progression, combat, inventory, persistence, rendering/input,
accessibility, original assets, content tooling, and quality disciplines. PWA
packaging adds installability, caches, offline assets, and update safety; it
does not create a separate game.

Account, multiplayer, live-service, and commerce must not become dependencies
of the offline campaign until a human resolves their contradiction. If approved,
they require explicit degraded states, privacy/security rules, operational
ownership, and recovery behavior. If deferred, their interfaces and data model
must not expand or block the first release.

## Explicit requests, safe assumptions, and approval gates

| Kind | Discovery conclusion | Handling |
| --- | --- | --- |
| Explicit requests | Small 2D single-player RPG; web/PWA; exploration, town, dungeon, combat, inventory, quests, saves, settings, ending, access, feedback, recovery. | Plan as the complete offline campaign. |
| Necessary implied capabilities | Shell/session, authored content/tooling, input/rendering, QA, release/update workflow, and balance. | Include in later contracts as enabling work, sized to the small release. |
| Safe assumptions | Original content; shared core; durable confirmed local saves when storage permits; connected features visibly degrade; minimal-data diagnostics. | Retain as reversible guardrails only. |
| Approval gates | Connected scope, account/sync, multiplayer/safety, commerce, stack/vendors, support matrix/budgets, content quantities, localisation, audio, and legal/store policy. | Record and obtain approval before selecting policies, services, or production quantities. |

## Reference boundary

The functional reference constrains high-level party-based turn-based adventure
scope only. It is never permission to reproduce branding, names, copy, story,
characters, lore, assets, music, layouts, screen composition, maps, distinctive
menus, flows, or interaction choreography. Original mechanics expression,
content, UI, art, and feedback must be created for this product.
