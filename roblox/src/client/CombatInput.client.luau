--!strict
-- Combat input for the local player.
--   Mouse1         punch; click again while the punch plays to chain into the 3-hit combo.
--                  With the Sword tool equipped: sword_slash.
--   Q              kick
--   F (hold)       block
-- Each attack asks the server for a hit exactly on its animation's "Hit" markers, which the
-- Blender exporter placed on the impact poses. The server validates and applies damage.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local UserInputService = game:GetService("UserInputService")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local AnimationController = require(pack:WaitForChild("AnimationController"))
local AnimationMeta = require(pack:WaitForChild("AnimationMeta"))
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

local function attack(s: CharacterState, name: string)
	local track: AnimationTrack? = s.controller:playAction(name, 0.08, 1)
	if track == nil then
		return
	end
	local meta = AnimationMeta[name]
	s.busyUntil = os.clock() + (if meta then meta.length * 0.8 else 0.6)
	if meta then
		for _, marker in meta.markers do
			if string.sub(marker.name, 1, 3) == "Hit" then
				local connection: RBXScriptConnection
				connection = track:GetMarkerReachedSignal(marker.name):Connect(function()
					attackRemote:FireServer(name, marker.name)
				end)
				track.Stopped:Once(function()
					connection:Disconnect()
				end)
			end
		end
	end
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

UserInputService.InputBegan:Connect(function(input: InputObject, processed: boolean)
	local s = state
	if processed or s == nil then
		return
	end
	if input.UserInputType == Enum.UserInputType.MouseButton1 then
		onPrimary(s)
	elseif input.KeyCode == Enum.KeyCode.Q then
		if canAct(s) and os.clock() >= s.busyUntil then
			attack(s, "kick")
		end
	elseif input.KeyCode == Enum.KeyCode.F then
		setBlocking(s, true)
	end
end)

UserInputService.InputEnded:Connect(function(input: InputObject)
	local s = state
	if s and input.KeyCode == Enum.KeyCode.F then
		setBlocking(s, false)
	end
end)

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
end

if player.Character then
	task.spawn(onCharacter, player.Character)
end
player.CharacterAdded:Connect(onCharacter)
