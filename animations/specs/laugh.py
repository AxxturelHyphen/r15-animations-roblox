"""Laugh emote: lean back, shoulders bounce in laughter, hand on belly, settle. 48 frames."""
SPEC = {
    "name": "laugh",
    "description": "Laugh: head thrown back, chest and shoulders bouncing, one hand on the belly, then settle back to neutral.",
    "fps": 30, "frame_end": 48, "loop": False, "priority": "Action", "contact": "feet",
    "keys": {
        "LowerTorso": {"ly": [(0, 0), (8, -0.05), (12, 0), (16, -0.05), (20, 0), (24, -0.05), (28, 0), (32, -0.05), (40, 0), (48, 0)]},
        "UpperTorso": {"rx": [(0, 0), (6, -10), (10, -6), (14, -12), (18, -6), (22, -12), (26, -6), (30, -12), (34, -6), (40, 0), (48, 0)]},
        "Head": {"rx": [(0, 0), (6, -20), (10, -12), (14, -22), (18, -12), (22, -22), (26, -12), (30, -22), (34, -12), (40, 0), (48, 0)]},
        "RightUpperArm": {"rx": [(0, 0), (6, -15), (34, -15), (44, 0)], "rz": [(0, -5), (6, 15), (34, 15), (44, -5)]},
        "RightLowerArm": {"rx": [(0, -8), (6, -95), (34, -95), (44, -8)]},
        "LeftUpperArm": {"rx": [(0, 0), (6, 10), (34, 10), (44, 0)], "rz": [(0, 5), (6, 15), (34, 15), (44, 5)]},
        "LeftLowerArm": {"rx": [(0, -8), (6, -25), (44, -8)]},
    },
}
