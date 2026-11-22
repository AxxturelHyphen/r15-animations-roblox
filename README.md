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

| Set | Animation | Frames @30fps | Loop | Priority |
|---|---|---|---|---|
| Locomotion | idle | 96 | ✓ | Idle |
| | walk | 32 | ✓ | Movement |
| | run | 20 | ✓ | Movement |
| | jump | 33 (spec 30, retimed by the critic) | | Movement |
| Combat | punch | 24 | | Action |
| | sword_slash | 30 | | Action |
| | hit_react | 20 | | Action |
| Emotes | wave | 48 | | Action |
| | dance | 64 | ✓ | Action |
| | cheer | 40 | | Action |

## Results

All 10 animations were **approved** by the Fable 5.2 critic within 2–3 rounds. Critic scores, first round → final:

| Animation | Fluidity | Posing | Timing | Transitions | Appeal |
|---|---|---|---|---|---|
| idle | 4 → 7 | 4 → 7 | 4 → 7 | 7 → 9 | 3 → 6 |
| walk | 5 → 8 | 3 → 8 | 5 → 8 | 5 → 8 | 4 → 7 |
| run | 4 → 8 | 3 → 8 | 4 → 8 | 5 → 7 | 4 → 7 |
| jump | 4 → 8 | 4 → 8 | 4 → 8 | 5 → 8 | 5 → 7 |
| punch | 5 → 7 | 4 → 7 | 6 → 8 | 6 → 8 | 5 → 7 |
| sword_slash | 5 → 8 | 3 → 8 | 6 → 8 | 5 → 7 | 5 → 8 |
| hit_react | 4 → 8 | 5 → 7 | 6 → 8 | 6 → 8 | 4 → 7 |
| wave | 5 → 7 | 4 → 7 | 5 → 7 | 6 → 8 | 4 → 7 |
| dance | 5 → 8 | 5 → 7 | 5 → 7 | 5 → 8 | 4 → 7 |
| cheer | 5 → 7 | 3 → 8 | 6 → 7 | 5 → 8 | 5 → 7 |

Typical first-pass problems the critic caught and fixed include:
- feet sinking through the floor (every clip with leg motion)
- the sword arm passing through the head, and the blade tip hitting the floor
- a frozen, perfectly symmetric idle
- everything keyed on the same frames
- a run with no flight phase
- fists clipping the head in the cheer

It also caught a bug in the pipeline itself: `plant_feet` compounded its corrections. That bug is fixed.

Per-round findings, metric tables and the change logs are in [`reports/SUMMARY.md`](reports/SUMMARY.md).
Before/after GIFs are in `output/previews/*_before_after.gif`.

Every exported `.rbxmx` is checked frame by frame with `python -m pipeline.verify_rbxmx`, which rebuilds the
poses using Roblox's Motor6D joint math (`C0 · Transform`). The largest difference from Blender is 4e-6 studs.

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
| `pipeline/export.py` | FBX + `.rbxmx` KeyframeSequence export, with a re-import check. |
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
`plant_feet` (re-keys LowerTorso height so the lowest foot touches the floor). The pose ops run first, then retime,
then plant_feet, then the joint-limit clamp.

## Using the animations in Roblox Studio

**Option A: `.rbxmx` KeyframeSequence (exact).** Drag `output/rbxmx/<anim>.rbxmx` into Studio (or use
*Insert from File*). Open it in the Animation Editor on an R15 rig, then *Publish to Roblox* to get an asset ID.
The poses are baked on every frame with linear easing, so the Blender curves are reproduced exactly.

**Option B: FBX.** In the Animation Editor, select an R15 rig, then *⋯ → Import → From FBX Animation* and pick
`output/fbx/<anim>.fbx`. The armature's bones are named after the R15 parts. The rig is built at **1 Blender unit = 1 stud**.
If root translation (the bob in walk/run, the crouch in jump) comes in at the wrong scale, re-export with a different
`global_scale` in `pipeline/export.py`. Rotations are not affected by scale.

Then play them from a script:

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
