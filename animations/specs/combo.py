"""Combo: three-hit chain from guard. Left jab (impact 6), right cross (16), left hook (30), recover by 48."""
SPEC = {
    "name": "combo",
    "description": "Three-hit combo: left jab, right cross with hip turn, left hook with the elbow up, then recovery to guard.",
    "fps": 30, "frame_end": 48, "loop": False, "priority": "Action", "contact": "feet",
    "keys": {
        "LowerTorso": {"ly": [(0, -0.12), (48, -0.12)],
                       "ry": [(0, 0), (6, -5), (16, 15), (24, -5), (30, -20), (48, 0)]},
        "UpperTorso": {"ry": [(0, 0), (6, -8), (16, 25), (24, -10), (30, -30), (48, 0)], "rx": [(0, 5), (16, 10), (48, 5)]},
        "Head": {"ry": [(0, 0), (16, -20), (30, 25), (48, 0)], "rx": [(0, 5), (48, 5)]},
        "LeftUpperArm": {"rx": [(0, -50), (6, -90), (11, -50), (24, -50), (30, -85), (36, -60), (48, -50)],
                         "rz": [(0, 15), (6, 0), (11, 15), (24, 30), (30, 80), (36, 30), (48, 15)]},
        "LeftLowerArm": {"rx": [(0, -110), (6, -5), (11, -110), (24, -100), (30, -90), (36, -100), (48, -110)]},
        "RightUpperArm": {"rx": [(0, -50), (11, -45), (16, -90), (22, -50), (48, -50)],
                          "rz": [(0, -15), (11, -25), (16, 10), (22, -15), (48, -15)]},
        "RightLowerArm": {"rx": [(0, -110), (11, -120), (16, -5), (22, -110), (48, -110)]},
        "LeftUpperLeg": {"rx": [(0, -15), (48, -15)]},
        "LeftLowerLeg": {"rx": [(0, 15), (48, 15)]},
        "RightUpperLeg": {"rx": [(0, 15), (48, 15)]},
        "RightLowerLeg": {"rx": [(0, 10), (48, 10)]},
        "RightFoot": {"rx": [(0, 0), (16, 15), (22, 0), (48, 0)]},
    },
}
