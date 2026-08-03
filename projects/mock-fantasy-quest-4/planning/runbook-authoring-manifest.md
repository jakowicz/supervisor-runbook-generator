# Runbook-authoring allocation ledger

This readable companion to [`runbook-authoring-manifest.json`](runbook-authoring-manifest.json) is the persistent allocation ledger for the mock-fantasy-quest-4 authoring system. The JSON is authoritative for IDs, provenance, dependencies, output paths, counters, and recovery state. Accepted IDs are immutable: resume from the first non-accepted batch and append only at `B0014` and `R0033`.

## Dispatcher checkpoint — D0004

D0004 expanded the eligible SHARD-04 exactly once into six contracts
(`IMP-0027`–`IMP-0032`), below its 250-record limit. Its GATE-0002,
GATE-0005, and GATE-0007 constraints remain implementation and release gates.
The contracts are allocated once between B0011 and B0012 (three outputs each),
with no product asset or audio work. No queued or ready P0 contracts remain,
so [`B0013`](../authoring-runbooks/B0013.md) is the sole final allocation audit;
SHARD-05 remains held. Counters now append at B0014/R0033; accepted work is unchanged.

## Dispatcher checkpoint — D0003

D0003 expanded the eligible SHARD-03 exactly once into six contracts
(`IMP-0021`–`IMP-0026`), below its 250-record limit. Its GATE-0002,
GATE-0003, and GATE-0004 constraints remain implementation gates. The six
contracts are allocated once between B0009 and B0010 (three outputs each),
with no product asset or audio work. SHARD-04 remains queued, so
[`D0004`](../authoring-runbooks/D0004.md) is the sole successor. Counters now
append at B0011/R0027; accepted work is unchanged.

## Dispatcher checkpoint — D0002

D0002 expanded the now-authorable `SHARD-02` exactly once into eight contracts
(`IMP-0013`–`IMP-0020`), below its 250-record limit. `GATE-0004` remains on
each affected contract as an implementation gate and was not treated as an
authoring blocker. The eight contracts are allocated once between B0007 and
B0008 (four outputs each), with asset reservation only in R0018. SHARD-03 and
SHARD-04 remain queued, so [`D0003`](../authoring-runbooks/D0003.md) is the
sole successor. Counters now append at B0009/R0021; accepted work is unchanged.

## Dispatcher checkpoint — D0001

D0001 expanded no chapter and allocated no B/R contracts. `SHARD-02` is the
first queued chapter, but `DEC-0004`/`GATE-0004` remains unresolved; `SHARD-03`
and `SHARD-04` retain their predecessor and gate blocks, while `SHARD-05` stays
held pending explicit authorisation. Every current catalogue contract
(`IMP-0001` through `IMP-0012`) is allocated exactly once. The dispatcher
therefore created [`D0002`](../authoring-runbooks/D0002.md) as the sole
successor, without advancing B/R counters or modifying accepted work.

## Wave 1 — foundation contracts

| Order | Batch | R contracts (maximum 7) | Dependency / parallel disposition | Checkpoint |
| --- | --- | --- | --- | --- |
| 1 | B0001 | R0001 | GATE-0001; no parallel work | Record gate and R0001 ownership |
| 2 | B0002 | R0002, R0003, R0010 | After B0001 | Validate seams, fixtures, tokens and retained gates |
| 3 | B0003 | R0004, R0008 | After B0002 | Validate state slice and P0 service exclusion |
| 4 | B0004 | R0005, R0006 | After B0003; R0006 waits for GATE-0003 | Validate content/save separation |
| 5 | B0005 | R0007, R0009, R0011 | After B0004; R0007/GATE-0003 and R0009/GATE-0005 remain blocked | Validate migration, diagnostics, provenance |
| 6 | B0006 | R0012 | After B0003 and B0004; safe in parallel with B0005 after B0004 | Cross-check foundation documentation and gates |
| 7 | B0007 | R0013, R0014, R0015, R0016 | After B0003; GATE-0004 retained | Validate domain-state seams and non-asset boundaries |
| 8 | B0008 | R0017, R0018, R0019, R0020 | After B0007; GATE-0004/provenance retained | Validate campaign integration, asset reservation, and SHARD-03 handoff |
| 9 | B0009 | R0021, R0022, R0023 | After B0007; SHARD-03 gates retained | Validate session, shell, and input boundaries |
| 10 | B0010 | R0024, R0025, R0026 | After B0009; SHARD-03 gates retained | Validate accessibility, recovery, evidence, and SHARD-04 handoff |
| 11 | B0011 | R0027, R0028, R0029 | After B0010; SHARD-04 gates retained | Validate PWA lifecycle, cache/save separation, and release boundaries |
| 12 | B0012 | R0030, R0031, R0032 | After B0011; SHARD-04 gates retained | Validate evidence holds, recovery documentation, and final PWA audit |
| 13 | B0013 | none | After B0012; SHARD-05 remains held | Final allocation audit; no new R allocation |

The batches are deliberately smaller than seven where a contract is context-heavy (state, persistence, content) or tightly coupled to its predecessor. Together they form an incremental foundation vertical slice: reproducible baseline, shared seams/test harness, deterministic game state and P0 exclusion, content and recovery boundaries, then provenance/diagnostic controls and documented closure. They do not imply that the game is implemented.

## Contract allocation and asset assessment

| R ID | IMP source | Writer | Output | Asset assessment |
| --- | --- | --- | --- | --- |
| R0001 | IMP-0001 | B0001 | `runbooks/R0001.md` | not applicable — tooling boundary only |
| R0002 | IMP-0002 | B0002 | `runbooks/R0002.md` | not applicable — interfaces only |
| R0003 | IMP-0003 | B0002 | `runbooks/R0003.md` | not applicable — deterministic fixtures only |
| R0004 | IMP-0004 | B0003 | `runbooks/R0004.md` | not applicable — state envelopes only |
| R0005 | IMP-0005 | B0004 | `runbooks/R0005.md` | not applicable — schema reserves later asset fields |
| R0006 | IMP-0006 | B0004 | `runbooks/R0006.md` | not applicable — save/recovery protocol |
| R0007 | IMP-0007 | B0005 | `runbooks/R0007.md` | not applicable — migrations only |
| R0008 | IMP-0008 | B0003 | `runbooks/R0008.md` | not applicable — negative service scope |
| R0009 | IMP-0009 | B0005 | `runbooks/R0009.md` | not applicable — local diagnostics only |
| R0010 | IMP-0010 | B0002 | `runbooks/R0010.md` | not applicable — no final art/fonts/icons |
| R0011 | IMP-0011 | B0005 | `runbooks/R0011.md` | not applicable — provenance control only |
| R0012 | IMP-0012 | B0006 | `runbooks/R0012.md` | not applicable — documentation only |
| R0013–R0017, R0019–R0020 | IMP-0013–IMP-0017, IMP-0019–IMP-0020 | B0007/B0008 | `runbooks/R0013.md`–`R0020.md` | not applicable — contract, fixture, integration, and documentation work only |
| R0018 | IMP-0018 | B0008 | `runbooks/R0018.md` | required — reserves original campaign asset groups; authoring must not create them |
| R0021–R0026 | IMP-0021–IMP-0026 | B0009/B0010 | `runbooks/R0021.md`–`R0026.md` | not applicable — session/UI/input/accessibility/recovery evidence contracts only; no product asset or audio creation |
| R0027–R0032 | IMP-0027–IMP-0032 | B0011/B0012 | `runbooks/R0027.md`–`R0032.md` | not applicable — PWA lifecycle, local release evidence, performance, and documentation contracts only; no product asset or audio creation |

No Wave 1 contract creates a product asset. Each contract still carries an explicit `asset_impact`, empty `asset_ids`, and an asset brief in the JSON; its author must prohibit incidental asset creation. A later asset-required contract must reserve stable product-specific IDs and a brief before assignment.

## Author packet and resume rules

Each B writer receives only the baseline terminology, target constraints, templates, authoring rules, and the named specification/catalogue records in its JSON `context_packet`. Every R record has canonical `source_specifications`, `source_catalogue_ids`, `authoring_batch`, and `factory_stages` provenance. Use [`runbooks/TEMPLATE.md`](../../../runbooks/TEMPLATE.md) plus the F014 metadata and asset requirements.

At every checkpoint, validate unique B/R IDs, output-path ownership, dependency closure, provenance, the batch maximum, asset assessment, and retained human gates. On failure, retain all assigned IDs, repair the bounded failed output, and resume that same batch. Never regenerate accepted contracts or renumber the ledger.

## Queued expansion chapters

| Chapter | Future allocation point | State |
| --- | --- | --- |
| SHARD-02 — Campaign content and domain logic | Wave 2 authoring allocation; GATE-0004 retained for implementation | expanded |
| SHARD-03 — Session, UI, input, and accessibility | Wave 3 authored; GATE-0002/0003/0004 retained for implementation | expanded |
| SHARD-04 — PWA delivery, performance, operations, release evidence | Wave 4 allocated; GATE-0002/0005/0007 retained for implementation/release | expanded |
| SHARD-05 — Connected-scope decision package | Only explicit authorisation after GATE-0006; no P0 R allocation | hold |

Expand one queued chapter into catalogue records before allocating its R IDs. This preserves the catalogue’s dependency graph and makes a future thousand-runbook programme resumable without changing accepted work.

## Structural check

```sh
node -e 'const m=require("./projects/mock-fantasy-quest-4/planning/runbook-authoring-manifest.json"); const r=m.r_contracts, b=m.batches, ids=a=>new Set(a).size===a.length; if (!ids(r.map(x=>x.id)) || !ids(b.map(x=>x.id)) || r.length!==m.expected_runbook_count || b.some(x=>x.r_contract_ids.length>7) || r.some(x=>!x.source_specifications.length || !x.source_catalogue_ids.length || !x.authoring_batch || !x.factory_stages.length || !["required","not_applicable"].includes(x.asset_impact) || !x.output_path || (x.asset_impact==="required" && (!x.asset_ids.length || !x.asset_brief))) ) process.exit(1); console.log("runbook authoring ledger structural check passed")'
```
