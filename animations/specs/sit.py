"""Sit: relaxed seated loop on a Roblox Seat, thighs horizontal, hands on thighs, 60 frames."""
SPEC = {
    "name": "sit",
    "description": "Seated idle on a Seat: thighs forward, shins hanging, hands resting on the thighs, breathing and a slow look-around.",
    "fps": 30, "frame_end": 60, "loop": True, "priority": "Core", "contact": "none",
    "keys": {
        "UpperTorso": {"rx": [(0, -5), (30, -3), (60, -5)]},
        "Head": {"ry": [(0, 0), (30, 12), (60, 0)], "rx": [(0, 0), (30, 3), (60, 0)]},
        "LeftUpperArm": {"rx": [(0, -25), (60, -25)], "rz": [(0, 4), (60, 4)]},
        "LeftLowerArm": {"rx": [(0, -60), (30, -62), (60, -60)]},
        "RightUpperArm": {"rx": [(0, -25), (60, -25)], "rz": [(0, -4), (60, -4)]},
        "RightLowerArm": {"rx": [(0, -60), (30, -62), (60, -60)]},
        "LeftUpperLeg": {"rx": [(0, -90), (60, -90)], "rz": [(0, 4), (60, 4)]},
        "LeftLowerLeg": {"rx": [(0, 90), (60, 90)]},
        "RightUpperLeg": {"rx": [(0, -90), (60, -90)], "rz": [(0, -4), (60, -4)]},
        "RightLowerLeg": {"rx": [(0, 90), (30, 80), (60, 90)]},
        "RightFoot": {"rx": [(0, 0), (30, -10), (60, 0)]},
    },
}
