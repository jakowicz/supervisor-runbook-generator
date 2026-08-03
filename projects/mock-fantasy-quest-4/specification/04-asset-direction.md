# 04A — Original visual asset direction

This canonical P0 visual brief supplements the experience contract. It uses an original warm hand-painted fantasy style: readable silhouettes, worn clay and moss, lantern-gold highlights, plum shadows, rain-blue accents, restrained texture, and high-contrast semantic UI planes. It must not copy a reference game's characters, maps, sprites, UI, visual composition, or animation.

## Required P0 families

| Family ID | Purpose and required variants |
| --- | --- |
| `ASSET-ENV-TOWN` | Original hillside town: ground, boundaries, beacon states, interactables, readable daylight variants. |
| `ASSET-ENV-DUNGEON` | Original Glassroot Hollow: floor/wall/exit language, collision markers, safe/locked/cleared states. |
| `ASSET-CHAR-PARTY` | Original party silhouettes with idle, walk, battle-ready, and readable status states. |
| `ASSET-CHAR-NPC` and `ASSET-ENEMY-HOLLOW` | NPC dialogue/avatar treatment plus a small original enemy roster with intent/status/defeated states. |
| `ASSET-ITEM-INVENTORY` and `ASSET-UI-GAMEPLAY` | Labelled items and semantic UI icons/states for title, dialogue, quest, combat, save, settings, errors, and focus. |
| `ASSET-FX-FEEDBACK` and `ASSET-PWA-IDENTITY` | Reduced-motion-safe optional feedback plus original PWA icons/manifest imagery. |

## Provenance and accessibility

Every final asset receives a stable individual `ASSET-*` ID, creator/source record, originality/licence disposition, source/exported variants, and an owning R contract. Essential meaning must have a text, accessible-name, or non-colour equivalent. Asset tasks own content/provenance; PWA delivery owns hashing and caching. A family is complete only when original provenance, variants, responsive readability, and accessibility are verified.
