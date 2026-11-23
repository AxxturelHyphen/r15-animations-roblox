--!strict
-- Combat input for the local player.
--   Mouse1         punch; click again while the punch plays to chain into the 3-hit combo.
--                  With the Sword tool equipped: sword_slash.
--   Q              kick
--   F (hold)       block
-- Gamepad: R2 punch/slash, X kick, L2 block. Touch: on-screen Hit, Kick and Block buttons.
-- Actions go through ContextActionService, so any input (or a test harness) can drive them.
-- Each attack asks the server for a hit exactly on its animation's "Hit" markers, which the
-- Blender exporter placed on the impact poses. The server validates and applies damage.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ContextActionService = game:GetService("ContextActionService")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local AnimationController = require(pack:WaitForChild("AnimationController"))
local AnimationMeta = require(pack:WaitForChild("AnimationMeta"))
local Feedback = require(pack:WaitForChild("Feedback"))
local remotes = pack:WaitForChild("Remotes")
local attackRemote = remotes:WaitForChild("Attack") :: RemoteEvent
local blockRemote = remotes:WaitForChild("Block") :: RemoteEvent

local player = Players.LocalPlayer

local COMBO_WINDOW = 0.45 -- seconds after a punch starts in which a second click upgrades it to the combo

type CharacterState = {
	humanoid: Humanoid,
	controller: any,
	busyUntil: number,
	punchStartedAt: number,
	blocking: boolean,
}

local state: CharacterState? = nil

local function canAct(s: CharacterState): boolean
	local humanoidState = s.humanoid:GetState()
	return s.humanoid.Health > 0
		and not s.blocking
		and humanoidState ~= Enum.HumanoidStateType.Seated
		and humanoidState ~= Enum.HumanoidStateType.Swimming
		and humanoidState ~= Enum.HumanoidStateType.Climbing
end

local function equippedSword(): Tool?
	local character = player.Character
	local tool = character and character:FindFirstChildOfClass("Tool")
	if tool and tool.Name == "Sword" then
		return tool
	end
	return nil
end

-- Marker signals are connected once per track (replaying a still-playing track does not fire Stopped,
-- so per-play connections would stack up and send duplicate hits).
local wiredTracks: { [AnimationTrack]: boolean } = {}

local function wireMarkers(track: AnimationTrack, name: string)
	if wiredTracks[track] then
		return
	end
	wiredTracks[track] = true
	local meta = AnimationMeta[name]
	if meta == nil then
		return
	end
	local seen: { [string]: boolean } = {}
	for _, marker in meta.markers do
		if string.sub(marker.name, 1, 3) == "Hit" and not seen[marker.name] then
			seen[marker.name] = true
			track:GetMarkerReachedSignal(marker.name):Connect(function()
				attackRemote:FireServer(name, marker.name)
			end)
		end
	end
	track.Destroying:Connect(function()
		wiredTracks[track] = nil
	end)
end

local function attack(s: CharacterState, name: string)
	local track: AnimationTrack? = s.controller:track(name)
	if track == nil then
		return
	end
	wireMarkers(track, name)
	s.controller:playAction(name, 0.08, 1)
	if name == "sword_slash" then
		Feedback.playSound("slash")
	end
	local meta = AnimationMeta[name]
	s.busyUntil = os.clock() + (if meta then meta.length * 0.8 else 0.6)
end

local function onPrimary(s: CharacterState)
	if not canAct(s) then
		return
	end
	local now = os.clock()
	if equippedSword() then
		if now >= s.busyUntil then
			attack(s, "sword_slash")
		end
		return
	end
	if s.controller:isPlaying("punch") and now - s.punchStartedAt <= COMBO_WINDOW then
		s.controller:stopAction("punch", 0.05)
		s.busyUntil = 0
		attack(s, "combo")
	elseif now >= s.busyUntil then
		s.punchStartedAt = now
		attack(s, "punch")
	end
end

local function setBlocking(s: CharacterState, on: boolean)
	if on == s.blocking or (on and s.humanoid.Health <= 0) then
		return
	end
	s.blocking = on
	if on then
		s.controller:playAction("block", 0.1, 1)
	else
		s.controller:stopAction("block", 0.15)
	end
	blockRemote:FireServer(on)
end

local function onAction(actionName: string, inputState: Enum.UserInputState, _input: InputObject?): Enum.ContextActionResult
	local s = state
	if s == nil then
		return Enum.ContextActionResult.Pass
	end
	local began = inputState == Enum.UserInputState.Begin
	if actionName == "PackPrimary" then
		if began then
			onPrimary(s)
		end
	elseif actionName == "PackKick" then
		if began and canAct(s) and os.clock() >= s.busyUntil then
			attack(s, "kick")
		end
	elseif actionName == "PackBlock" then
		if began then
			setBlocking(s, true)
		elseif inputState == Enum.UserInputState.End or inputState == Enum.UserInputState.Cancel then
			setBlocking(s, false)
		end
	end
	-- Pass, so the mouse still reaches the camera and tools.
	return Enum.ContextActionResult.Pass
end

ContextActionService:BindAction("PackPrimary", onAction, true, Enum.UserInputType.MouseButton1, Enum.KeyCode.ButtonR2)
ContextActionService:BindAction("PackKick", onAction, true, Enum.KeyCode.Q, Enum.KeyCode.ButtonX)
ContextActionService:BindAction("PackBlock", onAction, true, Enum.KeyCode.F, Enum.KeyCode.ButtonL2)
-- Touch buttons (only shown on touch devices), stacked above the jump button.
-- Other scripts (a custom mobile UI, a tutorial, the test harness) can trigger the same actions:
--   CombatInput.PackAction:Invoke("PackPrimary" | "PackKick" | "PackBlock", began: boolean)
local packAction = Instance.new("BindableFunction")
packAction.Name = "PackAction"
packAction.OnInvoke = function(action: unknown, began: unknown): boolean
	if typeof(action) ~= "string" then
		return false
	end
	onAction(action, if began == false then Enum.UserInputState.End else Enum.UserInputState.Begin, nil)
	return true
end
packAction.Parent = script

local TOUCH_BUTTONS: { { action: string, title: string } } = {
	{ action = "PackPrimary", title = "Hit" },
	{ action = "PackKick", title = "Kick" },
	{ action = "PackBlock", title = "Block" },
}
for i, button in TOUCH_BUTTONS do
	ContextActionService:SetTitle(button.action, button.title)
	ContextActionService:SetPosition(button.action, UDim2.new(1, -95 - (i - 1) * 75, 1, -230))
end

local function onCharacter(character: Model)
	local humanoid = character:WaitForChild("Humanoid") :: Humanoid
	-- The Animate script creates the controller; wait for it so both scripts share the same tracks.
	local controller = AnimationController.get(humanoid, 10) or AnimationController.new(humanoid)
	state = {
		humanoid = humanoid,
		controller = controller,
		busyUntil = 0,
		punchStartedAt = -math.huge,
		blocking = false,
	}
	humanoid.Died:Connect(function()
		state = nil
	end)
	character.ChildAdded:Connect(function(child)
		if child:IsA("Tool") and child.Name == "Sword" then
			Feedback.playSound("unsheath")
		end
	end)
end

if player.Character then
	task.spawn(onCharacter, player.Character)
end
player.CharacterAdded:Connect(onCharacter)
