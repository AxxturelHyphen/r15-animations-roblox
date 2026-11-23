"""Salute emote: stand tall, snap the right hand to the brow, hold, lower. 40 frames."""
SPEC = {
    "name": "salute",
    "description": "Military salute: chest up, right hand snaps to the brow with the elbow out, crisp hold, then lowers.",
    "fps": 30, "frame_end": 40, "loop": False, "priority": "Action", "contact": "feet",
    "keys": {
        "UpperTorso": {"rx": [(0, 0), (6, -5), (32, -5), (40, 0)]},
        "Head": {"rx": [(0, 0), (6, -5), (32, -5), (40, 0)]},
        "RightUpperArm": {"rx": [(0, 0), (6, -70), (32, -70), (40, 0)], "rz": [(0, -5), (6, -55), (32, -55), (40, -5)]},
        "RightLowerArm": {"rx": [(0, -8), (6, -130), (32, -130), (40, -8)]},
        "RightHand": {"rx": [(0, 0), (6, 20), (32, 20), (40, 0)]},
        "LeftUpperArm": {"rz": [(0, 6), (6, 2), (32, 2), (40, 6)]},
        "LeftUpperLeg": {"rz": [(0, 2), (6, 0), (32, 0), (40, 2)]},
        "RightUpperLeg": {"rz": [(0, -2), (6, 0), (32, 0), (40, -2)]},
    },
}
