"""Kick: right front kick from a guard stance. Chamber, extend (impact at frame 9), re-chamber, recover. 30 frames."""
GUARD = {"rx": -50, "lower": -110}
SPEC = {
    "name": "kick",
    "description": "Right front kick: knee chamber, snap extension (impact frame 9), re-chamber, step down, recover to guard.",
    "fps": 30, "frame_end": 30, "loop": False, "priority": "Action", "contact": "feet",
    "keys": {
        "LowerTorso": {"ly": [(0, -0.1), (9, -0.05), (30, -0.1)], "lz": [(0, 0), (9, -0.15), (30, 0)]},
        "UpperTorso": {"rx": [(0, 5), (6, 0), (9, -15), (15, -5), (30, 5)]},
        "Head": {"rx": [(0, 5), (9, 15), (30, 5)]},
        "RightUpperLeg": {"rx": [(0, 10), (6, -90), (9, -85), (12, -85), (15, -85), (22, 5), (30, 10)]},
        "RightLowerLeg": {"rx": [(0, 15), (6, 110), (9, 5), (12, 5), (15, 100), (22, 20), (30, 15)]},
        "RightFoot": {"rx": [(0, -15), (6, 20), (9, -20), (15, 20), (22, -10), (30, -15)]},
        "LeftUpperLeg": {"rx": [(0, -15), (9, -10), (30, -15)]},
        "LeftLowerLeg": {"rx": [(0, 15), (9, 20), (30, 15)]},
        "LeftUpperArm": {"rx": [(0, -50), (9, -30), (30, -50)], "rz": [(0, 15), (9, 30), (30, 15)]},
        "LeftLowerArm": {"rx": [(0, -110), (9, -90), (30, -110)]},
        "RightUpperArm": {"rx": [(0, -50), (9, -20), (30, -50)], "rz": [(0, -15), (9, -35), (30, -15)]},
        "RightLowerArm": {"rx": [(0, -110), (9, -80), (30, -110)]},
    },
}
