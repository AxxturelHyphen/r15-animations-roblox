"""Crouch idle: low sneaking crouch, breathing, 72 frames. Hips back over the feet, torso forward."""
SPEC = {
    "name": "crouch_idle",
    "description": "Low crouch idle: knees deeply bent with feet flat, hips back, torso leaning forward, arms ready, breathing.",
    "fps": 30, "frame_end": 72, "loop": True, "priority": "Idle", "contact": "feet",
    "keys": {
        "LowerTorso": {"ly": [(0, -0.56), (36, -0.58), (72, -0.56)], "lz": [(0, -0.25), (72, -0.25)]},
        "UpperTorso": {"rx": [(0, 25), (36, 27), (72, 25)]},
        "Head": {"rx": [(0, -20), (36, -21), (72, -20)], "ry": [(0, 0), (40, -8), (72, 0)]},
        "LeftUpperArm": {"rx": [(0, -25), (72, -25)], "rz": [(0, 10), (72, 10)]},
        "LeftLowerArm": {"rx": [(0, -50), (36, -54), (72, -50)]},
        "RightUpperArm": {"rx": [(0, -25), (72, -25)], "rz": [(0, -10), (72, -10)]},
        "RightLowerArm": {"rx": [(0, -50), (36, -54), (72, -50)]},
        "LeftUpperLeg": {"rx": [(0, -55), (72, -55)], "rz": [(0, 5), (72, 5)]},
        "LeftLowerLeg": {"rx": [(0, 95), (72, 95)]},
        "LeftFoot": {"rx": [(0, -40), (72, -40)]},
        "RightUpperLeg": {"rx": [(0, -55), (72, -55)], "rz": [(0, -5), (72, -5)]},
        "RightLowerLeg": {"rx": [(0, 95), (72, 95)]},
        "RightFoot": {"rx": [(0, -40), (72, -40)]},
    },
}
