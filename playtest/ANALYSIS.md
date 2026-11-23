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
2. Run `rojo build` and `luau-analyze` locally (not possible in this environment) and fix anything they flag.
3. Watch for: do they find the bench lever on their own? Do they notice parry and guard break without the sign? Do they try `/e highfive`? Does a set win feel like a win? Does anyone go back to the dummy challenge?
4. The next day, without prompting, ask: "What happened in that game?" Compare their answers with the table above.
