# Generated projects

Each completed F-series factory run creates one slugged workspace here. The
factory is run with the normal Supervisor collection command; there is no
special `generate-runbooks` command.

```zsh
./supervisor/.venv/bin/supervisor-run --run-all --runbooks-dir runbooks
```

Each project workspace contains:

- `PROJECT_BRIEF.md`: normalized source brief;
- `specification/`: canonical requirements, platform, experience, and domain
  specifications;
- `planning/`: the complete work checklist, dependency graph, and plan for
  creating the R files in manageable batches;
- `authoring-runbooks/`: generated B-series runbook-writing files. Each writes
  no more than seven R-series files; B files write Markdown instructions, not
  product code;
- `runbooks/`: generated R-series files: detailed instructions for the actual
  implementation and verification work;
- `.supervisor/`: isolated run state for the generated collections.

The relationship is deliberately layered:

```text
runbooks/INITIAL.md
  → repository F001–F016 factory files
  → projects/<slug>/authoring-runbooks/B....md
  → projects/<slug>/runbooks/R....md
```

The F-series files are reusable source factory instructions. They create the
project folder, specification, complete work checklist, and first B-series
files. A B-series file is a *runbook writer*: it takes one small part of that
checklist and writes no more than seven R-series Markdown files. “Bounded” is
only that size limit. It does not build the application. An R-series file is a
*product-work instruction*: it contains the detailed steps and success evidence
for one small piece of real product work.

In other words, the step that creates the R files is not an F-series file:
`F014` creates the first B files, then running each B file creates its R files.

For a very large product, a B dispatcher file creates more B-series runbook
writers for the remaining areas of the checklist. This is how the collection
scales to hundreds or thousands of R-series files without oversized prompts or
a separate manual run. The parent collection explicitly registers its generated
child collections, so the originating `--run-all` invocation follows them
automatically.
