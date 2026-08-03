# 04 — Experience contract

**Traceability:** This contract implements the original *matchday knowledge* challenge in [01-creative-direction.md](01-creative-direction.md) and the first-release systems `GAME-001`–`GAME-012` / journeys `J0`–`J5` in [02-game-design-bible.md](02-game-design-bible.md) and [02-feature-model.md](02-feature-model.md). There is no narrative content model: this is a non-fiction trivia puzzle, whose arc is invitation, confident calls, rising momentum, decisive prompt, then clear celebration or explanation. It must not introduce campaign, battle, characters, or a fictional world.

## Product promise and original language

The player enters a calm abstract broadcast studio, chooses a compact themed knowledge round, answers one card at a time, and leaves knowing what happened and what was saved. The visual vocabulary is **category fields**, **signal sweeps**, **stat blocks**, **pitch-line geometry**, and **celebration shapes**: original abstract objects rather than a stadium, fixture, presenter, club, competition, or broadcaster. Prompt hierarchy is always question → answer action → explanation → score/streak. Category colour supports scanning but a written category label and a distinct pattern do the semantic work.

Tone is precise, lively, adult, inclusive, and fact-first. Instructions use active plain language; correct feedback celebrates the decision, never the person; incorrect feedback explains without shaming. Questions, explanations, captions, error copy, and assets are independently authored. The Athletic and QuizUp establish only topic breadth and short-session outcomes: no marks, questions, wording, screen compositions, visual trade dress, audio, or interaction choreography may be reproduced.

## Information architecture and navigation

| Area / state | Purpose and primary actions | Navigation and recovery |
| --- | --- | --- |
| Home / local profile | Resume a confirmed paused run; begin `First Whistle`; choose a theme; open settings/help. | Home is the stable return target. Resume identifies the round and last confirmed boundary; a missing run simply omits Resume. |
| Round choice | Explain tutorial versus standard round, category, card count, timer mode, and availability. | Select starts only eligible validated content. An empty category says why and offers another eligible theme or Home. |
| Quiz / unresolved card | Show progress, question, format-specific answer control, optional pause, and accessible score/streak summary. | One card is actionable. Back/Pause opens a non-modal pause panel at a safe boundary; abandon requires confirmation. |
| Resolution / explanation | State correct/incorrect in text, icon, pattern, and optional cue; reveal canonical answer and concise explanation; continue only after state is clear. | Continue advances after a resolved snapshot boundary; no answer can be changed. |
| Results | Show answered/correct, score, best active-session streak, category, milestone/save status, then Replay, Choose theme, or Exit. | Reopening is read-only and never awards twice. |
| Settings / help | Text size, contrast, reduced motion, captions/descriptions, audio, input help, privacy/diagnostic choice, reset settings, and delete profile. | Available before or during a round; a changed setting takes effect immediately or at the next announced safe boundary. Return preserves the previous route. |
| Install/offline/update | Explain install readiness, cached-content state, download need, and a staged update. | Offline compatible content remains playable. Update applies only between rounds; decline/failed update retains the known-good package. |
| Recovery / error | Explain a write failure, corrupt draft, incompatible cache, or unexpected fault in plain language. | Offer only applicable Retry, Resume last confirmed state, Continue without saving, Discard draft, Return Home, or Reset cache after save protection. |

No first-release account, multiplayer, chat, ranking, purchase, live event, or remote sync route exists. A future connected feature requires a separate identity, reporting, moderation, consent, retention, outage, and safety flow; it must not be implied by this IA.

### State, privacy, and destructive-action rules

- A disabled Submit names its condition; a typed blank needs a separate explicit “Submit blank” choice.
- No eligible cards, unavailable first offline download, missing optional audio, unsupported gamepad, and unavailable language have explanatory fallback states, never a dead end or silent substitute.
- Failed saves keep the prior confirmed snapshot. Corrupt drafts offer the last confirmed snapshot or discard the draft; cache reset is never offered until save protection is reported.
- Abandon round, reset settings, and delete profile name their exact effects and offer Cancel as the initial safe action. Delete profile needs a final confirmation, removes local profile/settings/history/snapshots/recovery records/local diagnostics, and returns to first launch.
- Optional diagnostics and notifications are off until consent. Their panels state purpose, fields, retention/deletion, and any approved transport; denial never blocks play. P0 never requests names, contacts, location, ad/account IDs, payments, raw typed answers, question text, or save payloads.

## Interaction contract by surface

Semantic actions are `navigate`, `select`, `submit`, `back`, `pause`, `open-settings`, and `adjust-setting`. Every critical action has an equivalent on each available surface; presentation may adapt but rules/save semantics never do.

| Surface | Layout and input choreography | Required adaptation |
| --- | --- | --- |
| Web desktop / laptop | Centered reading column with persistent top progress; pointer hover reveals only nonessential help. | Keyboard works without pointer: `Tab`/`Shift+Tab` follow reading order, Enter/Space activates, arrows move within a radio/ordered group, Escape/Back pauses or closes a non-destructive panel. Browser back never silently abandons a round. |
| Web phone / PWA / Android / iPhone | Portrait-first single column; question before answers; sticky but non-obscuring progress/pause row. Landscape is a reflow, not a required orientation. | All primary targets are at least 44 × 44 CSS px (or platform equivalent), separated to prevent accidental answer selection. No hover dependency; respects system text scaling and safe areas. |
| Gamepad | Same single-focus sequence as keyboard; focus lands on page title or first meaningful action after every route/state change. | D-pad/left stick navigates; primary face button selects/submits; secondary backs/closes; Menu/Start pauses. Unsupported/disconnected gamepad is explained while touch/keyboard remain available. |
| Mouse / trackpad | Pointer targets match visible controls; hover only supplements labels/tooltips. | Click has an equivalent keyboard action; focus remains visible after a click. |
| Screen reader, switch, voice, assistive input | Native semantic controls are preferred over canvas-only controls; actions have stable accessible names. | Voice can invoke visible unique labels such as “Submit answer” and “Pause round”; it need not parse football answers as commands. Switch uses the same finite focus order. Status changes announce once without stealing focus. |

Remote-control/TV input is not a selected delivery target; it remains an approval item rather than implied P0 scope.

## Responsive visual behaviour and tokens

Use a portrait-first single-column core. At narrow widths, full-width answer controls stack. At tablet width, score/streak may sit beside the prompt only when reading measure and answer target size are preserved. At desktop width, cap the reading column; spare space is quiet studio texture, never a competing task. Reflow at browser zoom and system text enlargement; never truncate question, explanation, confirmation, or recovery copy.

Tokens are semantic and product-specific: `FT-SPACE-1..6`, `FT-TYPE-PROMPT`, `FT-TYPE-BODY`, `FT-TYPE-NUMERIC`, `FT-SURFACE-BASE`, `FT-SURFACE-CATEGORY-{world,domestic,club,records}`, `FT-STATE-{focus,correct,incorrect,warning}`, `FT-PATTERN-{field,grid,sweep}`, and `FT-MOTION-{none,brief,celebrate}`. Normal text meets 4.5:1 (3:1 only for large text); essential icons, focus indicators, and control boundaries meet 3:1. High contrast uses tested semantic tokens, not saturation alone.

Correct/incorrect combines a written result, icon, pattern/border, and optional audio. Focus is a high-contrast non-colour-only outline, never hidden behind sticky UI. Motion defaults to short non-flashing transitions; reduced motion replaces signal sweeps, card movement, and celebration bursts with immediate state changes. No animation flashes more than three times per second.

## Accessibility and content requirements

- Each route has one programmatic page title/heading and landmarks for header, main quiz, and complementary progress. Dialogs label their consequence, trap focus only while open, and restore focus to the invoker.
- Answer groups expose question text, format, selected state, position, and enabled/disabled reason. Score/streak labels are concise; progress exposes ordinal and total.
- Resolution uses a polite live region for outcome/score; blocking errors use assertive announcement only when action cannot continue. Captions/descriptions are visible on request and every cue has text. Decorative studio art is hidden from assistive tech.
- Text size persists and honours system scaling. Localisation externalises prompts, answers, explanations, categories, recovery/error strings, captions, and labels; a language is not selectable until aliases and factual review pass.
- Timer mode defaults off. If later enabled it states duration, has a non-timed alternative, offers extension/pause where applicable, and never prevents an explanation.

## Journey-to-presentation map and acceptance

| Journey | Location/screen state | Shared visual/audio IDs | Acceptance |
| --- | --- | --- | --- |
| J0 | Home, Settings, consent | `ASSET-SHL-001`, `ASSET-UI-001`, `AUDIO-SET-001` | Settings apply globally; consent denial remains playable; labels/focus order work. |
| J1 | First Whistle, prompt, resolution, results | `ASSET-QZ-001`, `ASSET-FBK-001..004`, `AUDIO-QZ-001..004` | Offline tutorial completes with readable non-colour feedback and confirmed save. |
| J2 | Theme choice, standard round, unavailable-theme empty state | `ASSET-QZ-002`, `AUDIO-QZ-001..003` | Eligible choice, clear empty state, replay/exit without social comparison. |
| J3 | Pause, save failure, recovery, delete confirmation | `ASSET-UI-003`, `AUDIO-SYS-002` | Prior confirmed state is protected; destructive choices are explicit/cancellable. |
| J4 | Editorial/release workflow, not player runtime | `ASSET-OPS-001` | Missing provenance or ambiguous answers block publish. |
| J5 | Download/update/error/recovery | `ASSET-SYS-001`, `AUDIO-SYS-001` | Safe-boundary update, offline fallback, retry/home, privacy-preserving diagnostic choice are clear. |

Before release, verify each row with keyboard, touch, screen reader, system text enlargement, high contrast, reduced motion, muted audio/captions, offline cached content, failed save, corrupt draft, and deletion. Final browser/OS/device/performance matrix remains an approval gate in `03-technical-contract.md`.
