"""Heavy landing ("superhero landing") after a big fall: catch, drop into a one-knee crouch with the right fist
on the floor (impact frame 4), hold, then rise. 26 frames. Played when the character lands from 18+ studs."""
SPEC = {
    "name": "land_heavy",
    "description": "Superhero landing: absorb the impact into a deep crouch, right fist planted on the floor, left arm back, hold, rise.",
    "fps": 30, "frame_end": 26, "loop": False, "priority": "Action", "contact": "feet",
    "keys": {
        "LowerTorso": {"ly": [(0, -0.2), (4, -0.95), (12, -0.9), (26, 0)], "lz": [(0, 0), (4, -0.35), (12, -0.3), (26, 0)]},
        "UpperTorso": {"rx": [(0, 10), (4, 40), (12, 36), (20, 12), (26, 0)]},
        "Head": {"rx": [(0, 0), (4, -30), (12, -28), (20, -8), (26, 0)]},
        "LeftUpperLeg": {"rx": [(0, -40), (4, -95), (12, -92), (26, 0)]},
        "LeftLowerLeg": {"rx": [(0, 60), (4, 120), (12, 118), (26, 0)]},
        "LeftFoot": {"rx": [(0, -20), (4, -25), (12, -26), (26, 0)]},
        "RightUpperLeg": {"rx": [(0, -20), (4, -10), (12, -12), (26, 0)]},
        "RightLowerLeg": {"rx": [(0, 50), (4, 130), (12, 128), (26, 0)]},
        "RightFoot": {"rx": [(0, 0), (4, 40), (12, 40), (26, 0)]},
        "RightUpperArm": {"rx": [(0, -30), (4, -35), (12, -35), (26, 0)], "rz": [(0, -80), (4, -10), (12, -10), (26, -5)]},
        "RightLowerArm": {"rx": [(0, -20), (4, -5), (12, -5), (26, -8)]},
        "LeftUpperArm": {"rx": [(0, -20), (4, 45), (12, 40), (26, 0)], "rz": [(0, 90), (4, 50), (12, 48), (26, 6)]},
        "LeftLowerArm": {"rx": [(0, -20), (4, -15), (26, -8)]},
    },
}
