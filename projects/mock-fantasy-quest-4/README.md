# mock-fantasy-quest-4 runbook factory handoff

This workspace is a **planning and runbook-authoring factory** for an eventual
implementation project. It does not contain a game implementation, product
test evidence, deployment, publishing, or release approval. The factory turns
the approved brief into bounded, reviewable implementation contracts; a later
implementation project chooses its stack and carries out those contracts only
after their gates are approved.

## Read the sources in this order

1. [`INITIAL.md`](INITIAL.md) is the original source of truth. It records the
   scope, selected targets, constraints, non-goals, and unanswered questions.
   [`PROJECT_BRIEF.md`](PROJECT_BRIEF.md) is its durable project-local copy.
2. The canonical [specification index](specification/README.md) is the stable
   requirement and decision system. Start with the [domain-discovery map]
   (specification/00-domain-discovery.md): it explains why exploration, town,
   dungeon, combat, inventory, quests, save/recovery, accessibility, web, and
   PWA systems appear in the downstream runbooks. The canonical specification
   must not override the original brief.
3. The planning catalogue—[`implementation-catalogue-index.md`](planning/implementation-catalogue-index.md)
   and its authoritative [JSON](planning/implementation-catalogue-index.json)—
   maps canonical requirements to bounded `IMP-*` contracts. The audited
   [delivery map](planning/05-delivery-map.md) and
   [contract audit](planning/09-contract-audit.md) provide dependency and
   closure evidence.

Responsive public web and installable PWA delivery are included by default for
this project. All actual platform requirements, including input, storage,
offline/update, browser support, and performance constraints, come from the
selected targets in the original brief and the canonical platform appendix;
they are not inferred from "web/PWA" alone.

## The three levels of work

| Level | Purpose | Inputs and outputs | Not permission to |
| --- | --- | --- | --- |
| Source brief and canonical specification | Preserve P0 scope, requirements, decisions, risks, target adaptations, and traceability | `INITIAL.md`, `PROJECT_BRIEF.md`, `specification/`, and `planning/` | Select gated technology, resolve an open decision, or build/release the game |
| B-series authoring runbooks | Write bounded `R####` implementation contracts from allocated `IMP-*` records | `authoring-runbooks/`, `planning/runbook-authoring-manifest.json`, and its Markdown ledger | Implement product code, create final assets, or claim product evidence |
| R-series implementation runbooks | Give the eventual implementation project one small, independently verifiable contract at a time | Repository-root `runbooks/R####.md` and the evidence paths named by each contract | Bypass its dependencies or human/external gates, publish, deploy, or release |

The `Final Fantasy V` reference is a high-level party-based, turn-based
adventure scope reference only. Never copy or request its branding, names,
story/lore, dialogue, maps, art, music, layouts, combat screens, or distinctive
interaction choreography. All creative work must be independently original and
follow the warm hand-painted, readable-silhouette, restrained-palette direction
with provenance and human creative review.

## Run the factory and authoring collections

Run these from the repository root. `--project mock-fantasy-quest-4` loads this
workspace's versioned, non-secret Supervisor configuration and uses its durable
state. An accepted task is skipped on a later collection run unless explicitly
retried.

### 1. Factory collection

Run the F-series factory collection and discover its registered child
collections:

```zsh
./supervisor/.venv/bin/supervisor-run --project mock-fantasy-quest-4 --run-all --runbooks-dir runbooks
```

The factory source collection is repository-root `runbooks/`; its child
registration is `runbooks/.supervisor-children/mock-fantasy-quest-4.json`.
The project factory state and raw, per-stage logs are under
`.state/factory.sqlite3` and `.state/live/` respectively.

### 2. B-series implementation-contract authoring

Run the current B-series collection after its prerequisites are accepted:

```zsh
./supervisor/.venv/bin/supervisor-run --project mock-fantasy-quest-4 --run-all --runbooks-dir projects/mock-fantasy-quest-4/authoring-runbooks
```

To run just a dependency-ready writer, use its immutable file—for example:

```zsh
./supervisor/.venv/bin/supervisor-run --project mock-fantasy-quest-4 --runbook projects/mock-fantasy-quest-4/authoring-runbooks/B0001.md
```

The authoring collection starts at `authoring-runbooks/INITIAL.md`; the
completed dispatch history starts at `authoring-runbooks/D0001.md`; the current
successor is `authoring-runbooks/D0003.md`. The B-series collection has its
own `.state/authoring-runbooks.sqlite3` and `.state/live/` evidence locations.
Its authoritative allocation ledger is
[`planning/runbook-authoring-manifest.json`](planning/runbook-authoring-manifest.json),
with [`planning/runbook-authoring-manifest.md`](planning/runbook-authoring-manifest.md)
as the readable companion. Each B writer may create only its manifest-owned
R-series paths.

Validate the generated collection after each bounded wave:

```zsh
python3 projects/mock-fantasy-quest-4/planning/validate_runbook_generation.py --wave B0001
python3 projects/mock-fantasy-quest-4/planning/validate_runbook_generation.py
```

The validator is structural authoring evidence only. Its report is terminal
output; retain the relevant Supervisor task result, live log, and manifest
checkpoint in `.state/` and `planning/`. It does not prove implementation,
browser behaviour, accessibility, visual quality, or release readiness.

### 3. R-series implementation contracts

After the responsible B writer has generated an R contract, dispatch it to the
eventual implementation project through the chosen **Codex-only Supervisor
pipeline** (`SUPERVISOR_AGENT_ORDER=codex`, followed by Supervisor's configured
independent precheck/test/browser/visual-review/completion gates). For one
selected contract:

```zsh
./supervisor/.venv/bin/supervisor-run --project mock-fantasy-quest-4 --runbook runbooks/R0001.md
```

For all currently generated R-series contracts, run each manifest-owned file
in its declared dependency order (only after every file exists):

```zsh
for runbook in runbooks/R*.md; do
  ./supervisor/.venv/bin/supervisor-run --project mock-fantasy-quest-4 --runbook "$runbook"
done
```

The R contracts are generated in repository-root `runbooks/`, while their
implementation evidence belongs only at the test, browser, visual, and other
paths named by each individual R contract. Do not treat a planned path or a
passing authoring validator as implementation evidence. The implementation
project must retain its own run state, test reports, browser artefacts, visual
review, and any human approval records at those declared locations.

## Scaling and safe resume

For a larger project, repeat this controlled wave:

1. Run one dispatcher wave (`D####`). It may expand at most one eligible
   chapter, then allocate a bounded group of B-series writers.
2. Run only the newly allocated, dependency-ready B-series tasks. Keep every
   B batch at seven or fewer R contracts and each dispatcher wave at ten or
   fewer B writers.
3. Run the structural validator through the last affected B batch, checkpoint
   accepted work, and repeat from the manifest's first unaccepted batch.
4. When no queued or ready work remains, run the one final-audit B task the
   dispatcher creates. It audits the authoring system; it is not an
   implementation or release audit.

Never renumber, regenerate, mutate, or overwrite an accepted B/R contract.
For an approved scope change, add a new dispatcher wave and new monotonic
catalogue/B/R IDs rather than altering accepted contracts. Stop the affected
work for human review when a source conflict, missing coverage, cycle,
ID/output collision, credentials, paid service, legal/compliance decision,
device/store access, deployment, publishing, or release approval is involved.

Safe resume points are the `checkpoint` and `state` fields in the authoritative
manifest, the first non-accepted B batch, durable state databases in `.state/`,
and the latest corresponding `.state/live/` log. Preserve unresolved questions
in `specification/decision-log.md` and retain their `GATE-*` records; recording
a gate is never approval to proceed.

## Directory and evidence map

| Location | Role |
| --- | --- |
| `INITIAL.md`, `PROJECT_BRIEF.md` | Original and durable source briefs; the original brief wins on conflict |
| `specification/` | Canonical requirements, decisions, traceability, platform appendix, domain-completeness review, and specification index |
| `planning/` | Delivery map, implementation catalogue, allocation manifest/ledger, authoring handoff, audit, and structural validator |
| `planning/runbook-generation-quality-gate.md` and validator output | The structural validation procedure and its per-wave terminal report; retain the corresponding Supervisor result and live log as durable evidence |
| `authoring-runbooks/` | `INITIAL.md`, immutable B-series writers, dispatchers, and child-collection registrations |
| `runbooks/` | F-series factory runbooks plus generated R-series implementation contracts; its `.supervisor-children/` registers this project authoring collection |
| `.state/factory.sqlite3`, `.state/authoring-runbooks.sqlite3` | Durable Supervisor task state for the factory and authoring collections |
| `.state/live/` | Raw per-stage Supervisor evidence logs; use reports/state commands configured by Supervisor to inspect durable evidence |
| Paths declared by an R contract | Future implementation tests, browser artefacts, visual-review evidence, recovery evidence, and human-gate records; no such artefacts are created by authoring alone |

The current safe boundary is an original, offline-capable, single-player 2D
fantasy RPG with one town, one dungeon, a short guided campaign and ending.
Connected identity/account state, multiplayer and safety services, live
operations, purchases/entitlements, advanced analytics/monetisation, seasonal
events, and player-created/shared content remain excluded or held until a new
approved product, privacy, security, operational, cost, and failure-mode
contract exists.
