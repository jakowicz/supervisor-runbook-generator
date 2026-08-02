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
- `planning/`: implementation catalogue, dependency graph, and batch manifest;
- `authoring-runbooks/`: B-series tasks that author bounded R-series contracts;
- `runbooks/`: generated R-series implementation and verification contracts;
- `.supervisor/`: isolated run state for the generated collections.

The parent collection explicitly registers its generated child collections, so
the originating `--run-all` invocation follows them automatically.
