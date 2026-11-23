# R15 Animation Forge

Custom **Roblox R15** character animations authored in **Blender** (headless `bpy`), reviewed **frame by frame**
by a **Fable 5.2 critic agent**, then fixed automatically by Claude, which edits the keyframes and F-curves from the critic's findings.

```
 animations/specs/*.py ──build──▶ .blend (R15 rig + action)
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                              ▼
         render (Cycles, 2 cams)            analyze (metrics)
         contact sheets · onion skin        accel spikes · kinks · seams · limits
         F-curve plots · GIF                feet contact/slide · lockstep · twinning
                    └──────────────┬──────────────┘
                                   ▼
                  Fable 5.2 critic agent (critic/critic_prompt.md)
                  ── reports/<anim>/iter_N.json (typed fix ops) ──
                                   ▼
                  apply_fixes.py ──▶ iter_N+1.blend ──▶ re-render, re-critique (≤ 3 rounds)
                                   ▼
                  export ──▶ output/fbx · output/rbxmx · output/blend · output/previews
```

## Animations

27 clips in eight sets (`high_five` and `land_heavy` were added for the playtest improvements):

| Set | Animation | Frames @30fps | Loop | Priority | Floor contact |
|---|---|---|---|---|---|
| Locomotion | idle | 96 | ✓ | Idle | feet |
|  | walk | 32 | ✓ | Movement | feet |
|  | run | 20 | ✓ | Movement | feet |
|  | jump | 33 (spec 30, retimed by the critic) |  | Movement | feet |
| Combat | punch | 24 |  | Action | feet |
|  | sword_slash | 30 |  | Action | feet |
|  | hit_react | 20 |  | Action | feet |
| Emotes | wave | 48 |  | Action | feet |
|  | dance | 64 | ✓ | Action | feet |
|  | cheer | 40 |  | Action | feet |
| Movement states | fall | 24 | ✓ | Movement | none |
|  | climb | 30 | ✓ | Movement | none |
|  | swim | 40 | ✓ | Movement | none |
|  | swim_idle | 60 | ✓ | Movement | none |
|  | sit | 60 | ✓ | Core | none |
| Combat 2 | block | 30 | ✓ | Action | feet |
|  | kick | 30 |  | Action | feet |
|  | combo | 48 |  | Action | feet |
|  | death | 50 |  | Action4 | body |
| Emotes 2 | point | 40 |  | Action | feet |
|  | laugh | 48 |  | Action | feet |
|  | clap | 40 |  | Action | feet |
|  | salute | 40 |  | Action | feet |
| Crouch | crouch_idle | 72 | ✓ | Idle | feet |
|  | crouch_walk | 40 | ✓ | Movement | feet |

Floor contact tells the metrics and fixes what should touch the floor: `feet`; `none` (airborne, on a truss, in water or on a seat); or `body` (lying down).

## Results

All 25 animations were **approved** by the Fable 5.2 critic. Most needed 2–3 rounds. `death` needed a 4th, verification-only round: its round-3 fix had only been dry-run, and it was applied and re-reviewed rather than shipped unseen. Critic scores, first round → final:

| Animation | Rounds | Verdict | Fluidity | Posing | Timing | Transitions | Appeal |
|---|---|---|---|---|---|---|---|
| idle | 2 | approved | 4 → 7 | 4 → 7 | 4 → 7 | 7 → 9 | 3 → 6 |
| walk | 2 | approved | 5 → 8 | 3 → 8 | 5 → 8 | 5 → 8 | 4 → 7 |
| run | 3 | approved | 4 → 8 | 3 → 8 | 4 → 8 | 5 → 7 | 4 → 7 |
| jump | 3 | approved | 4 → 8 | 4 → 8 | 4 → 8 | 5 → 8 | 5 → 7 |
| punch | 3 | approved | 5 → 7 | 4 → 7 | 6 → 8 | 6 → 8 | 5 → 7 |
| sword_slash | 3 | approved | 5 → 8 | 3 → 8 | 6 → 8 | 5 → 7 | 5 → 8 |
| hit_react | 3 | approved | 4 → 8 | 5 → 7 | 6 → 8 | 6 → 8 | 4 → 7 |
| wave | 2 | approved | 5 → 7 | 4 → 7 | 5 → 7 | 6 → 8 | 4 → 7 |
| dance | 3 | approved | 5 → 8 | 5 → 7 | 5 → 7 | 5 → 8 | 4 → 7 |
| cheer | 3 | approved | 5 → 7 | 3 → 8 | 6 → 7 | 5 → 7 | 5 → 7 |
| fall | 2 | approved | 5 → 8 | 6 → 7 | 5 → 7 | 8 → 8 | 4 → 7 |
| climb | 2 | approved | 5 → 8 | 3 → 8 | 4 → 7 | 8 → 8 | 4 → 7 |
| swim | 3 | approved | 6 → 8 | 3 → 8 | 6 → 7 | 8 → 8 | 4 → 7 |
| swim_idle | 3 | approved | 5 → 8 | 5 → 7 | 6 → 7 | 8 → 8 | 4 → 7 |
| sit | 2 | approved | 4 → 7 | 5 → 8 | 6 → 7 | 9 → 9 | 4 → 6 |
| block | 3 | approved | 4 → 7 | 3 → 8 | 5 → 7 | 7 → 9 | 3 → 7 |
| kick | 2 | approved | 5 → 8 | 5 → 8 | 6 → 8 | 3 → 8 | 5 → 8 |
| combo | 2 | approved | 5 → 8 | 5 → 8 | 4 → 8 | 3 → 8 | 5 → 8 |
| death | 4 | approved | 5 → 8 | 3 → 8 | 4 → 8 | 5 → 8 | 4 → 7 |
| point | 2 | approved | 4 → 7 | 5 → 7 | 4 → 8 | 6 → 8 | 4 → 7 |
| laugh | 2 | approved | 5 → 7 | 3 → 7 | 4 → 7 | 6 → 8 | 4 → 7 |
| clap | 2 | approved | 4 → 6 | 2 → 7 | 5 → 7 | 6 → 8 | 3 → 6 |
| salute | 2 | approved | 4 → 7 | 3 → 8 | 5 → 7 | 6 → 8 | 4 → 7 |
| crouch_idle | 2 | approved | 4 → 7 | 5 → 8 | 4 → 7 | 6 → 8 | 3 → 7 |
| crouch_walk | 2 | approved | 5 → 8 | 3 → 8 | 4 → 8 | 4 → 8 | 4 → 7 |

Typical first-pass problems the critic caught and fixed:
- feet sinking through the floor (almost every clip with leg motion), and skating crouch, kick and combo feet
- the sword arm through the head, and the blade in the floor
- a swim recovery that passed underwater through the head
- climbing hands that missed the truss
- clap hands that never met
- a salute hand inside the head
- a death that landed like a plank and then hovered above the floor
- frozen, symmetric idles, and everything keyed on the same frames

The critics also caught a bug in the pipeline itself: `plant_feet` compounded its corrections. That bug is fixed.

Per-round findings, metric tables and change logs are in [`reports/SUMMARY.md`](reports/SUMMARY.md).
Before/after GIFs are in `output/previews/*_before_after.gif`.

Every exported `.rbxmx` is checked frame by frame with `python -m pipeline.verify_rbxmx`, which rebuilds the
poses using Roblox's Motor6D joint math (`C0 · Transform`). The largest difference from Blender is 4.4e-6 studs.

## Simulated playtest

`playtest/` holds a simulated first session by two 12-year-old best friends: 3 independent runs per round, with separate zero-context Fable 5.2 agents writing the next-day lunch-table recall. It tracks which moments they talk about at school, complain about or forget. Over 3 rounds, the forgettable moments were rebuilt:
- stakes and the kill feed
- hit feedback
- parry and guard break
- sneak attacks
- a launch bench
- high fives
- set wins
- two new critic-approved clips: `high_five` and `land_heavy`

Results, what's still below the bar and a real-playtest checklist are in [`playtest/REPORT.md`](playtest/REPORT.md). The run used the Cook Loop; its ledger is in `cook/`.

## Roblox integration

`default.project.json` is a **Rojo** project that syncs the whole pack into Studio:
- all 25 KeyframeSequences, with hit and footstep markers
- a replacement `Animate` script for idle, walk, run, jump, fall, climb, swim, sit, crouch, death and `/e` emotes
- combat: Mouse1 punch and combo, Q kick, F block, a sword slash, server-validated hits, hit reactions
- a Studio test arena

See [`roblox/README.md`](roblox/README.md) for the quick start.

## Layout

| Path | What it is |
|---|---|
| `rig/r15_rig.py` | Procedural R15 armature + block meshes. Bone names = R15 part names. Channel conventions and joint limits. |
| `animations/specs/` | First-pass keyframe spec per animation (degrees / studs, 30 fps). |
| `pipeline/build.py` | Spec → `.blend` (rig, render scene, keyed action). |
| `pipeline/render.py` | Every frame from a 3/4 camera + an orthographic side camera → contact sheets, onion skin, F-curve plot, GIF. |
| `pipeline/analyze.py` | Objective per-frame metrics for the critic. |
| `critic/critic_prompt.md` | The Fable 5.2 critic brief: what to look for, severity, rig sign conventions. |
| `critic/findings_schema.json` | Critic report schema and the 9 typed fix ops. |
| `pipeline/validate_report.py` | Report validator (the critic runs it before handing a report back). |
| `pipeline/apply_fixes.py` | Applies fix ops to the F-curves, clamps joint limits, logs every change. |
| `pipeline/export.py` | FBX + `.rbxmx` KeyframeSequence export, with a re-import check. Also writes markers, `output/meta/*.json` and `roblox/src/shared/AnimationMeta.luau`. |
| `animations/markers.py` | Hit and footstep marker rules, resolved from the final curves at export. |
| `roblox/`, `default.project.json` | Rojo project + Luau: AnimationLoader/Controller, Animate, combat, test arena. `roblox/check_project.py` is an offline consistency check. |
| `pipeline/verify_rbxmx.py` | Rebuilds every `.rbxmx` frame with Roblox joint math and compares it to Blender. |
| `pipeline/iterate.py` / `summary.py` | Apply a round of reports and re-render; write SUMMARY.md and the before/after previews. |
| `reports/` | Critic reports per iteration, the logs of applied changes, and `SUMMARY.md`. |
| `output/` | Final deliverables. |

## Running it

```bash
pip install -r requirements.txt                 # bpy 5.3 (headless Blender), numpy, pillow, matplotlib

python -m pipeline.run_all --build              # iteration 0: build, render, analyze all 10
# critic round: a Fable 5.2 agent reads work/<anim>/iter_0/{review/*.png,metrics.json,keys.json}
#               and writes reports/<anim>/iter_0.json (see critic/critic_prompt.md)
python -m pipeline.validate_report reports/*/iter_0.json
python -m pipeline.apply_fixes walk 0           # → work/walk/iter_1.blend (+ reports/walk/iter_0_applied.log)
python -m pipeline.run_all --iter 1 walk        # re-render + re-analyze, then critique again
python -m pipeline.export                       # latest iteration of every animation → output/
```

The critic runs as a Claude Code subagent with `model: "fable"`. It reads the renders as images. Each round,
one critic per set (locomotion, combat, emotes) runs in parallel. The loop stops when a clip is `approved`
(no high- or medium-severity findings) or after 3 rounds.

## Fix ops

`set_pose`, `add_breakdown` (breakdown key or overshoot-and-settle), `offset_channel`, `scale_amplitude`,
`set_easing`, `offset_overlap` (drag and follow-through, wraps cyclically on loops), `smooth_transition`
(`loop_seam` with cyclic handles, Gaussian `smooth`, `remove_interior`), `retime` (with optional ripple), and
`plant_feet` (re-keys LowerTorso height so the lowest foot touches the floor, or with `parts: "all"` the lowest body part). The pose ops run first, then retime,
then plant_feet, then the joint-limit clamp.

## Using the animations in Roblox Studio

The easiest path is the Rojo project ([`roblox/README.md`](roblox/README.md)). To use individual clips by hand:

**Option A: `.rbxmx` KeyframeSequence (exact).** Drag `output/rbxmx/<anim>.rbxmx` into Studio (or use
*Insert from File*). Open it in the Animation Editor on an R15 rig, then *Publish to Roblox* to get an asset ID.
The poses are baked on every frame with linear easing, so the Blender curves are reproduced exactly.

**Option B: FBX.** In the Animation Editor, select an R15 rig, then *⋯ → Import → From FBX Animation* and pick
`output/fbx/<anim>.fbx`. The armature's bones are named after the R15 parts. The rig is built at **1 Blender unit = 1 stud**.
If root translation (the bob in walk/run, the crouch in jump) comes in at the wrong scale, re-export with a different
`global_scale` in `pipeline/export.py`. Rotations are not affected by scale.

Then play them from a script, or reuse `AnimationController` from the Rojo project:

```lua
local anim = Instance.new("Animation")
anim.AnimationId = "rbxassetid://<published id>"
local track = humanoid:WaitForChild("Animator"):LoadAnimation(anim)
track:Play()
```

## Notes

- The rig is built procedurally from the R15 joint layout (part names, joint pivots, blocky proportions). No Roblox assets are copied.
- Locomotion is in place. The jump keeps its vertical travel for the Humanoid's physics, and only crouches and stretches.
- The left limbs are orange and the right limbs blue in every render, so the critic can tell the sides apart.
