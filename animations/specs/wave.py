"""Wave emote: raise the right arm, wave the forearm three times, lower. 48 frames."""
SPEC = {
    "name": "wave",
    "description": "Friendly wave: the right arm raises, the forearm waves side to side three times, then lowers.",
    "fps": 30,
    "frame_end": 48,
    "loop": False,
    "priority": "Action",
    "keys": {
        "RightUpperArm": {"rz": [(0, -6), (8, -150), (38, -150), (48, -6)], "rx": [(0, 0), (8, -20), (38, -20), (48, 0)]},
        "RightLowerArm": {"rz": [(0, 0), (8, 30), (14, 50), (20, 10), (26, 50), (32, 10), (38, 30), (48, 0)]},
        "RightHand": {"rz": [(0, 0), (8, 0), (14, 15), (20, -15), (26, 15), (32, -15), (38, 0), (48, 0)]},
        "Head": {"rz": [(0, 0), (8, 6), (38, 6), (48, 0)], "ry": [(0, 0), (8, -10), (38, -10), (48, 0)]},
        "UpperTorso": {"rz": [(0, 0), (8, 4), (38, 4), (48, 0)]},
        "LeftUpperArm": {"rz": [(0, 6), (48, 6)]},
    },
}
