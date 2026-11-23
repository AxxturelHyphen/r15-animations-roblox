"""Death: struck, staggers, knees buckle, falls onto the back and lies still. 50 frames.

In Roblox set Humanoid.BreakJointsOnDeath = false so the animation can play instead of the ragdoll break.
"""
SPEC = {
    "name": "death",
    "description": "Death: recoil, stagger, knees buckle, collapse backward onto the floor, settle limp with the head turned.",
    "fps": 30, "frame_end": 50, "loop": False, "priority": "Action4", "contact": "body",
    "keys": {
        "LowerTorso": {"rx": [(0, 0), (6, -5), (18, 10), (28, -60), (34, -90), (50, -90)],
                       "ly": [(0, 0), (6, -0.1), (18, -0.6), (28, -1.1), (34, -1.5), (50, -1.5)],
                       "lz": [(0, 0), (6, -0.2), (18, -0.1), (34, -0.6), (50, -0.6)]},
        "UpperTorso": {"rx": [(0, 0), (6, -20), (18, 20), (28, -10), (34, 0), (50, 0)]},
        "Head": {"rx": [(0, 0), (6, -25), (18, 20), (30, -20), (36, 0), (50, -5)],
                 "ry": [(0, 0), (34, 0), (40, 35), (50, 35)]},
        "LeftUpperLeg": {"rx": [(0, 0), (18, -45), (28, -30), (34, -5), (50, -5)]},
        "LeftLowerLeg": {"rx": [(0, 0), (18, 95), (28, 60), (34, 10), (50, 10)]},
        "RightUpperLeg": {"rx": [(0, 0), (18, -35), (28, -40), (34, -15), (50, -15)], "rz": [(0, 0), (34, -10), (50, -10)]},
        "RightLowerLeg": {"rx": [(0, 0), (18, 85), (28, 70), (34, 30), (50, 30)]},
        "LeftUpperArm": {"rx": [(0, 0), (6, -40), (18, -20), (34, -10), (50, -10)], "rz": [(0, 5), (6, 40), (28, 30), (34, 70), (50, 70)]},
        "LeftLowerArm": {"rx": [(0, -8), (6, -30), (34, -20), (50, -20)]},
        "RightUpperArm": {"rx": [(0, 0), (6, -40), (18, -20), (34, -10), (50, -10)], "rz": [(0, -5), (6, -40), (28, -30), (34, -60), (50, -60)]},
        "RightLowerArm": {"rx": [(0, -8), (6, -30), (34, -35), (50, -35)]},
    },
}
