# Simulated first session: what two friends remember

Two simulated 12-year-old best friends (Kai and Robin, `personas.md`) play the Roblox build for the first time,
three independent sessions per round. Separate zero-context agents then write the next-day lunch-table
conversation and record which moments came up. **This is an LLM simulation grounded in the code, not a real
playtest.** Treat it as a design review that predicts what kids would retell. The real-playtest checklist is
at the bottom.

Verdicts: **talked about** (mentioned in at least 2 of 3 runs, mostly positive), **complained** (mentioned in at least 2 of 3, mostly negative),
**forgotten** (happened, mentioned in at most 1 of 3). Cells show the verdict and the mention count.

| Moment | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| M01 spawn | complained (3/3) | forgotten (0/3) | complained (3/3) |
| M02 walk-run | forgotten (0/3) | forgotten (0/1) | forgotten (0/2) |
| M03 jump-fall | forgotten (0/2) | forgotten (0/1) | forgotten (0/1) |
| M04 crouch | forgotten (0/3) | talked about (3/3) | talked about (2/3) |
| M05 climb-truss | talked about (3/3) | talked about (3/3) | talked about (2/3) |
| M06 jump-off-truss | talked about (3/3) | talked about (3/3) | talked about (3/3) |
| M07 swim | talked about (2/3) | forgotten (1/3) | talked about (2/3) |
| M08 sit-bench | forgotten (0/3) | talked about (3/3) | talked about (3/3) |
| M10 punch-air | forgotten (0/3) | forgotten (0/2) | forgotten (0/3) |
| M11 punch-dummy | forgotten (0/3) | forgotten (0/3) | forgotten (0/2) |
| M12 combo | forgotten (1/3) | forgotten (0/3) | talked about (2/3) |
| M13 kick | forgotten (0/3) | talked about (3/3) | talked about (3/3) |
| M14 block | talked about (2/3) | talked about (3/3) | talked about (2/3) |
| M15 sword-equip | talked about (2/3) | forgotten (1/3) | forgotten (1/3) |
| M16 sword-slash | talked about (3/3) | talked about (2/3) | complained (3/3) |
| M17 kill-dummy | complained (3/3) | talked about (3/3) | forgotten (0/3) |
| M18 hit-friend | talked about (3/3) | forgotten (0/3) | talked about (2/3) |
| M19 kill-friend | talked about (3/3) | talked about (3/3) | talked about (3/3) |
| M20 friend-blocks | complained (3/3) | forgotten (1/3) | forgotten (1/3) |
| M30 emote-wave | forgotten (0/3) | forgotten (1/1) | forgotten (0/3) |
| M31 emote-dance | talked about (3/3) | forgotten (1/3) | talked about (2/3) |
| M32 emote-cheer / point / laugh / clap / salute | forgotten (1/3) | talked about (2/3) | forgotten (1/1) |
| M33 emote-unknown | forgotten (1/3) | forgotten (0/3) | forgotten (0/3) |
| M34 emote-on-move | forgotten (1/3) | forgotten (0/2) | forgotten (0/2) |
| M35 high-five | n/a | talked about (3/3) | talked about (3/3) |
| M40 dummy-idle | talked about (2/3) | forgotten (0/3) | forgotten (0/3) |
| M41 explore-edges | complained (3/3) | forgotten (1/3) | talked about (2/3) |
| M42 goals | complained (3/3) | complained (3/3) | complained (3/3) |

| | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| Would play again | maybe, no, no | maybe, maybe, maybe | maybe, maybe, maybe |

## Pitches to Sam, the friend who hasn't played

- Round 1, run 1: "It's a grey parking lot where you find a sword by mashing keys, kill your friend so they do this hilarious roll-over death, and jump off a tower flapping your arms, but it's silent and there's nothing else to do."
- Round 1, run 2: "It's a grey test map where the sword looks sick and you can dance off a tower, but there's no actual game and nothing keeps score."
- Round 1, run 3: "It's not a game, it's a test place on a baseplate: the sword fights look good and you take a nap when you die, but there's no sound, no kill counter and nothing to do."
- Round 2, run 1: "It's a grey floor where you sword-fight your friend, but there's a bench that launches you into space and into a pool."
- Round 2, run 2: "It's a sword-fighting game where it says you slashed your friend 'into a nap', and there's a bench that launches you into a pool, but you run out of stuff in twenty minutes."
- Round 2, run 3: "It's a fighting game on a grey floor where the corner of the screen snitches on everything you do, and there's a bench that launches you into the sky, but you've done it all in twenty minutes."
- Round 3, run 1: "It's a grey baseplate but you pull a lever and yeet your friend off a bench into a pool, and the feed roasts whoever loses."
- Round 3, run 2: "It's a mid grey fighting game, but there's a bench that cannons you into a pool and the game roasts you in the corner when you get left hanging on a high five."
- Round 3, run 3: "It's a baseplate with really good fighting animations and a bench that launches you to space, but it's only twenty minutes of game."

## What changed between rounds

| Round | Build changes (each driven by the previous round's recall) |
|---|---|
| 1 | Baseline: the animation pack and test arena. No score, feedback or goals. |
| 2 | KO counter, kill feed in the voice of the death the kids loved ("Kai kicked Robin into a nap"), rivalry board, records (climb race, splash, dummy challenge), hit feedback (contact flash, sound, numbers, hit-stop, shake), kick and finisher knockback, block clang plus parry, crouch sneak attack, launch bench, splash scaled to fall height, superhero landing (new clip), two-player high five (new clip, plus "left hanging"), dance sync, taunts after a KO, emote hints, spawn shield. 20 code-review fixes. |
| 3 | First-to-5 **sets** with a win callout and automatic cheer, varied bench launches (so the splash record can be beaten), **dunks** in the feed, combo-finisher **guard break**. 5 code-review fixes. |
| After 3 (not re-simulated) | Splash clamp raised from 60 to 80 (the round-3 sims hit the 60 cap), kick works with the sword out, hits on a shielded player say SHIELDED, failed emotes say why, signs moved in front of the spawn, taunt window 4 s to 8 s. |

## Results against the bar

**Fixed: forgotten or complained in round 1, now talked about and holding:**
- crouch sneak attack (M04)
- bench launch (M08, the loudest moment in every round-2 and round-3 run)
- kick (M13)
- combo (M12, via guard break)

**New moments that landed:** the high five, including being "left hanging" (M35, 3/3 in both rounds), and set wins (inside M19).

**Steady favourites:** jumping off the tower, now with the superhero landing (M06); KOs with the "nap" feed (M19); the climb race (M05); block and parry (M14).

**Below the bar when the cap was reached:**
- **M42 "nothing to unlock" is complained about in every round.** The kids' consistent ask is progression: a shop, unlocks, a second map, more weapons, ranked. That is outside the scope chosen for this task ("light goals, no full game mode"), and it's the main reason "would play again" stayed at maybe ×3 instead of yes. It is the clearest next step.
- **M16 sword: a new complaint in round 3.** "The sword always wins, so it's whoever clicks first", and set 2 felt like set 1. Guard break helped the combo, but the sword needs balance (wind-up, stamina or a block counter) or more weapons.
- **M17 dummy challenge:** talked about in round 2, forgotten in round 3 ("a record with nobody watching"). Solo goals don't stick for a social pair. It could become a 2-player race on two dummies.
- **M31 dance and M07 pool** come and go. Both lack sound and music. The pool now matters as the bench target and for dunks, but swimming itself is "just blue".
- **M01 spawn** was complained about again in round 3, because the signs sat behind the spawn and shielded hits gave no feedback. Both were fixed after round 3 and are not yet re-simulated.
- **Plumbing** never gets retold, by design: walking, plain jumps, punching air, cancelling an emote (M02, M03, M10, M34).

**Play time:** about 16 min (round 1), then 19-22 min (round 2), then 19-22 min (round 3). Every run still ends with "we did everything".

## How the simulation was kept honest
- Session agents saw only the inventory (`inventory.md`, archived per round) and the code, never earlier rounds. Next-day agents saw only one session log.
- Session agents reported inventory/code mismatches; each one was fixed in the inventory or the code. One stale line in round 2 run 1 (dummy kills counting as KOs) was corrected with a visible note before its recall ran.
- These are still LLM predictions of kid behaviour, from 9 sessions with the same two personas. They are good at spotting "this has no feedback / no stakes / no story" and weak at real skill, frustration curves and novelty fading over days.

## Real-playtest checklist (two actual friends, about 20 minutes, then ask them the next day)
1. Publish the 27 clips and fill `roblox/src/shared/AnimationIds.luau`. In Studio, temporary KeyframeSequence IDs only work on the machine that made them, so two-player tests need published IDs.
2. ~~Run `rojo build` and `luau-analyze` locally and fix anything they flag.~~ Done on 2026-11-23: `rojo build`, luau-lsp (strict, Roblox types) and selene are clean, and `roblox/test/run_tests.py` plays the build in a real Roblox Studio, solo and with 2 clients (results in `roblox/GUIA.md` section 9). Fixed along the way: a Rojo-built place had no Terrain (no pool water) and used the retired legacy chat; combat and crouch input now go through ContextActionService (touch buttons and gamepad); server fall-height checks for splashes and landings tolerated replication lag badly; a hard bench launch could reach the pool floor before swimming started and lose the splash. Last run: solo 64/64, 2 clients 27/27, 0 script errors.
3. Watch for: do they find the bench lever on their own? Do they notice parry and guard break without the sign? Do they try `/e highfive`? Does a set win feel like a win? Does anyone go back to the dummy challenge?
4. The next day, without prompting, ask: "What happened in that game?" Compare their answers with the table above.

