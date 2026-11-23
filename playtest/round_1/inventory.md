# Moment inventory (ground truth, round 1)

Everything a player can actually experience in the current build, read from the code. The simulation may only
use moments listed here. If the players try anything else, it is logged as an attempt with its real
result, usually "nothing happens".

The place is a default Studio **Baseplate** (grey grid floor, a SpawnLocation at the origin) with the Rojo
project synced. Players spawn at the origin. **Directions from spawn:**
- truss: 24 studs east
- bench: 18 studs west
- training dummy: 14 studs north, facing spawn
- pool: about 40 studs south

There is no music, no HUD beyond Roblox's default, no objective, no score, no leaderboard and no round system.
The only sounds are Roblox's default character sounds: footsteps, jump, landing, swimming and climbing.

## Movement and states (`roblox/src/character/Animate.client.luau`)
| ID | Moment | What happens today | Missing |
|---|---|---|---|
| M01 spawn | Appear at the origin | Idle animation (breathing, weight shift). Default Roblox look. | No intro, title or hint of what to do |
| M02 walk-run | Move with WASD | At the default WalkSpeed 16 you always use the **run** cycle (run starts above 8.5 studs/s). Feet are speed-matched. | Nothing |
| M03 jump-fall | Jump with Space | jump animation, then blends into the fall loop with flailing arms if airborne longer | No landing animation or impact |
| M04 crouch | C or Left Ctrl | Low sneak pose, and crouch_walk at a slow 2.7 studs/s. Toggle. | No purpose (nothing to hide from), no indicator |
| M05 climb-truss | Walk into the truss | Hand-over-hand climb animation, 24 studs up to an 8×8 grey platform | Nothing at the top: no view reward, no marker, no timer |
| M06 jump-off-truss | Jump off the 24-stud platform | Long fall loop with flailing arms. Roblox has **no fall damage**; you land and keep running. | No impact, splat, sound or damage |
| M07 swim | Enter the pool: steps up to a 4-stud ledge, then over the 8-stud rim, water 8 deep | swim (front crawl) when moving, swim_idle (treading water) when still. Default splash and swim sounds. | No splash effect beyond default, nothing to do in the water |
| M08 sit-bench | Walk onto the bench Seat | Sit loop (breathing, look-around). Space to stand. | Nothing |

## Combat (`roblox/src/client/CombatInput.client.luau`, `roblox/src/server/CombatServer.server.luau`)
Players have the default 100 HP and the default overhead health bar, shown to *other* players once damaged.
| ID | Moment | What happens today | Missing |
|---|---|---|---|
| M10 punch-air | Mouse1 with nothing in front | Right cross animation | No whoosh |
| M11 punch-dummy | Mouse1 next to the dummy | 10 damage, and the dummy plays hit_react (snaps back) | **No hit sound, particles, damage number, screen shake or hit-stop.** The dummy shows **no health bar or name**, so you can't see its HP. |
| M12 combo | Mouse1 twice quickly (within 0.45 s) | 3-hit combo (jab, cross, hook): 7, 9 and 14 damage, each on its impact frame | Same as M11. No finisher payoff; the hook looks the same as any hit. |
| M13 kick | Q | Front kick, 15 damage on the extension | Same as M11 |
| M14 block | Hold F | Forearms up guard. Incoming hits do 20% damage, and the blocker does **not** play hit_react. | No block sound or spark. The attacker can't tell the hit was blocked. |
| M15 sword-equip | Press 1 (the Sword tool in the backpack) | Grey blade held forward in the right hand | No unsheathe sound |
| M16 sword-slash | Mouse1 with the Sword | Overhead diagonal slash with a lunge step, 22 damage, 7-stud reach | Same as M11. No trail or swing sound. |
| M17 kill-dummy | Bring the dummy's 150 HP to 0 (about 7 sword slashes or about 15 punches) | The dummy plays the death animation (stagger, sit, roll onto its back, lie flat), then **vanishes after 4 s** and a fresh dummy appears | No kill message, count or reward, and nothing tells you its HP |
| M18 hit-friend | Hit your friend with any attack | Damage, and the friend plays hit_react (unless blocking). Their health bar appears for you. | No hit sound, no score, no "1v1" framing |
| M19 kill-friend | Bring your friend's 100 HP to 0 | The friend plays the death animation (falls, rolls onto their back, lies there), then respawns at the origin after Roblox's default 5 s | No kill feed, count, taunt or victory moment |
| M20 friend-blocks | Hit a blocking friend | Only 2–4 damage; no visible difference for the attacker | No clang, spark or "BLOCKED" text |

## Emotes (`Animate.client.luau`: TextChatService command `/e` or `/emote`)
| ID | Moment | What happens today | Missing |
|---|---|---|---|
| M30 emote-wave | `/e wave` | Friendly wave | Nothing |
| M31 emote-dance | `/e dance` | Bouncy groove loop until you move | **Two players dancing are not synced.** No music. |
| M32 emote-cheer / point / laugh / clap / salute | `/e cheer`, `point`, `laugh`, `clap`, `salute` | Each plays once, then returns to idle | No sound (the laugh is silent) |
| M33 emote-unknown | `/e highfive`, `/e sit`, `/e flex` … | **Nothing happens**, and the chat message is swallowed | No feedback that the emote doesn't exist |
| M34 emote-on-move | Move during an emote | The emote stops | Nothing |

## Other
| ID | Moment | What happens today | Missing |
|---|---|---|---|
| M40 dummy-idle | Walk up to the dummy | The dummy stands breathing (idle loop), facing spawn | No name or prompt |
| M41 explore-edges | Walk to the edge of the baseplate | Big empty grey floor, then the void | Nothing |
| M42 no-goal | Look for something to do | Nothing: no objective, quest, timer, leaderboard or NPC | Everything |
