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

validate_factory_handoff() {
  python3 "$root/scripts/runbookgen_validate.py" "$project_name" \
    --require-game-design-complete --require-r-series

  python3 - "projects/$project_name" <<'PY'
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
}

repair_factory_failure() {
  local attempt="$1"
  local evidence="$2"
  local repair_id
  repair_id="E2E$((9000 + attempt))"
  echo "E2E REPAIR $attempt · sending captured factory failure to Codex" >&2
  local -a repair_command=(
    env
    SUPERVISOR_AUTO_COMMIT=false
    SUPERVISOR_AUTO_PUSH=false
    "SUPERVISOR_DATABASE_PATH=/tmp/runbookgen-e2e-repair-${project_name}-${attempt}.sqlite3"
    'SUPERVISOR_TEST_COMMANDS=["git diff --check"]'
    "$supervisor_run_cmd"
    --task-id "$repair_id"
    --title "Repair runbook-generator factory E2E failure"
    --objective "The factory E2E for projects/$project_name stopped incomplete or failed its final assertion. Work in this repository using the terminal. Inspect the factory, Supervisor, and generated project evidence; fix the root cause rather than weakening the checks; then run the focused terminal validation that demonstrates the repair. Captured failure output follows:\n\n${evidence:0:12000}"
    --acceptance "The captured E2E failure has a concrete root-cause fix."
    --acceptance "Focused terminal validation for the fix passes."
    --acceptance "The factory can be retried without discarding accepted work."
  )

  # A repair is intentionally visible by default on a developer Mac.  This
  # makes its Codex work, terminal checks, and final result inspectable.  CI or
  # a headless session can explicitly opt out with this variable.
  if [[ "${RUNBOOKGEN_VISIBLE_REPAIR_TERMINAL:-true}" == "true" ]]; then
    "$root/supervisor/scripts/open-visible-terminal.sh" --cwd "$root" --wait -- "${repair_command[@]}"
  else
    "${repair_command[@]}"
  fi
}

# A factory task normally repairs its own terminal failure through Supervisor.
# This outer loop covers failures discovered only by the E2E harness itself,
# such as a completed collection with no R handoff. Keep it bounded so an
# ambiguous product decision cannot spend agents indefinitely.
max_repairs="${E2E_REPAIR_ATTEMPTS:-2}"
for ((attempt = 0; attempt <= max_repairs; attempt++)); do
  factory_output=""
  factory_status=0
  if factory_output="$("$supervisor_run_cmd" --project "$project_name" 2>&1)"; then
    :
  else
    factory_status=$?
  fi
  printf '%s\n' "$factory_output"

  validation_output=""
  validation_status=0
  if validation_output="$(validate_factory_handoff 2>&1)"; then
    :
  else
    validation_status=$?
  fi
  printf '%s\n' "$validation_output"

  if [[ "$factory_status" -eq 0 && "$validation_status" -eq 0 ]]; then
    break
  fi
  if [[ "$attempt" -ge "$max_repairs" ]]; then
    echo "E2E failed after $((max_repairs + 1)) factory attempts; repair evidence is above." >&2
    exit 1
  fi
  repair_factory_failure "$((attempt + 1))" "$factory_output

$validation_output"
done

# A second invocation must use durable state rather than regenerating accepted work.
"$supervisor_run_cmd" --project "$project_name"
