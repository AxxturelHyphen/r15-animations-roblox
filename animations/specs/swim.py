"""Swim: front-crawl loop, body prone (LowerTorso tipped forward), 40 frames."""
SPEC = {
    "name": "swim",
    "description": "Front crawl: prone body, alternating overhead arm strokes with recovery out to the side, flutter kick, body roll, breath to the side.",
    "fps": 30, "frame_end": 40, "loop": True, "priority": "Movement", "contact": "none",
    "keys": {
        "LowerTorso": {"rx": [(0, 80), (10, 83), (20, 80), (30, 83), (40, 80)]},
        "UpperTorso": {"ry": [(0, 15), (20, -15), (40, 15)], "rx": [(0, -10), (40, -10)]},
        "Head": {"rx": [(0, -48), (40, -48)], "ry": [(0, 0), (20, 0), (25, 30), (30, 0), (40, 0)]},
        "LeftUpperArm": {"rx": [(0, -170), (10, -90), (20, 10), (30, -90), (40, -170)],
                         "rz": [(0, 10), (10, 0), (20, 10), (30, 80), (40, 10)]},
        "LeftLowerArm": {"rx": [(0, -10), (10, -30), (20, -10), (30, -40), (40, -10)]},
        "RightUpperArm": {"rx": [(0, 10), (10, -90), (20, -170), (30, -90), (40, 10)],
                          "rz": [(0, -10), (10, -80), (20, -10), (30, 0), (40, -10)]},
        "RightLowerArm": {"rx": [(0, -10), (10, -40), (20, -10), (30, -30), (40, -10)]},
        "LeftUpperLeg": {"rx": [(0, -15), (5, 15), (10, -15), (15, 15), (20, -15), (25, 15), (30, -15), (35, 15), (40, -15)]},
        "LeftLowerLeg": {"rx": [(0, 10), (5, 30), (10, 10), (15, 30), (20, 10), (25, 30), (30, 10), (35, 30), (40, 10)]},
        "LeftFoot": {"rx": [(0, 40), (40, 40)]},
        "RightUpperLeg": {"rx": [(0, 15), (5, -15), (10, 15), (15, -15), (20, 15), (25, -15), (30, 15), (35, -15), (40, 15)]},
        "RightLowerLeg": {"rx": [(0, 30), (5, 10), (10, 30), (15, 10), (20, 30), (25, 10), (30, 30), (35, 10), (40, 30)]},
        "RightFoot": {"rx": [(0, 40), (40, 40)]},
    },
}
