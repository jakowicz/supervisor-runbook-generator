# 04 — Asset direction

All asset groups use the original abstract broadcast-studio direction established
in `01-creative-direction.md`; they must not reproduce clubs, competitions,
broadcasters, The Athletic, QuizUp, kit designs, screenshots, or layouts.

Asset quantities, file formats, and final delivery budgets remain pending target
and packaging decisions. Each asset requires provenance and human creative
review before production use.

## Original-asset contract

The asset language is the same original *matchday knowledge* studio described
in `01-creative-direction.md` and `04-experience-contract.md`: category fields,
pitch-line geometry, stat blocks, signal sweeps, and celebration shapes. It
must not become a stadium, club, competition, broadcaster, player, kit, crest,
or reference-product trade dress. This non-fiction trivia release has no
fictional characters, locations, dialogue portraits, maps, or gameplay worlds.

IDs use `ASSET-<FAMILY>-<NNN>` and are immutable once a package references
them. A variant is recorded separately as state and size (for example, the
correct 2x variant of `ASSET-FBK-001`); locale is a manifest field, not baked into a
universal visual. The asset manifest records ID, version, source/checksum,
owner, licence/provenance, alt-text/meaning, variants, and review status.

Every release asset is created for this project or has documented rights. Do
not trace, scrape, prompt for, or modify a reference screenshot, mark, kit,
photo, or distinctive layout. Generated output retains prompt/model/version
and gets human originality review; third-party material needs licence and
attribution review. Uncertain provenance, embedded unlocalisable essential
text, missing alt/meaning treatment, or failed contrast/state review rejects
the asset. Decorative absence may fall back gracefully; required UI/state
assets reject a release.

## Families, variants, and acceptance

| Stable ID / priority | Purpose and screens | Required variants | Accessibility / acceptance |
| --- | --- | --- | --- |
| `ASSET-SHL-001` / P0 | App mark and quiet studio background: Home, install, results. | light/dark/high-contrast; phone/tablet/desktop crops; static. | Mark has an accessible name; background is decorative and preserves text/control contrast and safe areas. |
| `ASSET-QZ-001` / P0 | Reusable prompt-card field: First Whistle and standard question. | four category tokens; narrow/wide; no-text base. | Texture has no semantic meaning; prompt remains live scalable text. |
| `ASSET-QZ-002` / P0 | Category/round tile: choice and unavailable theme. | world/domestic/club/records; available/unavailable/selected/focus. | Label plus pattern distinguishes category; unavailable has explicit text and 3:1 boundaries. |
| `ASSET-UI-001` / P0 | Icons for pause, settings, resume, back, audio, captions, install. | default/focus/disabled/high-contrast; vector/1x/2x. | Icons supplement labels or have exact accessible names; non-colour focus and 44 × 44 CSS px target. |
| `ASSET-UI-003` / P0 | Pause, confirmation, recovery-panel framing. | normal/high-contrast/reduced-motion; modal/non-modal. | No essential text baked in; frame cannot cover focused action. |
| `ASSET-FBK-001` / P0 | Correct motif: rising signal/check and score increment. | correct/static/reduced-motion/high-contrast. | Written “Correct”, answer, and icon/pattern remain if art/motion/audio is absent. |
| `ASSET-FBK-002` / P0 | Incorrect motif: calm correction marker/explanation lead-in. | incorrect/static/reduced-motion/high-contrast. | Never punitive; written outcome/explanation are primary. |
| `ASSET-FBK-003` / P0 | Streak stat block/celebration shape. | streak-3/streak-4-plus/static/reduced-motion. | Score/streak is text; no flash above three per second. |
| `ASSET-FBK-004` / P0 | Completion/result celebration shape. | complete/replay/static/reduced-motion/high-contrast. | Results remain understandable without it; it cannot cover actions. |
| `ASSET-SYS-001` / P0 | Offline, update, cached-package, and error symbols. | ready/offline/downloading/failed/recovery. | Icon, text, and pattern pair; semantic UI announces errors. |
| `ASSET-OPS-001` / P1 | Internal editorial provenance/validation glyphs; J4 only. | draft/reviewed/blocked/published/withdrawn. | Text status is mandatory; icons cannot grant publication eligibility. |
| `ASSET-MKT-001` / P1 | Store/PWA listing imagery from studio system. | platform ratios; accessible preview copy; no-text master. | Shows actual capabilities, original art, approved alt copy; not needed to play. |

P0 sequence is shell → prompt/answer clarity → feedback/recovery → responsive
variants. No environment tiles, characters, portraits, item icons, effects
library, world map, or unrelated game-art family is in scope. For every ID,
review at 200% zoom, phone portrait, tablet, desktop, high contrast, reduced
motion, and with images disabled; verify mapping, non-colour state, label/alt,
safe crop, crispness, provenance/checksum, and no essential text burned into
reusable art. Final formats, byte budgets, and store specs await target approval.
