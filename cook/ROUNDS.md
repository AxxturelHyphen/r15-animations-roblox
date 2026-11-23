# Cook ledger: memorable first session

Started: 2026-11-23 (UTC), simulation round 1 already running
Time: floor none | cap 3 simulation rounds
Bar: forgotten to talked about (at least 2 of 3 mentions, plus detail or again at least once) | no regressions | would_play_again "yes" in at least 2 of 3
Calibration offset: none (no user estimate yet)
Usage: about 20% per hour, never 100%
Gate: report approved [no] | final [not started]
Best so far: round 1 baseline

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
