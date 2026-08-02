# Factory collection

This directory contains the runbook-generator's source collection. Read the
repository [README](../README.md) for the end-to-end workflow and Supervisor
configuration.

## Source files and roles

| File | Purpose |
| --- | --- |
| [INITIAL.md](INITIAL.md) | Product brief template and shared source of truth. This is user input, not an implementation runbook. |
| [F001.md](F001.md)–[F016.md](F016.md) | **F-series factory runbooks.** They turn the brief into a generated project's detailed plan, complete work checklist, and B-series runbook-writing files. |
| [TEMPLATE.md](TEMPLATE.md) | Required structure for a normal manually written runbook: goal, steps, success checks, and evidence. |
| [PRODUCT_BRIEF.template.md](PRODUCT_BRIEF.template.md) | Reusable non-interactive brief starting point. |

This directory contains only the reusable factory source. It never contains the
thousands of runbooks for a particular product.

| Series | Plain-English purpose | Output |
| --- | --- | --- |
| F-series | The factory: understand the brief, identify the required domains, and design a complete delivery plan. | A workspace in `projects/<slug>/`, including its specification, work checklist, and B-series files. |
| B-series | The runbook writers: write the next small set of implementation instructions. “Bounded” means one B file may write no more than seven R files. | Up to seven R-series files per B task; extra B files are created when more areas need coverage. |
| R-series | The product-work instructions: describe one small, ordered piece of real work. | Source changes, tests, assets, documentation, or other deliverables required by that R file. |

For example, a game may eventually have R runbooks for story, combat, content,
saves, and platform delivery; an IDE may have R runbooks for language services,
editing, debugging, and extensions. The F-series derives those areas from the
brief rather than assuming either example.

`F001`–`F004` understand the brief and domains, `F005`–`F010` make the delivery
map, `F011`–`F013` create and check the specification and work checklist,
`F014` creates the first B-series runbook-writing files, and `F015`–`F016`
establish quality and handoff material.

## Run the collection

From the repository root, complete `INITIAL.md` (or use `supervisor initial`),
then run:

```zsh
./supervisor/.venv/bin/supervisor-run --run-all --runbooks-dir runbooks
```

`--run-initial` runs only `F001`, which is useful for checking that the brief
can be normalized before committing to the full factory. `--run-all` reads
`INITIAL.md`, runs every F-series factory stage, then dynamically follows the
registered B-series and R-series collections. It stops only for a real failure
or explicit review gate.

Generated runbook state is kept beside each generated collection in
`.supervisor/supervisor.sqlite3`, keeping IDs such as `R0001` isolated between
projects.
