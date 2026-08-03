# Implementation catalogue index

This is the F012 implementation-authoring index for **mock-fantasy-quest-4**.
The machine-readable source is
[`implementation-catalogue-index.json`](implementation-catalogue-index.json).
It decomposes only the first bounded shard; it does not author R-series
runbooks or approve any decision gate.

## Scope and ownership rules

- **SHARD-01 — Foundation and core contracts** contains 12 independently
  verifiable contracts (limit: 250). It establishes framework-neutral seams,
  deterministic data contracts, local persistence/recovery protocols, quality
  controls, and documentation. It does not implement campaign behaviour,
  player UI, PWA lifecycle, or release actions.
- **Shared** owns campaign rules and platform-neutral contracts. **Web** owns
  browser input, responsive layout, origin storage, and web builds. **PWA** is
  a delivery/cache/install adaptation only: it reuses the shared game and web
  UI, while owning its service-worker lifecycle. Save data and cache data are
  deliberately separate.
- `GATE-*` records block dependent authoring; they are not defaults. The
  catalogue keeps connected capabilities out of P0 under `GATE-0006`.
- Content must be original. The functional reference never authorises copied
  names, text, lore, art, maps, layouts, music, or interaction choreography.

## Current contracts

| ID | Domain | Outcome | Prerequisites | Gate/status |
| --- | --- | --- | --- | --- |
| IMP-0001 | Foundation | Reproducible shared project baseline | — | GATE-0001 / gated |
| IMP-0002 | Foundation | Core and adapter dependency seams | IMP-0001 | current |
| IMP-0003 | Tests | Deterministic test/fixture harness | IMP-0001–0002 | current |
| IMP-0004 | Data | Deterministic state/command/event contract | IMP-0002–0003 | current |
| IMP-0005 | Content | Versioned content schema and validator | IMP-0001, 0003–0004 | current |
| IMP-0006 | Persistence | Local save/recovery protocol | IMP-0002–0004 | GATE-0003 / gated |
| IMP-0007 | Persistence | Pure migration runner | IMP-0005–0006 | GATE-0003 / gated |
| IMP-0008 | Security | P0 connected-service exclusions | IMP-0002, 0004 | current |
| IMP-0009 | Privacy | Local, redacted diagnostics boundary | IMP-0002–0003, 0006 | GATE-0005 / gated |
| IMP-0010 | Accessibility | Semantic design-token contract | IMP-0001–0002 | GATE-0002/0004 / gated |
| IMP-0011 | Content | Original-content provenance control | IMP-0005 | current + human review |
| IMP-0012 | Documentation | Foundation boundary documentation | IMP-0002, 0004, 0006, 0008 | current |
| IMP-0027 | PWA | Manifest and install eligibility boundary | IMP-0022, 0026 | GATE-0002/0007 retained |
| IMP-0028 | PWA | Safe cache, update, and offline recovery lifecycle | IMP-0006, 0021, 0027 | GATE-0002/0005 retained |
| IMP-0029 | Release | Local release configuration, integrity, and diagnostics checks | IMP-0008, 0009, 0028 | GATE-0005/0007 retained |
| IMP-0030 | Quality | Performance and compatibility evidence boundary | IMP-0023, 0028, 0029 | GATE-0002/0005 retained |
| IMP-0031 | Documentation | Player recovery and operator release/rollback boundary | IMP-0025, 0028, 0029 | GATE-0005/0007 retained |
| IMP-0032 | Quality | Final PWA/release evidence hold audit | IMP-0030, 0031 | GATE-0002/0005/0007 retained |

Each JSON contract has one title, domain, target allocation, requirement IDs,
bounded outcome, prerequisite list, sole files/data/API ownership, forbidden
scope, verification, human/external gate, complexity, and status. The only
dependency direction is toward earlier contracts, so the current graph is
acyclic.

## Domain-expansion queue

| Queue ID | Bounded domain (maximum contracts) | Dependency | Requirements/gate | Allocation |
| --- | --- | --- | --- | --- |
| SHARD-02 | Campaign content and domain logic (250) | SHARD-01 | Core P0 campaign; GATE-0004 | Shared core/content; no UI |
| SHARD-03 | Session, UI, input, and accessibility (250) | SHARD-01–02 | REQ-0005–0007, 0009–0010, 0012; GATE-0002–0004 | Shared UI model, Web adapters, inherited PWA UI |
| SHARD-04 | PWA delivery, performance, operations, and release evidence (250; expanded to six) | SHARD-01–03 | REQ-0011–0012, NFR-0001/0003/0006/0009/0011/0012; GATE-0002/0005/0007 retained | Separate web build and PWA lifecycle |
| SHARD-05 | Connected-scope decision package (250) | SHARD-01 | REQ-0014–0015; GATE-0006 | Hold; research/decision outputs only if authorised |

The JSON `requirement_coverage` map accounts for every canonical `REQ-*` and
`NFR-*` as current, queued, gated, or held, naming the corresponding contract
or expansion shard. No requirement is silently rejected or deferred.

## Structural validation

Use this check after edits:

```sh
node -e 'const c=require("./projects/mock-fantasy-quest-4/planning/implementation-catalogue-index.json"); const ids=new Set(c.contracts.map(x=>x.id)); if (ids.size!==c.contracts.length || c.first_bounded_domain.contract_count>c.first_bounded_domain.contract_limit || c.expansion_queue.some(x=>x.max_contracts>250) || Object.keys(c.requirement_coverage).length!==27 || c.contracts.some(x=>x.prerequisites.some(p=>!ids.has(p)))) process.exit(1); console.log("catalogue structural check passed")'
```
