--!strict
-- Server side of the AnimationPack combat demo.
--   * Validates attack requests (known attack + hit marker, alive, cooldown per hit) and runs a hitbox
--     in front of the attacker. Damage is reduced while the target blocks; unblocked hits play hit_react.
--   * Keeps R15 joints intact on death so the "death" animation can play (BreakJointsOnDeath = false).
--   * Fits the Sword tool's grip so the blade points the way it does in sword_slash.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local AnimationController = require(pack:WaitForChild("AnimationController"))
local remotes = pack:WaitForChild("Remotes")
local attackRemote = remotes:WaitForChild("Attack") :: RemoteEvent
local blockRemote = remotes:WaitForChild("Block") :: RemoteEvent

type AttackSpec = { damage: number, range: number, width: number, cooldown: number }

-- Keyed by "<animation>/<marker>"; markers come from animations/markers.py.
local ATTACKS: { [string]: AttackSpec } = {
	["punch/Hit"] = { damage = 10, range = 4.5, width = 4, cooldown = 0.35 },
	["combo/Hit1"] = { damage = 7, range = 4.5, width = 4, cooldown = 0.2 },
	["combo/Hit2"] = { damage = 9, range = 4.5, width = 4, cooldown = 0.2 },
	["combo/Hit3"] = { damage = 14, range = 4.5, width = 5, cooldown = 0.2 },
	["kick/Hit"] = { damage = 15, range = 5.5, width = 4, cooldown = 0.6 },
	["sword_slash/Hit"] = { damage = 22, range = 7, width = 6, cooldown = 0.6 },
}
local BLOCK_DAMAGE_FACTOR = 0.2

local lastHit: { [Player]: { [string]: number } } = {}
local blocking: { [Model]: boolean } = {}

local function aliveHumanoid(model: Instance?): Humanoid?
	local humanoid = model and model:FindFirstChildOfClass("Humanoid")
	if humanoid and humanoid.Health > 0 then
		return humanoid
	end
	return nil
end

local function playHitReact(humanoid: Humanoid)
	local controller = AnimationController.get(humanoid, 0) or AnimationController.new(humanoid)
	controller:playAction("hit_react", 0.05, 1)
end

attackRemote.OnServerEvent:Connect(function(player: Player, animationName: unknown, markerName: unknown)
	if typeof(animationName) ~= "string" or typeof(markerName) ~= "string" then
		return
	end
	local key = animationName .. "/" .. markerName
	local spec = ATTACKS[key]
	local character = player.Character
	local humanoid = aliveHumanoid(character)
	local root = character and character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if spec == nil or humanoid == nil or root == nil or blocking[character :: Model] then
		return
	end
	if animationName == "sword_slash" then
		local tool = (character :: Model):FindFirstChildOfClass("Tool")
		if tool == nil or tool.Name ~= "Sword" then
			return
		end
	end
	local times = lastHit[player] or {}
	lastHit[player] = times
	local now = os.clock()
	if now - (times[key] or -math.huge) < spec.cooldown then
		return
	end
	times[key] = now

	local params = OverlapParams.new()
	params.FilterType = Enum.RaycastFilterType.Exclude
	params.FilterDescendantsInstances = { character :: Model }
	local boxCFrame = root.CFrame * CFrame.new(0, 0, -spec.range / 2)
	local parts = workspace:GetPartBoundsInBox(boxCFrame, Vector3.new(spec.width, 5, spec.range), params)
	local victims: { [Humanoid]: Model } = {}
	for _, part in parts do
		local model = part:FindFirstAncestorOfClass("Model")
		local victim = aliveHumanoid(model)
		if victim and model then
			victims[victim] = model
		end
	end
	for victim, model in victims do
		local isBlocking = blocking[model] == true
		victim:TakeDamage(if isBlocking then spec.damage * BLOCK_DAMAGE_FACTOR else spec.damage)
		if not isBlocking and victim.Health > 0 then
			playHitReact(victim)
		end
	end
end)

blockRemote.OnServerEvent:Connect(function(player: Player, active: unknown)
	local character = player.Character
	if character and typeof(active) == "boolean" then
		blocking[character] = if active then true else nil
	end
end)

-- Sword grip: hold the handle in the fist with the blade pointing forward when the arm hangs,
-- matching the Blender sword used to author sword_slash.
local SWORD_HANDLE_OFFSET = CFrame.new(0, -0.15, -1.6)

local function fitSword(tool: Tool, character: Model)
	local hand = character:FindFirstChild("RightHand")
	local attachment = hand and hand:FindFirstChild("RightGripAttachment") :: Attachment?
	if attachment then
		-- RightGrip.C0 = attachment.CFrame and C1 = Tool.Grip, so handle = hand * C0 * Grip:Inverse().
		tool.Grip = SWORD_HANDLE_OFFSET:Inverse() * attachment.CFrame
	end
end

local function onCharacter(player: Player, character: Model)
	local humanoid = character:WaitForChild("Humanoid") :: Humanoid
	humanoid.BreakJointsOnDeath = false
	character.ChildAdded:Connect(function(child)
		if child:IsA("Tool") and child.Name == "Sword" then
			fitSword(child, character)
		end
	end)
	character.Destroying:Connect(function()
		blocking[character] = nil
	end)
end

Players.PlayerAdded:Connect(function(player: Player)
	player.CharacterAdded:Connect(function(character)
		onCharacter(player, character)
	end)
	if player.Character then
		onCharacter(player, player.Character)
	end
end)
for _, player in Players:GetPlayers() do
	if player.Character then
		onCharacter(player, player.Character)
	end
	player.CharacterAdded:Connect(function(character)
		onCharacter(player, character)
	end)
end

Players.PlayerRemoving:Connect(function(player: Player)
	lastHit[player] = nil
end)
