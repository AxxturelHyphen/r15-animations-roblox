"""Swim idle: treading water upright, sculling arms and eggbeater legs, 60 frames."""
SPEC = {
    "name": "swim_idle",
    "description": "Treading water: upright body bobbing, hands sculling in and out at the sides, alternating eggbeater kicks.",
    "fps": 30, "frame_end": 60, "loop": True, "priority": "Movement", "contact": "none",
    "keys": {
        "LowerTorso": {"rx": [(0, 10), (60, 10)], "ly": [(0, 0), (15, 0.08), (30, 0), (45, 0.08), (60, 0)]},
        "UpperTorso": {"rx": [(0, -5), (30, -3), (60, -5)]},
        "Head": {"rx": [(0, -12), (60, -12)], "ry": [(0, 0), (30, 10), (60, 0)]},
        "LeftUpperArm": {"rz": [(0, 50), (15, 60), (30, 50), (45, 60), (60, 50)], "rx": [(0, -20), (60, -20)],
                         "ry": [(0, 20), (15, -20), (30, 20), (45, -20), (60, 20)]},
        "LeftLowerArm": {"rx": [(0, -60), (60, -60)]},
        "RightUpperArm": {"rz": [(0, -60), (15, -50), (30, -60), (45, -50), (60, -60)], "rx": [(0, -20), (60, -20)],
                          "ry": [(0, 20), (15, -20), (30, 20), (45, -20), (60, 20)]},
        "RightLowerArm": {"rx": [(0, -60), (60, -60)]},
        "LeftUpperLeg": {"rx": [(0, -50), (15, -30), (30, -50), (45, -30), (60, -50)], "rz": [(0, 15), (60, 15)]},
        "LeftLowerLeg": {"rx": [(0, 90), (15, 50), (30, 90), (45, 50), (60, 90)]},
        "LeftFoot": {"rx": [(0, 20), (60, 20)]},
        "RightUpperLeg": {"rx": [(0, -30), (15, -50), (30, -30), (45, -50), (60, -30)], "rz": [(0, -15), (60, -15)]},
        "RightLowerLeg": {"rx": [(0, 50), (15, 90), (30, 50), (45, 90), (60, 50)]},
        "RightFoot": {"rx": [(0, 20), (60, 20)]},
    },
}
