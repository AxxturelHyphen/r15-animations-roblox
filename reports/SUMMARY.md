# Critic loop summary

Each animation went through: build → render/analyze → Fable 5.2 critique → automatic F-curve fixes → re-render, until the critic approved it (no high- or medium-severity findings). The planned cap was 3 critique rounds; `death` needed a 4th, verification-only round, because its round-3 fix had only been dry-run.

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
| fall | 2 | approved | r0: 0/2/1 · r1: 0/0/1 | 5/6/5/8/4 → 8/7/7/8/7 |
| climb | 2 | approved | r0: 1/3/0 · r1: 0/0/1 | 5/3/4/8/4 → 8/8/7/8/7 |
| swim | 3 | approved | r0: 1/2/1 · r1: 0/1/0 · r2: 0/0/1 | 6/3/6/8/4 → 8/8/7/8/7 |
| swim_idle | 3 | approved | r0: 0/3/1 · r1: 0/1/1 · r2: 0/0/1 | 5/5/6/8/4 → 8/7/7/8/7 |
| sit | 2 | approved | r0: 0/2/1 · r1: 0/0/1 | 4/5/6/9/4 → 7/8/7/9/6 |
| block | 3 | approved | r0: 2/1/0 · r1: 0/1/0 · r2: 0/0/0 | 4/3/5/7/3 → 7/8/7/9/7 |
| kick | 2 | approved | r0: 2/3/0 · r1: 0/0/1 | 5/5/6/3/5 → 8/8/8/8/8 |
| combo | 2 | approved | r0: 1/2/0 · r1: 0/0/0 | 5/5/4/3/5 → 8/8/8/8/8 |
| death | 4 | approved | r0: 1/3/0 · r1: 0/1/0 · r2: 0/1/0 · r3: 0/0/0 | 5/3/4/5/4 → 8/8/8/8/7 |
| point | 2 | approved | r0: 0/3/1 · r1: 0/0/0 | 4/5/4/6/4 → 7/7/8/8/7 |
| laugh | 2 | approved | r0: 1/1/1 · r1: 0/0/0 | 5/3/4/6/4 → 7/7/7/8/7 |
| clap | 2 | approved | r0: 1/1/0 · r1: 0/0/0 | 4/2/5/6/3 → 6/7/7/8/6 |
| salute | 2 | approved | r0: 1/2/0 · r1: 0/0/0 | 4/3/5/6/4 → 7/8/7/8/7 |
| crouch_idle | 2 | approved | r0: 1/3/0 · r1: 0/0/2 | 4/5/4/6/3 → 7/8/7/8/7 |
| crouch_walk | 2 | approved | r0: 2/3/0 · r1: 0/0/2 | 5/3/4/4/4 → 8/8/8/8/7 |

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

## fall

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 0 | 0 |
| velocity_corners | 0 | 0 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 0 | 0 |
| lockstep_key_frames | 1 | 0 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 0 | 0 |
| foot_penetration_frames | 0 | 0 |
| floating_frames | 0 | 0 |
| overlap_score | 0.0 | 1.0 |

**Round 0 critique** (needs_work): Clean loop with no pops, but it reads as a held 'hands up' pose that breathes rather than a fall: every bone is keyed on 0/12/24 and the arms only move 12-15 deg. Fixes: turn the arm motion into a real circular flail, stagger forearms, shins, feet and head, and add a counter-twist through the torso. The blend from jump is fine (similar leg tuck, arms already raised).

- `medium` **stiff** F[0, 24] LeftUpperArm, RightUpperArm: The spec asks for arms 'waving for balance', but on the sheets F000 and F012 are almost the same silhouette and the onion skin shows a single arm shape. UpperArm.rz moves only 15 deg (left) and 12 deg (right), UpperArm.rx is a flat -10, so the hands travel on a short straight line in one plane. The arm amplitude is doubled and an out-of-phase forward/back swing is added on rx (left forward at 6, back at 18; right the opposite), which makes each hand trace a loop instead of a line. → *scale_amplitude, set_pose, set_pose, set_pose, set_pose*
- `medium` **stiff** F[0, 24] LeftLowerArm, RightLowerArm, LeftLowerLeg, RightLowerLeg, Head, LeftFoot, RightFoot: metrics: overlap_score 0.0, 11 of 13 bones keyed on frame 12, and whole-body speed drops to 2.5 deg/frame on frames 0, 11, 12 and 23, so the whole body stops and reverses together twice per loop. Both feet are frozen (Foot.rx range 0). Forearms are delayed 3 frames, shins 2, head 3, and the feet get a loose dangle on different frames, so no frame has everything at rest. → *offset_overlap, offset_overlap, offset_overlap, set_pose, set_pose*
- `low` **stiff** F[0, 24] UpperTorso, LowerTorso: The trunk is a rigid column: LowerTorso.rx moves 2 deg and UpperTorso.rx 3 deg, with no twist, so the flailing arms do not act on the body (side view F000-F024, the teal blocks never move). A chest counter-twist (ry -7 at 6, +7 at 18, against the arm that swings forward) and double the rock on rx are added. → *set_pose, set_pose, scale_amplitude*
- *apply_fixes:* applied 13 ops, skipped 0; saved work/fall/iter_1.blend

**Round 1 critique** (approved): Approved. The arms now trace loops (hands swing about 1 stud forward and back as well as up and down), forearms, shins, head and feet are staggered, and the chest counter-twists; metrics are all 0 with overlap 1.0, the seam is closed and no parts intersect on any frame. It reads as a loose flailing fall on sheets F000-F024. One low polish item remains.

- `low` **timing** F[0, 8] RightFoot: RightFoot.rx goes 25 -> 38 in the first 4 frames and then takes 20 frames to drift back (curves.png), so the right foot flicks faster than anything else in the clip. It is below the pop threshold and hard to see at game distance. Moving the peak to frame 8 would even it out. → *retime*

Before/after: `output/previews/fall_before_after.gif`

## climb

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 0 | 0 |
| velocity_corners | 0 | 0 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 0 | 0 |
| lockstep_key_frames | 1 | 0 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 0 | 0 |
| foot_penetration_frames | 0 | 0 |
| floating_frames | 0 | 0 |
| overlap_score | 0.143 | 1.0 |

**Round 0 critique** (needs_work): Seamless and pop-free, but the pose does not sell a truss in front of the character: the reaching hand ends up directly above the shoulder and the hands drift 0.7 studs in depth, so it reads as marching on the spot with the arms overhead. Timing is one pure sine with every limb keyed on frame 15. Fixes: re-pose both arms and legs so hands and feet stay in the truss plane, give the reach a fast move plus a grip hold, let the feet follow the hands, and loosen the torso and head.

- `high` **awkward_pose** F[0, 30] LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm: Measured on the rig: at F000 the reaching left hand is only 0.12 studs in front of the root at height 5.72 (straight above the shoulder), while the pulling right hand is 0.84 in front at 5.10; they swap by F015. So each hand slides 0.7 studs toward and away from the truss every cycle, and both stay above the head (vertical travel only 0.6). Cause: UpperArm.rx -160 plus elbow -40 puts the forearm at -200 deg, i.e. tilted backward past vertical. Side view F000-F004: the orange forearm leans back over the head. New poses: reach = UpperArm -150 / elbow -10, pull = UpperArm -72 / elbow -95 (elbow tucked beside the ribs). Checked with the chest twist below: both hands sit 1.22-1.28 studs in front at each end of the stroke and travel 1.1 studs vertically (4.47 to 5.57), with no part intersections on any frame. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **awkward_pose** F[0, 30] LeftUpperLeg, RightUpperLeg, LeftLowerLeg, RightLowerLeg: The feet also wander in depth: the low foot is 0.34 studs in front of the root and the high foot 0.70 (F000 vs F015), so the feet pedal a circle under the body instead of stepping on rungs in front. The low leg now reaches forward (thigh -36, knee 28) and the high leg is thigh -88, knee 110, which keeps both feet 0.78-0.88 in front through the whole cycle. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **timing** F[0, 30] LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm, LeftUpperLeg, RightUpperLeg, LeftLowerLeg, RightLowerLeg, LeftFoot, RightFoot: Every limb is a single sine keyed on 0/15/30 (metrics: overlap_score 0.143, 12 of 13 bones keyed on frame 15; whole-body speed 5.7 deg/frame at frames 0, 14, 15, 29 and 44.7 mid-way). Hand and foot start, peak and stop on identical frames, and there is no moment where a hand grips: reach and pull take the same 15 frames. A breakdown near the top of each reach (left arm frame 25, right arm frame 10) makes the reach take about 10 frames and then hold on the rung for about 5, and the legs are delayed 3 frames so each foot steps just after the opposite hand has landed. → *add_breakdown, add_breakdown, add_breakdown, add_breakdown, offset_overlap*
- `medium` **stiff** F[0, 30] UpperTorso, LowerTorso, Head: Head.rx is a flat -15 and UpperTorso.rx a flat 5 for the whole loop; the only trunk motion is an 8 deg twist that goes the wrong way (ry +4 at F000 turns the chest left, pulling the reaching left shoulder away from the truss). The twist is reversed and slightly enlarged (-5 at 0, +5 at 15, reaching shoulder forward), the head counter-turns with a 2-frame lag so the face stays on the truss, the hips shift over the pushing leg (lx -0.08 at 7, +0.08 at 22) and the push-up bob grows from 0.10 to 0.15 studs. → *scale_amplitude, set_pose, set_pose, scale_amplitude, set_pose, set_pose, offset_overlap*
- *apply_fixes:* applied 28 ops, skipped 0; saved work/climb/iter_1.blend

**Round 1 critique** (approved): Approved. Verified on the rig: both hands stay 1.22-1.47 studs in front of the root through the whole cycle (1.22-1.28 at the top and bottom of each stroke) and travel 1.1 studs vertically (4.47 to 5.57); feet stay 0.79-0.88 in front. The reach now lands by about frame 10/25 and holds on the rung, the feet follow 3 frames later, and the chest turns the reaching shoulder toward the truss. Metrics all 0, overlap 1.0, no intersections, seam closed. Side view F000-F030 reads clearly as hand-over-hand on a truss in front. One low polish item remains.

- `low` **stiff** F[0, 30] Head: Head.rx is still a flat -15 for the whole loop; only the small counter-turn on ry moves the head. A slight extra look-up as each hand lands would add life, but it is not noticeable at game distance. → *set_pose, set_pose*

Before/after: `output/previews/climb_before_after.gif`

## swim

| Metric | iter 0 | iter 1 | iter 2 |
|---|---|---|---|
| accel_spikes | 0 | 8 | 0 |
| velocity_corners | 0 | 0 | 0 |
| loop_seam_issues | 0 | 0 | 0 |
| joint_limit_violations | 0 | 0 | 0 |
| dead_holds | 0 | 0 | 0 |
| lockstep_key_frames | 3 | 0 | 0 |
| twinned_channels | 0 | 0 | 0 |
| foot_slide_segments | 0 | 0 | 0 |
| foot_penetration_frames | 0 | 0 | 0 |
| floating_frames | 0 | 0 | 0 |
| overlap_score | 0.362 | 1.0 | 1.0 |

**Round 0 critique** (needs_work): The loop is smooth and the kick is fine, but the stroke is not a crawl: the recovering arm swings back to the front underneath the body, on the same path as the pull, so each arm is a pendulum and both hands hang below the chest at the same time. The forearm also passes through the head. Fixes: route the recovery out to the side and over the water with UpperArm.ry, add a real body roll timed to it, widen the breath, and stagger forearms and shins.

- `high` **awkward_pose** F[0, 40] LeftUpperArm, RightUpperArm: The spec intends 'recovery out to the side' and keys UpperArm.rz 80 at the recovery mid-point, but at that key rx is -90, so the arm already points along the rz axis and rz only twists it. Measured: at F030 the recovering left hand is at height 0.74, about 1.3 studs BELOW the body and under the chest (x +0.77, then +0.16 at F035), at the same height as the pulling right hand (0.76). The same happens to the right arm at F010. On the sheets F006-F010 (blue) and F026-F030 (orange) show the recovering arm hanging straight down. The forearm then cuts through the head: Head x RightLowerArm intersect on F015-F016 and Head x LeftLowerArm on F035. Fix: drop the rz twist at the mid-point and swing the arm out with ry instead (left +85/+88/+85 at 25/30/35, right -85/-88/-85 at 5/10/15; ry does nothing at the ends, where the arm lies along the body). Checked: the left hand now goes 1.95 (hip, F020) -> 2.62 (F025) -> 3.78 (F030, above the back) -> 3.43 (F035) -> entry, and no parts intersect on any frame. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **timing** F[0, 40] LowerTorso, UpperTorso: The only roll is UpperTorso.ry +/-15, and it peaks on frames 0 and 20, when one arm is entering and the other finishing; at the middle of each recovery (F010, F030) the chest is flat (ry 0). In a crawl the shoulder of the recovering arm is highest mid-recovery. The chest roll is shifted 10 frames earlier (peak +10.5 at F030 with the left shoulder up, -10.5 at F010) and a hip roll is added on LowerTorso.rz (+10 at 30, -10 at 10; for the prone body rz is the roll about its long axis). Amplitudes are kept moderate because the raised head sits about 1.1 studs off the roll axis and would otherwise wag sideways. → *set_pose, set_pose, scale_amplitude, offset_overlap*
- `medium` **timing** F[20, 36] Head: The breath is a 10-frame blip: Head.ry goes 0 -> 30 -> 0 on frames 20/25/30 with no hold, and 30 deg does not get the face out of the water (F024-F027, front view: the face still points forward and down). It now turns to 45 by F025, holds 35 at F030 and returns by F036, riding on the body roll, and counter-turns +12 at F010 so the face stays down while the body rolls the other way. → *set_pose, set_pose, set_pose, set_pose*
- `low` **stiff** F[0, 40] LeftLowerArm, RightLowerArm, LeftLowerLeg, RightLowerLeg: metrics: overlap_score 0.362, with 9-11 of 13 bones keyed on frames 10, 20 and 30. Elbows change direction on exactly the same frames as the shoulders, and knees with the hips, so the limbs move as rigid sticks. Forearms and shins are delayed 2 frames for drag in the pull and a whip in the flutter kick. → *offset_overlap, offset_overlap*
- *apply_fixes:* applied 20 ops, skipped 0; saved work/swim/iter_1.blend

**Round 1 critique** (needs_work): The stroke is now a real crawl. Verified on the rig: the recovering hand rises from 1.95 at the hip (F020) to 3.78 above the back (F030) and enters at about 3.2, while the other hand pulls underneath (0.30 at F030); the head/forearm intersections are gone (no intersections on any frame), the roll peaks mid-recovery and the breath holds. One regression from my own fix keeps it from approval: the shoulder twist that sets up the recovery snaps on and off.

- `medium` **transition** F[0, 40] LeftUpperArm, RightUpperArm: metrics: 8 accel spikes of 11-12 deg/frame^2, all on UpperArm.ry (left at frames 21, 24, 36, 39; right at 1, 4, 16, 19). The ry keys I added go 0 -> 85 in 5 frames at the start of each recovery and 85 -> 0 in 5 frames at entry (curves.png: a square-shouldered plateau). At those moments the arm lies along the body, so ry is almost pure twist: the square arm blocks spin about 85 deg in 5 frames as the hand leaves the hip and again as it enters (front view F020-F024 orange, F036-F039 orange; F000-F004 and F016-F019 blue). Fix: pre-load the twist. ry is set to +/-35 at the entry and exit keys (frames 0/40 and 20) and returned to 0 at the middle of the pull (left frame 10, right frame 30), so the fast part of the ramp shrinks from 85 to 50 deg. Dry-run on iteration 1: no accel spikes remain, no intersections on any frame, the recovery arc is unchanged (left hand 2.62 at F025, 3.78 at F030, 3.43 at F035), and the pull still passes under the body (hand x +0.90 at F010) with a slight outward sweep at catch and exit. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- *apply_fixes:* applied 6 ops, skipped 0; saved work/swim/iter_2.blend

**Round 2 critique** (approved): Approved. The shoulder-twist snap is gone: UpperArm.ry now ramps through a pre-loaded +/-35 (curves.png shows a rounded rise instead of the square step) and metrics report 0 accel spikes, 0 corners, overlap 1.0. Re-checked on the rig at iteration 2: the recovery arc is intact (left hand 1.93 at the hip on F020, 2.62 on F025, 3.78 above the back on F030, 3.43 on F035, entry about 3.2), the pull still passes under the body (hand x +0.90, height 0.30 on F010), no parts intersect on any frame and the seam is closed. Sheets F000-F040 read as an alternating front crawl with roll and a held breath to the left. One low polish item remains.

- `low` **stiff** F[0, 40] LeftFoot, RightFoot: Foot.rx is a flat 40 on both feet for the whole loop (curves.png), so the flutter kick ends in rigid pointed feet with no flick. With a 10-frame kick and feet this small it is not noticeable at game distance. A small amplitude on the foot, following the shin, would finish the whip. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*

Before/after: `output/previews/swim_before_after.gif`

## swim_idle

| Metric | iter 0 | iter 1 | iter 2 |
|---|---|---|---|
| accel_spikes | 0 | 0 | 0 |
| velocity_corners | 0 | 0 | 0 |
| loop_seam_issues | 0 | 0 | 0 |
| joint_limit_violations | 0 | 0 | 0 |
| dead_holds | 0 | 0 | 0 |
| lockstep_key_frames | 1 | 2 | 0 |
| twinned_channels | 0 | 3 | 0 |
| foot_slide_segments | 0 | 0 | 0 |
| foot_penetration_frames | 0 | 0 | 0 |
| floating_frames | 0 | 0 | 0 |
| overlap_score | 0.609 | 0.628 | 1.0 |

**Round 0 critique** (needs_work): Seamless and calm, but it does not read as treading water. Both upper arms twist the same way, so the hands swing left and right together like a steering wheel instead of sculling in and out; the elbows and feet are frozen; and the 'eggbeater' is a straight forward/back pedal. Fixes: mirror the right arm, add forearm sweep with drag, make the thighs circle, and enlarge the bob and the chest motion.

- `medium` **awkward_pose** F[0, 60] RightUpperArm, LeftUpperArm: LeftUpperArm.ry and RightUpperArm.ry carry identical keys (+20 at 0/30, -20 at 15/45). Positive ry turns toward the character's left for both arms, so the left hand sweeps out while the right sweeps in. The rz keys are also offset (left 50 at F000 while right is -60). Measured at F000: left hand x +2.66 / height 3.30, right hand x -2.20 / height 2.65; they swap at F015. On the sheets the blue arm is thrown wide while the orange one is folded in (F000), then the reverse (F012-F016). The right arm's ry and rz are mirrored and the scull is enlarged to +/-30. Checked: hands are at x +/-2.78 on F000 and F030 and sweep in to about +/-1.8 on F015. → *scale_amplitude, scale_amplitude, scale_amplitude*
- `medium` **stiff** F[0, 60] LeftLowerArm, RightLowerArm: LowerArm.rx is a flat -60 on both sides for all 60 frames, so the scull comes from the shoulder only and the arm moves as one bent bar (front view F000-F059: the elbow angle never changes). The elbows now open to about -52 on the out-sweep and close to -76 on the in-sweep, delayed 3 frames behind the upper arm. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, offset_overlap*
- `medium` **stiff** F[0, 60] LeftUpperLeg, RightUpperLeg: The legs only move on rx (thigh 20 deg, knee 40 deg) with UpperLeg.rz fixed at +/-15, so each foot goes straight up and down (side view: the feet trace a vertical line; lowest-foot height just oscillates). An eggbeater kick circles. rz keys are added a quarter cycle off the rx keys (left 25/8 at 8/23/38/53, right mirrored and opposite), so each knee traces an ellipse. No intersections on any frame. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `low` **stiff** F[0, 60] LowerTorso, UpperTorso, Head: The bob is 0.08 studs and UpperTorso.rx moves 2 deg, both too small to see at game distance (onion skin: one torso outline), and the chest and head turn exactly on the key frames 0/30/60. The bob is doubled, the chest motion enlarged with a slow +/-4 twist, and the chest and head are delayed 3 and 5 frames. → *scale_amplitude, scale_amplitude, set_pose, set_pose, offset_overlap, offset_overlap*
- *apply_fixes:* applied 24 ops, skipped 0; saved work/swim_idle/iter_1.blend

**Round 1 critique** (needs_work): Much better: the scull is now symmetric (hands at x +2.78/-2.78 on F000, sweeping in to about +/-1.8 on F015), the elbows open and close with drag, the knees circle and the bob is visible. No pops, seam closed, no intersections. What remains is mechanical regularity: the two arms are exact mirror images on every frame, most of the body still changes direction on frames 15 and 45, and the feet are still frozen.

- `medium` **stiff** F[0, 60] RightUpperArm, RightLowerArm, LeftLowerLeg, RightLowerLeg: metrics: twinning on UpperArm.ry, UpperArm.rz and LowerArm.rx (left and right are mirror-identical on every frame), lockstep with 8 of 13 bones keyed on frames 15 and 45, overlap_score 0.628 (below the 0.75 bar). On the sheets the two arms reach their widest (F000, F030) and closest (F015-F018, F045-F048) on exactly the same frames, which reads as a machine rather than someone treading water. Mirrored sculling is correct, so the shape is kept; only the timing is loosened: the whole right arm is delayed 2 frames and both shins 2 frames behind the thighs. Dry-run on iteration 1: no twinned channels, no frame with 7 or more bones keyed, no pops, no intersections; hands stay within 0.1 stud of symmetric (x +2.78/-2.70 on F000). → *offset_overlap, offset_overlap*
- `low` **stiff** F[0, 60] LeftFoot, RightFoot: Foot.rx is a flat 20 on both feet for all 60 frames (curves.png), so the kick ends in rigid paddles. The feet now point (34) about 3 frames after each knee extends and relax (16) as it bends, opposite on the two sides. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- *apply_fixes:* applied 10 ops, skipped 0; saved work/swim_idle/iter_2.blend

**Round 2 critique** (approved): Approved. The mechanical regularity is gone: the right arm now trails the left by 2 frames, the shins trail the thighs, and the feet point and relax after each knee (Foot.rx 16-34, opposite on the two sides). Metrics report 0 twinned channels, 0 lockstep frames, overlap 1.0 and no pops. Re-checked on the rig at iteration 2: the scull is still symmetric in shape (hands at x +2.78/-2.70 on F000, about +1.9/-1.8 on F015), no parts intersect on any frame and the seam is closed. Sheets F000-F060 read as treading water: hands scull in and out, knees circle, body bobs. One low polish item remains.

- `low` **stiff** F[0, 60] Head: Head.rx is a flat -12 for all 60 frames (curves.png); only the slow 10 deg turn on ry moves the head, so it does not react to the bob. A 2-3 deg nod trailing the bob would add life, but it is not visible at game distance. → *set_pose, set_pose, set_pose*

Before/after: `output/previews/swim_idle_before_after.gif`

## sit

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 0 | 0 |
| velocity_corners | 0 | 0 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 0 | 0 |
| lockstep_key_frames | 0 | 0 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 0 | 0 |
| foot_penetration_frames | 0 | 0 |
| floating_frames | 0 | 0 |
| overlap_score | 1.0 | 1.0 |

**Round 0 critique** (needs_work): A clean, seamless seated pose with correct thigh and shin angles, but the hands do not rest on the thighs as specified and the clip is close to a still image: peak whole-body speed is 2 deg/frame and the whole left side never moves. Fixes: bring the forearms in onto the thighs, enlarge the breathing and carry it into the arms, add a small weight shift and left-leg fidget, and give the look-around a hold.

- `medium` **awkward_pose** F[0, 60] LeftUpperArm, RightUpperArm, LeftUpperLeg, RightUpperLeg: The spec says 'hands resting on the thighs', but the forearms point straight ahead from the shoulders: measured hand centres at x +/-1.57 while the thighs span about x 0.03-0.97, so both hands hover in the air outside the knees (front view, every frame: the pose reads as holding a steering wheel). The upper arms are turned in (ry -35 left, +35 right), opened slightly (rz +/-14) and brought forward (rx -30), and the knees are opened 5 deg. Checked: hand centres move to x +/-0.79, with the underside of the hand at height 2.44 on the thigh top at 2.43, and no arm/torso or arm/leg intersection on any frame (a plain ry -35 without the rz change pushed the forearm 0.13 into the torso). → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, offset_channel, offset_channel*
- `medium` **stiff** F[0, 60] UpperTorso, LeftLowerArm, RightLowerArm, LeftLowerLeg, LeftFoot: metrics: whole-body speed never exceeds 2.05 deg/frame; UpperTorso.rx moves 2 deg and the elbows 2 deg. Sheets 1-4 show the same image on every frame except the right shin (10 deg swing). LeftUpperArm, LeftUpperLeg, LeftLowerLeg and both upper arms are completely flat, so the left half of the body is frozen. The breathing is doubled and carried into the elbows with a 4-frame lag, a +/-2 deg side weight shift is added, and the left leg gets a small swing and foot flex late in the loop (frames 44-48), out of phase with the right leg. → *scale_amplitude, scale_amplitude, offset_overlap, set_pose, set_pose, set_pose, set_pose*
- `low` **timing** F[0, 60] Head: Head.ry is a single sine, 0 -> 12 -> 0, never resting at either end, and Head.rx peaks on the same frame 30, so the look-around reads as a metronome. Breakdowns at 22 and 38 make the head arrive, hold the look for about half a second and return; the nod is delayed 6 frames. → *add_breakdown, add_breakdown, offset_overlap*
- *apply_fixes:* applied 18 ops, skipped 0; saved work/sit/iter_1.blend

**Round 1 critique** (approved): Approved. Verified: hand centres are at x +/-0.79 with the underside of each hand on the thigh top, and no arm/torso or arm/leg intersection on any frame (front view F000-F060: the hands sit on the knees instead of hovering outside them). Breathing now carries into the elbows, there is a small weight shift, the left leg fidgets, and the look-around holds for about half a second. Metrics all 0, overlap 1.0. It is a quiet clip by design, which suits a seat. One low polish item remains.

- `low` **timing** F[44, 60] LeftLowerLeg, LeftFoot: The left shin eases out over 44 frames and returns in 16, and the left foot flexes over 48 frames and returns in 12 (curves.png), so the return is noticeably quicker than the move out. Amplitudes are only 6 and 8 deg and no pop is flagged. Moving both extremes earlier would balance it. → *retime, retime*

Before/after: `output/previews/sit_before_after.gif`

## block

| Metric | iter 0 | iter 1 | iter 2 |
|---|---|---|---|
| accel_spikes | 0 | 0 | 0 |
| velocity_corners | 0 | 0 | 0 |
| loop_seam_issues | 0 | 0 | 0 |
| joint_limit_violations | 0 | 0 | 0 |
| dead_holds | 1 | 0 | 0 |
| lockstep_key_frames | 0 | 0 | 0 |
| twinned_channels | 0 | 0 | 0 |
| foot_slide_segments | 0 | 0 | 0 |
| foot_penetration_frames | 46 | 0 | 0 |
| floating_frames | 0 | 0 | 0 |
| overlap_score | 1.0 | 1.0 | 1.0 |

**Round 0 critique** (needs_work): The loop is seamless and the braced stance is balanced, but the block fails at its one job: the forearms flank the head and leave the face wide open (rz used where ry was needed, with the wrong roll sign), the clip is a 30-frame dead hold with zero motion in head, arms and legs, and both feet sit 0.04-0.08 studs under the floor for every frame.

- `high` **awkward_pose** F[0, 30] LeftUpperArm, LeftLowerArm, RightUpperArm, RightLowerArm: The guard does not guard. In every 3/4 cell (f0-f30) the whole face is visible between the arms: the forearms stand beside the head, splayed outward, instead of crossing in front of it as the spec asks. Cause: with the upper arms raised to rx -80 the rz +/-25 keys no longer swing the arm sideways, they roll it about its own length, and the sign used (Left rz -25, Right rz +25) tips the forearm tops OUTWARD. There is no ry at all, which is the channel that swings a raised arm across the chest. Re-pose: swing the raised upper arms inward with ry (left arm toward the character's right = ry < 0, right arm = ry > 0), flip the rz roll so the forearm tops lean inward (Left rz > 0, Right rz < 0), and open the elbows slightly so the forearms sit in front of the face instead of in the head. Dry-run FK: hands end at x +0.57/-0.60, z 4.25 (head centre z 4.34), about 0.3 studs clear of the face; the values are deliberately not mirror-identical. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **stiff** F[0, 30] UpperTorso, Head, LeftLowerArm, RightLowerArm, LeftUpperArm, RightUpperArm: The whole clip is one dead hold (metrics dead_holds [0,30], whole-body speed peaks at 0.2 deg/frame; all 31 cells are pixel-identical). Only UpperTorso.rx (2 deg) and LowerTorso.ly (0.03 studs) move; head, arms and legs have motion_range 0. A held block should breathe and brace: give the chest a visible breath, let the head sink behind the guard and the forearms give and tighten, and let the chest lead by 2 frames and the arms and head trail by 1-4 so nothing peaks on the same frame. Frame 0/30 stay untouched, so the loop stays closed. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, offset_overlap, offset_overlap, offset_overlap, offset_overlap, offset_overlap*
- `high` **awkward_pose** F[0, 30] LowerTorso, LeftUpperLeg, LeftLowerLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot: Both feet are sunk in the floor for the whole loop: LeftFoot z -0.054 at f0 down to -0.084 at f15, RightFoot -0.036 to -0.066 (46 penetration frames). The root is keyed 0.15-0.18 studs down but the leg bend only shortens the legs by about 0.10, and because the legs are static the 0.03-stud root bob pushes the soles in and out of the ground. Drive the bob from the legs instead (a small knee give at f15, with the ankles counter-rotated so the soles stay flat: thigh + knee + foot stays 0 on each leg), then re-ground the root on the feet. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, plant_feet*
- *apply_fixes:* applied 27 ops, skipped 0; saved work/block/iter_1.blend

**Round 1 critique** (needs_work): Round-1 fixes verified: the guard now covers the face, the hold breathes with staggered timing, the feet are planted with no penetration or slide, and the loop seam is clean. One medium problem remains, and it is a regression from my own re-pose: the hands and forearms intersect the head by up to 0.27 studs for the whole loop. One targeted re-pose moves the guard clear of the head.

- `medium` **awkward_pose** F[0, 30] LeftUpperArm, LeftLowerArm, RightUpperArm, RightLowerArm, Head: Regression from my own round-1 guard. The forearms now cover the face (fixed: the 3/4 cells no longer show it), the loop breathes (dead_holds 0, speed 2-5.5 deg/frame, seam clean) and both feet sit on the floor (0 penetration frames). But the guard was pulled in too tight: a box-overlap check on iter_1 shows both hands 0.25-0.27 studs INSIDE the head (LeftHand deepest at f23, RightHand at f0) and the forearms 0.17-0.18 inside it, on every frame, and the forearms 0.19 into the chest. It is hidden in the 3/4 view because the hands are in front of the face, but in the side view f0-f30 the blue forearm is drawn across the front third of the head with no gap, and it will show from any in-game camera to the side or behind. Cause: the head (1.2 wide, pushed 0.5-0.6 studs forward by the 10-15 deg lean plus 10-13 deg nod) occupies the space the hands were placed in. Fix: move the guard forward and open it: raise the upper arms a little (rx more negative), use less inward swing (ry toward 0: left -30 -> -15, right 36 -> 15) and more inward roll of the forearms instead (left rz 20 -> 40, right -14 -> -30), open both elbows to -60 at rest / -65 at the peak of the breath, and ease the chin tuck by 3 deg. The offsets keep the breathing curves and their staggered timing. Dry run on iter_1: hand/forearm-to-head overlap gone (none above 0.03 studs), forearm-to-chest down to 0.06-0.09, hands 0.3 studs in front of the face at mouth-to-eye height so the eyes look over the guard, all metrics still 0, seam still clean. → *offset_channel, offset_channel, offset_channel, set_pose, set_pose, set_pose, offset_channel, offset_channel, offset_channel, set_pose, set_pose, set_pose, offset_channel*
- *apply_fixes:* applied 13 ops, skipped 0; saved work/block/iter_2.blend

**Round 2 critique** (approved): Approved, no findings. Guard clearance verified on iter_2: a box-overlap check over all 31 frames finds no contact between either hand or forearm and the head (round 1 had the hands 0.25-0.27 studs inside it), and the side view f0-f30 now shows clear air between the face and the forearms. The hands sit about 0.3 studs in front of the face at mouth-to-eye height (hand centres z 4.0 / 4.16, head centre 4.4), so the 3/4 cells read as a raised forearm guard with the eyes just over it, and the two arms are deliberately not mirror images. The hold still breathes (chest leads, forearms and head trail by 1-4 frames; no dead hold, no lockstep, overlap_score 1.0), both feet stay planted with 0 penetration and 0 slide, and the loop seam is clean (frame 0 = frame 30, no seam issues, no velocity corners). Residual, below reporting level: the forearms brush the chest by 0.06-0.09 studs and the upper arms overlap the torso at the shoulder joint by 0.13-0.18, about the same as the 0.12 of the original spec pose and normal for this blocky rig with the arms brought across the body.


Before/after: `output/previews/block_before_after.gif`

## kick

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 14 | 19 |
| velocity_corners | 6 | 10 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 0 | 0 |
| lockstep_key_frames | 1 | 0 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 2 | 0 |
| foot_penetration_frames | 47 | 0 |
| floating_frames | 0 | 0 |
| overlap_score | 0.52 | 1.0 |

**Round 0 critique** (needs_work): The kick is well timed in outline (6-frame chamber, 3-frame snap to the f9 impact, fast re-chamber), but it is not grounded: the support foot skates 0.38 studs under the body, both feet are below the floor on every frame, and the body never shifts over the standing leg. The impact pose then freezes for 3 frames, and the arms move as one block keyed on the same frame as everything else. All fixes keep the hit on frame 9. The remaining accel spikes on RightLowerLeg/RightFoot are the snap of the kick and are intentional.

- `high` **transition** F[0, 30] LowerTorso, LeftUpperLeg, LeftLowerLeg, LeftFoot: The standing foot skates. LeftFoot is in contact on all 31 frames but its centre slides 0.38 studs backward between f0 and f9 (y -0.38 -> 0.00) and back again by f30 (side view: the orange foot walks under the body while the blue leg kicks; metrics: moves_backward, mean_speed 0.026). Two causes: the root is keyed 0.15 studs BACKWARD on the impact frame (lz -0.15 at f9) with nothing in the support leg to absorb it, and the support thigh/knee keys (-15/15 -> -10/20) tip the shin 10 deg with no ankle key, so the sole also tilts toes-down into the floor. Hips that retreat as the leg extends also make the kick weak. Fix: settle back slightly in the chamber (f5), drive the hips FORWARD into the extension (lz > 0 at f9), and re-key the support leg at f5/f9/f16 so the ankle stays over the same spot with the sole flat (thigh + knee + foot = 0). Values come from an FK solve of the 0.9/0.75-stud leg; in the dry run the support foot stays within 0.01 studs of y -0.38 for the whole clip. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `high` **awkward_pose** F[0, 30] RightUpperLeg, RightLowerLeg, RightFoot, LowerTorso: Feet through the floor on every frame (47 penetration frames). At rest (f0, f22-f30) the rear right foot is keyed rx -15 on a shin that leans 25 deg back (thigh 10 + knee 15), so the toes point 10 deg down and dig in 0.15 studs; on lift-off (f1-f3, z -0.19/-0.23/-0.13) and on the step-down (f19-f22, z down to -0.25) the foot swings through the ground toe-first, and it touches down at f19 about 0.5 studs ahead of where it ends, then drags back along the floor. The support foot is 0.07-0.16 under as well, because the root height never matches the leg bend. Fix: flatten the rear sole (thigh + knee + foot = 0 at f0/f22/f30) and finish the step at f22 so the foot does not creep afterwards; dorsiflex the ankle (Foot rx < 0 = toes up) and add knee at f2 and f20 so the toes clear on the way up and the foot stays airborne until it is over its landing spot; then re-ground the root on the lowest foot. Dry run: no penetration left, support foot at z 0.00 on every frame, rear foot within 0.035 of the floor when planted. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, add_breakdown, add_breakdown, add_breakdown, add_breakdown, plant_feet*
- `medium` **awkward_pose** F[4, 18] LowerTorso, LeftUpperLeg, LeftFoot: From f4 to f18 the character stands on the left leg only, but the pelvis stays exactly centred between where the two feet were (there is no lx key anywhere), so in the 3/4 view the body hangs beside its support foot and the kick reads weightless. Shift the hips 0.18 studs over the standing foot (lx > 0 = toward the character's left) before the foot leaves and back as it lands, and counter it in the support hip and ankle so the planted foot neither slides sideways nor rolls onto its edge (LeftUpperLeg rz < 0 swings the foot back to its old spot; LeftFoot rz is the opposite, to keep the sole flat). → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **timing** F[6, 12] RightUpperLeg, RightLowerLeg, UpperTorso, Head: The game fires the hit on f9 and the extension itself is good (knee 110 -> 5 deg in f6-f9), but it lands on a pose that is then frozen: RightUpperLeg and RightLowerLeg have identical keys at f9 and f12 (whole-body speed drops to 4 deg/frame; f9, f10 and f11 are the same picture), and the torso only leans 15 deg, so the kick reaches hip height with an upright body. Keep the impact on f9 but make it a snap that settles: drive the thigh above horizontal and lock the knee straight on f9, let both ease back to the existing f12 keys (a 3-frame recoil instead of a freeze), and commit the spine with more lean-back (UpperTorso rx < 0) while the head nods to stay on the target. → *add_breakdown, set_pose, set_pose, set_pose*
- `medium` **stiff** F[0, 30] LeftUpperArm, LeftLowerArm, RightUpperArm, RightLowerArm, Head, UpperTorso: All 12 animated bones are keyed on f9 (lockstep 12/12, overlap_score 0.52) and both arms do the same thing at the same time: they open and drop together and come back together, so the upper body moves as one block. Give the arms jobs: the left stays a tight guard in front of the chin, the right (kicking side) swings back and down as a counterweight to the leg (UpperArm rx > 0 = swung backward). Then break the lockstep: the arms and head trail the leg by 1-3 frames and the spine by 1, so the leg leads and the rest follows through. Dry run: lockstep frames 0, overlap_score 1.0. → *set_pose, set_pose, set_pose, set_pose, set_pose, offset_overlap, offset_overlap, offset_overlap, offset_overlap, offset_overlap, offset_overlap*
- *apply_fixes:* applied 48 ops, skipped 0; saved work/kick/iter_1.blend

**Round 1 critique** (approved): Approved. All five round-1 fixes hold in the iter_1 sheets: the support foot stays put (0 slide, 0 penetration), the rear foot clears on lift-off and lands on its spot at f21-f22, the hips shift over the standing leg and drive forward into the extension, the impact is a snap that settles (thigh -94 and knee locked on f9, recoil to f12, torso lean peaking a frame later), and the left guard / right counter-swing with 1-3 frame offsets removes the lockstep (overlap_score 1.0). The Hit marker (minimum of RightLowerLeg.rx in f4-f18) resolves to f9, the full-extension pose (-0.0 deg, next lowest 0.2 at f10). The 19 accel spikes and 10 velocity corners are all on RightLowerLeg / RightFoot / RightUpperLeg at the chamber, snap and re-chamber keys (f1-f2, f5-f9, f12-f15, f20-f22); in the sheets f6-f9 and f12-f15 read as a 3-frame whip out and back with clear in-between poses on f7, f8, f13 and f14, not as pops. Self-intersection is limited to 0.05-0.09 studs in the folded chamber at f6-f7. One optional low-severity polish item.

- `low` **transition** F[8, 10] LowerTorso: Polish only. LowerTorso.ly still carries the original spec key on f9 between the planted keys on f8 and f10, a one-frame dip of about 0.01 studs of the root exactly on the impact frame (visible as the notch in the ly curve). It is far below what the renders show, but the key is redundant; remove it so the root height through the impact is a clean line. → *smooth_transition*

Before/after: `output/previews/kick_before_after.gif`

## combo

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 12 | 28 |
| velocity_corners | 4 | 18 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 0 | 0 |
| lockstep_key_frames | 0 | 0 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 0 | 0 |
| foot_penetration_frames | 98 | 0 |
| floating_frames | 0 | 0 |
| overlap_score | 1.0 | 1.0 |

**Round 0 critique** (needs_work): The choreography is right (jab, cross with hip turn, hook, recover to the start guard) and the torso twist is well layered, but the lower body is not attached to the ground: the legs never move, so the twisting pelvis drags both feet about 0.37 studs across the floor, and the rear foot is 0.33-0.46 studs under it for the whole clip. The punches ease into their hit frames instead of snapping and have no contact hold, and the head turns away from the target on the cross and the hook. All fixes keep the hits on frames 6, 16 and 30. Accel spikes on the forearms are the punches themselves and are intentional.

- `high` **transition** F[0, 48] LowerTorso, LeftUpperLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot: Neither foot is grounded. (1) Penetration on all 49 frames: the rear right foot is keyed rx 0 on a shin that leans 25 deg back (thigh 15 + knee 10), so its toes point 25 deg down and sit 0.33 studs under the floor, 0.46 at f16 where the heel-lift key adds another 15 deg (the onion skin shows the blue foot below the ground line); the left foot is 0.09 under. (2) Both feet skate: the legs have motion_range 0 while LowerTorso.ry swings -5 / +15 / -20, so the rigid legs are carried round the root and the feet draw arcs on the floor - LeftFoot centre (0.50,-0.38) at f0 -> (0.58,-0.24) at f16 -> (0.34,-0.53) at f30, RightFoot (-0.50,0.48) -> (-0.62,0.38) -> (-0.31,0.62), about 0.37 studs each (watch the feet against the checker in the 3/4 cells f12-f30). Fix without losing the hip drive: counter-rotate both thighs on the pelvis-twist frames (UpperLeg ry = -LowerTorso ry) so the feet keep pointing forward, re-pose thigh/ankle so each ankle stays over its spot while its hip socket swings +/-0.13-0.17 studs (soles flat: thigh + knee + foot = 0 on the left; the rear foot keeps a 5 deg raised heel), and on the cross (f16) let the rear knee drive in with the heel 12 deg up instead of the toes going through the floor. Then lead the pelvis and legs by one frame so the hips start each punch, and re-ground the root. Dry run: 0 penetration frames, both feet within 0.03 studs of the floor on every frame, foot centres stay within 0.02 (left) / 0.05 (right) studs. → *offset_channel, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, offset_overlap, offset_overlap, plant_feet*
- `medium` **timing** F[0, 36] LeftUpperArm, LeftLowerArm, RightUpperArm, RightLowerArm: The three hits arrive soft. Each punch is a single eased Bezier segment that is slowest exactly where it should be fastest: the jab extends over all of f0-f6 and the elbow is already decelerating at f5 (f5, f6 and f7 look alike), the cross takes f11-f16, and the hook drifts out over f24-f30 (whole-body speed only 21-33 deg/frame, the slowest of the three). None of them holds its contact pose: the key on the hit frame is immediately followed by the retraction, so the pose the game fires its hit event on is on screen for one frame. Fix, keeping the hits on f6 / f16 / f30: a small coil at f3 and a straight (LINEAR) 3-frame extension for the jab; move the cross's wind-up key from f11 to f13 and the hook's from f24 to f27 so both travel in 3 frames; and add a one-to-two-frame contact hold after each hit (f7, f17, f32) before the arm comes back. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_easing, retime, retime*
- `medium` **awkward_pose** F[6, 36] Head: The head does not stay on the target. The body turns 40 deg left for the cross (LowerTorso 15 + UpperTorso 25 at f16) and 50 deg right for the hook (f30), but the head only counters by -20 / +25, so the face ends up 20 deg off to the left at f16 and 25 deg off to the right at f30 (3/4 cells f28-f33: the face has turned away from where the fist is going), and it does not counter the jab at all. Counter-rotate the neck by nearly the full body twist on each hit (Head ry opposite in sign to the torso ry) so the eyes stay forward while the shoulders turn underneath. → *set_pose, set_pose, set_pose, set_pose*
- *apply_fixes:* applied 50 ops, skipped 0; saved work/combo/iter_1.blend

**Round 1 critique** (approved): Approved, no findings. Round-1 fixes verified in the iter_1 sheets: both feet stay on their checker squares through all three hits (0 penetration, 0 slide, onion skin shows one clean foot pair on the floor line), the rear knee drives in with a small heel lift on the cross (f13-f17), the head stays on the target through the cross and the hook, and each punch now travels in 3 frames and holds its contact pose (f6-f7, f16-f17, f30-f32). Hit markers resolve to the intended poses: Hit1 = max LeftLowerArm.rx in f0-f12 -> f6 (-5 deg, jab fully extended), Hit2 = max RightLowerArm.rx in f11-f23 -> f16 (-5 deg, cross extended), Hit3 = max LeftUpperArm.rz in f24-f38 -> f30 (80 deg, hook across; the hold key at f32 is 78, so f30 stays the unique maximum). The 28 accel spikes and 18 velocity corners are all on the punching arms at the start and end of the strikes (f3/f6-f7, f13/f16-f17, f27/f30); the two largest corners (about 37-39 deg/frame on the forearms) are the deliberate LINEAR 3-frame extensions of the jab and cross. In the sheets they read as snaps with visible in-betweens (f4-f5, f14-f15, f28-f29), not pops, and each lands on a held pose. No self-intersection above 0.03 studs outside the shoulder joints.


Before/after: `output/previews/combo_before_after.gif`

## death

| Metric | iter 0 | iter 1 | iter 2 | iter 3 |
|---|---|---|---|---|
| accel_spikes | 0 | 10 | 10 | 5 |
| velocity_corners | 0 | 4 | 4 | 3 |
| loop_seam_issues | 0 | 0 | 0 | 0 |
| joint_limit_violations | 0 | 0 | 0 | 0 |
| dead_holds | 0 | 1 | 1 | 1 |
| lockstep_key_frames | 4 | 0 | 0 | 0 |
| twinned_channels | 1 | 0 | 0 | 0 |
| foot_slide_segments | 0 | 0 | 0 | 0 |
| foot_penetration_frames | 106 | 0 | 0 | 0 |
| floating_frames | 0 | 0 | 0 | 0 |
| overlap_score | 0.079 | 1.0 | 1.0 | 1.0 |

**Round 0 critique** (needs_work): The story beats are there (recoil, stagger, buckle, collapse backward, lie still) and the curves are clean, but the clip fails its contact rule: feet and shins are up to 0.8 studs under the floor through the buckle, and the head is 0.4 studs inside the floor in the pose that is held after death. The landing is eased like a lie-down, every bone arrives on frame 34 at once, and the final pose has both forearms and a knee held up in the air. The fixes end on a flat, limp pose on the back with every part resting on the floor; the last 5 frames are a deliberate hold.

- `high` **awkward_pose** F[0, 50] Head, UpperTorso, LowerTorso, LeftFoot, RightFoot: The body is under the floor for most of the clip (body_penetration on 106 part-frames) and, worst of all, in the pose it holds forever. (1) Final pose f34-f50: the head is sunk into the ground, z -0.21 at f34 growing to -0.42 at f50 (side view f40-f50: the beige head box hangs below the floor line). The head is 1.2 studs deep against the torso's 1.0, so it already sits 0.1 low when the body lies flat; Head.ry 35 then rolls the box about its long axis and drives a corner another 0.24 down, and Head.rx -5 tips the crown in further. A head lying on its back cannot be turned with ry without burying a corner, so drop the ry turn and loll the head toward the shoulder with rz instead (when the body lies flat rz slides the head in the floor plane), lift the chest 4 deg (UpperTorso rx > 0) so the neck clears, and lay the head back by the same amount. (2) Knee buckle f3-f33: the feet and shins are as much as 0.82 studs under the floor (RightFoot z -0.72 at f18, -0.82 at f21) because the root drop is hand-keyed and there are no ankle keys, so the feet stay square to the shins and the toes point 50 deg into the ground. Key the ankles so the soles stay on the floor while the knees fold (Foot rx < 0 = toes up, about -(thigh + knee), limited to -45), then let plant_feet with parts=all rest the lowest body part on the floor on every frame. Dry run: body_penetration 0, lowest part at z 0.00 on all 51 frames, and the root now sinks steadily (ly 0 -> -0.34 by f24 -> -1.49) instead of popping around. → *scale_amplitude, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, plant_feet*
- `medium` **awkward_pose** F[34, 50] LeftUpperArm, LeftLowerArm, RightUpperArm, RightLowerArm, LeftUpperLeg, LeftLowerLeg, RightUpperLeg, RightLowerLeg: The corpse is holding itself up. In the held pose both arms hover: UpperArm rx -10 lifts them off the ground and LowerArm rx -20 / -35 bends the forearms up into the air, so the hands float 0.8 (left) and 1.05 (right) studs above the floor (side view f34-f50: the blue forearm stands up above the chest). The right knee is also held up (thigh -15, knee 30). Nothing reads as limp, and the arms are near mirror images (rz 70 / -60). Lay everything down: swing the upper arms a few degrees toward the floor (UpperArm rx > 0), straighten the elbows and bend them in the floor plane with LowerArm rz instead of rx, use clearly different spreads left and right, and let the legs fall flat and slightly splayed, keeping the splay at 0 until the fall. Dry-run FK: every arm and leg part ends within 0.02 studs of the floor. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **timing** F[18, 40] LowerTorso, UpperTorso, Head: The fall has no weight. LowerTorso.rx goes 10 -> -60 over f18-f28 (7 deg/frame) and then only -60 -> -90 over f28-f34 (5 deg/frame) on an eased curve, so the body slows down as it nears the ground and is laid on the floor instead of hitting it; whole-body speed peaks at f30 and has faded to 20 deg/frame by f33. Nothing reacts to the landing either: the spine and head simply arrive (UpperTorso -10 -> 0, Head -20 -> 0). Make it accelerate into the ground and land two frames earlier: hold the topple back at f28 (-48), then go straight (LINEAR) to flat at f32, 10.5 deg/frame, with the root's backward slide arriving on the same frame. Keep the chest curled and the chin tucked on the way down (UpperTorso and Head rx > 0), let the shoulders slam and the chest rebound (f32 -> f34 -> settle f38), and let the head whip back to the floor a frame after the shoulders, bounce once and settle (f33 -> f36 -> f40). → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **stiff** F[0, 50] LeftUpperArm, LeftLowerArm, RightUpperArm, RightLowerArm, LeftUpperLeg, LeftLowerLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot: Everything moves on the same four frames: lockstep at f6 (7/11 bones), f18 (9/11), f28 (8/11) and f34 (11/11), overlap_score 0.079, and LeftUpperArm.rx / RightUpperArm.rx are identical curves (twinning). The whole body therefore reaches the floor pose on the single frame f34 and stops dead, like a posed mannequin being set down. Offset the limbs so they trail the torso by different amounts: the arms fling and land 2-5 frames late, forearms after upper arms and right after left, and the legs 3-4 frames late, so the knees are still up when the back hits at f32 and the feet flop down by f37-f38. Dry run: lockstep frames 0, overlap_score 1.0, no twinned channels. → *offset_overlap, offset_overlap, offset_overlap, offset_overlap, offset_overlap, offset_overlap*
- *apply_fixes:* applied 60 ops, skipped 0; saved work/death/iter_1.blend

**Round 1 critique** (needs_work): Round-1 fixes verified: nothing passes through the floor on any of the 51 frames, the held pose is flat on the back and limp (arms and legs on the ground, head lolled with rz instead of the corner-burying ry turn), the landing accelerates into f32 with a chest rebound and head bounce, and the limbs trail by 2-5 frames (lockstep 0, no twinning). The 10 accel spikes are the f32 impact (LowerTorso rx / ly, Head rx at f33) and read as a hit, not a pop; the dead hold at f45-f50 is the intended final hold. One medium problem remains: between f24 and f31 the body tips backward as a plank on its heels with the hips in the air instead of sitting down and rolling back. One set of leg keys fixes it.

- `medium` **transition** F[22, 33] LeftUpperLeg, LeftLowerLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot, LowerTorso: Round-1 fixes hold (no part below the floor on any frame, limp flat final pose, landing on f32 with rebound, staggered limbs), but the way the body gets to the floor is still wrong. After the knees buckle (f12-f23, a crouch on the toes) the legs partly straighten again while the pelvis tips back, so from f24 to f31 the character topples like a plank pivoting on its heels: in the side view f26-f27 it leans back 20-35 deg balanced on the feet, at f28-f30 the torso is at 48-70 deg with the hips still 0.5-1 stud in the air, and the hips, back and head all reach the floor together on f32 (the lowest part is a foot on every frame up to f31, then the head). A body whose knees have given way sits down first and then rolls onto its back. Cause: the leg keys at f31 (left) / f32 (right) open the knees to 60-70 deg and bring the thighs back to -30 / -40 just as the pelvis rotates to -90. Fix: keep the legs folded under the body as it goes back. Add a sit pose at f27 / f28 (thigh flexed -78 / -85 against the tilting pelvis, knee about 105, ankle counter-rotated so the sole stays on the floor: pelvis + thigh + knee + foot is about 0), keep the knees up and folded on the back-impact keys at f31 / f32, and let the existing f37 / f38 keys flop the legs flat. The 1-frame left/right stagger is kept. plant_feet with parts=all then re-rests the lowest part on every frame. Dry run on iter_1: hips reach the floor by f26-f27, the back rolls down over f28-f32 with the knees up, legs slide out by f37-f38; 0 penetration, 0 lockstep, final pose unchanged (every part within 0.03 studs of the floor), self-overlap in the fold at most 0.09 studs. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, plant_feet*
- *apply_fixes:* applied 13 ops, skipped 0; saved work/death/iter_2.blend

**Round 2 critique** (needs_work): Not approved. What holds from earlier rounds: no part passes through the floor on any of the 51 frames, the held final pose is flat on the back and limp with every part within 0.03 studs of the ground, the limbs are staggered (lockstep 0, no twinning), and the fall now sits down before it rolls back. One medium problem remains, and it comes from my own round-1 and round-2 keys: from f28 to f36 the body is propped on a foot or on the head, so the hips and back hover 0.2-0.3 studs above the floor through the landing and only settle on f37-f38. The fix in this report (3 spine/head keys, 12 leg keys, plant_feet parts=all) is verified by an in-memory dry run on iter_2 but has not been applied or rendered; it should be treated as an open item until someone reviews the result. The f45-f50 dead hold is the intended final hold.

- `medium` **awkward_pose** F[27, 37] LowerTorso, UpperTorso, Head, LeftUpperLeg, LeftLowerLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot: The sit-then-roll now reads in outline (hips sink over f24-f27, the back rolls down f28-f31, flat on f32, legs out by f37-f38) and nothing goes through the floor, but the body does not actually rest on the floor while it lands; it is propped up by one foot or by the head. Measured on iter_2: the pelvis never touches the ground between f28 and f36. Its lowest point is 0.20-0.26 studs up through the roll (f28-f31, resting on the left foot), and after the body is flat it is still 0.22-0.32 up at f32-f35 and 0.18 at f36, with the upper torso at 0.18-0.33 and the head 0.12-0.47 up at f33-f35; everything only reaches the floor on f37-f38. In the side view f33-f35 there is a visible strip of background under the whole lying body, which then sinks. So the impact frame has no contact (on f32 only the back of the head touches) and the corpse floats for about 5 frames. Two causes, both from my own earlier fixes: (1) the round-2 leg keys at f31 / f32 hold the knees 100 deg bent with the thighs only 40-48 deg up, so the shins point steeply down and, as the legs unfold toward f37 / f38, the left foot is pushed below the body and plant_feet lifts everything onto it; (2) the round-1 impact keys tip the chest (UpperTorso -3 at f32) and the head (rx -7 at f33) backward past flat, so the head becomes the lowest point and props the body up. Fix: let the feet leave the ground as the back goes down. Use slightly different sit keys at f27 / f28 so the hips land with the feet (solved so that hips and sole touch together), fold the knees up toward the chest on f31 / f32 (thigh -75 / -82, knee 92 / 98, so the shin is never steeper than the thigh and the feet are in the air), keep the chest at its resting 4 deg on f32 and the head-back key at -4 so the rebound and head bounce only go upward, then re-rest the body. Dry run on iter_2: the pelvis is on the floor from f28 to the end (lowest point 0.00-0.01 on every frame), the upper back arrives on f32 (0.00), the head touches on f32, bounces 0.08-0.16 over f33-f35 and settles, the feet stay 0.06-0.64 up until they drop on f36-f38, the final pose is unchanged, 0 penetration, 0 lockstep, self-overlap at most 0.10 studs in the fold, accel spikes down from 10 to 5. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, plant_feet*
- *apply_fixes:* applied 16 ops, skipped 0; saved work/death/iter_3.blend

**Round 3 critique** (approved): Approved, no findings. The hover is gone and iter_3 matches the dry run frame for frame. Measured on iter_3 (lowest point of each part per frame): the pelvis reaches the floor on f28 and stays there to the end (0.00 on f28-f35, 0.01 afterwards); the upper back rolls down behind it (0.34 at f28, 0.26, 0.18, 0.09, then 0.00 on f32); the head touches on f32 (0.01), bounces 0.08 / 0.16 / 0.14 over f33-f35 and settles by f38; the feet leave the ground as the back goes down (0.06-0.64 studs up on f29-f35) and drop on f36-f38. Nothing is below the floor on any of the 51 frames (body_penetration 0), and the held pose f38-f50 has every part within 0.03 studs of the ground. In the sheets the fall now reads as intended: recoil f0-f6, stagger and knee buckle f8-f23 with the weight on the right leg, hips dropping f24-f27, seated impact on f28, roll onto the back f28-f31 with the knees folding up, flat on f32 with a chest rebound and head bounce, legs flopping out f33-f38, head lolling to the side f38-f45, then the hold. There is no strip of background under the body in the side view at f32-f36 any more. Metrics: lockstep 0, overlap_score 1.0, no twinning, no joint-limit violations; the 5 accel spikes and 3 velocity corners are the two ground contacts (LowerTorso.ly at the seated impact on f24-f28, LowerTorso.rx and Head.rx as the back and head land on f32-f33) and read as impacts, not pops; the dead hold f45-f50 is the intended final hold. Below reporting level, left as is: the left foot rides 0.09-0.15 studs off the floor during f20-f27 while the right leg carries the buckle, the crouch is a little slow through f16-f23 (17-20 deg/frame), and the folded legs overlap the torso and each other by at most 0.10 studs on f27-f29. The spec's head turn is expressed as a sideways loll (Head rz) because any ry turn on a head lying flat buries a corner of the head in the floor.


Before/after: `output/previews/death_before_after.gif`

## point

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 0 | 5 |
| velocity_corners | 0 | 4 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 1 | 0 |
| lockstep_key_frames | 2 | 0 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 0 | 0 |
| foot_penetration_frames | 0 | 0 |
| floating_frames | 0 | 0 |
| overlap_score | 0.0 | 1.0 |

**Round 0 critique** (needs_work): Clean curves (no pops, feet planted, hands clear of the body) but it is a blocked-in pose-to-pose move, not an animation: every bone is keyed on F008 and F030 only (overlap_score 0.0), the arm swings up as one rigid rod with no anticipation, drag or settle, the whole body is frozen for 22 frames (F008-F030, whole-body speed 0.0), and the chest turns AWAY from the pointing arm, so the gesture has no commitment. Fixes: turn and lean the chest into the point, add a small wind-up, elbow/wrist drag and an overshoot-settle on arrival, let the head lead and trail the arm, and put one emphasis beat in the hold.

- `medium` **awkward_pose** F[8, 30] UpperTorso, Head: F008-F030: UpperTorso.ry is -10 (twist to the character's RIGHT), which pulls the pointing (right) shoulder back and away from the target. The spec asks to 'turn slightly into' the point, i.e. the right shoulder should come forward (ry > 0). Because the arm is a child of the chest, the -10 twist also aims the arm 10 deg off to the right: FK puts the hand at x -1.75, outside the shoulder line (x -1.5), while Head.ry +5 leaves the face looking somewhere else (net -5). In the 3/4 view the chest opens away from the arm and the pose reads as a stiff signpost. The spine is also dead vertical (no rx at all). Fix: flip the twist to +8 (factor -0.8 on the F008/F030 keys), counter the head to -5 so the face stays on the target (net +3), and lean the chest 4 deg into the gesture (UpperTorso.rx > 0 = forward). After the fix the hand sits at x -1.1, converging on the target in front of the character, 6 deg above horizontal. → *scale_amplitude, scale_amplitude, set_pose, set_pose*
- `medium` **timing** F[0, 12] RightUpperArm, RightLowerArm, RightHand, Head, UpperTorso, LeftUpperArm: F000-F008: the arm is raised by a single RightUpperArm.rx curve 0 -> -100 with one ease-in/ease-out; the elbow moves 3 deg (-8 -> -5) and RightHand.rx is 0 on every key, so the arm rotates about the shoulder like a rigid bar (side view F002-F007: forearm and hand stay perfectly collinear). There is no anticipation before F001, and at F008 everything (6 of 6 bones, lockstep) hits its final value on the same frame and stops dead: no overshoot, no settle (whole-body speed 5.9 at F007, 0.0 at F008). Fix: a 2-frame wind-up (arm back +8, elbow starting to fold), the elbow leading with the forearm dragging (-40 at F005) and whipping straight on arrival, wrist drag then flick (Hand.rx +18 at F005 = trailing, -8 at F008, 0 at F012), a 6 deg overshoot on the upper arm that settles by F012, the head arriving 3 frames early (look, then point), the chest 1 frame early and the left counter-swing 2 frames late. → *set_pose, set_pose, set_pose, add_breakdown, set_pose, set_pose, set_pose, retime, retime, retime*
- `medium` **stiff** F[8, 30] RightUpperArm, RightLowerArm, Head: F008-F030: metrics.dead_holds reports a 22-frame hold with whole-body speed exactly 0.0; frames F008 through F030 on both contact sheets are pixel-identical. Over half of the 40-frame clip is a freeze frame, which reads as the game hanging rather than a character holding a gesture. Fix: one emphasis beat in the middle of the hold ('that one!'): the arm dips 7 deg at F018 with a slightly soft elbow and jabs back out to -102 at F021 before easing to the -100 hold key, and the head nods 4 deg toward the target at F020. The overshoot-settle from the previous finding covers F008-F012, so the body is never fully static. → *set_pose, set_pose, set_pose, set_pose, set_pose*
- `low` **transition** F[30, 40] RightLowerArm, Head, UpperTorso: F030-F040: every channel leaves its hold on F030 and lands on F040 with the same ease, and the arm comes down as the same rigid bar that went up (elbow -5 -> -8). Fix: let the elbow relax as the arm falls (-24 at F036, straightening into the neutral -8), keep the head on the target 3 frames longer and the chest 1 frame longer so the arm leads the recovery. → *set_pose, retime, retime*
- *apply_fixes:* applied 22 ops, skipped 0; saved work/point/iter_1.blend

**Round 1 critique** (approved): Approved. All four iter-0 findings are fixed. The chest now turns and leans into the point (UpperTorso ry +8, rx +4) and the hand sits at world (-1.10, -2.34, 4.06) on the hold: forward of the right shoulder, converging on the target, about 6 deg above horizontal (side view F012-F030). The raise has a 2-frame wind-up (F002-F003), a dragging elbow and wrist (F004-F006), a 6 deg overshoot at F008 that settles by F012, the head arrives at F005 ahead of the arm, and the F018-F021 emphasis beat breaks the old 22-frame freeze (dead_holds 0, lockstep 0, overlap_score 1.0). The lowering leads with the arm and a soft elbow (F034-F037). No part intersects another on any half frame. Residuals, not worth another round: accel peaks of about 12.7 deg/frame^2 on the F002-F008 raise are the intended snap, and the F018-F021 beat is subtle at this render size.


Before/after: `output/previews/point_before_after.gif`

## laugh

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
| floating_frames | 0 | 0 |
| overlap_score | 0.703 | 1.0 |

**Round 0 critique** (needs_work): The lean-back and the head throw read, but the signature pose is broken and the laugh is a metronome. The 'hand on the belly' never touches the body: FK puts the right hand at (x -1.36, y -1.2, z 3.4) for the whole F006-F034 hold, sticking straight out in front of the right shoulder at chest height, while the forearm is 0.26 studs inside the side of the chest. The bounce is four identical beats with chest and head keyed on the same frames and both arms frozen, and the root bob has no knee bend behind it, so it only pushes the feet 0.05 studs through the floor. Fixes: fold the right arm across the body so the hand rests on the front of the torso (verified in contact, no penetration), give the laugh a forward 'catch' before the throw-back, a big first burst that decays, a head that trails the chest, a left arm that shakes with it, and remove the root bob.

- `high` **awkward_pose** F[3, 39] RightUpperArm, RightLowerArm, RightHand, UpperTorso: F003-F039: RightUpperArm rx -15 / rz +15 with the elbow at -95 points the forearm straight ahead, so the hand hangs in mid-air at world (-1.36, -1.2, 3.4), 0.7 studs in front of the chest and outside the torso's right edge (x -1.0): it is nowhere near the belly (side view F006-F034: the forearm sticks out like a shelf; 3/4 view: the hand floats beside the body). rz +15 on the right arm is adduction (toward the character's left), which drives the elbow into the torso: the forearm box overlaps the chest by 0.16-0.26 studs on F004-F038 and clips the hips by 0.07 on F003 and F039. Fix, solved with FK against the leaning chest (rx -6 to -12): lift the elbow forward and out (upper arm rx -68, rz -40 = abducted away from the body, ry +20 = turned toward the character's left) and fold the forearm across the front of the torso (elbow rx -117 plus forearm ry +60 / rz -51, hand rz +19 to lay it flat). The hand then sits at chest-local (-0.49, -1.01, 2.8): on the front of the torso just right of centre, at the bottom of the ribcage, which is as low as the short R15 arm can reach without the forearm cutting through the body. Hand-to-torso gap 0.04 studs, forearm touching (0.03 or less). The arm is a child of the chest, so the hand stays planted while the chest bounces. ry/rz/hand-rz are new channels (neutral 0 at F000 and F048). → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose*
- `medium` **timing** F[0, 40] UpperTorso, Head, LeftUpperArm, RightUpperArm, RightLowerArm, RightHand: F006-F034: UpperTorso.rx alternates -6/-12 and Head.rx -12/-22 on exactly the same frames (6, 10, 14 ... 34), so head and chest move as one block with no overlap, and all four 'ha' beats have the same size and the same 8-frame period (curves.png: two identical sine waves). Both arms are frozen from F006 to F034 (flat curves), so the 'shoulders bouncing' in the spec never happens. The entry is a single 6-frame snap into the full pose with no anticipation (accel spikes +-9.7 on RightLowerArm.rx at F001/F005; lockstep on F006, 6 of 7 bones). Fix: a 2-frame forward catch before the throw-back (chest +5, head +6 at F002; rx > 0 is forward), a bigger first burst that decays (chest and head x1.25 / x1.2 on F006-F014, x0.7 about their mid values on F022-F034), the head delayed 2 frames so it whips after the chest, the right arm delayed 2 frames so the hand lands on the body after the lean starts (this also removes the accel spikes), and three shake accents on the free left arm (rz 20 / 13 / 18 at F012 / F020 / F028; left-arm rz > 0 is away from the body). These ops must run after the hand-on-belly finding because the offset moves the F006/F034 arm keys set there. → *scale_amplitude, scale_amplitude, scale_amplitude, scale_amplitude, set_pose, set_pose, offset_overlap, offset_overlap, set_pose, set_pose, set_pose*
- `low` **awkward_pose** F[1, 39] LowerTorso, LeftFoot, RightFoot: F001-F039: LowerTorso.ly dips to -0.05 on F008/F016/F024/F032, but no leg channel is animated, so the dip is not absorbed by the knees: metrics.feet.lowest_z_per_frame follows the root exactly and both feet go 0.05 studs under the floor four times (right at the penetration threshold). The bob itself is invisible at this size; the bounce reads through the chest, head and arms. Fix: remove the interior root keys so ly stays 0 and the feet sit on the floor. → *smooth_transition*
- *apply_fixes:* applied 26 ops, skipped 0; saved work/laugh/iter_1.blend

**Round 1 critique** (approved): Approved. The right hand now rests on the front of the torso for the whole F008-F036 hold: hand centre at world (-0.48, -0.9, 2.95), 0.04 studs off the chest, forearm in contact (overlap 0.03 or less), nothing inside the body (was 0.26 inside the chest with the hand floating 0.7 studs in front). It rides the chest correctly as it bounces. The laugh has a forward catch at F002-F004 before the throw-back, a big first burst that decays (side view F008/F016 vs F024/F032), the head whipping 2 frames behind the chest, and a left arm that shakes with it. Root bob removed: feet at 0.0 on every frame. Metrics are clean (0 spikes, 0 corners, 0 holds, 0 lockstep, overlap_score 1.0). Residuals: the hand sits at the bottom of the ribcage rather than the belly proper, which is the lowest the R15 arm reaches without the forearm cutting the body, and the right elbow is carried fairly high (above the shoulder line in F008-F036) to get there; RightLowerArm.ry is at its +60 limit.


Before/after: `output/previews/laugh_before_after.gif`

## clap

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 58 | 33 |
| velocity_corners | 42 | 25 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 0 | 0 |
| lockstep_key_frames | 6 | 0 |
| twinned_channels | 4 | 0 |
| foot_slide_segments | 0 | 0 |
| foot_penetration_frames | 0 | 0 |
| floating_frames | 0 | 0 |
| overlap_score | 0.476 | 1.0 |

**Round 0 critique** (needs_work): The hands never meet, so this is not a clap. Forward kinematics on the 'closed' keys (F008, F013, F018, F023, F028, F033) puts the hand centres at x = +-1.23, i.e. 2.46 studs apart with a 1.66-stud air gap between the hand boxes (each hand is 0.8 wide), and on the 'open' keys at x = +-1.39: each hand travels 0.16 studs sideways but 0.22 studs up and down, at head height (z 3.53-3.75), so it reads as two fists pumping beside the face. The four arm channels are also exact mirrors (4 twinned channels) and the body under the arms is static. Fixes: re-aim the arms so the forearms converge in front of the chest and the existing six-beat rz oscillation on the forearms now closes the hands exactly to contact (0.00 studs, never overlapping, checked on every half frame in a dry run), make the right hand the dominant one, and give the chest and head a beat that follows the claps.

- `high` **awkward_pose** F[4, 36] LeftUpperArm, LeftLowerArm, RightUpperArm, RightLowerArm, LeftHand, RightHand: F004-F036: the clap is driven by UpperArm.rz and LowerArm.rz (-15/-35 and -10/-35 on the left, mirrored on the right). With the upper arm already raised 55 deg forward, rz (about the forward axis) mostly rolls the arm around its own length, and the forearm rz axis is only 30 deg off the forearm direction, so 25 deg of rz moves the hand 0.16 studs sideways. Measured hand centres: closed keys (+-1.23, -1.87, 3.75), open keys (+-1.39, -1.93, 3.53): the hand boxes are never closer than 1.66 studs. The crossed-arms look in the 3/4 view is perspective only; nothing touches and nothing passes through. The pose is also too high (hands at z 3.75 = mouth height, 1.9 studs in front of the body). Because left and right are exact mirrors (metrics.twinning: UpperArm rx/rz and LowerArm rx/rz), the motion is perfectly symmetric as well. Fix, solved with FK: raise the upper arms a little more (rx -66 left / -70 right), swing them inward with the new UpperArm.ry channel (left -11 = toward the character's right, right +12 = toward the left), hold UpperArm.rz constant (left +11, right -8) instead of oscillating it, open the elbows (rx -34 left / -28 right) and remap the existing forearm rz beats so they do the clapping: left -31 open / -49 closed, right +17 open / +47 closed. Closed keys then give hand centres (+0.50, -1.62, 3.37) and (-0.43, -1.63, 3.41): the boxes touch at 0.00 studs in front of the chest, slightly left of centre; open keys give a 0.63-stud gap. The right hand travels 0.57 studs and the left 0.30, so the right is the striking hand and the mirror symmetry is gone. Timing of the six beats is unchanged. In the dry run the hands never overlap between keys and no arm part touches the torso, head or the other arm. → *scale_amplitude, scale_amplitude, set_pose, set_pose, set_pose, set_pose, scale_amplitude, scale_amplitude, scale_amplitude, scale_amplitude, scale_amplitude, scale_amplitude*
- `medium` **stiff** F[6, 34] UpperTorso, Head, LowerTorso: F006-F034: UpperTorso.rx is a flat +5 for 28 frames and LowerTorso.ly a flat -0.03, so the 'slight bounce' in the spec does not exist: the torso is a statue with two arms flapping on it, and the only secondary motion is a 2 deg head bob keyed on exactly the clap frames (lockstep_key_frames on F008/F013/F018/F023/F028/F033, overlap_score 0.476). The -0.03 root offset has no knee bend behind it, so it just sinks both feet 0.03 studs into the floor for F008-F028 (feet.lowest_z_per_frame -0.03). Fix: a chest pulse that follows every second clap by one frame (rx 3.5 at F014 and F024, 6.5 at F019 and F029; rx > 0 is a forward lean), the head bob delayed 1 frame so it reacts to the clap instead of hitting with the hands, and the root offset removed so the feet sit on the floor. The arms are children of the chest, so the hand contact is unaffected. → *set_pose, set_pose, set_pose, set_pose, offset_overlap, smooth_transition*
- *apply_fixes:* applied 18 ops, skipped 0; saved work/clap/iter_1.blend

**Round 1 critique** (approved): Approved. The hands now actually meet: on every closed key (F008, F013, F018, F023, F028, F033) the hand boxes touch at 0.00 studs in front of the chest (centres about (+0.50, -1.62, 3.37) and (-0.43, -1.63, 3.41)), they open to a 0.63-stud gap on the open keys, and on no half frame do they overlap or pass through each other; no arm part touches the torso, head or the other arm. The right hand is the striking hand (twinned_channels 0, was 4), the chest pulses after every second clap with the head trailing by a frame, and the feet sit on the floor (lowest z 0.0, was -0.03). Lockstep 0, overlap_score 1.0. Residuals: accel_spikes 33 and velocity_corners 25 remain (down from 58 and 42); they are the 5-frame clap beat itself, 18-30 deg forearm reversals every 2-3 frames, and read as crisp impacts rather than pops. The opening is small and the left forearm hides part of it in the 3/4 view; the closing stroke takes 3 frames and the rebound 2, where the reverse would be a little snappier. Both are polish only.


Before/after: `output/previews/clap_before_after.gif`

## salute

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 3 | 2 |
| velocity_corners | 0 | 0 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 1 | 1 |
| lockstep_key_frames | 2 | 1 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 0 | 0 |
| foot_penetration_frames | 0 | 0 |
| floating_frames | 0 | 0 |
| overlap_score | 0.0 | 0.762 |

**Round 0 critique** (needs_work): The salute does not read as a salute because the hand never reaches the brow. Forward kinematics on the F006-F032 hold puts the right hand centre at (x -0.87, y -0.41, z 4.23): jaw height (the brow is at z ~4.8), buried 0.11-0.15 studs in the head and 0.18 in the top of the chest, with the forearm 0.18 inside the chest as well. The clip is also fully lockstep (all 8 bones keyed on F006 and F032, overlap_score 0.0) and frozen solid for 26 frames. Fixes: re-pose the arm so the fingertips rest against the right temple at brow height with the elbow out (checked collision-free on every half frame in a dry run), bring the body to attention before the hand lands and relax it after the arm starts down, add a small rebound on contact, and let the chest breathe through the hold.

- `high` **awkward_pose** F[5, 33] RightUpperArm, RightLowerArm, RightHand, Head, UpperTorso: F005-F033 (both views): with RightUpperArm rx -70 / rz -55 and the elbow folded to -130, the hand box sits at world (-0.87, -0.41, 4.23). The head spans x +-0.6 and z 3.95-5.15, so the hand is at jaw height, 0.55 studs below the brow, and it overlaps the head by 0.11-0.15 studs (box-box penetration depth) and the top of the chest by 0.18; the forearm is 0.18 inside the chest too. In the side view the blue hand covers the lower face, and in the 3/4 view the forearm merges into the shoulder and neck. RightHand.rx +20 also bends the hand back off the forearm, breaking the straight forearm-to-fingertip line a salute needs. Fix (solved with FK against the -5/-5 chest/head hold): upper arm rx -89, ry -56 (new channel; with the arm raised this swings the elbow out to the character's right), rz -48, elbow -110, hand rx -7. That puts the elbow at about (-2.0, -0.4, 4.35) and the hand centre at (-1.02, -0.1, 4.82): fingertips against the right temple at brow height, 0.02 studs clear of the head, forearm and hand more than 0.2 clear of the chest; the elbow has to sit above the shoulder because the R15 arm is too short to reach the brow otherwise. The scale ops only change the F006/F032 hold keys (F000/F040 stay neutral): rx -70 -> -89, rz -55 -> -48 (pivot -5), elbow -130 -> -110 (pivot -8), hand +20 -> -7. → *scale_amplitude, scale_amplitude, set_pose, set_pose, scale_amplitude, scale_amplitude*
- `medium` **stiff** F[0, 40] UpperTorso, Head, LeftUpperLeg, RightUpperLeg, LeftUpperArm, RightUpperArm, RightLowerArm: metrics: lockstep_key_frames F006 (8 of 8 bones) and F032 (8 of 8), overlap_score 0.0. Heels, left arm, chest, head, shoulder, elbow and wrist all start on F000, arrive on F006 and leave on F032 with identical eases, so the move reads as one interpolated pose change; the hand reaches the brow and simply stops (whole-body speed 20.7 at F005, 0.0 at F006), with no contact accent. Fix: come to attention first (heels and left arm arrive at F003, chest and head at F004), the shoulder lands at F006 and the elbow closes one frame later at F007, then a 3.5 deg rebound of the elbow outward at F008 that presses back in by F011 (the rebound moves the hand AWAY from the head, gap 0.02 -> 0.06, so it cannot penetrate). On the release the arm leaves at F032 while chest, head, heels and left arm hold attention until F034. → *retime, retime, retime, retime, add_breakdown, add_breakdown*
- `medium` **stiff** F[6, 32] UpperTorso, Head, LeftUpperArm, RightUpperArm: metrics: dead_holds F006-F032, 26 frames with whole-body speed exactly 0.0 (65% of the clip); F006 to F032 on the contact sheets are identical images. A salute should be rigid, but not a still frame. Fix: one slow breath through the hold, staggered so the parts never peak together: chest lifts a further 3 deg (rx -5 -> -8, chest up) by F017, the head counters 2 deg by F021 so the gaze stays level, the left arm eases 2 deg off the body by F024, and the saluting arm sags 2 deg (rx -89 -> -87) by the end of the hold, which also slides the hand slightly away from the head (gap 0.02 -> 0.04). The arm and head are both children of the chest, so the brow contact holds while it breathes. → *add_breakdown, add_breakdown, add_breakdown, set_pose*
- *apply_fixes:* applied 16 ops, skipped 0; saved work/salute/iter_1.blend

**Round 1 critique** (approved): Approved. The hand reaches the brow: on the F007-F032 hold the hand centre is at world (-1.02 to -1.05, 0.0, 4.82-4.83), fingertips against the right temple at brow height with a 0.02-0.04 stud gap to the head (was at jaw height, 0.11-0.15 inside the head and 0.18 inside the chest). It never enters the head on any half frame, including the F006-F008 arrival (gap 0.02-0.06) and the release, and the forearm is clear of the chest. Both views read clearly as a salute (F006-F033). The body comes to attention by F003-F004 before the hand lands at F006-F007, the elbow rebound at F008-F011 gives a contact accent, and the body holds attention until F034 while the arm leaves at F032. Residuals, left deliberately: the elbow sits above the shoulder because the R15 arm cannot reach the brow otherwise; dead_holds still reports F015-F024 (9 frames at 0.19-0.36 deg/frame), which is the slow breath in a hold that is meant to be crisp; lockstep 1 at F034 is the body relaxing together after the arm has gone; on the way up the hand arcs slightly above brow height (z 5.1 at F005) before settling down onto it.


Before/after: `output/previews/salute_before_after.gif`

## crouch_idle

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 0 | 0 |
| velocity_corners | 0 | 0 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 2 | 0 |
| lockstep_key_frames | 0 | 0 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 0 | 0 |
| foot_penetration_frames | 46 | 0 |
| floating_frames | 0 | 0 |
| overlap_score | 1.0 | 1.0 |

**Round 0 critique** (needs_work): The crouch pose itself is good (compact, balanced over the feet, clear sneak silhouette) and the seam values match, but the clip is close to a still image: the whole lower body has zero motion, the fastest moment of the loop is 0.83 deg/frame, every moving channel peaks on frame 36 and stops on frame 0, and the two arms are identical. Both feet are also rolled 5 degrees onto their outer edges and sit 0.035-0.055 studs under the floor for the whole clip, sinking further as the hips drop. Fixes: flatten the feet and let the knees take the breathing, add a slow weight shift from foot to foot with the feet pinned, turn the head drift into a look left then right, break the arm symmetry and stagger the phases, then plant_feet. Dry run on a scratch copy: 0 penetration frames, feet static (drift 0.00), 0 dead holds, 0 seam issues.

- `high` **awkward_pose** F[0, 72] LowerTorso, LeftUpperLeg, LeftLowerLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot: The feet are not flat and are under the floor on all 73 frames. lowest_z is -0.035 on F000 and -0.055 on F036 for both feet (23 frames per foot beyond the -0.05 threshold, F025-F047). Two causes. (1) UpperLeg.rz is +-5 (knees apart) with nothing at the ankle to undo it, so each foot is rolled 5 deg: the outer edge is 0.039 below the sole line and the inner edge is lifted (foot z range -0.035..+0.343 for a 0.30 tall block). (2) LowerTorso.ly breathes 0.02 studs down to frame 36 while all six leg channels are constant (motion_range 0), so the hips push the rigid legs straight through the floor (ankle z 0.303 on F000, 0.292 on F020) instead of the knees bending. Fix: counter the splay at the ankles (Foot.rz/ry, solved so the sole is level) and let the legs absorb a slightly larger breath: hips 0.04 studs lower on frame 36 with the thigh, knee and ankle folding 2-4 deg to keep each ankle exactly where it is (2-bone IK values). plant_feet runs last (dry run: max correction 0.005 studs). → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, plant_feet*
- `medium` **stiff** F[0, 72] LowerTorso, LeftUpperLeg, LeftLowerLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot: Sheets 1-4: from F000 to F072 the side view is the same picture; hips, thighs, shins and feet never change (motion_range 0 on every leg channel, LowerTorso 0.02 studs). Whole-body speed peaks at 0.83 deg/frame and the analyzer reports dead holds on F000-F005 and F032-F042. Nobody holds a deep crouch for 2.4 s without moving their weight. Fix: a slow weight shift, 0.05 studs toward the left foot on frame 18 and toward the right on frame 54 (a quarter cycle out of phase with the breath, so the hips trace a small loop and never stop). The legs lean the other way (UpperLeg.rz 2.4 / 7.6 instead of 5) and the ankles roll with them (Foot.rz/ry), solved so both feet stay pinned and flat: dry run foot drift 0.00 studs. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, smooth_transition*
- `medium` **stiff** F[0, 72] Head, UpperTorso, LeftUpperArm, RightUpperArm, RightLowerArm: The upper body does not read as someone sneaking. The head only drifts 8 deg to the right and back (Head.ry 0 to -8 on F040), the chest moves 2 deg, the upper arms are constant, and the left and right arms are exact mirror copies (both LowerArm.rx -50 to -54; identical arm silhouettes in the 3/4 view on every frame). Fix: make the head scan, left to +10 on frame 14 and right to -12 on frame 50, with the chest following by about a third (UpperTorso.ry +3 / -3.5) and tipping 1.5 deg against the weight shift (rz, 3 frames after the hips); deepen the chest breath to 28; break the arm twinning: left upper arm reaches 3 deg further forward on the exhale (frame 40), right upper arm eases back 3 deg (frame 44) and out 3 deg (rz -13 on frame 30), and the right forearm breathes 1.6x as much as the left. → *smooth_transition, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, scale_amplitude, smooth_transition*
- `medium` **transition** F[0, 72] UpperTorso, Head, LeftLowerArm, RightLowerArm: Every animated channel has its extremes on frames 0/72 and 36 (Head.ry on 40), so the whole body eases to a dead stop twice per loop: whole-body speed is 0.04 deg/frame on F000 and 0.05 on F071, and 0.12 on F036. The stop at the seam makes the loop point visible as a pause every 2.4 s even though the values match. Fix: stagger the phases so nothing stops together and the motion carries through the seam: chest breath 4 frames after the hips, head nod 8 frames, left forearm 6 frames and right forearm 10 frames (offset_overlap wraps around the loop and makes the curves cyclic). → *offset_overlap, offset_overlap, offset_overlap, offset_overlap*
- *apply_fixes:* applied 52 ops, skipped 0; saved work/crouch_idle/iter_1.blend

**Round 1 critique** (approved): Approved. All 52 iteration-0 ops applied with no skips or clamps and the render matches the dry run. Sheets 1-4: the soles are level and on the floor line in every side-view cell (lowest foot z -0.000 to +0.009, 0 penetration frames, foot drift 0.00 studs, so the feet stay pinned through the weight shift). The breathing now goes through the legs: hips drop 0.04 to F036 while knees fold 93 to 97 and the chest leans to 28 four frames later (compare F000 and F040 side views). The weight shift reads in the 3/4 view (hips toward the orange leg around F018, toward the blue around F054) with the chest tipping against it. The head looks left (F014) then right (F050, face visible in the side view on F040-F060), and the arms are no longer mirror copies. Whole-body speed stays between 1.85 and 3.35 deg/frame (was 0.04 at the seam), no dead holds, and F072 matches F000 with no seam metric. No regressions found. The motion is deliberately small, which suits a sneak idle. Only low-severity polish remains.

- `low` **timing** F[14, 50] Head: The head pans from +10 (F014) to -12 (F050) at an even rate with no pause at either side, so it reads as a slow sweep rather than a look, a hold and a look the other way. Holding the left look a few frames longer would sharpen it. Polish only. → *set_pose*
- `low` **stiff** F[0, 72] LeftHand, RightHand: The hands have no keys and stay locked to the forearms for the whole loop. A few degrees of wrist motion trailing the forearm breath would finish the arms. → *set_pose, set_pose, smooth_transition*

Before/after: `output/previews/crouch_idle_before_after.gif`

## crouch_walk

| Metric | iter 0 | iter 1 |
|---|---|---|
| accel_spikes | 0 | 0 |
| velocity_corners | 0 | 0 |
| loop_seam_issues | 0 | 0 |
| joint_limit_violations | 0 | 0 |
| dead_holds | 0 | 0 |
| lockstep_key_frames | 1 | 0 |
| twinned_channels | 0 | 0 |
| foot_slide_segments | 0 | 0 |
| foot_penetration_frames | 29 | 0 |
| floating_frames | 0 | 0 |
| overlap_score | 0.621 | 1.0 |

**Round 0 critique** (needs_work): The crouch silhouette, the arm/leg opposition and the loop seam values are right, but the legs do not work as a walk on a floor. At each contact pose the front foot hangs 0.12 studs in the air while the rear foot is 0.18 under the floor, so no root height can ground both; the stance foot eases to a stop at every contact instead of sliding back steadily; and the planted foot swivels with the pelvis twist. The upper body is frozen apart from a 20 degree shoulder swing keyed on frame 20. Fixes: stance legs re-keyed so the sole stays flat on the floor and travels back at a constant 0.035 studs/frame for 24 frames (4 frames of double support), a heel peel and a clean swing with a soft, flat landing, hip counter-twist, a small weight shift over the stance foot, staggered arms/chest/head, then plant_feet as a safety net. Dry run of these ops on a scratch copy: 0 penetration frames, 0 slide segments, 0 seam issues, overlap 1.0.

- `high` **awkward_pose** F[0, 40] LowerTorso, LeftUpperLeg, LeftLowerLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot: Feet through the floor and skating for most of the cycle. Side view F000-F006 and F033-F040: the rear (blue) foot and shin are cut by the floor line; F013-F026 the same for the orange leg. Metrics: LeftFoot under the floor on 14 frames (F013-F026, down to -0.189 at F022), RightFoot on 15 frames (F000-F006, F033-F040, -0.181), shins down to -0.235. At the contact poses (F000, F020) the front foot is 0.118 ABOVE the floor while the rear foot is at -0.178, a 0.30 stud mismatch that no root offset can fix: the front leg (thigh -75, knee 85) is 0.30 shorter than the rear leg (thigh -35, knee 80), so plant_feet alone would leave the leading foot floating at contact. The planted foot also does not move back at a steady rate: every leg channel has an extreme on frames 0 and 20, so the stance foot decelerates to a stop at each contact (contact segments: mean 0.034-0.041 studs/frame with std 0.020-0.021, i.e. +-50-60%; whole-body speed falls from ~20 to 3.0 deg/frame at F019/F039). With playback scaled to ground speed that reads as the foot alternately slipping and sticking. Fix: clear the old interior leg keys and re-key the stance leg from a 2-bone IK solve so the sole is flat (Foot rx = -(thigh + knee)), on the floor, and the ankle travels back linearly at 0.035 studs/frame from 0.80 studs in front of the root; stance lasts 24 frames per foot (left 0-24, right 20-44) which gives 4 frames of double support. Root height becomes a gentle bob, lowest just after each contact (frames 2, 22) and highest at the passing pose (12, 32), with half the old range so the head stays steady. plant_feet runs last as a safety net (dry run: max correction 0.009 studs). → *smooth_transition, smooth_transition, set_pose, set_pose, set_pose, set_pose, set_pose, smooth_transition, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, smooth_transition, plant_feet*
- `high` **timing** F[0, 40] LeftUpperLeg, LeftLowerLeg, LeftFoot, RightUpperLeg, RightLowerLeg, RightFoot: The step has no readable lift-off or touch-down. Lift-off: the trailing foot stays flat and slides forward under the floor (right foot F000-F006, left F020-F026, z -0.18 to -0.09) before it pops up; there is no heel peel, although the ankle is already at its -45 limit. Landing: the swing foot is still 0.12 above the floor on the frame the spec calls contact (left F000/F040, right F020) and only reaches the floor 3 frames later (left foot z 0.119, 0.099, 0.055, 0.010 on F000-F003) while it is already moving backward, so the foot lands late and drags. Fix: heel peel over the last 8 frames of stance (toe stays planted and keeps sliding, heel rises to 22 deg at lift-off on frame 24 left / 4 right), then a 16-frame swing with the knee folding to ~130 deg, 0.20-0.24 studs of toe clearance, the foot levelling out before it comes down, and the forward travel easing so the foot touches down flat with zero vertical speed and already matching ground speed (a careful, sneaking step). These keys are the swing half of the same IK solve as cwalk-1, so the seam at frame 0/40 stays closed. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, smooth_transition*
- `medium` **transition** F[0, 40] LeftUpperLeg, RightUpperLeg: LowerTorso.ry swings -5 to +5 and the legs follow it rigidly, so the planted foot yaws 10 degrees on the floor during its stance and drifts sideways: the left ankle is at x 0.434 on F000 (toed in, 3/4 view) and at 0.497-0.500 on F010-F020. A planted foot should not twist. Fix: counter the pelvis twist at the hips (UpperLeg.ry = -LowerTorso.ry: +5 on frame 0, -5 on frame 20, same key frames and easing as the pelvis), so the legs stay in the direction of travel and only the hips rotate over them. → *set_pose, set_pose, set_pose, set_pose, smooth_transition*
- `medium` **stiff** F[0, 40] LowerTorso, LeftUpperLeg, RightUpperLeg, LeftFoot, RightFoot: In the 3/4 view the hips run on a rail: LowerTorso has no lx at all, so the weight never moves over the supporting foot even though each foot carries the body alone for 16 frames in a deep crouch. Fix: shift the root 0.05 studs toward the stance side at mid-stance (left, +lx, on frame 12; right on frame 32), lean both legs the opposite way by 2.6 deg (UpperLeg.rz) so the feet stay where they are, and roll the ankles back by 2.2 deg (Foot.rz) so the soles stay flat. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, smooth_transition*
- `medium` **stiff** F[0, 40] UpperTorso, Head, LeftUpperArm, RightUpperArm, LeftLowerArm, RightLowerArm: Above the hips only the shoulders move: UpperTorso.rx, Head.rx and both LowerArm.rx are flat lines (motion_range 0), and pelvis twist, chest counter-twist, head and both arms are all keyed on frame 20 (lockstep 11 of 13 bones, overlap_score 0.621), so the arms swing like rigid L-shapes exactly in phase with the legs. Fix: let the chest give 2-3 deg into each step (lean to 27 just after contact on frames 5/25, back to 24 on 15/35) with the head countering 2 frames later so the gaze stays level; flex the elbow as the arm comes forward and open it as it goes back (-54 / -67, peaking 2 frames after the upper arm); delay the arm swing 3 frames behind the legs, the chest twist 1 frame and the head 3 frames for drag. → *set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, set_pose, smooth_transition, offset_overlap, offset_overlap, offset_overlap*
- *apply_fixes:* applied 105 ops, skipped 0; saved work/crouch_walk/iter_1.blend

**Round 1 critique** (approved): Approved. All 105 iteration-0 ops applied with no skips or clamps and the render matches the dry run. Sheets 1-3: both feet now sit on the floor line through stance with flat soles (lowest foot z between -0.008 and +0.010 on every frame, 0 penetration frames, shins clear). Stance travel is steady: left contact segment F000-F025 and right F019-F040 move backward with speed std 0.009 and 0.006 against means of 0.030-0.033 (was 0.020-0.021), and whole-body speed stays between 12.5 and 25.9 deg/frame, so the stop at each contact is gone. Lift-off reads: heel peels from F016/F036 with the toe planted, the foot leaves on F004/F024, the knee folds to about 130 and the toe clears by 0.11-0.20. Touch-down is flat on F000/F020 from 0.02 the frame before. The planted foot no longer swivels, the hips shift 0.05 over the stance foot (3/4 view F012 vs F032), and arms, chest and head are staggered (overlap 1.0, no lockstep). Seam: F040 matches F000, no seam or corner metrics. No regressions found. Only low-severity polish remains.

- `low` **stiff** F[0, 40] LeftHand, RightHand: The hands have no keys, so each hand stays locked in line with its forearm through the whole arm swing (3/4 view, all frames). A few degrees of wrist drag would soften the arms. Polish only: hand trails back (+rx) while its arm travels forward and leads on the way back. → *set_pose, set_pose, set_pose, set_pose, smooth_transition*
- `low` **timing** F[24, 40] LeftLowerLeg, RightLowerLeg: The swing foot's height is slightly double-humped: toe clearance peaks at 0.20 on F029-F030 (left) / F009-F010 (right), sags to 0.11 on F034-F035 / F014-F015, then holds 0.12 before it comes down over the last 3 frames (0.12, 0.07, 0.02, 0.00). It never touches the floor and is hard to see at speed; a little more knee fold late in the swing would make it one arc. → *add_breakdown, add_breakdown*

Before/after: `output/previews/crouch_walk_before_after.gif`

