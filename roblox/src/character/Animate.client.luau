--!strict
-- Replaces Roblox's default "Animate" script (same name in StarterCharacterScripts).
-- Drives the AnimationPack clips from Humanoid state:
--   idle / walk / run (playback speed matched to ground speed), jump -> fall, climb, swim / swim_idle,
--   sit, death, crouch (C or Left Ctrl) with crouch_idle / crouch_walk, and chat emotes "/e <name>".

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TextChatService = game:GetService("TextChatService")
local UserInputService = game:GetService("UserInputService")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local AnimationController = require(pack:WaitForChild("AnimationController"))
local AnimationMeta = require(pack:WaitForChild("AnimationMeta"))
local Feedback = require(pack:WaitForChild("Feedback"))
local remotes = pack:WaitForChild("Remotes")
local stateRemote = remotes:WaitForChild("State") :: RemoteEvent
local socialRemote = remotes:WaitForChild("Social") :: RemoteEvent

local character = script.Parent
local humanoid = character:WaitForChild("Humanoid") :: Humanoid
local controller = AnimationController.new(humanoid)

local EMOTES: { [string]: boolean } = {
	highfive = true, -- two-player: matched on the server (Social.server.luau)
	wave = true,
	dance = true,
	cheer = true,
	point = true,
	laugh = true,
	clap = true,
	salute = true,
}
local MOVE_THRESHOLD = 0.75 -- studs/s; below this the character counts as standing still
-- Above this ground speed walk becomes run. The cycles were authored for about 3.2 (walk) and
-- 6.0 (run) studs/s; playback is scaled to the real speed, within MAX_CYCLE_RATE.
local RUN_THRESHOLD = 8.5
local MAX_CYCLE_RATE = 3.5
-- Crouch movement speed is derived from the speed crouch_walk was animated for, so the sneak cycle
-- plays at CROUCH_CYCLE_RATE x without foot sliding (about 2.7 studs/s for the current clip).
local CROUCH_CYCLE_RATE = 3
local CROUCH_FALLBACK_FACTOR = 0.35

type Mode = "ground" | "air" | "climb" | "swim" | "seated" | "dead"
local mode: Mode = "ground"
local crouching = false
local standingWalkSpeed = humanoid.WalkSpeed
local groundSpeed = 0
local currentEmote: string? = nil
local jumpStartedAt = -math.huge
local fallStartY: number? = nil -- highest point of the current airborne stretch

local rootPart = character:WaitForChild("HumanoidRootPart") :: BasePart

local function airborneHeight(): number
	local start = fallStartY
	fallStartY = nil
	return if start then start - rootPart.Position.Y else 0
end

-- Playback speed so the feet match the ground speed the cycle was authored for.
local function cycleSpeed(name: string, speed: number): number
	local meta = AnimationMeta[name]
	local authored = meta and meta.authoredSpeed
	if authored and authored > 0 then
		return math.clamp(speed / authored, 0.4, MAX_CYCLE_RATE)
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

local function crouchWalkSpeed(): number
	local meta = AnimationMeta.crouch_walk
	if meta and meta.authoredSpeed and meta.authoredSpeed > 0 then
		return meta.authoredSpeed * CROUCH_CYCLE_RATE
	end
	return standingWalkSpeed * CROUCH_FALLBACK_FACTOR
end

local function setCrouching(on: boolean)
	if on and mode ~= "ground" then
		return
	end
	crouching = on
	stateRemote:FireServer("crouch", on)
	if on then
		stopEmote()
	end
	humanoid.WalkSpeed = if on then crouchWalkSpeed() else standingWalkSpeed
	updateGround()
end

humanoid.Running:Connect(function(speed: number)
	groundSpeed = speed
	if mode == "dead" or mode == "seated" then
		return
	end
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
	if mode == "dead" then
		return
	end
	setMode("climb")
	setCrouching(false)
	-- Freeze the cycle while hanging still; otherwise scale by climb speed.
	local rate = math.abs(speed) / math.max(humanoid.WalkSpeed * 0.7, 1)
	controller:playBase("climb", 0.15, if math.abs(speed) < 0.1 then 0 else math.clamp(rate, 0.3, 2))
end)

humanoid.Swimming:Connect(function(speed: number)
	if mode == "dead" then
		return
	end
	setMode("swim")
	setCrouching(false)
	if speed > 1 then
		controller:playBase("swim", 0.3, math.clamp(speed / 10, 0.5, 2))
	else
		controller:playBase("swim_idle", 0.4, 1)
	end
end)

humanoid.Seated:Connect(function(active: boolean)
	if mode == "dead" then
		return
	end
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

-- Track how far we fell: a big fall onto the ground gets a superhero landing, into water a splash.
humanoid.StateChanged:Connect(function(_old: Enum.HumanoidStateType, new: Enum.HumanoidStateType)
	if mode == "dead" then
		return
	end
	if new == Enum.HumanoidStateType.Freefall or new == Enum.HumanoidStateType.Jumping then
		local y = rootPart.Position.Y
		if fallStartY == nil or y > (fallStartY :: number) then
			fallStartY = y
		end
	elseif new == Enum.HumanoidStateType.Landed then
		local height = airborneHeight()
		if height >= Feedback.HEAVY_LANDING_STUDS then
			controller:playAction("land_heavy", 0.05, 1)
			socialRemote:FireServer("landing", height)
		end
	elseif new == Enum.HumanoidStateType.Swimming then
		local height = airborneHeight()
		if height > 2 then
			socialRemote:FireServer("splash", height)
		end
	elseif new == Enum.HumanoidStateType.Running or new == Enum.HumanoidStateType.Climbing
		or new == Enum.HumanoidStateType.Seated then
		fallStartY = nil
	end
end)

-- Keep the peak height updated while airborne (jumps rise before they fall).
game:GetService("RunService").Heartbeat:Connect(function()
	local start = fallStartY
	if start and rootPart.Position.Y > start then
		fallStartY = rootPart.Position.Y
	end
end)

UserInputService.InputBegan:Connect(function(input: InputObject, processed: boolean)
	if processed then
		return
	end
	if input.KeyCode == Enum.KeyCode.C or input.KeyCode == Enum.KeyCode.LeftControl then
		setCrouching(not crouching)
	end
end)

local EMOTE_LIST = "highfive (with a friend), wave, dance, cheer, point, laugh, clap, salute"

local function systemMessage(text: string)
	if TextChatService.ChatVersion == Enum.ChatVersion.TextChatService then
		local channels = TextChatService:FindFirstChild("TextChannels")
		local system = channels and channels:FindFirstChild("RBXSystem")
		if system and system:IsA("TextChannel") then
			system:DisplaySystemMessage(text)
		end
	else
		pcall(function()
			game:GetService("StarterGui"):SetCore("ChatMakeSystemMessage", { Text = text })
		end)
	end
end

-- Join a friend's dance in time: match the playback position of a nearby dancer.
local function syncDance(track: AnimationTrack)
	for _, other in workspace:GetDescendants() do
		if other:IsA("Animator") and not other:IsDescendantOf(character) then
			local model = other:FindFirstAncestorOfClass("Model")
			local otherRoot = model and model:FindFirstChild("HumanoidRootPart")
			if otherRoot and otherRoot:IsA("BasePart") and (otherRoot.Position - rootPart.Position).Magnitude <= 16 then
				for _, t in other:GetPlayingAnimationTracks() do
					if t.Animation and t.Animation.Name == "dance" then
						track.TimePosition = t.TimePosition
						return
					end
				end
			end
		end
	end
end

local function playEmote(name: string)
	if not EMOTES[name] then
		systemMessage(`No emote called "{name}". Try: {EMOTE_LIST}`)
		return
	end
	if mode ~= "ground" or groundSpeed > MOVE_THRESHOLD or crouching then
		return
	end
	stopEmote()
	if name == "highfive" then
		socialRemote:FireServer("emote", name) -- the server matches two players and plays it on both
		return
	end
	local track = controller:playAction(name, 0.2, 1)
	if track then
		currentEmote = name
		if name == "dance" then
			syncDance(track)
		end
		socialRemote:FireServer("emote", name) -- taunts after a KO, dance parties
	end
end

local function emoteFromMessage(message: string): string?
	local lower = string.lower(message)
	return string.match(lower, "^/e%s+(%a+)") or string.match(lower, "^/emote%s+(%a+)")
end

if TextChatService.ChatVersion == Enum.ChatVersion.TextChatService then
	-- The built-in RBXEmoteCommand would swallow "/e" and only knows Roblox's default emotes,
	-- so replace it locally with a command that knows this pack's emotes.
	local commands = TextChatService:FindFirstChild("TextChatCommands")
	local builtIn = commands and commands:FindFirstChild("RBXEmoteCommand")
	if builtIn and builtIn:IsA("TextChatCommand") then
		builtIn.Enabled = false
	end
	local command = Instance.new("TextChatCommand")
	command.Name = "AnimationPackEmote"
	command.PrimaryAlias = "/e"
	command.SecondaryAlias = "/emote"
	command.Triggered:Connect(function(_source: TextSource, message: string)
		local name = emoteFromMessage(message)
		if name then
			playEmote(name)
		end
	end)
	command.Parent = commands or TextChatService
	script.Destroying:Connect(function()
		command:Destroy()
	end)
else
	Players.LocalPlayer.Chatted:Connect(function(message: string)
		local name = emoteFromMessage(message)
		if name then
			playEmote(name)
		end
	end)
end

-- Other scripts (e.g. an emote wheel) can call this through the character's "PlayEmote" BindableFunction.
local playEmoteFunction = Instance.new("BindableFunction")
playEmoteFunction.Name = "PlayEmote"
playEmoteFunction.OnInvoke = function(name: unknown): boolean
	-- Humanoid:PlayEmote may pass an Animation instance; this pack's emotes are addressed by name.
	if typeof(name) ~= "string" then
		return false
	end
	playEmote(name)
	return currentEmote == name
end
playEmoteFunction.Parent = script

updateGround()
