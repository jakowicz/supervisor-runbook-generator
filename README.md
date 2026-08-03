# Runbook Generator

This repository is a generic, Supervisor-driven factory for turning a concise
product brief into a complete, dependency-ordered implementation plan. It is
not tied to a particular app type, framework, agent, or delivery platform.

Given a brief for a game, desktop application, web product, operating system,
developer tool, service, document system, or any other product, the factory
first discovers the product domains and creates a canonical specification. For
games, it also creates and completes a game-specific design programme before
implementation planning begins. It then builds a scalable collection of
detailed implementation runbooks.

## Install Supervisor

Install the global Supervisor CLI once. It requires Python 3.10 or newer but
does not require administrator access:

```zsh
curl -fsSL https://raw.githubusercontent.com/jakowicz/supervisor/main/scripts/install.sh -o /tmp/supervisor-install.sh
bash /tmp/supervisor-install.sh
```

If the installer says `~/.local/bin` is not on your `PATH`, add the line it
prints to your shell profile, then open a new terminal. Confirm the commands
are available:

```zsh
supervisor --help
supervisor-run --help
```

## Start a factory run

From the repository root, there are only two actions required to start a
factory run.

1. Create a named project workspace and its
   `projects/<project-name>/INITIAL.md` brief with the interactive wizard. It
   asks for the project name, product type, target systems, users,
   requirements, constraints, and reference products. Responsive web and PWA
   support are included by default.

```zsh
supervisor initial --force
```

   `--force` deliberately replaces an existing brief with the same project
   name; omit it if you want the command to refuse to overwrite it.

   For games, the wizard also offers optional visual and music/sound direction.
   You can leave either blank: the later design process derives an original
   direction from the brief and creates only the asset or audio work that the
   selected game design genuinely requires.

2. Review the generated `projects/<project-name>/INITIAL.md`, make any edits
   you want, then run that named project:

```zsh
supervisor-run --project <project-name>
```

`--project` reads that project's `INITIAL.md` and runs the reusable F-series.
For games, it follows the F005-created game-design collection and will not
continue at F006 until the final game-design audit is accepted. F014 then
creates the bootstrap implementation-authoring controls, which dynamically
dispatch B-series authors. It keeps the factory's durable task history in
`projects/<project-name>/.state/`, its
versioned project configuration in `projects/<project-name>/.env`, and private
credentials in ignored `projects/<project-name>/.secrets.env`, so a later
`supervisor-run --project <project-name>` resumes at the first unfinished task
and does not rerun accepted tasks. That workspace contains its normalized brief,
specification, complete work checklist, game-design collection (for games),
generated GB/B-series authoring files, R-series product-work handoff, and
handoff documentation.

### Generated R runbooks are handed off, not run here

Keep using this command to run the factory and its B-series authors:

```zsh
supervisor-run --project <project-name>
```

After the B-series authoring collection is complete, the factory stops. Its
final deliverable is the generated R collection in
`projects/<project-name>/runbooks/`; the factory never registers or executes it
as a child collection.

An R file is **generated** as soon as a B writer creates its Markdown file. It
is not accepted by the runbook generator: a separate implementation supervisor
will later run the R files, apply that implementation project's `.env` pipeline,
collect evidence, and decide acceptance in its own durable state. This keeps
the factory focused on producing excellent product-work instructions rather
than also building the product.

## Factory end-to-end test

Run the opt-in real-agent factory acceptance test through the generator CLI:

```zsh
scripts/runbookgen e2e
```

It prompts you to choose from a few small example projects—three games (including
a football-trivia game targeting Android and iOS), a todo
app, text editor, mini OS utility, file-processing API, or internal helpdesk—
then runs that project's factory and verifies a second run resumes accepted
work. For unattended use, set a scenario explicitly:

```zsh
E2E_SCENARIO=todo-app scripts/runbookgen e2e
```

For example, the command above creates `projects/e2e-todo-app/`, then runs the
F-series factory, any required game-design collection, and its generated
B-series authoring collection. It validates the resulting R-series handoff and
runs once more to confirm durable resume behaviour; it does not implement or
run the R-series product work. The
workspace remains under `projects/` for inspection.

## See or resume project progress

From the repository root, list every named workspace and its current phase,
accepted/pending counts, next task, and exact resume command:

```zsh
supervisor projects
```

Run `supervisor-run --project <project-name>` at any time to resume that
project. Its SQLite task state makes accepted tasks skip safely and returns to
the first unfinished task.

For the more detailed factory view, including live F/G/B/C/D work, generated
R-runbook counts, and the next action, run:

```zsh
scripts/runbookgen status <project-name>
```

The status view also states the hard authoring ceiling: each `GB` writer may
create at most five G game-design runbooks, and each `B` writer may create at
most five R implementation runbooks. Larger products automatically use more
small writer batches rather than asking one agent to create an oversized set.

## What the runbook series mean

These are this factory's names, not an industry-standard vocabulary. The letter
describes *which layer of work a runbook belongs to*, rather than a product
feature or a required technology. In normal use, you only need to care about
`INITIAL.md`, F, GB/G (for games), B, and R.

### Runbooks you normally use

| Series | Meaning | Created by | Where it lives | What it does |
| --- | --- | --- | --- | --- |
| `INITIAL.md` | Source brief | You or `supervisor initial` | `projects/<project-name>/` | The concise source brief: what is being made, for whom, where it will run, constraints, references, and desired outcome. It gives every later stage its context. |
| `F001`–`F016` | **Factory** | This repository | `runbooks/` | **Factory runbooks.** They analyse the brief and create the game-design programme (when needed), then the implementation-authoring plan. They do not build the requested product. |
| `GB0001`, `GB0002`, … | **Bounded game-design authoring batch** | The initial F005-created GD dispatcher, then later GD dispatchers; games only | `projects/<slug>/game-design-runbooks/` | **Game-design runbook-writing tasks.** F005 creates the design programme and its first dispatcher; GD dispatchers then create GB batches. A GB task writes the next small set of G design runbooks. Like B, it has a hard limit: one GB task may write no more than five G files. |
| `G0001`, `G0002`, … | **Game-design runbook** | GB design-runbook writers, for games only | `projects/<slug>/game-design-runbooks/` | **Actual game-specific design work.** G files create and review detailed original game bibles—such as story, world, characters, bosses, question banks, scoring, or fairness—before implementation runbooks are authored. GC checkpoints, GD dispatchers, and a final GQ audit scale and verify that work. |
| `B0001`, `B0002`, … | **Bounded implementation-runbook authoring batch** | The initial F014-created `D0001` dispatcher, then later D dispatchers | `projects/<slug>/authoring-runbooks/` | **Runbook-writing tasks.** F014 creates the bootstrap dispatcher; that dispatcher creates the first B batches, and later D dispatchers create further batches. A B task writes the next small set of R files. Like GB, it has a hard limit: one B task may write no more than five R files. |
| `R0001`, `R0002`, … | **Real product-work runbook** | B-series runbook-writing tasks | `projects/<slug>/runbooks/` | **Product-work runbooks.** Each R file gives detailed instructions and success checks for one small piece of building, testing, reviewing, documenting, or original-asset work. Every R file explicitly declares asset metadata and provenance links to its canonical specification, catalogue records, B batch, and originating F stages. |

### Internal planning and coordination

These files and records let the factory safely scale to a large application.
They are important to the generator, but not things you normally need to read
or manage while building the product.

| Internal ID | Meaning | Created by | Where it lives | What it does |
| --- | --- | --- | --- | --- |
| `REQ-0001`, `REQ-0002`, … | **Functional requirement** | F011 specification/traceability stage | `projects/<slug>/specification/requirements.md`, `requirements.json`, and `traceability-matrix.md` | A stable statement of behaviour or capability the product must provide. It is a requirement, not a runnable task. |
| `NFR-0001`, `NFR-0002`, … | **Non-functional requirement** | F011 specification/traceability stage | `projects/<slug>/specification/requirements.md`, `requirements.json`, and `traceability-matrix.md` | A stable quality or constraint requirement—such as performance, accessibility, security, reliability, privacy, compatibility, or observability. It is not a runnable task. |
| `IMP-0001`, `IMP-0002`, … | **Implementation catalogue record** | The F-series planning stages and later D dispatchers | `projects/<slug>/planning/implementation-catalogue-index.json` and the authoring manifest/ledger | **Planning and traceability records, not runnable runbooks.** Each record captures a needed piece of work, its requirements, dependencies, ownership, verification, and asset assessment before it is allocated to a B writer. |
| `C0001`, `C0002`, … | **Catalogue checkpoint** | F014 creates the bootstrap checkpoint; later D dispatchers create further checkpoints when needed | `projects/<slug>/authoring-runbooks/` | **Authoring coordination only.** A C task validates the catalogue, manifest, IDs, dependency coverage, and batch limits before another writing wave proceeds. It creates no product code and normally creates no R files. |
| `GC0001`, `GC0002`, … | **Game-design checkpoint** | A GD dispatcher; games only | `projects/<slug>/game-design-runbooks/` | **Game-design coordination only.** A GC task checks the selected design modules, design-unit coverage, ownership, and evidence before another GB/G wave proceeds. It creates no product code. |
| `GD0001`, `GD0002`, … | **Game-design dispatcher** | F005 creates `GD0001`; each earlier GD dispatcher creates at most one successor; games only | `projects/<slug>/game-design-runbooks/` | **Game-design coordination only.** A GD task selects the next game-design area, allocates bounded GB batches, and leaves one successor only if more game-design work remains. GB batches then write the G game-design runbooks. It does not build the product. |
| `GQ0001` | **Final game-design audit** | The final GD dispatcher; games only | `projects/<slug>/game-design-runbooks/` | **Game-design completion gate.** It proves every selected design module and `GAME-*` design unit has accepted, canonical evidence before Supervisor may continue to F006. |
| `D0001`, `D0002`, … | **Implementation-runbook dispatcher** | F014 creates `D0001`; each earlier D dispatcher creates at most one successor | `projects/<slug>/authoring-runbooks/` | **Authoring coordination only.** A D task expands one eligible implementation-planning chapter, allocates the next bounded B batches, and leaves one successor dispatcher only if more catalogue work remains. B batches then write the R implementation runbooks. It does not build the product or write R implementation files itself. |

### How the generated runbooks and records connect

Solid arrows show files or records created by a stage. Dotted arrows show
validation, scheduling, or traceability links rather than a task creating its
source material.

```mermaid
flowchart TD
    INITIAL["INITIAL.md\nsource brief"] --> F["F001–F005\nfactory discovery and planning"]
    F --> GD["GD0001…\ngame-design dispatcher\ngame-design-runbooks/"]
    GD --> GB["GB0001…\nbounded G-runbook writers"]
    GB --> G["G0001…\ngame-specific design bibles"]
    GC["GC checkpoints"] -. "validates" .-> G
    GD -. "schedules and checks waves" .-> GC
    GQ["GQ final audit"] -. "proves complete" .-> G
    GQ -. "accepted completion gate\nfor games" .-> POSTF["F006–F016\nfactory authoring plan"]
    F -. "non-games" .-> POSTF

    POSTF --> SPEC["Canonical specification\nprojects/<name>/specification/"]
    SPEC --> REQ["REQ-*\nfunctional requirements"]
    SPEC --> NFR["NFR-*\nquality and constraint requirements"]
    POSTF --> IMP["IMP-*\nimplementation catalogue records\nprojects/<name>/planning/"]
    REQ -. "covered by" .-> IMP
    NFR -. "covered by" .-> IMP
    SPEC -. "defines" .-> IMP

    POSTF --> C["C0001…\ncatalogue checkpoints\nauthoring-runbooks/"]
    POSTF --> D
    C -. "validates catalogue, IDs,\ndependencies, and batch limits" .-> IMP
    C -. "permits next wave" .-> D

    D["D0001…\ndispatchers\nauthoring-runbooks/"] -. "expands one eligible chapter\nand allocates a later wave" .-> IMP
    D --> B["B0001…\nbounded R-runbook writers\nauthoring-runbooks/"]
    D -. "creates successor when needed" .-> D

    B --> R["R0001…\nproduct-work runbooks\nrunbooks/"]
    R -. "requirement_ids" .-> REQ
    R -. "requirement_ids" .-> NFR
    R -. "source_catalogue_ids" .-> IMP
    R -. "source_specifications" .-> SPEC
    R -. "authoring_batch" .-> B
```

In short:

```text
your brief → F001–F005 → GD/GB/G game design (games only) → F006–F016 → D/B runbook authoring → R-series product work
                         ↑ GC/GQ coordinate game design              ↑ C/D coordinate implementation authoring
```

### Game-design phase

Games insert a mandatory project-scoped G-series phase before implementation
authoring. It is intentionally generated from the selected game's own design
signals, rather than a fixed RPG template.

```text
F001–F005: understand the game and create the G-design programme
  → GD dispatchers allocate GB writers (at most five G files per GB)
  → G-series: create detailed, game-specific bibles in bounded waves
  → GC checkpoints and a final GQ audit prove design and production inventory are complete
  → F006–F016: create the implementation catalogue and bootstrap D dispatcher
  → D dispatchers allocate B writers (at most five R files per B)
  → B writers create the R implementation-runbook handoff
```

For example, an RPG may receive separate design work for story, world, party,
bosses, enemies, quests, jobs, and progression. A football trivia game instead
receives question-source, category, answer-adjudication, scoring, fairness,
mode, anti-repeat, and editorial-content work. The factory does not proceed to
the B/R implementation layer until the generated G collection's final audit is
accepted.

The stable planning chain is `REQ/NFR requirement → specification → IMP
catalogue record → B writer → R runbook`. `REQ-0007` is a functional behaviour
requirement; `NFR-0004` is a quality/constraint requirement. Neither is another
name for `IMP-0007` or `R0007`. `IMP-0007` is a planning record, while `R0007`
is an executable piece of product work. Their numbers are intentionally
independent. One IMP record may be split into several R files, combined with
related IMP records into one R file, or held until its dependencies are ready.
An R file records that mapping in `requirement_ids` and `source_catalogue_ids`.

The hierarchy stops there: F creates the plan and the initial dispatchers, GD
creates GB batches for G design work, and D creates B batches for R
implementation work. G files define game-specific design evidence; R files
describe the real implementation or verification work. For example,
a B file for an RPG's combat area might write up to five R files: basic combat,
damage calculation, enemies, abilities, battle UI, balancing, and tests. For a
large product, more B files are created for the next areas instead of making one
agent write thousands of R files at once. The factory automatically finds later
B files and stops once the complete R handoff has been structurally validated.
The separate implementation supervisor later runs the R files.

`GC`, `GD`, `GQ`, `C`, and `D` are deliberately less important to the
application than F, GB/G, B, and R. They are internal factory controls: GC/GD/GQ
validate, schedule, and close game-design work; C/D validate and schedule
implementation-runbook authoring. They should be visible in status so a paused
factory can be understood, but they are not application features and do not
become part of the generated app.

### How runbooks reference one another

Runbooks do not pass the whole project history into every later prompt. They
use a small, explicit chain of references, while the full workspace remains
available for targeted lookup.

| When | What is used | Why |
| --- | --- | --- |
| `F001` | `projects/<name>/INITIAL.md` | The user’s original brief is the source of truth. F001 normalizes it but never replaces it. |
| `F002`–`F004` | `INITIAL.md`, `PROJECT_BRIEF.md`, and the relevant earlier specification chapters | These stages refine product/domain, technical, and experience decisions. They use the documents produced by earlier F stages—not every earlier F Markdown procedure. |
| `F005` | The game-design signals, initial bible, creative direction, and dependency map | For games, it creates `GD0001` and the prerequisite G collection. For other products, it continues directly with the delivery map. |
| A GD/GB/G/GC/GQ game-design wave | Its assigned design modules, canonical design inputs, game-design manifest, and production inventory | It creates and proves the game-specific bibles before F006 can begin. Each GB writer receives a focused batch of no more than five G outputs. |
| `F006`–`F010` | The canonical `specification/` chapters and earlier planning outputs; the completed G manifest for games | These stages translate established decisions into dependencies, delivery areas, authoring contracts, and a safe handoff. |
| `F011`–`F013` | The canonical specification plus the delivery/contract planning outputs | These stages create the traceability system, implementation catalogue, dependency graph, and small B-series batches. |
| `F014`–`F016` | The catalogue, authoring manifest, quality gate, and canonical specification | F014 creates the bootstrap C/D controls; D creates B writers, which write R contracts. These stages validate the handoff and register the authoring child collection for a separate implementation supervisor. |
| A B-series writer | Its own F013 context packet: only the assigned catalogue records, relevant specification sections, target constraints, templates, and reserved IDs | It writes no more than five R files without needing a huge prompt or unrelated product context. |
| A C checkpoint or D dispatcher | The authoring manifest, catalogue, ledger, and only the relevant canonical specification chapter | It validates and schedules the authoring process; it is not product implementation context. |
| An R-series task | Its own objective, dependencies, acceptance criteria, and provenance metadata | It performs one small piece of product work. It can open the linked canonical files when it needs more detail. |

Each generated R file must declare this provenance in its front matter:

```yaml
requirement_ids:
  - REQ-0007
  - NFR-0004
source_specifications: specification/03-technical-contract.md#save-state
source_catalogue_ids: IMP-SAVE-001
authoring_batch: B0007
factory_stages: F003,F005,F012,F013
asset_impact: required
asset_ids: ASSET-SAVE-001
audio_impact: not_applicable
audio_ids: ""
```

These fields answer different questions:

- `requirement_ids` — which functional (`REQ-*`) and quality/constraint (`NFR-*`) requirements the task fulfils or verifies.
- `source_specifications` — which canonical requirement sections explain the work.
- `source_catalogue_ids` — which planned implementation records the task covers.
- `authoring_batch` — which bounded B writer created this R task.
- `factory_stages` — which F stages established the underlying requirement.
- `asset_impact` and `asset_ids` — whether the task owns original visual or
  other assets, and their stable IDs.
- `audio_impact` and `audio_ids` — whether the task owns music, sound effects,
  voice, or other audio, and their stable IDs.

The F and B references provide **provenance**, not a reason to use procedural
factory Markdown as implementation requirements. The canonical specification
and planning files remain the authoritative context. R-to-R dependencies define
execution order; this factory follows an explicit `.supervisor-children/`
registration from the F collection to the B collection only. The resulting R
collection is deliberately left for the separate implementation supervisor.

After every B-series authoring wave, run that project's structural quality gate
(for example, `python3 projects/<project-name>/planning/validate_runbook_generation.py`).
It checks authoring provenance, ownership, assets, browser-test reservations,
and coverage; it is not evidence of product implementation, testing, or release
readiness.

### Terms used in this repository

| Term | Meaning here |
| --- | --- |
| **Runbook** | A Markdown work instruction with scope, steps, dependencies, and evidence required to mark it complete. |
| **Runbook-writing task / authoring task** | A runbook whose output is more runbook Markdown files. GB-series files write G files; B-series files write R files. The GC/GD/GQ and C/D files coordinate those authoring loops. |
| **Bounded** | Deliberately limited in size. A GB-series task writes at most five G files, and a B-series task writes at most five R files. |
| **Functional requirement (`REQ-*`)** | A stable statement of behaviour or capability the product must provide. Stored in the project’s `specification/requirements.md` and `requirements.json`, with coverage shown in `traceability-matrix.md`. |
| **Non-functional requirement (`NFR-*`)** | A stable quality, safety, delivery, or operating constraint—such as performance, accessibility, security, reliability, privacy, or compatibility. Stored and traced alongside functional requirements. |
| **Catalogue** | The complete checklist of product work that must eventually be covered: features, technical foundations, content, quality, release work, and dependencies. |
| **Implementation catalogue record (`IMP-*`)** | One stable planned work record in `planning/implementation-catalogue-index.json` and the authoring manifest/ledger. It is allocated to an authoring batch before one or more R-series runbooks are written. It is not itself runnable. |
| **Collection** | A folder of runbooks that Supervisor can run. The root F collection creates a game-design child collection when needed and an implementation-authoring child collection; it deliberately does not run the final R collection. |
| **Catalogue checkpoint (C)** | An internal authoring control that checks the catalogue and allocation ledger before a new writing wave can proceed. It creates no application deliverable. |
| **Game-design dispatcher (GD)** | An internal game-design control that creates the next bounded GB-series files when more selected game-design work remains. It creates no application deliverable. |
| **Implementation dispatcher (D)** | An internal authoring control that creates the next bounded B-series files when more parts of the catalogue still need R runbooks. It creates no application deliverable. |
| **Contract** | The required shape of a runbook: its goal, inputs, steps, acceptance criteria, and evidence. It is not a legal agreement or an API contract. |

### F-series factory stages, in detail

The F-series is deliberately product-agnostic. It uses the brief to decide what
“complete” means for this particular product: an RPG may need story, systems,
content, balancing, save state, and platform work; an IDE may need language
services, debugging, extensions, and source control; an operating system may
need kernel, hardware, security, installation, and system-management work.

| Stage | What it establishes | Main output for later stages |
| --- | --- | --- |
| `F001` | Reads `INITIAL.md`, normalizes the requested outcome, distinguishes explicit requirements from safe assumptions and unanswered decisions, and discovers the product-specific system families. | `PROJECT_BRIEF.md` and the first domain-discovery specification. |
| `F002` | Defines the domain model, key users or actors, journeys, feature areas, release slices, and the boundaries between first release and later work. | A product map that can be divided into independently buildable areas. |
| `F003` | Defines the technical and quality foundations appropriate to the brief: architecture, data, integrations, privacy/trust, resilience, performance, observability, and testability. | Cross-cutting technical, data, trust, and quality contracts. |
| `F004` | Defines the intended experience without copying a reference product: interaction principles, accessibility, localisation, visual/art direction where relevant, and platform adaptations. | Original experience, accessibility, and presentation constraints. |
| `F005` | Turns the product map into a dependency graph. For games, it also creates `GD0001`, the project-scoped G design collection, and its completion gate. | Dependency-ordered implementation map; for games, a bounded game-design programme that must complete before F006. |
| `F006` | Defines the authoring contracts for platform foundations and core domain systems. For games it consumes the accepted G design manifest. | Reusable instructions for the foundation and domain portions of the catalogue. |
| `F007` | Defines authoring contracts for user-facing features, workflows, gameplay/content, and experience quality. | Reusable instructions for feature and experience portions of the catalogue. |
| `F008` | Defines authoring contracts for security/trust, operations, administration/tooling, release, support, and lifecycle work where the product needs them. | Reusable instructions for operational and release portions of the catalogue. |
| `F009` | Audits the emerging catalogue against the brief, dependencies, targets, quality constraints, lifecycle, and omitted-but-necessary work. | A gap-checked catalogue with omissions, conflicts, and decisions recorded. |
| `F010` | Resolves the specification-to-authoring handoff: stable scope boundaries, task granularity, acceptance evidence, and the inputs needed to write implementation runbooks. | Final authoring inputs; no product code is created. |
| `F011` | Builds the canonical specification and requirements-traceability system, so every planned area can be traced back to the brief, a constraint, or a justified dependency. | Canonical specification and traceability records. |
| `F012` | Builds the full implementation catalogue and its dependency graph, including foundations, features, content, assets, quality, operations, and release work as applicable. | The complete checklist from which R-series tasks will be written. |
| `F013` | Divides that checklist into small, dependency-safe authoring batches that can scale from a handful to thousands of R files. | Batch plan and B-series dispatch strategy. |
| `F014` | Creates and registers the bootstrap C checkpoint and `D0001` dispatcher. **It does not create B or R files directly.** D dispatches B writers; each B writer writes at most five detailed R-series product-work runbooks. | `authoring-runbooks/C….md` and `D….md` bootstrap controls. |
| `F015` | Checks that the B batches and their intended R contracts cover the catalogue, obey dependency ordering, and include `asset_impact`/`asset_ids` and `audio_impact`/`audio_ids` wherever required. | Validated authoring batches and implementation-contract rules. |
| `F016` | Publishes the project-scoped handoff: records how factory authoring resumes and hands the generated R collection to a separate implementation supervisor. | Handoff documentation, registered B collection, and R implementation handoff. |

The division of responsibility is therefore:

- `F001`–`F004`: understand and specify the particular product.
- `F005`–`F010`: make its delivery work coherent, complete, and authorable.
- `F011`–`F013`: turn that into a traceable catalogue and scalable batch plan.
- `F014`–`F016`: bootstrap, validate, and hand off the D/B authoring loop that produces the R-series product-work handoff.

## The product brief drives the result

The factory treats `INITIAL.md` as the source of truth. It does not assume that
every product is a game or a web application.

- A role-playing game may need narrative, world, character, combat, content,
  balancing, save-state, and platform chapters.
- An IDE may need language services, editing, debugging, extensions, workspace,
  and source-control chapters.
- An operating system may need kernel, hardware, identity, process, storage,
  installation, security, and system-management chapters.

These are examples only. The discovery runbooks derive the appropriate domains,
relationships, quality requirements, content/tooling needs, and platform work
from the actual brief.

## Supervisor configuration

The nested [supervisor/README.md](supervisor/README.md) documents the reusable
orchestrator. Its project-local `.env` defines the active agents, stage order,
validation commands, browser or visual QA, timeouts, write permissions, and
publishing policy. The factory does not require one fixed agent pipeline.

Use `supervisor configure` to review those settings. Use `supervisor update` to
pull a newer Supervisor and apply its committed environment migrations to the
project `.env` without overwriting existing values.

## Repository layout

| Path | Purpose |
| --- | --- |
| [runbooks/](runbooks/) | The reusable F-series factory collection. |
| [projects/](projects/) | Generated, project-scoped specifications and runbook collections. |
| [supervisor/](supervisor/) | Reusable evidence-gated orchestration submodule. |

Read [runbooks/README.md](runbooks/README.md) for the collection-level file
conventions and [projects/README.md](projects/README.md) for generated project
workspaces.
