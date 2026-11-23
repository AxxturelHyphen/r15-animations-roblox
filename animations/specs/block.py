"""Block: held guard loop, forearms raised in front of the face, braced stance. 30 frames."""
SPEC = {
    "name": "block",
    "description": "Held block: forearms crossed up in front of the face, chin tucked, knees bent in a braced stance, subtle breathing.",
    "fps": 30, "frame_end": 30, "loop": True, "priority": "Action", "contact": "feet",
    "keys": {
        "LowerTorso": {"ly": [(0, -0.15), (15, -0.18), (30, -0.15)]},
        "UpperTorso": {"rx": [(0, 10), (15, 12), (30, 10)]},
        "Head": {"rx": [(0, 10), (30, 10)]},
        "LeftUpperArm": {"rx": [(0, -80), (30, -80)], "rz": [(0, -25), (30, -25)]},
        "LeftLowerArm": {"rx": [(0, -100), (30, -100)]},
        "RightUpperArm": {"rx": [(0, -80), (30, -80)], "rz": [(0, 25), (30, 25)]},
        "RightLowerArm": {"rx": [(0, -100), (30, -100)]},
        "LeftUpperLeg": {"rx": [(0, -25), (30, -25)]},
        "LeftLowerLeg": {"rx": [(0, 35), (30, 35)]},
        "LeftFoot": {"rx": [(0, -10), (30, -10)]},
        "RightUpperLeg": {"rx": [(0, 10), (30, 10)]},
        "RightLowerLeg": {"rx": [(0, 20), (30, 20)]},
        "RightFoot": {"rx": [(0, -30), (30, -30)]},
    },
}
