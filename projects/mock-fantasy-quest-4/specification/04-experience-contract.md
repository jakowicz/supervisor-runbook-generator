# 04 — Experience and accessibility contract

**Inputs:** [product brief](01-product-brief.md), [feature model](02-feature-model.md), and [technical, data, trust, and quality contract](03-technical-contract.md). This is the experience contract for the P0 offline campaign: one town, one dungeon, turn-based combat, inventory, quests, saves, settings, and a short ending. It specifies behaviour and presentation without choosing an engine, a library, exact art assets, or an unapproved connected service.

## Experience premise and originality boundary

The player arrives as a wayfinder in **Larkspur Reach**, a small hillside town whose old beacon has gone dark. A local request leads through the nearby **Glassroot Hollow** to relight it. This is a compact, hopeful mystery about attention, repair, and returning safely—not a borrowed world, cast, plot, place, or visual identity. The ending is a quiet return to the town with the beacon restored and the campaign marked complete.

The visual language is original: warm hand-painted fantasy with broad, readable silhouettes; worn clay, moss, lantern-gold, plum shadow, and rain-blue accents; gently textured scenery; and simple, high-contrast interface planes. Characters, creature designs, maps, names, dialogue, quest structure, UI composition, animation timing, sound, and gameplay choreography must be independently authored. The functional reference informs only the broad capability of a party-based, turn-based adventure. It must not inform trade dress, screen layouts, menus, copy, world-building, assets, or distinctive sequences.

## Information architecture and navigation

The shell has a persistent, semantic navigation model. The game view is the primary workspace; panels are temporary layers rather than separate unexplained destinations.

```text
Launch / title
├── New game → accessibility quick setup (skippable) → tutorial → town → dungeon → ending
├── Continue / Load → slot picker → restored safe boundary → game view
├── Settings → accessibility, controls, audio, display, language (when supplied)
├── Help & controls → input-specific action reference
├── Save data → load, delete-confirmation, recovery status
├── Privacy & diagnostics → local-data explanation, consent / clear actions
└── PWA status → install guidance, offline readiness, safe update state

Game view
├── objective / quest panel
├── inventory and party panels
├── pause menu → save, settings, help, return to title
└── contextual interaction / dialogue / combat layers
```

- The title exposes only available actions. With no valid save, `Continue` and `Load` are absent or disabled with the accompanying explanation; `New game` remains the primary action.
- `Escape`, a visible pause affordance, and the mapped gamepad pause action open pause at any safe playable state. Focus loss or tab hiding pauses the game and explains this only once per session.
- Every panel has a visible title, close control, and a known return target. Closing restores the prior selection and scroll position where feasible. Browser Back never silently discards progress: it closes a transient panel first; leaving the game prompts only when an unsaved, recoverable change would be lost.
- Modal layers are reserved for blocking choices: save deletion, settings reset, a new-game replacement of an existing active slot, and a recovery choice. They state consequence, affected slot/data, irreversible status, and a safe default (`Cancel`). No timed dialog expires.
- Navigation labels use player language: `Quest`, `Bag`, `Party`, `Save`, `Settings`, and `Help`. Icons always have adjacent text or an accessible name; an icon alone is never the only cue.

## Story, content, and feedback principles

Writing is concise, warm, and grounded. Dialogue advances in short, skimmable turns: speaker name, one thought or action, then a clear response/continue choice. Quest copy answers **what happened**, **what to do next**, and **where to go** without hiding required direction in decorative prose. The tutorial teaches one action at a time: move/interact, select a combat action and target, observe the result, then save. It never assumes prior genre knowledge.

Narrative presentation gives players control: advance, review the current exchange, and enable captions; it does not auto-advance essential text. A quest update is both spoken/written in the panel and visibly confirmed near the objective. Victory, gained item, blocked route, invalid action, save completion, update-ready, and recovery messages use a combination of short text, an icon or shape, optional audio/haptic feedback where the platform supports it, and a non-blocking visual change. Colour and sound are supplementary, never the sole signal.

Combat is an ordered decision loop: announce whose turn it is, offer legal actions, show required target selection, then resolve with an interruptible/reduced-motion-friendly result and return to the next decision. Illegal or unavailable choices explain why and preserve the current turn. Exploration interactions use an explicit prompt with the action name; locked routes name the missing condition rather than merely refusing movement.

## Layout, visual tokens, and responsive behaviour

The game scene retains its 2D world view while the interface reflows around it. Essential information is never permanently covered by a decorative frame, cut off by device notches, or dependent on hover.

| Token / rule | Contract |
| --- | --- |
| `--surface-base`, `--surface-raised` | Warm parchment/dark-plum interface planes. Body text and essential icons meet at least **4.5:1** contrast; large text (at least 24 CSS px regular or 18.66 CSS px bold) meets **3:1**. |
| `--text-primary`, `--text-muted` | Primary is used for all essential content. Muted text is never the only carrier of an instruction, state, or warning and meets 4.5:1 when conveying necessary text. |
| `--accent-action`, `--state-success/warning/danger` | Accent is paired with text and a distinct icon/shape. Focus does not rely on the action colour. Error and destructive states use wording plus iconography. |
| `--focus-ring` | A high-visibility 3 CSS-px minimum outline with at least 3:1 contrast against adjacent colours; never removed. It has clear offset from the focused control. |
| Typography | Sans-serif UI type with clear letterforms; text scaling is supported to 200% without clipping, overlap, horizontal page scrolling, or lost actions. Body/default dialogue begins at a readable base size; users may choose larger text and line spacing. |
| Spacing and targets | Minimum 44 by 44 CSS px target for touch-operable controls, with 8 CSS px separation where adjacent targets could be confused. Targets are not made smaller on compact screens. |
| Motion | Motion is brief, non-essential, and can be reduced. Respect `prefers-reduced-motion`; provide an in-game reduction setting that removes camera shake, parallax, flashes, auto-panning, and nonessential transitions. No essential timing depends on animation. |

| Viewport | Layout behaviour |
| --- | --- |
| Phone / narrow portrait | Full-width world view with safe-area insets. Objective is a compact expandable summary; action controls form a bottom reachable sheet. Inventory, quest, settings, and dialogue become full-screen panels with a sticky close/back control. Combat actions stack or use a single-column selection list; no critical control is below the browser chrome. |
| Tablet / medium | World stays primary with a side or bottom contextual panel. Combat has a clear action area and target area side-by-side when space allows; otherwise it uses the phone sequence. Panels never overlap the action prompt. |
| Desktop / wide | Centred game stage with persistent but collapsible objective/status rail. Inventory and quest can use a two-column inspection layout; combat keeps actions and party/enemy status simultaneously visible. Mouse hover may preview a definition but never supplies essential information. |

Rotation, resize, zoom, virtual keyboards, and PWA display-mode changes preserve the current game state and selection where practical. If reflow temporarily obscures the selected control, focus moves to the panel heading and a short status message announces the layout change. Full screen is optional and provides an obvious exit path.

## Input and interaction adaptation

All supported physical inputs invoke one semantic action vocabulary: move, inspect/interact, confirm, cancel/pause, open quest, open bag, open settings, navigate previous/next, and choose a legal combat action/target. A player can complete every core journey without pointer precision, dragging, multi-touch, rapid repetition, or a time limit.

| Surface / input | Required adaptation |
| --- | --- |
| Keyboard | Arrow keys and WASD move/navigate where appropriate; Tab and Shift+Tab move through UI controls in visual reading order; Enter/Space confirm; Escape cancels/closes/pause. Avoid keyboard traps; provide an early `Skip to game controls` link from the shell. Key repeat must not confirm a destructive choice or consume multiple turn actions. Control mappings are visible and remappable subject to the later-approved configuration depth; conflicts are explained before saving. |
| Mouse / trackpad | Click targets match the semantic controls; hover is optional enrichment only. Right-click is not required. The pointer never needs to trace tiny map details to perform a required interaction. |
| Touch | On-screen controls are reachable, labelled, and may be toggled in settings. Use tap-to-confirm and explicit target selection; do not require pinch, swipe-only navigation, double tap, drag, or long press. A touch action has the same feedback as its keyboard equivalent. |
| Gamepad | Feature-detect rather than promise a model. Show button glyphs only after detection and accompany them with action text. D-pad/left stick navigates; primary face button confirms; secondary face button cancels; menu button pauses; shoulder buttons may switch top-level panels when discoverable. A disconnected controller preserves state and presents keyboard/mouse/touch alternatives without blocking. |
| Remote / focus-only devices | These are not a selected delivery target. If a browser presents only directional/confirm/back focus input, the menus use the gamepad-style focus order and all core controls remain reachable; continuous exploration is not promised until a target/device decision is approved. |
| Voice and other assistive input | Voice command recognition is not collected, enabled, or required in P0. Controls expose standard semantic HTML roles, names, states, and operable buttons so browser voice control, switch control, eye tracking, and other assistive input can target visible actions by label. Canvas/world interactions have equivalent labelled UI prompts and action-list routes. |

## Accessibility policy

The release target is WCAG 2.2 AA for the public UI and the operable game controls, evaluated with automated checks and manual keyboard, screen-reader, zoom/reflow, touch, and reduced-motion review on the approved browser/device matrix. This is a product quality target; exact assistive-technology combinations remain a release approval gate rather than an invented compatibility claim.

- Use semantic landmarks for banner/title navigation, main game controls, complementary objective/status, and dialogs. Mark decorative art as hidden from assistive technology. Give the world canvas a concise labelled description and provide its essential current state through adjacent semantic status and action elements.
- Every interactive element has a unique accessible name that matches its visible label where one exists. Examples: `Open quest: Relight the Beacon`, `Use Moss Tonic on Rowan`, `Close inventory`, `Save slot 1`, and `Delete slot 1`.
- Dialogues announce speaker and text through a controlled, non-interrupting status mechanism; combat announces turn start, selected action/target, damage/healing, and victory/defeat without flooding announcements for decorative animation frames. Notifications are concise, deduplicated, and reviewable in the status/quest panel.
- Focus is visible at all times, enters a dialog at its heading or first safe action, remains contained only while that blocking dialog is open, and returns to its invoking control when closed. A newly opened non-modal panel receives focus on its heading. Error focus moves to an actionable summary, not an arbitrary visual element.
- Do not use flicker above three flashes per second. Provide captions/subtitles for all non-text audio that conveys story, instruction, combat state, or warning; identify speaker and relevant sound in concise text. Master audio, music, effects, caption visibility, text size, contrast, and motion settings are reachable before starting a new game and while paused.
- Required state has a text equivalent: party health uses values and state wording as well as bars; enemy intent uses a label/icon; map interaction, quest progression, and save status use text. Visual settings include a higher-contrast mode and non-colour state markers.
- Users can pause, slow, or disable nonessential movement and screen effects. No essential dialogue, battle selection, confirmation, error message, or recovery choice disappears by timeout.
- Settings save independently of campaign saves where storage permits. If persistence fails, keep the in-session choice, state that it will not persist, and preserve a usable default. Reset settings is confirmed and describes the affected preference categories.

## Empty, error, recovery, destructive, and privacy-sensitive states

| Situation | Experience requirement |
| --- | --- |
| Empty inventory / no quest / no save | State what is empty, why it may be empty, and the next useful action: e.g., `No items yet—explore the town and finish the first encounter.` No decorative blank panels. |
| Invalid action, locked exit, unavailable target | Keep the player’s state and turn intact; name the unmet requirement and return focus to the legal choices. Do not use a generic `Error` as the only explanation. |
| Storage failure, corrupt save, or interrupted save | Never claim a save completed until confirmed. Retain the last valid checkpoint; show retry, return-to-title, and fallback/new-game paths. Quarantined saves are explained as preserved but unusable; recovery text avoids blame. |
| Offline, install, cache, or update state | Explain whether the current cached version can play, whether an initial download is required, and that an update will wait for a save-safe title/menu boundary. Declining install or update does not block play on a valid cached/current release. |
| Fault / crash recovery | Present plain-language retry, return to title, and safe-recovery actions. Preserve confirmed progress. A diagnostic option is optional and clearly separate from recovery. |
| Delete a save | Require a confirmation dialog that names the slot, its progress/time where available, and that deletion is irreversible. Initial focus is `Cancel`; `Delete` is visually and semantically distinct and cannot be activated through a stale/repeated input. Only the selected local slot and associated recovery metadata are removed. |
| New game over an active slot / reset settings | Explain precisely what will change. New game must use a separate slot or obtain explicit confirmation before replacing a selected slot. Settings reset affects preferences only, not campaign state. |
| Diagnostics and local data | P0 sends no telemetry. Before any consent-gated local diagnostic record is created or exported, state purpose, included minimal fields, retention, deletion control, and that it does not affect play. `Clear diagnostic data` confirms the local-only effect. Never show save contents or dialogue in diagnostics UI. |

## PWA-specific experience

The web and installed PWA share the campaign, controls, accessibility settings, semantic UI, and local-save behaviour. Installation is an optional convenience: the title/PWA status area explains availability and has a non-modal fallback when the browser offers no install prompt. Offline status is visible but not alarming. An uncached first visit tells the player that the game cannot begin offline until its assets finish downloading; a known-good installed/cache version continues if an update check fails.

An update notice appears only at a safe boundary (title or paused menu after a confirmed save) and says whether reloading is needed. It offers `Update now` and `Later`; it never reloads during combat, a save write, a modal choice, or essential dialogue. Cache refresh messaging does not imply that save data was refreshed, deleted, or synchronised.

## Content and interaction review checklist

Before a content or UI change ships, review it against this contract: original provenance; clear next action and empty/error copy; keyboard, touch, mouse, gamepad, and semantic assistive-input operation; visible focus and accurate accessible names; contrast and non-colour cues; 44 CSS-px touch targets; 200% text/reflow; captions and reduced motion; safe save/update/recovery behaviour; destructive confirmation; and consent/minimisation for any privacy-sensitive interface.

## Open decisions retained for approval

- Exact content quantities, party size, localisation languages, full control-remapping depth, audio scope, and supported browser/device/assistive-technology matrix.
- The legal, age/parental, regional, and certification policies that may change content warnings or accessibility obligations.
- Account identity, remote sync, multiplayer, player safety/moderation, live operations, commerce, and analytics. These remain outside the offline P0 experience; no social, payment, reporting, account, or remote-data UI may be designed as committed functionality without approval.
