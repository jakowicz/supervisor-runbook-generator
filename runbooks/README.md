# Runbooks

Put one Markdown runbook here for each small, independently reviewable task.
Start with `TEMPLATE.md`, assign a unique task ID and sequence, and be precise
about acceptance criteria. Then run it from `../supervisor`:

```zsh
./.venv/bin/supervisor-run --runbook ../runbooks/T001.md
```
