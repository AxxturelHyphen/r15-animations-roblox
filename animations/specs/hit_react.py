"""Hit reaction: struck from the front, snap back, recoil and recover. 20 frames."""
SPEC = {
    "name": "hit_react",
    "description": "Frontal hit reaction: the upper body snaps back, the arms fly out, then recovers to neutral.",
    "fps": 30,
    "frame_end": 20,
    "loop": False,
    "priority": "Action",
    "keys": {
        "LowerTorso": {"lz": [(0, 0), (3, -0.25), (8, -0.1), (20, 0)], "ly": [(0, 0), (3, -0.1), (8, -0.05), (20, 0)]},
        "UpperTorso": {"rx": [(0, 0), (3, -25), (8, 5), (20, 0)]},
        "Head": {"rx": [(0, 0), (3, -30), (8, 10), (20, 0)]},
        "LeftUpperArm": {"rx": [(0, 0), (3, -30), (8, -10), (20, 0)], "rz": [(0, 5), (3, 35), (8, 10), (20, 5)]},
        "LeftLowerArm": {"rx": [(0, -8), (3, -30), (8, -15), (20, -8)]},
        "RightUpperArm": {"rx": [(0, 0), (3, -30), (8, -10), (20, 0)], "rz": [(0, -5), (3, -35), (8, -10), (20, -5)]},
        "RightLowerArm": {"rx": [(0, -8), (3, -30), (8, -15), (20, -8)]},
        "LeftUpperLeg": {"rx": [(0, 0), (3, 10), (8, -5), (20, 0)]},
        "LeftLowerLeg": {"rx": [(0, 0), (3, 10), (8, 10), (20, 0)]},
        "RightUpperLeg": {"rx": [(0, 0), (3, 10), (8, -5), (20, 0)]},
        "RightLowerLeg": {"rx": [(0, 0), (3, 10), (8, 10), (20, 0)]},
    },
}
