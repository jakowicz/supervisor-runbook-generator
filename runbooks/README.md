# Factory collection

This directory contains the runbook-generator's source collection. Read the
repository [README](../README.md) for the end-to-end workflow and Supervisor
configuration.

## Source files and roles

| File | Purpose |
| --- | --- |
| [F001.md](F001.md)–[F016.md](F016.md) | **F-series factory runbooks.** They turn the brief into a generated project's detailed plan, complete work checklist, and B-series runbook-writing files. |
| [TEMPLATE.md](TEMPLATE.md) | Required structure for a normal manually written runbook: goal, steps, success checks, and evidence. |

This directory contains only the reusable factory source. It never contains the
thousands of runbooks for a particular product.

| Series | Plain-English purpose | Output |
| --- | --- | --- |
| F-series | The factory: understand the brief, identify the required domains, and design a complete delivery plan. | A workspace in `projects/<slug>/`, including its specification, work checklist, and B-series files. |
| B-series | The runbook writers: write the next small set of implementation instructions. “Bounded” means one B file may write no more than seven R files. | Up to seven R-series files per B task; extra B files are created when more areas need coverage. |
| C-series | Catalogue checkpoints: validate the authoring catalogue, allocations, dependencies, and limits before the next writing wave. | No product work. C files are internal coordination files in `projects/<slug>/authoring-runbooks/`. |
| D-series | Dispatchers: expand one eligible planning chapter and create the next bounded B-series writing wave when more work remains. | More B-series authoring files, not R files or product work. D files live beside B/C files in `projects/<slug>/authoring-runbooks/`. |
| R-series | The product-work instructions: describe one small, ordered piece of real work. | Source changes, tests, assets, documentation, or other deliverables required by that R file. |

`C` means **Catalogue checkpoint** and `D` means **Dispatcher**. They are
factory-internal coordination runbooks, so they are far less important to the
application than the F/B/R chain: they neither define the product nor build it.
They exist only to let a very large catalogue grow safely without duplicating,
skipping, or overloading B-series writers. They share `authoring-runbooks/` and
its durable state with B files because all three operate in the runbook-writing
layer, before R-series product work is run.

Every R-series file must make an explicit asset decision in its front matter:
`asset_impact: required` with stable comma-separated `asset_ids`, or
`asset_impact: not_applicable` with a blank `asset_ids`. Asset-required files
also describe asset purpose, variants, ownership, original-art constraints, and
verification in an `## Asset assessment` section. This lets the Supervisor use
its opt-in asset lane only where the product work genuinely needs it.

Every R-series file also makes an explicit audio decision: `audio_impact:
required` with stable `audio_ids`, a cue brief, duration, loop policy, and
audio-style version; or `audio_impact: not_applicable` with the documented
empty/default values. When required, Supervisor uses the independent local
audio lane—cue director, ACE-Step 1.5 XL Turbo generator, then technical and
provenance QA—before the coding stage. F004 creates an audio-direction and cue
map only when the product actually needs music, sound effects, voice, or
audible feedback.

Every R-series file must also carry provenance metadata: `source_specifications`
links to the smallest relevant canonical specification sections,
`source_catalogue_ids` identifies its implementation-catalogue records,
`authoring_batch` names its B-series writer, and `factory_stages` records the
F-series stages that established the requirement. This lets an implementation
agent retrieve focused canonical context without treating procedural F/B files
as its requirements source.

For example, a game may eventually have R runbooks for story, combat, content,
saves, and platform delivery; an IDE may have R runbooks for language services,
editing, debugging, and extensions. The F-series derives those areas from the
brief rather than assuming either example.

`F001`–`F004` understand the brief and domains, `F005`–`F010` make the delivery
map, `F011`–`F013` create and check the specification and work checklist, and
`F014` creates the first B-series runbook-writing files. When Supervisor runs
those B files, each one writes up to seven R-series product-work runbooks. If
more R files are required, B dispatcher files create more B files. `F015`–`F016`
establish quality and handoff material.

## Run the collection

From the repository root, create a named project brief with `supervisor initial`,
review `projects/<project-name>/INITIAL.md`, then run:

```zsh
supervisor-run --project <project-name>
```

`--run-initial` runs only `F001`, which is useful for checking that the named
brief can be normalized before committing to the full factory. `--project`
reads that workspace's `INITIAL.md`, runs every F-series factory stage, then
dynamically follows its registered B-series and R-series collections. It keeps
state inside the named workspace and stops only for a real failure or explicit
review gate.

Generated runbook state is kept in the named workspace's `.state/` directory,
keeping IDs such as `R0001` isolated between projects. The workspace also owns
its private `.env`, including its art direction and project-specific Supervisor
configuration. For games, `supervisor initial` also asks for optional music and
sound direction. Leaving it blank configures Gemma 4 12B to create an original
direction and ACE-Step 1.5 XL Turbo as the local audio generator.
