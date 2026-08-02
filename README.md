# Runbook Generator

This repository is a generic, Supervisor-driven factory for turning a concise
product brief into a complete, dependency-ordered implementation plan. It is
not tied to a particular app type, framework, agent, or delivery platform.

Given a brief for a game, desktop application, web product, operating system,
developer tool, service, document system, or any other product, the factory
first discovers the product domains and creates a canonical specification. It
then builds a scalable collection of detailed implementation runbooks.

## What it produces

```text
INITIAL.md
  → F001–F016: discovery, specification, requirements, catalogue, and factory
  → B-series: bounded runbook-authoring tasks
  → R-series: detailed implementation and verification runbooks
```

The B-series prevents context limits from reducing quality: each authoring task
creates no more than seven R-series implementation runbooks. The Supervisor
discovers later B-series waves and registered child collections automatically,
so one `--run-all` invocation continues until the generated collection reaches
its final audit or a real review gate.

## Start a factory run

Create the initial brief interactively. The wizard selects product category and
target systems, always includes responsive web and PWA support, and asks for
users, constraints, platform requirements, references, and open decisions.

```zsh
./supervisor/.venv/bin/supervisor initial --force
```

Review [runbooks/INITIAL.md](runbooks/INITIAL.md), then run the collection once:

```zsh
./supervisor/.venv/bin/supervisor-run --run-all --runbooks-dir runbooks
```

The F-series creates a new workspace under `projects/<project-slug>/`. That
workspace contains its normalized brief, specification, catalogue, generated
authoring collection, implementation runbooks, and handoff documentation.

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
| [runbooks/](runbooks/) | The F-series factory collection, templates, and the initial brief. |
| [projects/](projects/) | Generated, project-scoped specifications and runbook collections. |
| [supervisor/](supervisor/) | Reusable evidence-gated orchestration submodule. |

Read [runbooks/README.md](runbooks/README.md) for the collection-level file
conventions and [projects/README.md](projects/README.md) for generated project
workspaces.
