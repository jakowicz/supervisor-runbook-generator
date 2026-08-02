# Factory collection

This directory contains the runbook-generator's source collection. Read the
repository [README](../README.md) for the end-to-end workflow and Supervisor
configuration.

## Source files

| File | Purpose |
| --- | --- |
| [INITIAL.md](INITIAL.md) | Product brief template and shared source of truth. |
| [F001.md](F001.md)–[F016.md](F016.md) | The specification-to-runbook factory stages. |
| [TEMPLATE.md](TEMPLATE.md) | Contract format for a normal hand-authored runbook. |
| [PRODUCT_BRIEF.template.md](PRODUCT_BRIEF.template.md) | Reusable non-interactive brief starting point. |

The F-series is intentionally generic. It discovers the domains required by
the selected product and platforms, creates a canonical specification, then
creates B-series authoring tasks. Each B-series task writes at most seven
R-series implementation runbooks in a generated project workspace.

## Run the collection

From the repository root, complete `INITIAL.md` (or use `supervisor initial`),
then run:

```zsh
./supervisor/.venv/bin/supervisor-run --run-all --runbooks-dir runbooks
```

`--run-initial` runs only F001. `--run-all` reads `INITIAL.md`, dynamically
discovers the generated B-series and R-series collections, and stops only for a
real failure or explicit review gate.

Generated runbook state is kept beside each generated collection in
`.supervisor/supervisor.sqlite3`, keeping IDs such as `R0001` isolated between
projects.
