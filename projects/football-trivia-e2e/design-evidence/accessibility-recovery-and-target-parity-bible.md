# Accessibility, recovery, and target parity bible

## Purpose and non-negotiable invariants

This is the accepted design evidence for `GAME-009`–`GAME-012` and
`GPI-012`–`GPI-015`. It governs the shared first-release game on responsive
web, PWA, Android, and iOS. It does not approve an account, remote sync,
target-exclusive content, a target-exclusive ruleset, or a target delivery
matrix.

Every target consumes the same published question revision, adjudication rule,
score-event ledger, local-profile schema, confirmed-snapshot format, and
result/milestone idempotency rule. An adapter may translate input, layout,
installation, permission wording, or cache handling; it must not transform an
answer, scoring outcome, round seed, content eligibility decision, or confirmed
save. A target that cannot read a supported confirmed snapshot must preserve it
and enter recovery; it must never replace it with an empty profile.

Essential meaning is always exposed in plain visible text and semantic state.
Audio, colour, iconography, vibration, and animation may reinforce that meaning
but are never its sole carrier. The normal round has no time limit; optional
timer mode remains explicitly enabled and its availability does not alter the
following equivalence requirements.

## GPI-012 — profile, settings, and four input mappings

First launch creates a local profile without sign-in and presents **Start First
Whistle** and **Settings** as plain-language controls. Optional notification and
diagnostic permission denial leaves the same tutorial, settings, saving, and
return paths available. Settings include text-size, high-contrast presentation,
reduced motion, cue volume/mute, captions/descriptions, and input help.

| Shared action | Touch | Pointer | Keyboard | Gamepad |
| --- | --- | --- | --- | --- |
| Navigate / choose a control | Tap its labelled target; swipe only scrolls, never chooses. | Click its labelled target; wheel only scrolls. | Tab / Shift+Tab moves focus; arrow keys move within an answer group or ordered pair. | D-pad or left stick moves focus; no hover-only state is required. |
| Select an answer / reorder | Tap option; drag is optional and has visible move up/down alternatives. | Click option; drag is optional and has visible move up/down alternatives. | Space or Enter selects; ordered pair uses documented arrow-key move commands. | South button selects; ordered pair exposes labelled move commands using D-pad. |
| Confirm / continue | Tap **Submit**, **Continue**, or the named recovery action. | Click the same labelled control. | Enter or Space activates the focused named control. | South button activates the focused named control. |
| Back / pause / open help | Tap visible **Back**, **Pause**, or **Help**; system back is an equivalent where available. | Click the visible named control. | Escape returns/backtracks where safe; P pauses; both are documented and focus remains visible. | East button returns/backtracks where safe; Menu/Start pauses; both are documented. |

No action depends on a gesture, hover, pointer precision, or platform system
button alone. Back never discards an unresolved answer, a draft, or local data:
it reaches the existing pause, confirmation, or recovery path. Focus order is
prompt → instructions → answer controls → submit → explanation/secondary
actions, with a persistent visible focus indicator; feedback moves focus to its
heading once and does not steal it for animation.

## Accessible feedback equivalents

The following table is the release copy and presentation contract. Screen-reader
announcement is the stated text once per state change; captions/descriptions
show the same essential message. Contrast mode preserves the text and semantic
state rather than replacing it with a colour-only palette.

| Meaning | Required visible and semantic text | Non-colour equivalent | Audio/caption equivalent | Reduced-motion path |
| --- | --- | --- | --- | --- |
| Category / question context | Category name and question number (for example, “World tournament history — Question 3 of 10”). | Named category plus a distinct pattern/label; never colour alone. | No cue is required; any entry cue caption repeats the category/context. | Static panel and label; no sweep required. |
| Selected, unselected, and disabled answer | “Selected: [answer]”, “Not selected”, or “Unavailable until [condition]”. | Border, check/selection icon with accessible name, and text state. | No cue is required; any selection cue is captioned “Answer selected”. | Static state change. |
| Correct, incorrect, blank, or enabled-timer timeout | Outcome name, points, streak result, canonical answer/explanation, and next action. | Labelled success/error/empty/time icon or pattern, not green/red alone. | Caption names the same outcome and score/streak information; mute changes no meaning. | Static feedback with no forced celebration, shake, flash, or countdown motion. |
| Streak / score update | “Score: N. Streak: N.” and, when applicable, bonus/cap text. | Labelled streak marker and numeral; not a colour, pulse, or sound alone. | Caption names points, streak, bonus, or cap. | Static score/streak marker. |
| Pause, saved, or recovery condition | State heading, what is retained, any risk, and named actions. | Icon/pattern is supplementary to the heading and action labels. | Caption/description repeats heading and named actions; no cue is required. | No auto-moving modal or animated warning. |
| Offline, update, unavailable content, or unexpected error | Plain-language notice naming availability, retained progress, and next action. | Text heading and icon/pattern; status is not conveyed through network colour alone. | If a cue plays, caption repeats the notice; mute changes no path. | Static notice; no looping spinner as the only status. |

All minimum target contrast, text scaling, semantic-label, and touch-target
requirements are subject to the selected OS/browser matrix. Until that matrix is
approved, certification records the actual settings and assistive technology
used rather than claiming a numeric platform conformance level.

## GPI-013 — recovery states and fault evidence

`SaveSnapshot` means an immutable confirmed snapshot. A draft is never a
confirmed save. At tutorial completion, each resolved-question boundary,
explicit pause, and completed result, the system attempts to write a new
confirmed snapshot without mutating the previous one.

| Recovery state | Entry condition | Required notice and actions | Preservation invariant |
| --- | --- | --- | --- |
| `write_failed` | A confirmed-snapshot write fails. | “Progress could not be saved. Your last confirmed progress is safe.” Offer **Retry** and **Continue without saving**. | Retain and make recoverable the previous confirmed snapshot; do not imply that the current unresolved state is saved. |
| `interrupted_resume` | App/browser/OS ends or backgrounds after a prior confirmed boundary. | “Continue your saved round?” Offer **Resume confirmed round** and **Return home**. | Restore the exact confirmed content revision, position, score ledger, and unresolved state; interruption creates no blank, timeout, abandon, or duplicate completion event. |
| `draft_recovery` | Draft is corrupt, incomplete, or incompatible while a confirmed snapshot exists. | “A recent in-progress change could not be recovered. Your confirmed progress is safe.” Offer **Resume confirmed progress**, **Discard draft**, and **Return home**. | Keep the confirmed snapshot until the player explicitly deletes local data; never silently overwrite it with the draft or a new profile. |
| `delete_local_data` | Player requests local-data deletion. | Confirmation names that local profile, history, results, and snapshots will be removed and cannot be resumed. Offer **Delete local data** and **Cancel**. | Only confirmed deletion clears those local records and returns to first launch. Cancel changes nothing; remote state is not implied. |

Fault-injection evidence must cover: failed write at a resolved boundary;
failed pause write; termination after confirmed pause; termination after a
resolved attempt; corrupt draft with a valid snapshot; incompatible draft with a
valid snapshot; retry succeeding after `write_failed`; and cancellation versus
confirmation of local deletion. Each fixture asserts unchanged shared rules,
no silent loss of confirmed progress, and no duplicated result/milestone.

## GPI-014 — offline, update, and error notices

The installed published content batch and current confirmed snapshot support a
basic session offline. No notice may block a locally available tutorial or
round merely because a network, optional permission, or diagnostic endpoint is
unavailable.

| Notice ID | Trigger | Player-facing notice | Required handling |
| --- | --- | --- | --- |
| `OFFLINE-CACHED` | Network is unavailable and required installed content is present. | “You’re offline. Installed questions and saved progress are available.” | Start/resume remains available; suppress live-refresh expectation. |
| `OFFLINE-CONTENT-UNAVAILABLE` | Requested content is not installed and cannot be fetched. | “This question set is not available offline. Try again when connected or choose an installed round.” | Preserve current confirmed save; offer installed content or return home. |
| `UPDATE-STAGED` | A compatible content version is available during a round. | “An update is ready and will be used after this round.” | Freeze the active round’s content revision and rules; apply only between rounds. |
| `CACHE-INCOMPATIBLE` | Cache cannot support the pending content version. | “An update needs a cache refresh. Your confirmed progress will be kept.” | Preserve/export the confirmed snapshot before reset; provide **Refresh cache** and **Return home**. |
| `UNEXPECTED-ERROR` | A non-recoverable unexpected operation error occurs. | “Something went wrong. Your confirmed progress is safe.” | Offer **Retry** and **Return home**; optional minimised diagnostic consent is separate and denial changes no recovery route. |

Six release fixtures are required: offline launch of First Whistle with cached
assets; offline resume from a confirmed snapshot; unavailable non-installed
content; compatible update arriving mid-round; incompatible-cache refresh with
confirmed-save restoration; and unexpected error with diagnostic permission
denied. Each verifies the exact notice, named action, preserved snapshot, and
unchanged adjudication/score semantics.

## GPI-015 — target parity and certification matrix

The matrix states first-release parity requirements, not approval of a specific
device, browser, orientation, performance budget, packaging route, store
submission, crash provider, privacy declaration, or language set. Those remain
human approval gates. “Required” means a candidate target must demonstrate the
item before it can be certified in the eventual selected matrix.

| Capability / certification evidence | Responsive web | PWA | Android phone | iPhone (iOS) |
| --- | --- | --- | --- | --- |
| Shared content, answer, score, save, recovery, result, and milestone semantics | Required; no web rule branch. | Required; no PWA rule branch. | Required; no Android rule branch. | Required; no iOS rule branch. |
| Input and focus evidence | Keyboard, pointer, touch, and gamepad maps; responsive visible focus. | Browser/device-supported maps plus install-surface focus evidence. | Touch map and external keyboard where OS/device offers it; visible focus for non-touch navigation. | Touch map and external keyboard where OS/device offers it; visible focus for non-touch navigation. |
| Accessible feedback evidence | Text scale, contrast, captions/descriptions, non-colour states, reduced motion, semantic labels. | Same shared feedback contract before/after install and offline. | Same shared feedback contract using selected OS accessibility settings. | Same shared feedback contract using selected OS accessibility settings. |
| Offline/update evidence | Cached installed content/snapshot and notices where web delivery supports them. | Install, offline cache, staged update, and incompatible-cache recovery notices. | Packaged installed content, offline snapshot, staged update/recovery notices. | Packaged installed content, offline snapshot, staged update/recovery notices. |
| Form-factor adaptation | Responsive phone, tablet, and desktop layout; no hidden critical control. | Responsive installed layout; no PWA-only content/mode. | Sufficient touch targets; orientation only after approval. | Sufficient touch targets; orientation only after approval. |
| Certification record | Chosen browser/OS/device, input methods, assistive-tech/settings evidence, fixture IDs, defects, and sign-off. | Above plus install/offline/update evidence. | Chosen device/OS, packaging/store/privacy evidence, battery/thermal/size budget evidence, and sign-off. | Chosen device/OS, packaging/store/privacy evidence, battery/thermal/size budget evidence, and sign-off. |

Certification is blocked, rather than waived, until the target matrix and its
approval gates are selected. A failure on any target is resolved by fixing the
shared core or its adapter; it cannot be resolved by altering a question,
answer rule, score rule, save schema, or recovery guarantee for that target.

## Release evidence checklist

- Record one successful keyboard-and-touch traversal of every critical action,
  plus the gamepad equivalent on supported web/browser candidates.
- Verify each feedback-table meaning with cue volume muted, high contrast,
  enlarged text, captions/descriptions enabled, and reduced motion enabled.
- Execute all eight GPI-013 fault fixtures and six GPI-014 offline/update/error
  fixtures against each selected target’s applicable capabilities.
- Compare serialized confirmed snapshots and resulting score/milestone records
  across targets for the same round seed and input sequence.
- Retain the selected target/device/browser/OS evidence and approval record;
  no unselected target is represented as certified.
