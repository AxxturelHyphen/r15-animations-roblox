# Cook ledger: memorable first session

Started: 2026-11-23 (UTC), simulation round 1 already running
Time: floor none | cap 3 simulation rounds
Bar: forgotten to talked about (at least 2 of 3 mentions, plus detail or again at least once) | no regressions | would_play_again "yes" in at least 2 of 3
Calibration offset: none (no user estimate yet)
Usage: about 20% per hour, never 100%
Gate: report approved [no] | final [report written, playtest/REPORT.md]
Best so far: round 3 build + post-round polish (commit after 'Polish after round 3')

## Decisions
- 2026-11-23 No questions after intake: the user said "don't ask me anything", and the plan questions already set scope, animation policy and personas.
- 2026-11-23 Recall critics are separate zero-context agents that see only one session log, because Cook requires fresh-context critics and it stops the inventory from leaking into memory.
- 2026-11-23 Effects follow the slop ban: functional impact or contact feedback only, no decorative particles or shockwave rings.
- 2026-11-23 Sounds come only from the built-in rbxasset sounds: no external asset IDs, and nothing to license.

- 2026-11-23 M02 walk/run, M10 punch-air and M34 emote-cancel are plumbing: no kid retells walking. Bar for them: never complained about. They get small polish only. Logged so the bar isn't silently lowered.
- 2026-11-23 "Complained about" counts as not yet worth talking about, so M01, M17, M20, M41 and M42 are in scope too.

## User feedback inbox
- 2026-11-23 "simulate two best friends playing your roblox game for the first time ... improve the forgettable ones until they're worth talking about" | rounds 1-3 | open
- 2026-11-23 "Use leonxlnx/cook skill and taste-skill ... Install it urself don't ask me anything" | installed to ~/.claude/skills (cook, design-taste-frontend) | done

---

## Round 01 (baseline)

Focus: measure the current build. No changes.
Sessions: 3 (Robin first, Kai first, both together). They played 16:40, 15:40 and 16:15, and all three runs left for another game.
Highs reported by the session agents: dying and rolling onto your back (M19), self-invented sword 1v1 stakes (M18/M19), jumping off the truss together, the dance-off-the-edge (M06, M31).
Lows: the empty baseplate and no goal (M41/M42), a dummy kill that pays out nothing (M17), hitting a blocking friend with no feedback (M20).
Recall (3 zero-context next-day critics, eyeballed; counted by `playtest/aggregate.py`):
- Talked about (positive): M05 climb, M06 jump off truss, M07 pool, M14 block, M15/M16 sword, M18/M19 PvP and the death "nap", M31 dance, M40 dummy.
- Complained about (memorable for the wrong reason): M01 spawn camping/no hint, M17 the dummy pays nothing, M20 block reads as lag, M41 empty edges, M42 no goal or score.
- Forgotten: M02 walk/run, M03 jump, M04 crouch, M08 bench, M10 punch-air, M11 punch-dummy, M12 combo, M13 kick, M30 wave, M32 emotes, M33 unknown emote, M34 emote cancel.
- Would play again: maybe / no / no. The pitch to Sam: "a grey test map ... no actual game and nothing keeps score."

Stop check: bar [no] | cap [round 1 of 3] -> next round
Next focus: score and stakes first (the most repeated complaint, M42), then the forgotten combat and social moments.

---

## Round 02 (build)

Focus: the complaint and forgotten lists from round 1. One system per cause, the smallest change that gives each moment a story:
- Stakes (M42, M17, M18/M19 score argument): leaderstats (KOs, best combo, climb time, splash, dummy challenge), head-to-head rivalry board, kill feed in the voice of the loved death ("Kai sent Robin to nap").
- Hits that land (M11, M12, M13, M10): impact flash at the contact point, built-in hit sounds, damage numbers, hit-stop, a visible dummy health bar; the combo finisher and the kick knock the target back (kick someone off the tower or into the pool).
- Block (M20): clang, spark and "BLOCKED" for the attacker; a parry within 0.25 s of raising the guard staggers the attacker.
- Crouch (M04): sneak attack from behind while crouched does double damage, with a "SNEAK ATTACK" callout.
- Bench (M08): a launch lever on the bench aimed at the pool; a friend fires it with a prompt.
- Pool (M07): a cannonball splash scaled to fall height, plus a biggest-splash record.
- Jump (M03): a heavy landing after a big fall gets a superhero-landing animation (new clip `land_heavy`) and a thud.
- Emotes (M30, M32, M33): a two-player high-five (new clip `high_five`, or "left hanging"), dance sync, a hint listing emotes on an unknown `/e`, and a taunt window after a KO.
- Spawn and edges (M01, M41): 3 s spawn shield, a sign at spawn with the controls and the board, and a kill-feed line for falling off the world.

Changes (commits 57297d1, then the review fixes):
- New: `Feedback.luau`, `GameState.luau`, `Social.server.luau`, `FeedbackClient.client.luau`. Rewritten: `TestArena`. Extended: `CombatServer`, `Animate`, `CombatInput`. New remotes: Feedback, State, Social.
- New clips `high_five` and `land_heavy` are in the Fable critic loop (round 0 review running).
- An independent code review found 20 issues, all fixed. The worst: stacked hit-stops could freeze clips; parry could be spammed by toggling block; records could be faked; dummy kills farmed KOs; the signs faced away from spawn.

Measured: `roblox/check_project.py`: the 25 shipped clips pass; high_five and land_heavy are pending export (expected).
Not checked: anything in Studio (no Roblox here); luau-analyze and rojo build (downloads blocked).
Simulation round 2: 3 fresh session agents running, with the round-2 inventory only.

Recall, round 2 (3 fresh zero-context critics; eyeballed, counted by aggregate.py):
- Fixed (now talked about, positive): M04 crouch sneak attack 3/3, M08 bench launch 3/3, M13 kick 3/3, M17 dummy 3/3, M32 emote taunts 2/3, new M35 high five 3/3.
- Complaint resolved but neutral (now forgotten): M01, M20, M41.
- Still complained about: M42, 3/3 ("I got to seven and it didn't even say I won", no rounds or shop).
- Regressions: M07 pool ("just blue", eclipsed by the bench), M31 dance (silent), M15 sword equip, M18 hit-friend (absorbed into M19), M40 dummy idle.
- Still forgotten: M11/M12 punches and combo ("the sword beats punching"), plus plumbing (M02, M03, M10, M34).
- New complaint: the bench throws the same arc every time, so the splash record can't be beaten.
- Would play again: maybe / maybe / maybe (round 1: maybe / no / no). Play time: 21, 19 and 22 min (round 1: 16-17 min).
- Inventory error caught by a session agent (dummy kills listed as KOs after the review fix). Fixed the inventory, and marked a correction in run 1's log before its recall ran.

Stop check: bar [no: M42 complained, regressions, play-again not "yes"] | cap [round 2 of 3] -> round 3
Next focus: a win moment (M42), a beatable splash (M08/M07), the pool tied into fights (M07), a purpose for punches (M11/M12).

---

## Round 03 (build, last round under the cap)

Changes:
- Rivalry sets: the first player to 5 KOs on the same rival wins the set. A "KAI WINS THE SET 5-3!" callout for everyone, the record ping, an automatic cheer on the winner, set wins on the board, and the head-to-head resets for the next set. (M42, M19)
- Bench launch: the height (about 30-62 studs) and the landing spot in the pool vary on every pull, so the splash record can be beaten. (M08, M07)
- Dunk: hit into the pool within 3 s of a knockback, and the feed says "Kai dunked Robin into the pool". (M07, M13)
- Guard break: the combo finisher (Hit3) ignores block and parry, with a "GUARD BREAK!" callout, so punches beat a turtling sword user. (M11, M12, M14)

Review: 5 findings in the round-3 diff (dunk credited on any hit; repeated dunks; bench launch credited as a dunk; splash clamp at 60; guard break kept the guard). All fixed.

Recall, round 3 (3 fresh zero-context critics; eyeballed, counted by aggregate.py):
- Holding: M04 2/3, M08 3/3, M13 3/3, M35 3/3, M19 3/3 (set wins retold), M06 3/3, M05 2/3, M14 2/3. M12 combo now talked about 2/3 (guard break). M07 and M31 back to 2/3.
- Still complained about: M42 3/3 (no unlocks, shop or second map), M01 3/3 (signs behind spawn, silent shield), and new: M16 sword 3/3 ("whoever clicks first").
- Regressed: M17 dummy challenge 0/3 ("a record with nobody watching").
- Would play again: maybe / maybe / maybe. Play time 19-22 min.
- Session agents found code/inventory mismatches (splash cap 60, kick with the sword, shield silence, sign placement). Fixed after the round: "Polish after round 3" commit, not re-simulated.

Stop check: bar [no: M42 and M16 complained, play-again not "yes"] | cap [3 of 3 reached] -> stop at cap.
Below the bar, reported plainly in `playtest/REPORT.md`: progression and unlocks are out of the chosen scope (M42), the sword needs balance (M16), solo goals don't stick (M17), there's no music for the dance or pool. The post-round fixes are unverified by simulation, and nothing is verified in Studio.
