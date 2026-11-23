# Moment inventory (ground truth, round 3 build)

Everything a player can actually experience in the current build, read from the code. The simulation may only
use moments listed here. If the players try anything else, it is logged as an attempt with its real
result, usually "nothing happens".

The place is a default Studio **Baseplate** (grey grid floor, a SpawnLocation at the origin) with the Rojo
project synced. Players spawn at the origin. **Directions from spawn:**
- truss: 24 studs east
- bench: 18 studs west
- training dummy: 14 studs north, facing spawn
- pool: about 40 studs south

There is no music. The Roblox player list shows **KOs** and **High Fives** for each player (leaderstats).
A **kill feed** in the top-right corner shows events, and big **centre callouts** show records and combat moments.
Sounds are Roblox's default character sounds plus built-in sounds for hits, blocks, KOs, records, splashes,
landings and the high-five clap. There is no round system and no shop or progression.

**At spawn:** a 3-second spawn shield (a ForceField: no damage while it lasts). Two signs face the spawn:
- **CONTROLS**: click punch / combo, Q kick (knocks people flying), hold F block (tap just before a hit: PARRY; the combo's 3rd hit breaks a block),
  C crouch (hit from behind: SNEAK ATTACK x2), 1 sword, `/e highfive` with a friend, `/e dance` and so on, and "First to 5 KOs on a rival wins the set".
- **RECORDS board**: fastest climb, biggest splash, dummy challenge, total high fives, and **RIVALRIES**
  (head-to-head KO score, e.g. "Kai 3 - 2 Robin"), updated live.

## Movement and states (`roblox/src/character/Animate.client.luau`)
| ID | Moment | What happens today | Missing |
|---|---|---|---|
| M01 spawn | Appear at the origin | Idle, a 3 s spawn shield, and the CONTROLS sign and RECORDS board facing you | No intro cutscene |
| M02 walk-run | Move with WASD | At the default WalkSpeed 16 you always use the **run** cycle (run starts above 8.5 studs/s). Feet are speed-matched. | Nothing |
| M03 jump-fall | Jump with Space | jump, then the fall loop. **A fall of 18+ studs onto the ground plays a superhero landing** (one knee down, fist on the floor) with a thud, dust and a camera shake for anyone nearby. | Small jumps have no landing animation |
| M04 crouch | C or Left Ctrl | Low sneak pose, slow crouch_walk (2.7 studs/s). **Hitting someone from behind while crouched does double damage**, with a red "SNEAK ATTACK!" number and callout. | No stealth beyond that: name and health still show |
| M05 climb-truss | Walk into the truss | Climb animation. **Climb race:** step on the green pad at the base to start a timer, then touch the gold bell at the top. Your time is announced and a new record gets a callout, a ping and the board. | Nothing |
| M06 jump-off-truss | Jump off the 24-stud platform | Long flailing fall; still no fall damage. **Lands as a superhero landing** with a thud and dust (see M03). Jumping off into the pool isn't possible (the pool is 40 studs away). | Nothing |
| M07 swim | Enter the pool | swim and swim_idle. Falling into the water makes a splash sized by fall height (big ones show "SPLASH 45!"); splashes of 6+ studs count for the biggest-splash record. **Getting knocked into the pool by someone (a kick or combo finisher in the last 3 s) puts "Kai dunked Robin into the pool" in the feed.** | Nothing to do underwater |
| M08 sit-bench | Walk onto the bench Seat (it faces the pool) | Sit loop. **A red lever next to it has a "Launch!" prompt (E). Anyone can pull it, and it flings whoever is sitting into the pool. Every launch is different: about 30 to 65 studs high, landing anywhere in the pool**, followed by a splash sized by the height and a feed line, "Kai launched Robin into the pool". So the splash record can always be beaten by a luckier launch. | Nothing |

## Combat (`roblox/src/client/CombatInput.client.luau`, `roblox/src/server/CombatServer.server.luau`)
Players have the default 100 HP and the default overhead health bar, shown to *other* players once damaged.
| ID | Moment | What happens today | Missing |
|---|---|---|---|
| M10 punch-air | Mouse1 with nothing in front | Right cross animation | No whoosh |
| M11 punch-dummy | Mouse1 next to the dummy | 10 damage. A white contact flash, a hit thud, a floating damage number, a short hit-stop (both freeze for a split second) and a small camera shake for the attacker. The dummy snaps back (hit_react), and **its name and health bar are now visible**. | Nothing |
| M12 combo | Mouse1 twice quickly | 3-hit combo: 7, 9 and 14. The hook (third hit) is heavy: a gold flash, a bigger number, a longer hit-stop, and the target is knocked back about 10 studs into the air. **The hook is a GUARD BREAK: it goes straight through block and parry** (an orange "GUARD BREAK!"), so punches beat someone who turtles behind block with a sword. | Nothing |
| M13 kick | Q | Front kick, 15 damage, heavy hit feedback, and **launches the target about 15 studs away and up**, enough to kick a friend off the truss platform or across the floor | Nothing |
| M14 block | Hold F | Guard up. Hits do 20% damage with a blue flash, a metal clang and "BLOCKED" over the blocker for everyone. **Raising the guard within 0.25 s before a hit is a PARRY:** no damage, a teal flash, a high clang, "PARRY!", a freeze, and the attacker staggers. | Nothing |
| M15 sword-equip | Press 1 | Blade in the right hand, with a built-in unsheathe sound | Nothing |
| M16 sword-slash | Mouse1 with the Sword | Slash with a swish sound, 22 damage, heavy hit feedback, a small knockback | No blade trail |
| M17 kill-dummy | Bring the dummy's 150 HP to 0 | Death animation, the KO sound and a kill-feed line ("Kai slashed the Training Dummy into a nap"). It does **not** count as a KO (only player KOs do). It respawns after 4 s, and it walks back to its spot if kicked away. **Dummy challenge:** an orange pad in front of it has a prompt, "10 s damage challenge". A 10-second countdown runs, the total damage is announced, and the best total goes on the RECORDS board. | Nothing |
| M18 hit-friend | Hit your friend | Same hit feedback as on the dummy (numbers, flash, thud, hit-stop, shake); the friend's health bar shows | Nothing |
| M19 kill-friend | Bring your friend's 100 HP to 0 | The friend plays the death animation (falls, rolls onto their back) and a KO sound plays. The kill feed says e.g. "Kai kicked Robin into a nap"; +1 KO in the player list; the RIVALRIES line updates ("Kai 4 - 2 Robin"). **Sets: the first player to 5 KOs on the same rival wins the set. A big callout for both, "KAI WINS THE SET 5-3 vs Robin!", the record ping, the winner automatically plays the cheer emote, the feed says "Kai won set 1 against Robin (5-3)", the board shows sets won ("(sets 1-0)"), and the KO score resets for the next set.** Respawn after 5 s, with a 3 s spawn shield. | Nothing |
| M20 friend-blocks | Hit a blocking friend | "BLOCKED", a clang and a blue flash; a perfect-timing block becomes a PARRY that staggers you | Nothing |

## Emotes (`Animate.client.luau`: TextChatService command `/e` or `/emote`)
| ID | Moment | What happens today | Missing |
|---|---|---|---|
| M30 emote-wave | `/e wave` | Friendly wave. **Within 4 s after you KO someone, any emote is a taunt in the kill feed** ("Kai waved bye-bye to Robin"). | Nothing |
| M31 emote-dance | `/e dance` | Groove loop. **Joining a friend who is dancing syncs you to their beat**, and two dancers near each other put "Dance party! Kai + Robin" in the feed. | No music |
| M32 emote-cheer / point / laugh / clap / salute | `/e cheer`, `point`, `laugh`, `clap`, `salute` | Play once. Used within 4 s of a KO, they become taunts in the feed: "Kai laughed at Robin", "slow-clapped", "saluted", "pointed at". | No sound on the laugh |
| M33 emote-unknown | `/e flex` or anything unknown | A system chat line: `No emote called "flex". Try: highfive (with a friend), wave, dance, ...` | Nothing |
| M35 high-five | `/e highfive` | **Two players both type it within 3 s and within 7 studs of each other:** they snap to face each other and do a synced high five, with a slap sound and a flash at the hands. "Kai and Robin high-fived!" goes in the feed and both get +1 High Fives. **Alone:** after 3 s you raise your hand anyway and the feed says "Kai was left hanging". | Nothing |
| M34 emote-on-move | Move during an emote | The emote stops | Nothing |

## Other
| ID | Moment | What happens today | Missing |
|---|---|---|---|
| M40 dummy-idle | Walk up to the dummy | The dummy stands breathing (idle loop), facing spawn | No name or prompt |
| M41 explore-edges | Walk to the edge of the baseplate | Big empty grey floor, then the void. Falling off the world puts "Robin fell off the world" in the feed. | Still empty |
| M42 goals | Look for something to do | Light goals: rivalry **sets (first to 5, with a win callout)**, climb race, biggest splash (beatable through random bench launches), dummy challenge and high-five count, all on the RECORDS board | No rounds, levels, shop or unlocks |


Note for the simulation: assume the animations are published, so both friends see each other's animations.
