# Runbook Generator

This repository is a generic, Supervisor-driven factory for turning a concise
product brief into a complete, dependency-ordered implementation plan. It is
not tied to a particular app type, framework, agent, or delivery platform.

Given a brief for a game, desktop application, web product, operating system,
developer tool, service, document system, or any other product, the factory
first discovers the product domains and creates a canonical specification. It
then builds a scalable collection of detailed implementation runbooks.

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
   requirements, constraints, references, and open decisions. Responsive web
   and PWA support are included by default.

```zsh
supervisor initial --force
```

   `--force` deliberately replaces an existing brief with the same project
   name; omit it if you want the command to refuse to overwrite it.

2. Review the generated `projects/<project-name>/INITIAL.md`, make any edits
   you want, then run that named project:

```zsh
supervisor-run --project <project-name>
```

`--project` reads that project's `INITIAL.md`, runs the reusable F-series, then
automatically follows the generated B-series and R-series files. It keeps the
factory's durable task history in `projects/<project-name>/.supervisor/`, so a
later `supervisor-run --project <project-name>` resumes at the first unfinished
task and does not rerun accepted tasks. That workspace contains its normalized
brief, specification, complete work checklist, generated B-series
runbook-writing files, R-series product-work runbooks, and handoff
documentation.

## See or resume project progress

From the repository root, list every named workspace and its current phase,
accepted/pending counts, next task, and exact resume command:

```zsh
supervisor projects
```

Run `supervisor-run --project <project-name>` at any time to resume that
project. Its SQLite task state makes accepted tasks skip safely and returns to
the first unfinished task.

## What the F, B, and R series mean

The letters describe *which layer of work a runbook belongs to*, rather than a
product feature or a required technology.

| Series | Created by | Where it lives | What it does |
| --- | --- | --- | --- |
| `INITIAL.md` | You or `supervisor initial` | `projects/<project-name>/` | The concise source brief: what is being made, for whom, where it will run, constraints, references, and desired outcome. It gives every later stage its context. |
| `F001`–`F016` | This repository | `runbooks/` | **Factory runbooks.** They analyse the brief, write the detailed product plan, and create the files that will write the final implementation instructions. They do not build the requested product. |
| `B0001`, `B0002`, … | The F-series and later B dispatcher files | `projects/<slug>/authoring-runbooks/` | **Runbook-writing tasks.** A B task writes the next small set of R files. “Bounded” simply means it has a hard limit: one B task may write no more than seven R files. |
| `R0001`, `R0002`, … | B-series runbook-writing tasks | `projects/<slug>/runbooks/` | **Product-work runbooks.** Each R file gives detailed instructions and success checks for one small piece of building, testing, reviewing, or documenting the requested product. |

In short:

```text
your brief → F-series factory → B-series runbook writers → R-series product work
```

The hierarchy stops there: F creates the plan and the B files, B writes R files,
and R files describe the real implementation or verification work. For example,
a B file for an RPG's combat area might write up to seven R files: basic combat,
damage calculation, enemies, abilities, battle UI, balancing, and tests. For a
large product, more B files are created for the next areas instead of making one
agent write thousands of R files at once. The Supervisor finds those later B
files and the R files automatically, so one `--run-all` invocation continues
until the generated collection reaches its final audit or a real review gate.

### Terms used in this repository

| Term | Meaning here |
| --- | --- |
| **Runbook** | A Markdown work instruction with scope, steps, dependencies, and evidence required to mark it complete. |
| **Runbook-writing task / authoring task** | A runbook whose output is more runbook Markdown files. It does not write application code. B-series files are these tasks. |
| **Bounded** | Deliberately limited in size. A B-series task writes a maximum of seven R-series files. |
| **Catalogue** | The complete checklist of product work that must eventually be covered: features, technical foundations, content, quality, release work, and dependencies. |
| **Collection** | A folder of runbooks that Supervisor can run. The root F collection creates child B and R collections for one generated project. |
| **Dispatcher** | A B-series file whose only job is to create the next B-series files when more parts of the catalogue still need R runbooks. |
| **Contract** | The required shape of a runbook: its goal, inputs, steps, acceptance criteria, and evidence. It is not a legal agreement or an API contract. |

The F-series has these broad responsibilities:

| Factory stages | Responsibility |
| --- | --- |
| `F001`–`F004` | Normalize the brief and discover the product, platform, technical, and experience domains that matter for this particular request. |
| `F005`–`F010` | Break those domains into delivery areas, dependencies, quality requirements, and small pieces of work that will each become R files. |
| `F011`–`F013` | Produce the detailed specification, a check that nothing important is missing, the complete work checklist (catalogue), and the plan for writing R files in batches. |
| `F014` | Create and register the first B-series runbook-writing files for the generated project. **F014 does not create R files directly:** when Supervisor runs each B file, that B file writes up to seven R-series product-work runbooks. Later B dispatcher files create more B files when required. |
| `F015`–`F016` | Define quality gates, validate the factory output, and prepare handoff material. |

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
