"""Idle: relaxed breathing loop, 96 frames at 30 fps (3.2 s)."""
SPEC = {
    "name": "idle",
    "description": "Relaxed standing idle with breathing, a slight weight shift and a small look-around.",
    "fps": 30,
    "frame_end": 96,
    "loop": True,
    "priority": "Idle",
    "keys": {
        "LowerTorso": {"ly": [(0, 0), (48, -0.03), (96, 0)], "lx": [(0, 0), (48, 0.04), (96, 0)]},
        "UpperTorso": {"rx": [(0, 0), (48, 2), (96, 0)]},
        "Head": {"rx": [(0, 0), (48, -2), (96, 0)], "ry": [(0, 0), (48, 8), (96, 0)]},
        "LeftUpperArm": {"rz": [(0, 6), (48, 8), (96, 6)], "rx": [(0, 2), (96, 2)]},
        "LeftLowerArm": {"rx": [(0, -8), (48, -10), (96, -8)]},
        "RightUpperArm": {"rz": [(0, -6), (48, -8), (96, -6)], "rx": [(0, 2), (96, 2)]},
        "RightLowerArm": {"rx": [(0, -8), (48, -10), (96, -8)]},
        "LeftUpperLeg": {"rz": [(0, 2), (96, 2)]},
        "RightUpperLeg": {"rz": [(0, -2), (96, -2)]},
    },
}
