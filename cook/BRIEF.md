# Cook brief: memorable first session

Written once after intake. Intake was covered by the user's answers to the plan questions on 2026-11-23,
so there are no open questions.

## Target
Two simulated 12-year-old best friends (Kai and Robin, `playtest/personas.md`) play the Roblox build for the
first time. Every moment they **forgot** the next day becomes a moment they **talk about at school**.
The moments they already talk about must stay talked about.

"References" here are not images. They are the user's goal and the round-1 baseline in
`playtest/round_1/REPORT.md`. **Shots** are the inventory moments (`playtest/inventory.md`, `cook/SHOTS.md`).

## Bar (per moment and per round)
- A previously forgotten moment counts as fixed when it is **mentioned in at least 2 of 3** fresh next-day recalls,
  and **retold with detail or wanted again in at least 1**.
- Talked-about moments must not regress (still mentioned in at least 2 of 3).
- Session level: `would_play_again` is "yes" in at least 2 of 3 runs. In round 1 it is whatever the baseline says.
- Every number comes from a critic (eyeballed). The counts are measured only in the sense that
  `playtest/aggregate.py` counted them from the critics' JSON.

## Critics (zero context)
- Session agents (Fable 5.2) see only the inventory, the personas and the code, never earlier rounds.
- Next-day agents (Fable 5.2) see only one session log. They never see the inventory, the code or my opinion.
- 3 runs per round; the median is effectively "at least 2 of 3".

## Rules
- Scope from intake: juice, two-player social moments and light goals. No full game mode.
- New animations go through the Blender to Fable critic loop (max 3 rounds), then export.
- Visual effects must have a gameplay job: an impact flash at the contact point, a block spark, a splash scaled to
  fall height. Cook's slop ban applies: no decorative particles, no glowing orbs, no shockwave rings popping out of things.
- Sound: only Roblox's built-in `rbxasset://sounds/*` files that ship with every client, credited as such.
  No third-party asset IDs.
- No invented simulation features: every simulated beat cites an inventory ID that matches the code.

## Time
Capped job: at most 3 simulation rounds (from the approved plan). No time floor.

## Deliverable and permissions
- Luau changes in `roblox/`, any new animations in `output/`, and `playtest/REPORT.md` with the before/after recall table.
- Allowed: commit and push to `guija/festive-turing-kfdsdv` and update draft PR #1. No public publishing.
