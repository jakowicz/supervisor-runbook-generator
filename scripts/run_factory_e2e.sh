#!/usr/bin/env bash
set -euo pipefail

# Opt-in, real-agent acceptance test. It intentionally uses the configured
# Supervisor/Codex pipeline and leaves its workspace behind for inspection.
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
supervisor_cmd="${SUPERVISOR_COMMAND:-$root/supervisor/.venv/bin/supervisor}"
supervisor_run_cmd="${SUPERVISOR_RUN_COMMAND:-$root/supervisor/.venv/bin/supervisor-run}"
export PYTHONPATH="$root/supervisor${PYTHONPATH:+:$PYTHONPATH}"

scenario="${E2E_SCENARIO:-}"
if [[ -z "$scenario" && -t 0 && -t 1 ]]; then
  echo "Choose an E2E sample project:"
  select choice in "Fantasy quest" "Arcade puzzle" "Football trivia (Android and iOS)" "Todo app" "Text editor" "Mini OS utility" "File processing API" "Internal helpdesk"; do
    case "$REPLY" in
      1) scenario="fantasy-quest" ;;
      2) scenario="arcade-puzzle" ;;
      3) scenario="football-trivia" ;;
      4) scenario="todo-app" ;;
      5) scenario="text-editor" ;;
      6) scenario="mini-os" ;;
      7) scenario="file-processing-api" ;;
      8) scenario="internal-helpdesk" ;;
      *) echo "Enter a number from 1 to 8." >&2; continue ;;
    esac
    break
  done
fi
scenario="${scenario:-fantasy-quest}"
game_characteristics=""

case "$scenario" in
  fantasy-quest)
    category="Game"
    product="A deliberately small offline 2D fantasy adventure: one town, one dungeon, turn-based combat, inventory, quests, save/load, settings, and a short ending."
    reference="Final Fantasy V for party-based turn-based adventure scope only"
    targets=""
    art_direction="Original warm hand-painted fantasy, readable silhouettes, restrained palette"
    ;;
  arcade-puzzle)
    category="Game"
    product="A compact single-player arcade puzzle game with short rounds, clear controls, score tracking, accessibility settings, and local progress."
    reference="Tetris for short, readable puzzle sessions and escalating challenge only"
    targets=""
    art_direction="Original high-contrast geometric arcade art with accessible colour choices and clear piece silhouettes"
    ;;
  football-trivia)
    category="Game"
    product="A feature-rich football trivia game for quick mobile sessions: themed rounds, multiple question formats, answer validation, scoring streaks, accessible feedback, local progress, and a curated first-release question bank."
    reference="The Athletic quiz formats for football-topic breadth and QuizUp for short competitive trivia sessions only"
    targets="Android phone,iPhone (iOS)"
    game_characteristics="2D presentation,Single-player game,Puzzle, card, board, or turn-based game"
    art_direction="Original modern football broadcast graphics, bold category colours, readable typography, and celebratory but accessible feedback"
    ;;
  todo-app)
    category="Consumer application"
    product="A small cross-device todo app for capturing tasks, grouping them into lists, completing work, and recovering safely from mistakes."
    reference="Todoist for task capture, projects, priorities, and recurring work"
    targets="iPhone (iOS),macOS"
    art_direction=""
    ;;
  text-editor)
    category="Document, planning, or content system"
    product="A focused plain-text editor for drafting notes, organising documents, searching content, and exporting a finished file."
    reference="Obsidian for local-first text editing, document organisation, and search"
    targets="macOS,Windows"
    art_direction=""
    ;;
  mini-os)
    category="Operating-system or device utility"
    product="A simulated mini operating-system control centre that lets users inspect device status, adjust safe settings, and follow recovery guidance."
    reference="macOS Disk Utility for status presentation, guarded actions, and recovery-oriented workflows"
    targets="macOS,Windows"
    art_direction=""
    ;;
  file-processing-api)
    category="Service, API, or background system"
    product="An API and background service that accepts small data files, validates records, reports progress, and returns downloadable processing results."
    reference="Stripe for clear API contracts, reliable asynchronous processing, and operational visibility"
    targets="Backend API,Background workers / scheduled jobs,Admin or operations portal"
    art_direction=""
    ;;
  internal-helpdesk)
    category="Business / internal application"
    product="An internal helpdesk for support staff to triage requests, assign owners, record resolutions, and review operational queues."
    reference="Zendesk for ticket queues, assignment, statuses, and operational workflows"
    targets="Admin or operations portal"
    art_direction=""
    ;;
  *)
    echo "Unknown E2E scenario: $scenario" >&2
    echo "Choose one of: fantasy-quest, arcade-puzzle, football-trivia, todo-app, text-editor, mini-os, file-processing-api, internal-helpdesk." >&2
    exit 2
    ;;
esac

project_name="${E2E_PROJECT_NAME:-e2e-$scenario}"
initial_command=(
  "$supervisor_cmd" initial --non-interactive --force
  --project-name "$project_name" --category "$category"
  --product "$product" --reference "$reference"
)
[[ -n "$targets" ]] && initial_command+=(--targets "$targets")
[[ -n "$game_characteristics" ]] && initial_command+=(--game-characteristics "$game_characteristics")
[[ -n "$art_direction" ]] && initial_command+=(--art-direction "$art_direction")

echo "E2E scenario: $scenario ($category) · project: $project_name"
"${initial_command[@]}"

# This harness must be safe in a normal, dirty development worktree. The
# generated files remain available for inspection; no task commits or pushes.
"$root/supervisor/.venv/bin/python" -c "from pathlib import Path; from supervisor.manage import _set_env_values; _set_env_values(Path('projects/$project_name/.env'), {'SUPERVISOR_AUTO_COMMIT': 'false', 'SUPERVISOR_AUTO_PUSH': 'false'})"

"$supervisor_run_cmd" --project "$project_name"

project_root="projects/$project_name"
python3 - "$project_root" <<'PY'
import sys
from pathlib import Path
from supervisor.runbooks import load_task

root = Path(sys.argv[1])
assert (root / '.env').is_file(), 'missing project .env'
assert (root / '.state').is_dir(), 'missing project .state'
runbooks = sorted((root / 'runbooks').glob('R*.md'))
assert runbooks, 'expected at least one generated R-series runbook'
for path in runbooks:
    task = load_task(path)
    assert task.asset_impact in {'required', 'not_applicable'}
    if task.asset_impact == 'required':
        assert task.asset_ids, f'{path} needs stable asset_ids'
print(f'E2E PASS: {len(runbooks)} valid R-series runbooks in {root}')
PY

# A second invocation must use durable state rather than regenerating accepted work.
"$supervisor_run_cmd" --project "$project_name"
