"""Crouch walk: slow sneaking walk cycle in a low crouch, in place, 40 frames.

Frame 0: left foot contact (forward), 10: left foot under the hips, 20: right foot contact, 30: left leg passing.
"""
SPEC = {
    "name": "crouch_walk",
    "description": "Sneaking crouch walk: long careful steps in a low crouch, small arm swing, steady head.",
    "fps": 30, "frame_end": 40, "loop": True, "priority": "Movement", "contact": "feet",
    "keys": {
        "LowerTorso": {"ly": [(0, -0.56), (5, -0.6), (15, -0.52), (20, -0.56), (25, -0.6), (35, -0.52), (40, -0.56)],
                       "lz": [(0, -0.25), (40, -0.25)], "ry": [(0, -5), (20, 5), (40, -5)]},
        "UpperTorso": {"rx": [(0, 25), (40, 25)], "ry": [(0, 5), (20, -5), (40, 5)]},
        "Head": {"rx": [(0, -20), (40, -20)], "ry": [(0, -2), (20, 2), (40, -2)]},
        "LeftUpperLeg": {"rx": [(0, -75), (10, -55), (20, -35), (30, -65), (40, -75)]},
        "LeftLowerLeg": {"rx": [(0, 85), (5, 100), (10, 95), (20, 80), (30, 120), (40, 85)]},
        "LeftFoot": {"rx": [(0, -10), (10, -40), (20, -45), (30, -45), (40, -10)]},
        "RightUpperLeg": {"rx": [(0, -35), (10, -65), (20, -75), (30, -55), (40, -35)]},
        "RightLowerLeg": {"rx": [(0, 80), (10, 120), (20, 85), (25, 100), (30, 95), (40, 80)]},
        "RightFoot": {"rx": [(0, -45), (10, -45), (20, -10), (30, -40), (40, -45)]},
        "LeftUpperArm": {"rx": [(0, -15), (20, -35), (40, -15)], "rz": [(0, 10), (40, 10)]},
        "LeftLowerArm": {"rx": [(0, -60), (40, -60)]},
        "RightUpperArm": {"rx": [(0, -35), (20, -15), (40, -35)], "rz": [(0, -10), (40, -10)]},
        "RightLowerArm": {"rx": [(0, -60), (40, -60)]},
    },
}
