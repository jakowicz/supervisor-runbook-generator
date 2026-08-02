# Runbooks

Put one Markdown runbook here for each small, independently reviewable task.
Start with `TEMPLATE.md`, assign a unique task ID and sequence, and be precise
about acceptance criteria. Then run it from `../supervisor`:

```zsh
./.venv/bin/supervisor-run --runbook ../runbooks/T001.md
```

## Document-producing example collection

`F001.md` through `F016.md` are one example collection: given a completed
`INITIAL.md`, they create a project workspace, canonical specification, and a
scalable authoring collection. The B-series authoring tasks then create up to
seven R-series implementation runbooks each. This avoids trying to generate a
thousand detailed contracts in one Codex context. The Supervisor itself has no
special runbook-generation mode; it can run this or any other collection of
document, planning, or implementation tasks:

1. Complete [`INITIAL.md`](INITIAL.md) with the application or document
   collection you want to create.
2. Run the entire collection:

```zsh
supervisor-run --run-all --runbooks-dir runbooks
```

`--run-all` reads `INITIAL.md` before starting any task and gives its contents
to every task in the collection. Use `--run-initial` in place of `--run-all` to
run only F001 after the brief is ready.

Instead of editing the template manually, create it interactively from the
Supervisor checkout. The command always includes responsive web and PWA support,
then asks for product category, users, capabilities, selected systems, per-target
constraints, cross-platform behaviour, reference boundaries, and open decisions:

```zsh
supervisor initial --force
```

One command follows the generated child collections automatically. The authoring
dispatcher creates a bounded next wave, the runner discovers it, and continues
until the generated implementation collection's final audit completes:

```zsh
supervisor-run --run-all --runbooks-dir runbooks
```

To deliberately resume or run an already-generated project collection by
itself, use:

```zsh
supervisor-run --run-all --runbooks-dir projects/<project-slug>/authoring-runbooks
```

Each collection stores its resumable Supervisor state in its parent
`.supervisor/supervisor.sqlite3`, so `R0001` in two separate generated projects
cannot collide. Set `SUPERVISOR_DATABASE_PATH` only when deliberately sharing
state between collections.
