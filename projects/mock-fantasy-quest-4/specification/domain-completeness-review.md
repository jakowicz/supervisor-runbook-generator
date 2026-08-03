# Domain-completeness review

Review basis: discovery map plus feature, technical, experience and delivery contracts. “Chapter” may be an existing bounded F001–F010 source until later authoring expands it. Every family has explicit entities/rules, dependencies, authoring model where needed, and a release decision.

| System family | Requirement chapter / entities and rules | Cross-domain dependencies | Authoring model | Release decision |
| --- | --- | --- | --- | --- |
| Shell/session/input/rendering | SPEC-02/04; Session, InputAction, viewport; pause/focus semantic action rules | save, accessibility, scenes | routes, controls, layouts | P0 shared core; web adapters |
| Town/dungeon exploration | SPEC-02; Scene, Exit, Interactable; collision/gates/safe boundaries | quests, combat, save, content | original scene/layout/NPC/exit data | P0: exactly one town/one dungeon |
| Narrative/quests/tutorial/ending | SPEC-02; Quest, Dialogue, Campaign; predicates/reward-once/ending | scenes, inventory, combat, save | original text/localisation keys and quest graph | P0; quantities/locales gated |
| Combat/party/rewards | SPEC-02; Party, Encounter; legal turns/defeat/checkpoints | quests, inventory, save | encounters/actions/reward definitions | P0; party size/balance gated |
| Inventory/progression | SPEC-02; Item, inventory; legal use/protected quest items | quests, party, save | item/equipment definitions | P0 |
| Persistence/recovery | SPEC-02/03; snapshot/checkpoint; atomic/version/quarantine rules | all durable game state, PWA cache | schema/migrations/fixtures | P0, storage policy gated |
| Accessibility/localisation/feedback | SPEC-04; preferences/options; semantic/reflow/non-colour rules | shell, input, content | strings, captions, tokens, feedback assets | P0; exact targets/locales/assets gated |
| Content/original assets | SPEC-02/03; ContentPackage; validation/reachability/provenance | all gameplay and UI | source manifest, assets, locale, validator | P0; original boundary explicit |
| PWA/release/quality | SPEC-03; cache/version/release; safe activation/rollback | persistence, shell, content | manifest/precache/release metadata/evidence | P0 PWA, operations thresholds gated |
| Privacy/diagnostics | SPEC-03/04; diagnostic record; consent/redaction/deletion | recovery, release | diagnostic schema and disclosure | P0 local-minimal; transport/retention gated |
| Account/sync | SPEC-00; potential identity/replication/conflict rules | save/privacy/security | none until approved | hold, GATE-0006 |
| Multiplayer/safety/live service/commerce | SPEC-00; service/safety/entitlement models not authored | privacy/security/operations/legal | none until approved | hold, GATE-0006 |

**Conclusion:** the P0 game disciplines are complete enough to decompose without rediscovery. Deferred/contradictory connected disciplines are deliberately represented as held chapters rather than omitted or silently designed. No copied reference expression is authorised in any chapter.
