"""Point emote: point forward with the right arm, hold, lower. 40 frames."""
SPEC = {
    "name": "point",
    "description": "Point: turn slightly into a straight-armed point forward and a little up, hold, then lower.",
    "fps": 30, "frame_end": 40, "loop": False, "priority": "Action", "contact": "feet",
    "keys": {
        "UpperTorso": {"ry": [(0, 0), (8, -10), (30, -10), (40, 0)]},
        "Head": {"ry": [(0, 0), (8, 5), (30, 5), (40, 0)], "rx": [(0, 0), (8, -5), (30, -5), (40, 0)]},
        "RightUpperArm": {"rx": [(0, 0), (8, -100), (30, -100), (40, 0)], "rz": [(0, -5), (8, -10), (30, -10), (40, -5)]},
        "RightLowerArm": {"rx": [(0, -8), (8, -5), (30, -5), (40, -8)]},
        "RightHand": {"rx": [(0, 0), (8, 0), (40, 0)]},
        "LeftUpperArm": {"rx": [(0, 0), (8, 10), (30, 10), (40, 0)], "rz": [(0, 6), (40, 6)]},
    },
}
