--!strict
-- Replaces Roblox's default "Animate" script (same name in StarterCharacterScripts).
-- Drives the AnimationPack clips from Humanoid state:
--   idle / walk / run (playback speed matched to ground speed), jump -> fall, climb, swim / swim_idle,
--   sit, death, crouch (C or Left Ctrl) with crouch_idle / crouch_walk, and chat emotes "/e <name>".

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local UserInputService = game:GetService("UserInputService")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local AnimationController = require(pack:WaitForChild("AnimationController"))
local AnimationMeta = require(pack:WaitForChild("AnimationMeta"))

local character = script.Parent
local humanoid = character:WaitForChild("Humanoid") :: Humanoid
local controller = AnimationController.new(humanoid)

local EMOTES = {
	wave = true,
	dance = true,
	cheer = true,
	point = true,
	laugh = true,
	clap = true,
	salute = true,
}
local MOVE_THRESHOLD = 0.75 -- studs/s; below this the character counts as standing still
local RUN_THRESHOLD = 12 -- studs/s; above this walk becomes run
local CROUCH_SPEED_FACTOR = 0.5

type Mode = "ground" | "air" | "climb" | "swim" | "seated" | "dead"
local mode: Mode = "ground"
local crouching = false
local standingWalkSpeed = humanoid.WalkSpeed
local groundSpeed = 0
local currentEmote: string? = nil
local jumpStartedAt = -math.huge

-- Playback speed so the feet match the ground speed the cycle was authored for.
local function cycleSpeed(name: string, speed: number): number
	local meta = AnimationMeta[name]
	local authored = meta and meta.authoredSpeed
	if authored and authored > 0 then
		return math.clamp(speed / authored, 0.4, 3)
	end
	return 1
end

local function stopEmote()
	if currentEmote then
		controller:stopAction(currentEmote, 0.2)
		currentEmote = nil
	end
end

local function updateGround()
	if mode ~= "ground" then
		return
	end
	if groundSpeed > MOVE_THRESHOLD then
		stopEmote()
		if crouching then
			controller:playBase("crouch_walk", 0.2, cycleSpeed("crouch_walk", groundSpeed))
		elseif groundSpeed > RUN_THRESHOLD then
			controller:playBase("run", 0.2, cycleSpeed("run", groundSpeed))
		else
			controller:playBase("walk", 0.2, cycleSpeed("walk", groundSpeed))
		end
	else
		controller:playBase(if crouching then "crouch_idle" else "idle", 0.25, 1)
	end
end

local function setMode(newMode: Mode)
	mode = newMode
	if newMode ~= "ground" then
		stopEmote()
	end
end

local function setCrouching(on: boolean)
	if on and mode ~= "ground" then
		return
	end
	crouching = on
	humanoid.WalkSpeed = if on then standingWalkSpeed * CROUCH_SPEED_FACTOR else standingWalkSpeed
	updateGround()
end

humanoid.Running:Connect(function(speed: number)
	groundSpeed = speed
	if mode == "air" or mode == "climb" or mode == "swim" then
		-- Running fires when the character lands or leaves a ladder or water.
		setMode("ground")
	end
	updateGround()
end)

humanoid.Jumping:Connect(function(active: boolean)
	if active and mode ~= "dead" then
		setMode("air")
		setCrouching(false)
		jumpStartedAt = os.clock()
		controller:playBase("jump", 0.1, 1)
	end
end)

humanoid.FreeFalling:Connect(function(active: boolean)
	if not active or mode == "dead" then
		return
	end
	setMode("air")
	-- Let the jump's take-off finish before blending into the fall loop.
	local jumpMeta = AnimationMeta.jump
	local remaining = (jumpMeta and jumpMeta.length * 0.55 or 0.3) - (os.clock() - jumpStartedAt)
	task.delay(math.max(remaining, 0), function()
		if mode == "air" and humanoid:GetState() == Enum.HumanoidStateType.Freefall then
			controller:playBase("fall", 0.3, 1)
		end
	end)
end)

humanoid.Climbing:Connect(function(speed: number)
	setMode("climb")
	setCrouching(false)
	-- Freeze the cycle while hanging still; otherwise scale by climb speed.
	local rate = math.abs(speed) / math.max(humanoid.WalkSpeed * 0.7, 1)
	controller:playBase("climb", 0.15, if math.abs(speed) < 0.1 then 0 else math.clamp(rate, 0.3, 2))
end)

humanoid.Swimming:Connect(function(speed: number)
	setMode("swim")
	setCrouching(false)
	if speed > 1 then
		controller:playBase("swim", 0.3, math.clamp(speed / 10, 0.5, 2))
	else
		controller:playBase("swim_idle", 0.4, 1)
	end
end)

humanoid.Seated:Connect(function(active: boolean)
	if active then
		setMode("seated")
		setCrouching(false)
		controller:playBase("sit", 0.3, 1)
	else
		setMode("ground")
		updateGround()
	end
end)

humanoid.Died:Connect(function()
	setMode("dead")
	controller:stopAll(0.1)
	controller:playAction("death", 0.1, 1)
end)

UserInputService.InputBegan:Connect(function(input: InputObject, processed: boolean)
	if processed then
		return
	end
	if input.KeyCode == Enum.KeyCode.C or input.KeyCode == Enum.KeyCode.LeftControl then
		setCrouching(not crouching)
	end
end)

local function playEmote(name: string)
	if not EMOTES[name] or mode ~= "ground" or groundSpeed > MOVE_THRESHOLD or crouching then
		return
	end
	stopEmote()
	if controller:playAction(name, 0.2, 1) then
		currentEmote = name
	end
end

local player = Players.LocalPlayer
player.Chatted:Connect(function(message: string)
	local name = string.match(string.lower(message), "^/e%s+(%a+)") or string.match(string.lower(message), "^/emote%s+(%a+)")
	if name then
		playEmote(name)
	end
end)

-- Other scripts (e.g. an emote wheel) can call this through the character's "PlayEmote" BindableFunction.
local playEmoteFunction = Instance.new("BindableFunction")
playEmoteFunction.Name = "PlayEmote"
playEmoteFunction.OnInvoke = function(name: string): boolean
	playEmote(name)
	return currentEmote == name
end
playEmoteFunction.Parent = script

updateGround()
