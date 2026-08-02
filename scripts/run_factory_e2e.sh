#!/usr/bin/env bash
set -euo pipefail

# Opt-in, real-agent acceptance test. It intentionally uses the configured
# Supervisor/Codex pipeline and leaves its workspace behind for inspection.
project_name="${E2E_PROJECT_NAME:-e2e-fantasy-quest}"

supervisor initial --non-interactive --force \
  --project-name "$project_name" --category Game \
  --product "A deliberately small offline 2D fantasy adventure, scoped to require roughly 18 implementation runbooks: exploration, one town, one dungeon, turn-based combat, inventory, quests, save/load, settings, and a short ending." \
  --reference "Final Fantasy V for party-based turn-based adventure scope only" \
  --art-direction "Original warm hand-painted fantasy, readable silhouettes, restrained palette"

supervisor-run --project "$project_name"

project_root="projects/$project_name"
python3 - "$project_root" <<'PY'
import sys
from pathlib import Path
from supervisor.runbooks import load_task

root = Path(sys.argv[1])
assert (root / '.env').is_file(), 'missing project .env'
assert (root / '.state').is_dir(), 'missing project .state'
runbooks = sorted((root / 'runbooks').glob('R*.md'))
assert 15 <= len(runbooks) <= 20, f'expected 15-20 R-series files; found {len(runbooks)}'
for path in runbooks:
    task = load_task(path)
    assert task.asset_impact in {'required', 'not_applicable'}
    if task.asset_impact == 'required':
        assert task.asset_ids, f'{path} needs stable asset_ids'
print(f'E2E PASS: {len(runbooks)} valid R-series runbooks in {root}')
PY

# A second invocation must use durable state rather than regenerating accepted work.
supervisor-run --project "$project_name"
