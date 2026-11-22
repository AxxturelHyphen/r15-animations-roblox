# Critic loop summary

Each animation went through: build → render/analyze → Fable 5.2 critique → automatic F-curve fixes → re-render, until the critic approved it (no high- or medium-severity findings) or 3 rounds had run.

Metrics are issue counts from `pipeline/analyze.py` (lower is better), except `overlap_score` (higher is better: 1.0 means no lockstep keys).

| Animation | Rounds | Final verdict | Findings per round (H/M/L) | Critic scores, first → last (fluidity/posing/timing/transitions/appeal) |
|---|---|---|---|---|
| idle | 2 | approved | r0: 1/2/1 · r1: 0/0/0 | 4/4/4/7/3 → 7/7/7/9/6 |
| walk | 2 | approved | r0: 3/3/0 · r1: 0/0/0 | 5/3/5/5/4 → 8/8/8/8/7 |
| run | 3 | approved | r0: 3/1/0 · r1: 0/1/0 · r2: 0/0/0 | 4/3/4/5/4 → 8/8/8/7/7 |
| jump | 3 | approved | r0: 2/4/0 · r1: 0/1/0 · r2: 0/0/0 | 4/4/4/5/5 → 8/8/8/8/7 |
| punch | 3 | approved | r0: 1/3/0 · r1: 1/0/0 · r2: 0/0/1 | 5/4/6/6/5 → 7/7/8/8/7 |
| sword_slash | 3 | approved | r0: 3/1/0 · r1: 1/1/0 · r2: 0/0/1 | 5/3/6/5/5 → 8/8/8/7/8 |
| hit_react | 3 | approved | r0: 1/2/0 · r1: 0/1/0 · r2: 0/0/0 | 4/5/6/6/4 → 8/7/8/8/7 |
| wave | 2 | approved | r0: 1/1/0 · r1: 0/0/1 | 5/4/5/6/4 → 7/7/7/8/7 |
| dance | 3 | approved | r0: 2/2/0 · r1: 0/1/0 · r2: 0/0/0 | 5/5/5/5/4 → 8/7/7/8/7 |
| cheer | 3 | approved | r0: 2/1/0 · r1: 0/3/1 · r2: 0/0/0 | 5/3/6/5/5 → 7/8/7/7/7 |

## idle

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 0 | 0 |
| velocity_corners | 0 | 0 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 3 | 0 |
| lockstep_key_frames | 1 | 0 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 0 | 0 |
| foot_penetration_frames | 0 | 0 |
| floating_frames | None | 0 |
| overlap_score | 0.0 | 1.0 |

**Round 0 critique** (needs_work): Technically clean (no pops, seamless loop) but lifeless: the motion is too small to see, everything is keyed on frame 48 and the stance is a symmetric straight-legged pose. Fixes: larger breathing and look-around, a real weight shift onto the left leg with a relaxed right knee, staggered timing for chest, head and arms, and the root re-planted so the feet stop sinking.

- `high` **stiff** F[0, 96] UpperTorso, Head, LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm: The idle is almost a still image. On the sheets F000, F024 and F048 cannot be told apart, and the onion skin is a single silhouette. metrics: whole-body speed peaks at 0.62 deg/frame, three dead holds (frames 0-8, 40-56, 88-96), and the ranges are tiny (UpperTorso.rx 2 deg, arms 2 deg, Head.rx 2 deg, Head.ry 8 deg). The breathing and the look-around do not read at game camera distance. → *scale_amplitude, scale_amplitude, scale_amplitude, scale_amplitude*
- `medium` **awkward_pose** F[0, 96] LowerTorso, UpperTorso, Head, LeftUpperLeg, RightUpperLeg, RightLowerLeg, RightFoot: The spec asks for a slight weight shift, but LowerTorso.lx only moves 0.04 studs and the legs stay locked at rz +/-2 for the whole clip, so in the front view the hips never move and the stance is a symmetric, straight-legged A-pose (no line of action). Because the legs do not compensate, the small shift that exists slides both feet sideways. Fix: a real shift onto the left leg at frame 48 (hips 0.14 studs left, pelvis rolled 2 deg so the right hip drops, both legs counter-rotated -7 deg so the feet stay where they are), the free right leg relaxes with a soft knee (thigh -14, knee 28, ankle -14), and the chest and head counter-tilt to stay balanced. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **stiff** F[0, 96] UpperTorso, Head, LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm: Every channel has exactly one interior key, at frame 48 (lockstep 7 of 9 bones, overlap_score 0.0). curves.png shows nine copies of the same half-sine: chest, head, both arms and both elbows all reach their extreme on the same frame and all stop together, which is what produces the 16-frame dead hold around frame 48. Left and right arms are also mirror images. Fix: stagger the parts so nothing peaks together. The look-around leads, the chest follows the hips, and the arms and forearms drag behind by different amounts on each side. → *offset_overlap, offset_overlap, offset_overlap, offset_overlap, offset_overlap, offset_overlap, offset_overlap, offset_overlap*
- `low` **awkward_pose** F[0, 96] LowerTorso, LeftFoot, RightFoot: The breathing is done by dropping the root 0.03 studs while the legs stay straight, so both feet sink into the floor: lowest foot z goes from -0.015 at frame 0 to -0.045 at frame 48 (just under the 0.05 penetration threshold, but the feet are below the floor on all 97 frames). Re-plant the root after the weight shift so the supporting foot sits on the floor. → *plant_feet*
- *apply_fixes:* applied 28 ops, skipped 0; saved work/idle/iter_1.blend

**Round 1 critique** (approved): Approved. All iteration-0 fixes landed: the weight shift onto the left leg with a relaxed right knee reads clearly from F020 to F070 (peak at F048), the head look-around leads it (F036-F040), chest and arms peak on different frames (no lockstep, overlap 1.0, no dead holds), and both feet stay on the floor (0 penetration, lateral foot drift 0.00). The loop seam is clean and the black-leg render artifact is gone. Remaining polish only: the motion is still on the subtle side and the hands are not animated.


Before/after: `output/previews/idle_before_after.gif`

## walk

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 0 | 0 |
| velocity_corners | 0 | 1 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 0 | 0 |
| lockstep_key_frames | 1 | 0 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 2 | 3 |
| foot_penetration_frames | 62 | 0 |
| floating_frames | None | 0 |
| overlap_score | 0.629 | 1.0 |

**Round 0 critique** (needs_work): The beats and the arm/leg opposition are right and the loop seam is clean, but the lower body is broken: both feet are under the floor for the whole cycle, the ankles roll the wrong way, the swing leg drags instead of clearing, and the planted foot skates. The upper body is one sine wave keyed on frame 16 with no weight shift. Fixes: rebuilt heel-to-toe roll, higher swing, linear stance thigh, hip sway with pelvis and chest tilt, staggered arms/head, root re-planted.

- `high` **awkward_pose** F[0, 32] LeftFoot, RightFoot: Both feet are under the floor for 31 of 32 frames (metrics: 62 penetration frames, down to -0.355 studs at frame 18). In the side view the heel of the front foot and the toe of the back foot are cut off by the floor line in every cell of F000-F004 and F014-F020. The cause is the ankle curve, which adds to the leg angle instead of countering it: at contact (F000/F016) the front foot is pitched 35 deg toes-up (thigh -25 + knee 5 + foot -15) and the back foot 47 deg toes-down (22 + 10 + 15), and at mid-stance (F008) the supporting foot is still 12 deg toes-down. Fix: a proper heel-to-toe roll. Heel strike at -20 deg, flat from frame 3 to 11, heel peeling off to +22 deg at the opposite contact, and the ankle flexed (not pointed) through the swing so the long R15 toe can clear the ground. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `high` **awkward_pose** F[16, 32] LeftUpperLeg, LeftLowerLeg, RightUpperLeg, RightLowerLeg: The swing leg never gets off the ground. With knee flexion of only 40-50 deg and the thigh still at -10 at the passing pose (F008 right leg, F024 left leg), the swing foot hangs lower than the supporting foot for the whole swing (F002-F009: right toe at -0.35 to -0.11 while the stance foot is at -0.13 to -0.06), so it reads as a shuffle and the passing pose has no silhouette. Fix: fold the swing leg properly (knee 68 at 4 frames after toe-off, 75 at passing, still 52 on the reach), bring the thigh through to -30 at passing, and start the knee break at toe-off (20 deg instead of 10) so the knee does not snap. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **transition** F[0, 16] LeftUpperLeg, LeftLowerLeg, RightUpperLeg, RightLowerLeg: The planted foot does not travel back at a steady speed, so it will skate on the ground in game (metrics: contact speed std 0.065-0.067 studs/frame against a mean of 0.11). The thigh eases in and out of the contact and toe-off extremes (curves.png: S-shaped UpperLeg.rx), which makes the foot crawl for the first and last 3 frames of each stance and rush through the middle. The 15 deg knee bump at frame 4 adds to it. Fix: constant-speed (linear) thigh through each stance phase, a thigh key at the down pose that compensates for the knee flex, a softer down-pose knee, and cyclic handles on the leg curves so the swing still eases through the loop seam. → *set_pose, set_pose, set_pose, set_pose, smooth_transition, set_easing, set_easing*
- `medium` **stiff** F[0, 32] LowerTorso, UpperTorso, LeftUpperLeg, RightUpperLeg: In the 3/4 view the hips and shoulders only twist (ry); there is no side-to-side weight transfer and no pelvis or shoulder tilt on any frame, so the walk looks like it runs on rails. Compare F008 and F024: the torso is in the identical place although the weight is on opposite legs. Fix: shift the hips 0.07 studs over the supporting leg at each passing pose, drop the swing-side hip 2.5 deg, counter-tilt the chest (2 frames late), and counter-rotate both legs 5 deg so the planted foot does not slide sideways. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, smooth_transition*
- `medium` **stiff** F[0, 32] UpperTorso, Head, LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm: All 13 animated bones are keyed on frame 16 and every upper-body curve is a single sine that peaks exactly on the contact frames (lockstep 13 of 13, overlap_score 0.63). Arms, forearms, chest twist and head all reverse on the same frame as the legs, the forearm just rides the upper arm, and the chest lean (UpperTorso.rx 4) and head pitch never change. Fix: let the chest twist and upper arms trail the legs by 1 frame, the forearms by 3 and the head by 2, and give the chest a small nod into each step (6 deg just after contact, 3 deg at the high point). → *smooth_transition, set_pose, set_pose, set_pose, set_pose, smooth_transition, offset_overlap, offset_overlap, offset_overlap, offset_overlap*
- `high` **awkward_pose** F[0, 32] LowerTorso: The root bob (LowerTorso.ly, -0.08 to +0.05) was authored without regard to the leg poses, so the body is 0.06-0.35 studs too low on every frame; this is the other half of the floor penetration in walk-1. After the leg and foot corrections above, re-key the root on every frame so the supporting foot sits exactly on the floor. → *plant_feet*
- *apply_fixes:* applied 55 ops, skipped 0; saved work/walk/iter_1.blend

**Round 1 critique** (approved): Approved. Feet are on the floor for the whole cycle (0 penetration frames, from 62), the heel-to-toe roll reads in the side view (heel strike F000/F016, flat F003-F011, heel-off F012-F016), the swing leg now folds and clears with a clear passing pose (F008, F024), and the hips shift over the supporting leg with staggered chest, arms and head (no lockstep, overlap 1.0). The supporting foot's contact point moves back at 0.09-0.14 studs/frame through the stance. The 3 foot_slide_segments left in the metrics come from the swing foot skimming within 0.06 of the floor being counted as contact (stance-only std is 0.02), not from visible skating. Remaining polish only: toe clearance is tight at F004-F005 and F020-F021, the toe-off thigh has a 3.4 deg/frame corner at F016, and the root bob is small (0.04 studs).


Before/after: `output/previews/walk_before_after.gif`

## run

| Metric | iter 0 | iter 1 | iter 2 |
|---|---|---|---|
| accel_spikes | 23 | 18 | 20 |
| velocity_corners | 6 | 9 | 11 |
| loop_seam_issues | 0 | 0 | 0 |
| joint_limit_violations | 0 | 0 | 0 |
| dead_holds | 0 | 0 | 0 |
| lockstep_key_frames | 1 | 0 | 0 |
| twinned_channels | 0 | 0 | 0 |
| foot_slide_segments | 4 | 2 | 2 |
| foot_penetration_frames | 21 | 0 | 0 |
| floating_frames | None | 0 | 0 |
| overlap_score | 0.629 | 1.0 | 1.0 |

**Round 0 critique** (needs_work): Good energy in the arms and a clean loop seam, but it is not yet a run: there is no flight phase, the stance foot is buried in the floor at mid-stance and skates, the hip hyper-extends to 40 deg, and the knee and thigh pop through the recovery. The upper body is keyed in lockstep on frame 10. Fixes: rebuilt stance and recovery leg poses, flat-foot contact with a toe roll, a keyed flight arc with the root planted during stance, pumping elbows and staggered upper body.

- `high` **awkward_pose** F[0, 20] LeftUpperLeg, LeftLowerLeg, RightUpperLeg, RightLowerLeg: The leg poses do not describe a run. Contact (F000/F010) is an over-striding, straight-legged heel dig with the thigh at -35; the hip then hyper-extends to +40 (F010 left leg, the thigh is far behind the body with the knee still bent 30), and the recovery whips from +40 to -55 in 5 frames with the knee jumping 30 to 95 in 3 frames (accel spikes of 14-19 deg/frame^2 on LowerLeg at frames 1-3 and 10-13, velocity corners at 3, 5, 10, 13, 15). The planted foot also skates: its speed goes 0.15, 0.37, 0.43, 0.37, 0.32, 0.27 studs/frame (std 0.09) because the thigh eases out of the contact. Fix: land closer under the body (thigh -22, knee 14), absorb to a 42 deg knee at frame 3, push off to +22 at frame 7, start folding the trailing knee in flight (70 at the opposite contact) into a 105 deg recovery, and space the stance thigh keys so the foot travels at a steady 0.2 studs/frame. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `high` **awkward_pose** F[0, 20] LeftFoot, RightFoot: Feet go through the floor on 21 frames. The stance foot is pitched 17-30 deg toes-down at mid-stance while the root dips (F003-F004: -0.34 and -0.37 studs, the whole foot is under the floor line in the side view), the contact is a 30 deg toes-up heel strike, and the recovering foot hangs 83-104 deg toes-down and also clips the floor as it passes under the body (F003/F013: -0.13). Fix: land almost flat (-8 deg), keep the foot flat from frame 2 to 4 by dorsiflexing against the shin, roll onto the toe for push-off at 6-7, and keep the ankle flexed through the recovery. Foot keys follow the new leg keys from run-1. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, smooth_transition*
- `medium` **stiff** F[0, 20] UpperTorso, Head, LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm: All 13 bones are keyed together on frame 10 (lockstep 13 of 13, overlap_score 0.63). The chest lean is frozen at 12 deg and the head at -8 for the whole cycle, the elbows only change 15 deg (-80 to -95) so the arms swing as rigid L-shapes, and arms, chest twist and head all reverse on the contact frame. Fix: pump the elbows (about -72 on the back swing, -110 in front), let the chest drive into each landing (15 deg at the absorb, 10 in flight), and trail the chest twist and upper arms by 1 frame and the forearms and head by 2. → *smooth_transition, set_pose, set_pose, set_pose, set_pose, smooth_transition, scale_amplitude, offset_overlap, offset_overlap, offset_overlap, offset_overlap*
- `high` **timing** F[0, 20] LowerTorso: The spec calls for a flight phase at frames 5-9, but there is none: metrics report no frame with both feet off the ground, and on F008-F009 the trailing toe is still on the floor while the leading heel is already arriving, so it reads as a fast walk. The root curve is also out of phase with the legs (it peaks at frame 6, during push-off, and is already falling through the frames that should be airborne). Fix: plant the root to the supporting foot through each stance (frames 0-7 and 10-17) and key a ballistic arc for the two airborne frames between them. → *set_pose, set_pose, set_pose, set_pose, plant_feet, plant_feet*
- *apply_fixes:* applied 58 ops, skipped 0; saved work/run/iter_1.blend

**Round 1 critique** (needs_work): Big improvement: no floor penetration (from 21 frames), a readable contact / absorb / push-off / flight sequence (F000, F003-F004, F006-F007, F008-F009), a 105 deg recovery, pumping elbows and no lockstep. One medium problem is left: the supporting foot skates during push-off and the root rises unevenly into the flight. Everything else is polish (knee accel of 11 deg/frame^2 at toe-off and contact is acceptable for a run).

- `medium` **transition** F[5, 9] LeftUpperLeg, LeftLowerLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot, LowerTorso: During push-off the planted toe slides back twice as fast as the rest of the stance: the contact point moves 0.19 studs/frame while the foot is flat (F001-F004 left, F011-F014 right) but 0.41 on F006/F016 and 0.25 on F007/F017 (metrics: stance speed std 0.059, 2 foot_slide_segments). The thigh sweeps 9 deg/frame from F005 to F007 while the foot also whips from 8 to 30 deg of pitch about the ankle. The root also rises unevenly (+0.09, +0.14, +0.05, +0.01 over F004-F008), and the trailing toe is only 0.05 above the floor on F008/F018, so the flight shows on a single frame per step. Fix: a shorter, slower hip extension through push-off (thigh 2 at frame 5, 17 at frame 7), a softer toe roll (ankle -21 at 6, -13 at 7), a slightly higher flight arc, and the stance root re-planted. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, plant_feet, plant_feet*
- *apply_fixes:* applied 16 ops, skipped 0; saved work/run/iter_2.blend

**Round 2 critique** (approved): Approved. The push-off fix landed: the root now rises evenly from the absorb (F003-F004) through toe-off (F007) into the flight (F008-F009), and the supporting foot stays on the floor for the whole stance (lowest z 0.00 on F000-F007 and F010-F017, 0 penetration frames, from 21 at iteration 0). Stance speed std is 0.034 (from 0.09 at iteration 0 and 0.059 at iteration 1) against a mean of 0.20 studs/frame, which no longer reads as skating at 20 frames per cycle; it is just over the 0.03 metric threshold, so the 2 foot_slide_segments remain as a known, low-severity item. Also left as polish: the flight registers on one frame per step by the metric (the trailing toe is 0.09 above the floor on F008/F018), and the knee has accel peaks of about 11 deg/frame^2 at toe-off and contact, which suit a run. Loop seam clean, no lockstep, overlap 1.0.


Before/after: `output/previews/run_before_after.gif`

## jump

| Metric | iter 0 | iter 1 | iter 2 |
|---|---|---|---|
| accel_spikes | 68 | 82 | 82 |
| velocity_corners | 32 | 29 | 29 |
| loop_seam_issues | 0 | 0 | 0 |
| joint_limit_violations | 0 | 0 | 0 |
| dead_holds | 0 | 0 | 0 |
| lockstep_key_frames | 3 | 1 | 1 |
| twinned_channels | 6 | 0 | 0 |
| foot_slide_segments | 0 | 2 | 0 |
| foot_penetration_frames | 56 | 0 | 0 |
| floating_frames | None | 0 | 0 |
| overlap_score | 0.433 | 0.889 | 0.889 |

**Round 0 critique** (needs_work): Clear phases and a good arm swing, but the feet are below the floor on 28 of 31 frames, the 'airborne' frames look like standing on bent legs, the landing absorbs in 2 frames, the take-off pops in 3, and left and right are perfect mirrors with everything keyed on frames 6, 9 and 23. Fixes: flat feet in both crouches, hips over the toes at take-off, a higher uneven tuck, arms leading with staggered forearms, chest and head, a 4-frame landing and 4-frame take-off, and the root re-planted wherever a foot touches the floor.

- `high` **awkward_pose** F[0, 30] LeftFoot, RightFoot, LowerTorso: The feet are not flat in either crouch. At the anticipation (F006) and the landing absorb (F023) the foot is pitched 10 deg toes-down (thigh -70/-60 + knee 110/100 + foot -30), so the toes are pushed through the floor (-0.12 to -0.24 on F002-F006 and F022-F028). At take-off the ankle snaps to +40 while the ankle joint stays in place, so the toes swing 0.5 studs backwards under the floor instead of the heel lifting (F007-F009, down to -0.50). Fix: -40 on the ankle at the bottom of both crouches so the foot is flat, a less extreme toe point at take-off (28), and move the hips with the feet: slightly further back in the crouches and 0.2 studs forward over the toes at take-off so the feet do not slide. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **awkward_pose** F[10, 21] LeftUpperLeg, LeftLowerLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot, LowerTorso: The airborne section does not read as airborne. The root returns to standing height by frame 14 while the feet are pointed 50-60 deg down, so the toes hang below the floor line for the whole 'flight' (F010-F021: -0.15 to -0.40) and in the side view the character seems to stand on bent legs. The tuck is also weak and perfectly symmetric (both legs thigh -40, knee 80). Fix: carry the take-off extension through the air (root +0.35 at the apex), tuck harder and unevenly (left thigh -52 / knee 96, right -42 / 84) and relax the toe point so the feet clear the floor. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **stiff** F[0, 30] LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm, UpperTorso, Head: Left and right sides are mirror-identical on all six limb channel pairs (twinning: UpperLeg, LowerLeg, Foot, UpperArm rx and rz, LowerArm), and all 13 bones are keyed together at the crouch (frame 6) and the landing (frame 23), 8 of 13 at take-off (overlap_score 0.43). The arms hit their back-swing on the same frame the legs bottom out, so they do not drive the jump, and the forearms, chest and head have no follow-through. Fix: the arms lead the legs by 1 frame, the right arm swings slightly smaller than the left, the forearms drag 1 and 2 frames behind, the chest unfolds 1 frame after the hips and the head settles 2 frames late. → *offset_overlap, scale_amplitude, offset_overlap, offset_overlap, offset_overlap, offset_overlap*
- `medium` **timing** F[21, 30] LeftLowerLeg, RightLowerLeg, LeftUpperLeg, RightUpperLeg, LowerTorso: The landing absorbs in 2 frames: between F021 and F023 the knees go from 20 to 100 deg, the hips drop 0.65 studs and the chest folds 15 deg (accel spikes of 46-48 deg/frame^2 on both knees at 21 and 23, the largest in the clip; whole-body speed 190 deg/frame). It reads as the character being teleported into the squat with no weight. Fix: stretch contact-to-bottom to 4 frames; later keys ripple, so the clip becomes 2 frames longer and the 7-frame recovery is kept. → *retime*
- `medium` **timing** F[6, 10] LeftLowerLeg, RightLowerLeg, LeftUpperLeg, RightUpperLeg, LeftUpperArm, RightUpperArm: Take-off goes from the deepest crouch to full extension in 3 frames (F006-F009): knees 110 to 5, arms 50 to -150 in 4 frames, whole-body speed 410 deg/frame at frame 7, with accel spikes of 35-39 on knees and upper arms and velocity corners of 10-12 deg/frame at frames 6 and 9. There is no slow-out of the crouch, so the extension reads as a pop, not a push. Fix: give the push one more frame (keys on frames 8-9 and everything after move 1 frame later; the clip ends at frame 33 after both retimes). → *retime*
- `high` **awkward_pose** F[0, 30] LowerTorso: Root height does not follow the legs: 56 foot-penetration frames in total (28 per foot, every frame except the first and last). After the pose and timing changes above, lift the root on every frame where a foot is at or below the floor (crouch, take-off on the toes, landing and recovery) and leave the airborne frames alone. → *plant_feet*
- *apply_fixes:* applied 25 ops, skipped 0; saved work/jump/iter_1.blend

**Round 1 critique** (needs_work): The fixes worked: feet are flat in both crouches and never below the floor (0 penetration frames, from 56), the take-off rolls onto the toes with the hips over them (F008-F011), the tuck is clearly airborne and uneven (F013-F018), the arms lead the legs, the landing absorbs over 4 frames (F022-F026) and nothing is mirrored any more. One medium problem is left, the feet creeping forward through the landing. The lockstep at F010 (arms and legs fully extended together) is the intended take-off extreme, and the remaining accel spikes belong to the take-off and landing impacts.

- `medium` **transition** F[20, 30] LowerTorso, LeftFoot, RightFoot: After touchdown the planted feet slide forward about 0.2 studs: the toe contact point moves from +0.46 at F020 to +0.71 at F025 and the foot keeps creeping until F030 (metrics: contact drift 0.19 left / 0.20 right on frames 20-33, both flagged as slide segments). The hips are still travelling back towards the crouch offset (LowerTorso.lz -0.38 at F026) while the feet are already down, so the feet land 0.17 studs behind where they end up. Fix: have the hips almost over the feet at touchdown and sit back less at the bottom of the absorb. → *set_pose, set_pose*
- *apply_fixes:* applied 2 ops, skipped 0; saved work/jump/iter_2.blend

**Round 2 critique** (approved): Approved. The landing fix landed: the feet now stay where they touch down (contact drift 0.05 left / 0.02 right on F020-F033, from 0.19 / 0.20; 0 foot_slide_segments) and the absorb F022-F026 and recovery F027-F033 read with weight. Feet are never below the floor (0 penetration frames, from 56 at iteration 0), the crouch feet are flat, the take-off rolls onto the toes with the arms leading, and F013-F018 are clearly airborne with an uneven tuck. Left as documented polish: one lockstep frame at F010, which is the intended full-extension take-off pose (arms and legs together), and the accel spikes and velocity corners at frames 6-12 and 22-26, which are the take-off and landing impacts of an explosive move and do not read as pops on the sheets. Note the clip is 33 frames (30 in the spec) after the take-off and landing retimes.


Before/after: `output/previews/jump_before_after.gif`

## punch

| Metric | iter 0 | iter 1 | iter 2 |
|---|---|---|---|
| accel_spikes | 12 | 15 | 15 |
| velocity_corners | 9 | 10 | 10 |
| loop_seam_issues | 0 | 0 | 0 |
| joint_limit_violations | 0 | 0 | 0 |
| dead_holds | 0 | 0 | 0 |
| lockstep_key_frames | 1 | 0 | 0 |
| twinned_channels | 0 | 0 | 0 |
| foot_slide_segments | 0 | 0 | 0 |
| foot_penetration_frames | 50 | 0 | 0 |
| floating_frames | None | 14 | 0 |
| overlap_score | 0.556 | 1.0 | 1.0 |

**Round 0 critique** (needs_work): The 3-frame strike (5-8) reads, but the rear foot is buried in the floor for the whole clip, the wind-up is too small to sell the cross, the extended pose freezes dead for frames 8-12 and lands at chest height, and everything arrives on frame 8 with no hip-shoulder-fist sequencing. Legs are completely static (range 0).

- `high` **awkward_pose** F[0, 24] RightFoot, LowerTorso: Rear (right) foot is under the floor on every frame: metrics lowest z -0.31 at f0, -0.44 at f8, visible in every side view as the blue toe below the floor line. Cause: RightUpperLeg rx 15 + RightLowerLeg rx 10 tilt the shin 25 deg back and RightFoot rx is 0 (15 at f8), so the toe points 25-40 deg into the ground. Left foot also sinks 0.07 (root ly -0.1). → *set_pose, set_pose, set_pose, plant_feet*
- `medium` **timing** F[0, 5] UpperTorso, LowerTorso, RightUpperArm: Wind-up is barely visible: frames 0-5 look almost identical in both views (shoulder only 10 deg back, torso -15, hips -10). The cross has no coil to unwind from, so the 146 deg/frame burst at f6 reads as a pop rather than a release. → *set_pose, set_pose, set_pose*
- `medium` **timing** F[8, 12] RightUpperArm, RightLowerArm, UpperTorso: Frames 8-12 are a dead freeze (whole-body speed 0.39-2.2 deg/frame; f8-f11 cells are identical), and the fist lands at chest height (arm exactly horizontal, rx -90) with a nearly upright torso. Needs a snap past the target and a settle, a higher fist and more commitment in the spine. → *set_pose, set_pose, set_pose, set_pose, set_pose, add_breakdown*
- `medium` **stiff** F[4, 13] LowerTorso, RightLowerArm, Head, LeftUpperArm, LeftLowerArm: overlap_score 0.556, 8 of 12 bones keyed on frame 8: hips, shoulders, elbow and head all start and stop on the same frames, so there is no kinetic chain. The left guard arm moves only 5 deg and does not counter the punch. → *offset_overlap, offset_overlap, offset_overlap, set_pose, set_pose*
- *apply_fixes:* applied 18 ops, skipped 0; saved work/punch/iter_1.blend

**Round 1 critique** (needs_work): Iteration-0 problems are fixed: no foot penetration, a readable coil at f4-5, a 3-frame strike (67/132/117 deg per frame) into a moving hold, fist at chin height, hips-chest-elbow now sequenced (overlap 1.0). The accel spikes and velocity corners are all on the strike start/stop (f5-9) and read as the intended snap, not pops. One regression blocks approval: the root now drifts upward and the whole character hovers through the strike.

- `high` **awkward_pose** F[4, 17] LowerTorso, RightFoot: Both feet are off the floor on f4-17 (both_feet_airborne_frames; lowest foot z 0.11 at f4 rising to 0.27-0.28 at f11-13; visible gap under the feet in the side view f8-f15). LowerTorso ly climbs from -0.03 to +0.27 at f12 although the legs never move, so the correct height is constant: the per-frame value that grounds the lowest foot is -0.03 on every frame (within 0.04). This was introduced by the iteration-0 plant_feet pass (it reported a max correction of 0.104 but the keys ramp to +0.27), so plant_feet is not used here. The rear foot is also 0.07 above the floor at f0/f24 with the front foot grounded; 5 deg less ankle compensation puts its toe down. → *smooth_transition, set_pose, set_pose, set_pose, set_pose, set_pose*
- *apply_fixes:* applied 6 ops, skipped 0; saved work/punch/iter_2.blend

**Round 2 critique** (approved): Approved. Both feet sit on the floor for all 25 frames (lowest z 0.00 on every frame, floating 0, penetration 0, slide 0) and the hover from iteration 1 is gone (ly flat at -0.03). Coil at f4-5, 3-frame strike (66/131/117 deg per frame), moving hold f9-12 and eased recovery all read. The 15 accel spikes and 10 velocity corners are all on f4-9, i.e. the start and stop of the strike on the arm, chest and hips, and read as the intended snap. Only polish remains.

- `low` **stiff** F[0, 24] LeftUpperLeg, LeftLowerLeg, LowerTorso: All four leg channels are constant (motion range 0) and the root height is flat, so the lower body never loads or drives the punch; the weight shift is carried only by the hip and chest twist. A small front-knee dip on the wind-up would add weight. Polish only. → *set_pose, set_pose, plant_feet*

Before/after: `output/previews/punch_before_after.gif`

## sword_slash

| Metric | iter 0 | iter 1 | iter 2 |
|---|---|---|---|
| accel_spikes | 8 | 13 | 15 |
| velocity_corners | 4 | 6 | 7 |
| loop_seam_issues | 0 | 0 | 0 |
| joint_limit_violations | 0 | 0 | 0 |
| dead_holds | 0 | 0 | 0 |
| lockstep_key_frames | 2 | 0 | 0 |
| twinned_channels | 0 | 0 | 0 |
| foot_slide_segments | 0 | 2 | 0 |
| foot_penetration_frames | 47 | 0 | 0 |
| floating_frames | None | None | 0 |
| overlap_score | 0.407 | 1.0 | 1.0 |

**Round 0 critique** (needs_work): Beat structure is sound (10-frame wind-up, 4-frame cut, follow-through, recovery) but the posing has three hard errors: the right forearm and hand pass through the head for the whole wind-up, the blade tip ends in the floor with the hand buried against the front thigh, and the rear foot is up to 0.5 studs under the floor. Everything is also keyed on frames 10/14 (overlap 0.41).

- `high` **awkward_pose** F[6, 11] RightUpperArm, RightLowerArm, RightHand: Frames 6-11: the raised right arm sits on top of the face/head in the front view. FK check of keys.json at f10 puts ~33% of the forearm and ~37% of the hand inside the head box. Cause is a sign trap: with the arm raised to rx -160, RightUpperArm rz -40 tips the UPPER end toward the character's left (into the head); rz < 0 only means 'out to the right' for a hanging arm. A positive rz carries the raised hand out past the right shoulder (clears the head completely at +25). → *set_pose, add_breakdown*
- `high` **awkward_pose** F[0, 30] RightFoot, LeftFoot, LowerTorso, LeftUpperLeg, LeftLowerLeg, RightUpperLeg, RightLowerLeg: Right foot is under the floor on all 31 frames (-0.25 at f0 to -0.51 at f17-19), left foot sinks to -0.20 at f19-20 and floats +0.05 at f10. The rear shin tilts back 20-45 deg with no ankle compensation (RightFoot is not animated), so the toe stabs down; the root then drops 0.3. Also the legs peak at f12 and start straightening immediately while the root stays lowest over f14-18, so the lunge never holds. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, plant_feet*
- `high` **awkward_pose** F[14, 21] RightUpperArm, RightHand: Frames 15-20: the arm finishes hanging at the hip (RightUpperArm rx -10, rz 25) with the wrist bent 30 deg down, so the blade tip reaches the floor (FK: tip at -0.3 studs at f18 before any root correction; front view shows the blade meeting its shadow) and the sword hand presses into the front of the left thigh. At f14 the blade still points slightly upward, so the edge does not lead the cut. End the cut forward of the body with the wrist snapping earlier. → *set_pose, set_pose, set_pose*
- `medium` **stiff** F[9, 19] LowerTorso, RightHand, Head, LeftUpperArm, LeftLowerArm: overlap_score 0.407; 8 of 12 bones are keyed on both f10 and f14, so hips, chest, arm, wrist and head all reverse on the same frame. The sword has no lag behind the arm and the hips do not lead the cut. → *offset_overlap, offset_overlap, offset_overlap, offset_overlap*
- *apply_fixes:* applied 18 ops, skipped 0; saved work/sword_slash/iter_1.blend

**Round 1 critique** (needs_work): The three posing errors are fixed: the raised arm now passes outside the head (face unobstructed f6-11; FK re-check of the iter-1 keys shows no arm or blade samples inside the head), the blade ends forward and above the floor on f15-20, and there is no foot penetration. Strike spikes at f10-15 are the intended snap. Two problems remain: the root hops during the recovery, and the feet swivel on the floor through the cut.

- `high` **transition** F[20, 28] LowerTorso, RightFoot: During the recovery the root pops up: LowerTorso ly goes -0.15 (f18) to +0.17 (f24) and back to -0.01 (f30), leaving both feet airborne on f21-27 (lowest foot z up to 0.23-0.27; visible as the body lifting in the side view f22-f25 and the hump in the ly curve). The height that actually grounds the lowest foot is a smooth dip: -0.01 at f0, -0.16 at f12-16, -0.01 at f30. Introduced by the iteration-0 plant_feet pass, so the root is re-keyed explicitly instead. The rear foot also rides a constant 0.045 above the floor; 3 deg of toe-down closes it. → *smooth_transition, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, offset_channel*
- `medium` **transition** F[9, 17] LowerTorso, UpperTorso: Planted feet slide: right foot drifts 0.34 studs over f11-15 and the left 0.22 over f0-19 (foot_slide_segments 2). The legs hang off LowerTorso, so its ry swing of -15 (f9) to +15 (f13) to +20 (f17) swivels both feet around the root while they are on the floor. Halve the pelvis twist and move the difference into the chest so the shoulder line, arm path and sword arc stay the same. → *scale_amplitude, set_pose, set_pose, set_pose*
- *apply_fixes:* applied 14 ops, skipped 0; saved work/sword_slash/iter_2.blend

**Round 2 critique** (approved): Approved. Feet are grounded on all 31 frames (max 0.01 clearance, floating 0, penetration 0, slide 0); the recovery hop and the foot swivel from iteration 1 are gone, with the twist now carried by the chest. The raised arm passes outside the head (f6-11), the blade stays clear of the head and ends forward above the floor (f15-20). The 15 accel spikes and 7 velocity corners sit on f10-15, the start and stop of the cut on the sword arm, wrist, chest and counter-swinging left arm, and read as the intended snap. Only polish remains.

- `low` **timing** F[13, 18] RightUpperArm: The sword arm stops dead at f14 (rx -160 to -40 in 4 frames, then only 5 deg of drift to f18; velocity corner 5.17 deg/frame at f14). The follow-through is carried by the chest and wrist, which works, but a small overshoot-and-settle on the shoulder would soften the stop. Polish only. → *add_breakdown*

Before/after: `output/previews/sword_slash_before_after.gif`

## hit_react

| Metric | iter 0 | iter 1 | iter 2 |
|---|---|---|---|
| accel_spikes | 7 | 6 | 3 |
| velocity_corners | 6 | 3 | 3 |
| loop_seam_issues | 0 | 0 | 0 |
| joint_limit_violations | 0 | 0 | 0 |
| dead_holds | 0 | 0 | 0 |
| lockstep_key_frames | 2 | 0 | 0 |
| twinned_channels | 5 | 0 | 0 |
| foot_slide_segments | 0 | 0 | 0 |
| foot_penetration_frames | 26 | 0 | 0 |
| floating_frames | None | None | 0 |
| overlap_score | 0.0 | 1.0 | 1.0 |

**Round 0 critique** (needs_work): The 3-frame snap back and the long settle are the right shape, but the body moves as one rigid block: every bone is keyed on frames 3 and 8 (overlap 0.0), arms and legs are perfectly mirrored, and both feet dig 0.3 studs into the floor and skate backwards at the impact.

- `high` **awkward_pose** F[1, 12] LeftUpperLeg, RightUpperLeg, LeftLowerLeg, RightLowerLeg, LowerTorso: Both feet penetrate the floor from f1 to f12, worst -0.30 at f3 (side view f2-f5: toes below the floor line). At f3 the thighs swing BACK (rx +10) with knees +10, tilting the shins 20 deg so the toes stab down, while the root slides back 0.25 studs: the feet skate backwards with the hips (moves_backward true). When the hips are knocked back the feet should stay put, i.e. thighs angle forward (rx < 0) and the shins stay vertical. Values differ left/right to break the mirror. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, plant_feet*
- `medium` **stiff** F[0, 20] LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm, UpperTorso: Five channel pairs are mirror-identical (twinning: UpperArm rx/rz, LowerArm rx, UpperLeg rx, LowerLeg rx) and the torso only pitches, so f2-f5 read as a symmetric 'surprise' pose rather than a hit. Make the blow land off-centre: twist the chest, throw the left arm wider and keep the right arm tighter. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **stiff** F[0, 10] Head, LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm: overlap_score 0.0: all 11 bones are keyed on f3 and f8, so head, chest and arms hit their extremes on the same frame and reverse together. The head should whip a frame after the chest and the arms should drag behind, forearms last. → *offset_overlap, offset_overlap, offset_overlap, offset_overlap, offset_overlap*
- *apply_fixes:* applied 21 ops, skipped 0; saved work/hit_react/iter_1.blend

**Round 1 critique** (needs_work): Much improved: the feet stay under the body instead of digging in and skating, the pose is asymmetric (chest twist, wide left arm, tight right arm) and head and arms now trail the chest (overlap 1.0, no twinning). The remaining spikes (UpperTorso rx f3, LeftUpperArm rz f4) are the snap reversing and read correctly. One regression remains: the root bobs up and down during the settle.

- `medium` **transition** F[4, 17] LowerTorso: LowerTorso ly wobbles 0 -> +0.11 (f6) -> 0 (f8) -> +0.13 (f13) -> 0, lifting both feet off the floor on f5-6 and f12-14 (lowest foot z 0.10-0.13) and producing the ly accel spikes at f3, f6 and f8. With the corrected leg poses the height that grounds the lowest foot is 0 +/- 0.012 on every frame, so the 21 per-frame keys left by the iteration-0 plant_feet pass are noise; removing them leaves the 0-valued end keys and a flat curve. → *smooth_transition, set_pose, set_pose*
- *apply_fixes:* applied 3 ops, skipped 0; saved work/hit_react/iter_2.blend

**Round 2 critique** (approved): Approved. The root bob is gone (ly flat at 0; feet within 0.03 studs of the floor on every frame, floating 0, penetration 0, slide 0). The 3-frame snap back, off-centre asymmetric pose (f3-6), trailing head and arms, forward rebound at f8-9 and eased settle to neutral all read cleanly. The three remaining accel spikes (UpperTorso rx f3, LeftUpperArm rz f4, root lz f3) are the snap reversing and are intended. No findings.


Before/after: `output/previews/hit_react_before_after.gif`

## wave

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 2 | 0 |
| velocity_corners | 0 | 0 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 0 | 0 |
| lockstep_key_frames | 2 | 0 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 0 | 0 |
| foot_penetration_frames | 0 | 0 |
| floating_frames | None | None |
| overlap_score | 0.444 | 1.0 |

**Round 0 critique** (needs_work): The wave does not read as a wave: the forearm only ever flops outward from an almost straight raised arm (hand never stacks over the elbow) and it swings twice, not the three times in the spec. Head, torso and arm all arrive and leave on frames 8 and 38 (overlap 0.44), the hand moves in phase with the forearm (no drag), and the left arm and whole lower body are frozen for 48 frames. No clipping, no foot problems, and the clip returns to idle cleanly at 48.

- `high` **awkward_pose** F[8, 38] RightUpperArm, RightLowerArm, RightHand: F008-F038: RightUpperArm.rz holds -150 while RightLowerArm.rz swings +10..+50, so the forearm's total frontal angle is -140..-100: it only bends OUTWARD/down from a near-straight arm (F012-F016 the forearm is horizontal, pointing away from the body; F020/F032 the arm is just straight). That is a sideways elbow hinge the wrong way and the hand never sits above the elbow, so the silhouette is a stiff semaphore, not a wave. Only two out-swings (keys 14 and 26) although the spec asks for three. Fix: drop the elbow out to the side (-125), fold the forearm up toward vertical (centre -40, inside the +-60 elbow rz limit) and re-key three waves of +-20 on 5-frame beats, with the hand following. → *set_pose, set_pose, smooth_transition, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **stiff** F[0, 48] Head, UpperTorso, RightUpperArm, RightLowerArm, RightHand, LeftUpperArm, LeftLowerArm: metrics: lockstep at frames 8 and 38 (5 of 6 bones keyed), overlap_score 0.444. Head turn, torso lean and the arm raise all start at 0 and stop on 8, then freeze until 38 (curves.png: three flat plateaus). The hand keys sit on the forearm keys with the same sign, so there is no wrist drag. LeftUpperArm has motion range 0 and nothing below the waist moves in any of the 49 frames, so only one arm is alive. The arm raise also stops dead at F008 (accel spike 10.1 at frames 1 and 7) with no settle. Fix: the head leads the gesture, the forearm and hand trail the upper arm, the raise overshoots and settles, the chest turns into the wave and breathes through the hold, and the free arm gets a small counter-move. → *add_breakdown, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, offset_overlap, offset_overlap, offset_overlap*
- *apply_fixes:* applied 26 ops, skipped 0; saved work/wave/iter_1.blend

**Round 1 critique** (approved): Iteration-0 problems are fixed. From F009 the forearm stands up over the elbow (upper arm -125, forearm centred on -40) and swings out at F014, F024 and F034: three clear waves, with the hand trailing 1 frame behind the forearm and staying well outside the head (F019-F021, F029-F031 are the closest frames, no contact). The raise overshoots to -133 at F008 and settles by F012, the head leads at F006, the chest and left arm now move, and the clip returns to idle at F048. All metrics are zero, overlap 1.0; the two logged clamps were no-ops at exactly -60. Nothing new was introduced. Only polish remains: the wrist flick is small.

- `low` **stiff** F[10, 40] RightHand: RightHand.rz only reaches +12/-15 (keys F015-F035), so at the 3/4 camera distance the hand reads as nearly rigid on the forearm in F014-F036; the wave is carried almost entirely by the 40-degree forearm swing. A slightly larger flick would sell the drag. Optional polish. → *scale_amplitude*

Before/after: `output/previews/wave_before_after.gif`

## dance

| Metric | iter 0 | iter 1 | iter 2 |
|---|---|---|---|
| accel_spikes | 0 | 0 | 0 |
| velocity_corners | 0 | 0 | 0 |
| loop_seam_issues | 0 | 0 | 0 |
| joint_limit_violations | 0 | 0 | 0 |
| dead_holds | 0 | 0 | 0 |
| lockstep_key_frames | 7 | 0 | 0 |
| twinned_channels | 3 | 1 | 1 |
| foot_slide_segments | 0 | 0 | 0 |
| foot_penetration_frames | 58 | 0 | 0 |
| floating_frames | None | None | 0 |
| overlap_score | 0.0 | 1.0 | 1.0 |

**Round 0 critique** (needs_work): The loop seam itself is clean (frame 64 equals frame 0, every seam key is a flat extremum, speed 5.9 deg/frame on both sides, no seam metric), but the groove is mechanical. The hip sway is a pure root translation, so both planted feet skate 0.3 studs side to side all loop; the soles sink 0.07 studs on every beat; both legs are mirror-identical; the chest leans the same way the hips shift (a plank, no counter-line); and every part hits its extremes on the same frames (overlap_score 0.0) with the forearms frozen at -90.

- `high` **transition** F[0, 64] LowerTorso, LeftUpperLeg, RightUpperLeg, LeftFoot, RightFoot: LowerTorso.lx swings +0.15 (F000/F032) to -0.15 (F016/F048) and no leg channel compensates (legs only have rx), so the whole character including both feet translates sideways: metrics show one contact segment 0-64 per foot with mean_speed 0.0232 studs/frame (0.3 studs per 16 frames) while planted. Visible in the 3/4 view as the feet drifting across the floor tiles between F000 and F016. Fix: lean both legs against the hip shift (hips left = leg ends to the character's right = UpperLeg.rz < 0, about atan(0.15/1.47) = 5.8 deg) and roll the feet back flat with the opposite Foot.rz. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `high` **awkward_pose** F[0, 64] LeftUpperLeg, LeftLowerLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot, LowerTorso: metrics: 58 foot-penetration frames; both feet are 0.070 studs under the floor on every down-beat (F000, F016, F032, F048, F064; side view F013-F019 and F029-F035 shows the sole below the floor line). The root drops 0.15 studs but thigh -20 / knee 35 only shortens the leg about 0.08. The bounce also reads small for a 'bouncy groove'. Fix: deepen the knee action 1.4x (thigh -28, knee 49, foot -21 still cancel to a flat foot) so the legs really absorb about 0.15 studs, then re-plant the root on the floor. → *scale_amplitude, plant_feet*
- `medium` **stiff** F[0, 64] LeftUpperLeg, LeftLowerLeg, RightUpperLeg, RightLowerLeg, UpperTorso: metrics twinning: Upper/LowerLeg and Foot rx are mirror-identical for the whole loop, so the hip sway never becomes a weight shift, and all four beats are the same pose. UpperTorso.rz is -8 (top tips to the character's LEFT) exactly when the hips are shifted LEFT (F000/F032) and +8 when they are right (F016/F048): hips and chest go the same way, the body tilts as one plank and there is no opposing hip/shoulder line. Fix: on each beat sink further into the unweighted leg (right leg when hips are left at 0/32/64, left leg at 16/48; foot keys untouched so that foot rolls onto its toe by about 4 deg), and reverse the chest tilt so the shoulders counter the hips. → *scale_amplitude, scale_amplitude, scale_amplitude, scale_amplitude, scale_amplitude, scale_amplitude*
- `medium` **stiff** F[0, 64] UpperTorso, Head, LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm: metrics: overlap_score 0.0, lockstep on frames 8/16/24/32/40/48/56 (up to 11 of 13 bones keyed together). Head nod, chest tilt, arm pumps and knee bounce all peak on the same frame, so nothing drags or follows through (curves.png: every curve is the same phase-locked sine). Left/RightLowerArm.rx is a constant -90 (motion range 0): the pumps come from the shoulder only and the elbows look welded (F000-F064, side view: the forearm-upper-arm angle never changes). Fix: open the elbow to -65 when the arm is back and close it to about -95 when it punches forward, then offset chest, head, upper arms and forearms progressively later than the hips; finally re-close the seam and make every curve cyclic so the offsets wrap cleanly. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, offset_overlap, offset_overlap, offset_overlap, offset_overlap, smooth_transition*
- *apply_fixes:* applied 36 ops, skipped 0; saved work/dance/iter_1.blend

**Round 1 critique** (needs_work): Most iteration-0 problems are fixed: the sideways foot skate is gone (foot centre x moves 0.02 studs instead of 0.30), the feet no longer sink (lowest z -0.005..+0.015, 0 penetration frames), the legs alternate a deeper off-leg bend, the chest now counters the hips, the elbows work and the overlap score is 1.0. The loop seam is still clean (F063 -> F064/F000 continuous on every curve, speeds match the other beats). One problem remains, and my 1.4x knee scale made it worse: the planted feet now skate forward and back about 0.14-0.15 studs on every beat. Foot.rx is still mirror-identical left/right (the one remaining twinned channel), which is harmless for flat planted feet.

- `medium` **transition** F[0, 64] LeftUpperLeg, RightUpperLeg, LeftFoot, RightFoot, LowerTorso: Side view, F000 vs F008 vs F016 (and every beat after): both feet shift forward on each down-beat and back on each up-beat while staying on the floor. Measured in the iter_1 blend, foot centre moves from y -0.168 at F008/F024 to -0.304 (weighted leg) and -0.318 (off leg) at F000/F016/F032: 0.14-0.15 studs every 8 frames (it was 0.10 in iteration 0; metrics still show mean_speed 0.018 studs/frame in a single 0-64 contact segment). Cause: thigh -28 / knee 49 puts the ankle 0.9*sin(28) - 0.75*sin(21) = 0.15 studs ahead of the hip. Fix: keep the knee bend but share it so the ankle stays under the hip (0.9*sin(thigh) = 0.75*sin(knee - thigh)): thighs x0.79 (-28 -> -22, -33.6 -> -26.5, -7 -> -5.5) and feet x1.29 (-21 -> -27, -7 -> -9) so the weighted foot stays flat and the off foot keeps its 5-degree toe roll; then re-plant, since the legs get about 0.02 studs shorter at the bottom of the bounce. → *scale_amplitude, scale_amplitude, plant_feet*
- *apply_fixes:* applied 3 ops, skipped 0; saved work/dance/iter_2.blend

**Round 2 critique** (approved): Approved. The fore-aft foot skate is fixed: measured in the iter_2 blend, foot centre y stays within -0.128..-0.151 over the whole loop (0.023 studs, was 0.15) and x within 0.02, with mean contact speed 0.003 studs/frame (was 0.018). Lowest foot z is -0.0005..+0.009, so no sinking or floating, and the bounce is still about 0.13 studs. Side view F000/F008/F016/F032: the feet stay put while the knees work. The seam is continuous (F063 -> F064 = F000 on every curve). Weight shift, counter-tilted chest, working elbows and offset head/arms all survive from iteration 1; fists stay 1.34+ studs from the head centre. The only metric left is Foot.rx twinning, which is correct for two flat planted feet. Remaining polish, not worth another pass: the bounce is an even sine, so the down-beat does not hit harder than the up-beat.


Before/after: `output/previews/dance_before_after.gif`

## cheer

| Metric | iter 0 | iter 1 | iter 2 |
|---|---|---|---|
| accel_spikes | 8 | 9 | 7 |
| velocity_corners | 4 | 4 | 6 |
| loop_seam_issues | 0 | 0 | 0 |
| joint_limit_violations | 0 | 0 | 0 |
| dead_holds | 0 | 0 | 0 |
| lockstep_key_frames | 2 | 4 | 2 |
| twinned_channels | 7 | 3 | 3 |
| foot_slide_segments | 0 | 0 | 0 |
| foot_penetration_frames | 52 | 0 | 0 |
| floating_frames | None | None | 0 |
| overlap_score | 0.447 | 0.595 | 0.814 |

**Round 0 critique** (needs_work): Good crouch-to-burst structure, but the two fist pumps fold both forearms 60 deg inward from near-vertical upper arms, so the fists close over the top corners of the head, and the toes dip up to 0.21 studs through the floor on both pumps (0.09 in the crouch). All 13 bones are keyed together on 6 and 12, left and right are mirror-identical on 7 channels, and the head and chest freeze from 12 to 40. Note: the clip ends in the V pose as the spec asks ('then a hold'), so it relies on the engine fade-out to return to idle.

- `high` **awkward_pose** F[15, 33] LeftLowerArm, RightLowerArm, LeftUpperArm, RightUpperArm, Head: F016-F020 and F028-F033 (3/4 view): with UpperArm.rz at +-165 (15 deg off vertical) the pump is done purely with LowerArm.rz +-60, which swings each forearm 45 deg past vertical toward the midline; the forearms and fists cover and intersect the upper corners of the head (head half-width 0.6 studs, hand inner edge reaches about 0.35) and the V collapses into a diamond over the face. The upper arms do not move at all during the pumps (rz 165 -> 160 drift). Fix: make it a real pump: the elbows drop out to +-135 on each pump while the forearms fold only +-45, which leaves them vertical outside the head ('goalpost'), then punch back up to the +-165 V. → *scale_amplitude, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `high` **awkward_pose** F[2, 39] LeftFoot, RightFoot, LowerTorso: metrics: 52 penetration frames; lowest foot z -0.09 in the crouch (F002-F009) and -0.21 on both pumps (F015-F021, F027-F039). Side view F016-F020 and F028-F034: the toes point down through the floor line. Cause: on the pumps the thigh is -10 and the knee +20, tilting the shin 10 deg, but Foot.rx stays 0 (keys only at 0/6/12/40) so the foot pitches toe-down 10 deg; the root also drops 0.1 studs, more than the legs shorten. The burst frames F011-F013 and F023-F025 float 0.03-0.05 studs instead. Fix: counter-rotate the feet on the pump keys so the soles stay flat, then re-plant the root on the floor for the whole clip. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, plant_feet*
- `medium` **stiff** F[6, 40] Head, UpperTorso, LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm: metrics: lockstep at frames 6 and 12 with 13 of 13 bones keyed, overlap_score 0.447, twinning on 7 channels (both arms rx/rz, both legs). The arms, chest, head and legs all hit the top of the burst on F012 and stop together (accel spikes 15 on UpperArm.rz at F011-F012, no settle), the two arms are perfect mirrors on every frame, and Head.rx (-15) and UpperTorso.rx are frozen from F012 to F040 while the arms pump (curves.png: flat lines). Fix: let the chest arch overshoot and settle after the burst, nod the head with each pump, add a small alternating chest twist so the pumps are not symmetric, and drag the arms behind the body (right arm 1 frame, left arm 2; forearms 2 more) with the head 2 frames late. → *add_breakdown, set_pose, set_pose, set_pose, set_pose, set_pose, offset_overlap, offset_overlap, offset_overlap, offset_overlap, offset_overlap*
- *apply_fixes:* applied 25 ops, skipped 0; saved work/cheer/iter_1.blend

**Round 1 critique** (needs_work): The head clipping is fixed: on both pumps (F019-F022, F031-F035) the elbows drop out to +-135 and the forearms stand vertical outside the head; the closest forearm vertex stays 1.36 studs from the head centre. Foot penetration is gone (0 frames, worst -0.015). The arms now trail the body by 1-4 frames and the left and right arms are no longer twinned. Three things remain: the feet skate 0.2 studs forward and back in the crouch (present in iteration 0, I missed it), the re-plant left both feet hovering 0.07-0.08 studs during the final settle (F033-F037), and the legs, root and chest still share keys on 6/12/18/30 (overlap 0.595). The fast arm thrust is the source of the accel-spike metrics; it reads as an intended snap, so it is polish only. The clip still ends in the V pose, as the spec asks.

- `medium` **transition** F[0, 12] LeftUpperLeg, RightUpperLeg, LeftFoot, RightFoot: Side view F000 -> F006 -> F012: both planted feet slide forward under the body in the crouch and back again in the burst. Measured in the iter_1 blend, foot centre y goes -0.150 (F000) -> -0.349 (F006) -> -0.150 (F012): 0.2 studs each way in 6 frames. Cause: thigh -35 / knee 60 at F006 puts the ankle 0.9*sin(35) - 0.75*sin(25) = 0.2 studs ahead of the hip. Fix: same knee bend with the thigh at -27 so the ankle stays under the hip (0.9*sin(27) = 0.75*sin(33)), and the foot at -33 to stay flat (-27 + 60 - 33 = 0). → *set_pose, set_pose, set_pose, set_pose*
- `medium` **awkward_pose** F[32, 38] LowerTorso, LeftFoot, RightFoot: Introduced by the iteration-0 re-plant: LowerTorso.ly was keyed +0.07 at F034 and F036 (curves.png: the purple bump at the end), so both feet lift off the floor with flat soles while the knees are still bent: lowest foot z is +0.038 at F032, +0.066 at F033, +0.078 at F034, +0.074 at F035, +0.071 at F036, +0.053 at F037 (both feet lose contact at F033-F036 per the contact segments). It reads as an unmotivated float in the final settle. Smaller floats of 0.02-0.04 sit at F008-F010 and F020-F022. Every even frame now carries a root key, so a second plant pass corrects those keys exactly instead of inserting new ones. → *plant_feet*
- `medium` **stiff** F[6, 30] UpperTorso: metrics: lockstep on frames 6, 12, 18 and 30 (8 of 13 bones: both legs, both feet, the root and the chest), overlap_score 0.595. The legs and root have to move together to keep the feet planted, but the chest lean (UpperTorso.rx keys 6/12/16) and twist (ry keys 18/30) change direction on exactly the same frames as the knees, so the spine has no drag behind the hips in the crouch (F006) or the burst (F012). Fix: let the chest follow the hips by one frame. → *offset_overlap*
- `low` **timing** F[7, 16] LeftUpperArm, RightUpperArm: metrics: 8 accel spikes of 10-15 deg/frame^2 and 4 velocity corners on UpperArm.rz around the thrust (right arm keys 7 -> 13, left 8 -> 14). The arms cover 145 degrees in 6 frames and stop dead at 165 (F012-F014 in the 3/4 view), then reverse into the first pump. The speed suits a cheer; only the start and stop are abrupt. Optional polish: lightly round the thrust without re-timing it. → *smooth_transition*
- *apply_fixes:* applied 7 ops, skipped 0; saved work/cheer/iter_2.blend

**Round 2 critique** (approved): Approved. All three iteration-1 problems are fixed. Crouch skate: foot centre y stays within -0.147..-0.176 for the whole clip and is flat at -0.15 through F000-F012 (was a 0.2-stud slide). Hover: lowest foot z is within +-0.001 on every frame, floating 0, penetration 0 (the LowerTorso.ly bump at F034-F036 is gone). Lockstep: overlap_score is 0.814; the chest now trails the hips by a frame. The head clipping stays fixed (closest forearm vertex 1.36 studs from the head centre on F025-F026; F019-F022 and F031-F035 show the forearms vertical outside the head). What the metrics still show is not a visible defect: the 2 lockstep frames (6 and 12) come from the per-frame arm keys the smoothing pass wrote on F006-F016 coinciding with the leg keys, not from parts stopping together; the 6 accel spikes (10-12.6, down from 15) and 6 small velocity corners are the 6-frame arm thrust, which should snap; the leg twinning is a symmetric two-footed crouch. Not changed, by design: the clip ends in the V pose as the spec asks, so it relies on the engine fade-out to return to idle.


Before/after: `output/previews/cheer_before_after.gif`

