"""High five: wind up, slap a partner's raised hand at head height (contact frame 10), follow through. 30 frames.

The game plays it on both friends at the same time, facing each other, and fires the "Clap" marker on contact.
"""
SPEC = {
    "name": "high_five",
    "description": "High five: lean in, wind the right hand up and back, slap forward at head height, follow through and relax.",
    "fps": 30, "frame_end": 30, "loop": False, "priority": "Action", "contact": "feet",
    "keys": {
        "LowerTorso": {"ly": [(0, 0), (6, -0.08), (10, 0.02), (16, -0.04), (30, 0)]},
        "UpperTorso": {"ry": [(0, 0), (6, -14), (10, 10), (16, 6), (30, 0)], "rx": [(0, 0), (6, -4), (10, 8), (30, 0)]},
        "Head": {"rx": [(0, 0), (6, -12), (10, -6), (30, 0)], "ry": [(0, 0), (6, 8), (10, -4), (30, 0)]},
        "RightUpperArm": {"rx": [(0, 0), (6, -150), (10, -125), (14, -110), (22, -40), (30, 0)],
                          "rz": [(0, -5), (6, -30), (10, -10), (30, -5)]},
        "RightLowerArm": {"rx": [(0, -8), (6, -70), (10, -8), (14, -15), (30, -8)]},
        "RightHand": {"rx": [(0, 0), (6, 25), (10, -15), (14, 0), (30, 0)]},
        "LeftUpperArm": {"rx": [(0, 0), (6, 10), (10, 15), (30, 0)], "rz": [(0, 6), (10, 12), (30, 6)]},
        "LeftUpperLeg": {"rx": [(0, 0), (6, -5), (10, -12), (20, -5), (30, 0)]},
        "LeftLowerLeg": {"rx": [(0, 0), (10, 12), (30, 0)]},
        "RightUpperLeg": {"rx": [(0, 0), (10, 6), (30, 0)]},
    },
}
