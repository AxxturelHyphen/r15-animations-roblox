--!strict
-- Shared constants for game feedback (server decides, FeedbackClient renders).
--
-- Sounds use only Roblox's built-in content files (rbxasset://sounds/...), which ship with every client,
-- so there are no third-party asset IDs to license. The ones marked "core" are used by Roblox's own
-- character sounds and are certain to exist; the others are classic built-ins. If one is missing in a
-- future client it simply stays silent. Swap any of them for your own uploaded sounds here.

local Feedback = {}

Feedback.Sounds = {
	hit = { id = "rbxasset://sounds/action_jump_land.mp3", volume = 0.9, pitch = 1.6 }, -- core
	heavyHit = { id = "rbxasset://sounds/action_jump_land.mp3", volume = 1.0, pitch = 1.05 }, -- core
	slash = { id = "rbxasset://sounds/swordslash.wav", volume = 0.7, pitch = 1 }, -- classic sword
	unsheath = { id = "rbxasset://sounds/unsheath.wav", volume = 0.6, pitch = 1 }, -- classic sword
	block = { id = "rbxasset://sounds/unsheath.wav", volume = 0.9, pitch = 1.8 }, -- metallic clang
	parry = { id = "rbxasset://sounds/unsheath.wav", volume = 1.0, pitch = 2.4 },
	ko = { id = "rbxasset://sounds/uuhhh.mp3", volume = 0.8, pitch = 1 }, -- classic death sound
	record = { id = "rbxasset://sounds/electronicpingshort.wav", volume = 0.7, pitch = 1 },
	splash = { id = "rbxasset://sounds/impact_water.mp3", volume = 1.0, pitch = 0.8 }, -- core
	land = { id = "rbxasset://sounds/action_jump_land.mp3", volume = 1.0, pitch = 0.7 }, -- core
	clap = { id = "rbxasset://sounds/action_jump_land.mp3", volume = 1.0, pitch = 2.6 }, -- core, pitched up into a slap
	launch = { id = "rbxasset://sounds/action_jump.mp3", volume = 1.0, pitch = 0.6 }, -- core
}

-- Event kinds sent through Remotes.Feedback (server -> clients).
export type HitKind = "normal" | "heavy" | "blocked" | "parry" | "sneak" | "guardbreak"

Feedback.Colors = {
	normal = Color3.fromRGB(255, 255, 255),
	heavy = Color3.fromRGB(255, 196, 64),
	blocked = Color3.fromRGB(150, 190, 255),
	parry = Color3.fromRGB(120, 255, 200),
	sneak = Color3.fromRGB(255, 110, 110),
	guardbreak = Color3.fromRGB(255, 150, 40),
	record = Color3.fromRGB(255, 220, 90),
	feed = Color3.fromRGB(235, 235, 240),
}

-- Gameplay tuning shared by server and client.
Feedback.HEAVY_LANDING_STUDS = 18 -- falls at least this high get the superhero landing
Feedback.HIGH_FIVE_RANGE = 7 -- studs
Feedback.HIGH_FIVE_WINDOW = 3 -- seconds a high-five request waits for a partner
Feedback.TAUNT_WINDOW = 4 -- seconds after a KO in which an emote counts as a taunt
Feedback.CHALLENGE_SECONDS = 10

-- Play a built-in sound, positioned in the world when a position is given (client side).
function Feedback.playSound(name: string, position: Vector3?)
	local spec = Feedback.Sounds[name]
	if spec == nil then
		return
	end
	local sound = Instance.new("Sound")
	sound.SoundId = spec.id
	sound.Volume = spec.volume
	sound.PlaybackSpeed = spec.pitch
	local holder: Instance
	if position then
		local part = Instance.new("Part")
		part.Anchored = true
		part.CanCollide = false
		part.CanQuery = false
		part.CanTouch = false
		part.Transparency = 1
		part.Size = Vector3.new(0.2, 0.2, 0.2)
		part.CFrame = CFrame.new(position)
		part.Parent = workspace
		sound.RollOffMinDistance = 10
		sound.RollOffMaxDistance = 120
		holder = part
	else
		holder = game:GetService("SoundService")
	end
	sound.Parent = holder
	sound:Play()
	task.delay(3, function()
		if holder:IsA("BasePart") then
			holder:Destroy()
		else
			sound:Destroy()
		end
	end)
end

return Feedback
