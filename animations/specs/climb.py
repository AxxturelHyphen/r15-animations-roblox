"""Climb: hand-over-hand ladder/truss climb loop, 30 frames. The truss is directly in front of the character."""
SPEC = {
    "name": "climb",
    "description": "Ladder/truss climb loop: opposite hand and foot reach up together, pull-up through the body, look up.",
    "fps": 30, "frame_end": 30, "loop": True, "priority": "Movement", "contact": "none",
    "keys": {
        "LowerTorso": {"ly": [(0, 0), (7, 0.1), (15, 0), (22, 0.1), (30, 0)]},
        "UpperTorso": {"rx": [(0, 5), (30, 5)], "ry": [(0, 4), (15, -4), (30, 4)]},
        "Head": {"rx": [(0, -15), (30, -15)]},
        "LeftUpperArm": {"rx": [(0, -160), (15, -110), (30, -160)]},
        "LeftLowerArm": {"rx": [(0, -40), (15, -90), (30, -40)]},
        "RightUpperArm": {"rx": [(0, -110), (15, -160), (30, -110)]},
        "RightLowerArm": {"rx": [(0, -90), (15, -40), (30, -90)]},
        "LeftUpperLeg": {"rx": [(0, -25), (15, -75), (30, -25)]},
        "LeftLowerLeg": {"rx": [(0, 40), (15, 100), (30, 40)]},
        "LeftFoot": {"rx": [(0, -15), (15, -25), (30, -15)]},
        "RightUpperLeg": {"rx": [(0, -75), (15, -25), (30, -75)]},
        "RightLowerLeg": {"rx": [(0, 100), (15, 40), (30, 100)]},
        "RightFoot": {"rx": [(0, -25), (15, -15), (30, -25)]},
    },
}
