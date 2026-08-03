# 04B — Original audio direction and cue map

This canonical P0 audio brief requires original warm, lightly hand-played fantasy instrumentation with clear loops and modest dynamics. It must not reuse, imitate, sample, or reproduce recognisable melodies, arrangements, or sound identity from a reference game. Music, effects, and feedback are independently adjustable; non-text meaningful audio has captions/text equivalents and audio failure never blocks play.

| Cue ID | Trigger | Loop / duration |
| --- | --- | --- |
| `AUDIO-MENU-LOOP` | Title, pause, and safe settings surfaces. | Seamless 30-second loop. |
| `AUDIO-TOWN-LOOP` | Larkspur Reach exploration. | Seamless 45-second loop. |
| `AUDIO-DUNGEON-LOOP` | Glassroot Hollow exploration. | Seamless 45-second loop. |
| `AUDIO-BATTLE-LOOP` | Active turn-based combat. | Seamless 30-second loop. |
| `AUDIO-VICTORY-STING` | Encounter/quest success. | One-shot, 2–4 seconds. |
| `AUDIO-UI-FEEDBACK` | Focus, selection, unavailable action, confirmation. | One-shot, under 1 second. |
| `AUDIO-SAVE-FEEDBACK` and `AUDIO-QUEST-FEEDBACK` | Save/recovery and objective/reward feedback. | One-shot, under 2 seconds. |
| `AUDIO-ENDING-LOOP` | Beacon-restored ending. | Seamless 30-second loop. |

Each cue must be allocated to an audio-required `IMP-*` and R contract with a stable `audio_id`, brief, duration, loop policy, trigger, mix category, caption/text equivalent, and originality review. Local generation still needs cue-level review for loop seams, clipping, trigger correctness, accessibility, and no recognisable reference melody.
