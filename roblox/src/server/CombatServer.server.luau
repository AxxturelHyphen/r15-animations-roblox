--!strict
-- Server side of the AnimationPack combat demo.
--   * Validates attack hits: one attack in flight per player, a shared minimum gap between attacks,
--     hit markers accepted only in order and inside the timing window the animation defines
--     (AnimationMeta marker times), sword hits only with the Sword, unarmed hits only without it.
--   * Runs a hitbox in front of the attacker. Blocking cuts damage; unblocked hits play hit_react.
--   * Keeps R15 joints intact on death so the "death" animation can play (BreakJointsOnDeath = false).
--   * Fits the Sword tool's grip so the blade points the way it does in sword_slash.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local AnimationMeta = require(pack:WaitForChild("AnimationMeta"))
local Feedback = require(pack:WaitForChild("Feedback"))
local ReplicatedPlay = require(pack:WaitForChild("ReplicatedPlay"))
local GameState = require(script.Parent:WaitForChild("GameState"))
local remotes = pack:WaitForChild("Remotes")
local attackRemote = remotes:WaitForChild("Attack") :: RemoteEvent
local blockRemote = remotes:WaitForChild("Block") :: RemoteEvent
local stateRemote = remotes:WaitForChild("State") :: RemoteEvent
local feedbackRemote = remotes:WaitForChild("Feedback") :: RemoteEvent

-- knockback: horizontal studs/s away from the attacker, plus lift (studs/s up). Kicks and the combo finisher
-- launch people, so you can kick a friend off the tower or into the pool.
type HitSpec = { damage: number, range: number, width: number, knockback: number?, lift: number?, heavy: boolean? }

-- Keyed by animation, then hit marker (markers come from animations/markers.py).
local ATTACKS: { [string]: { [string]: HitSpec } } = {
	punch = { Hit = { damage = 10, range = 4.5, width = 4 } },
	combo = {
		Hit1 = { damage = 7, range = 4.5, width = 4 },
		Hit2 = { damage = 9, range = 4.5, width = 4 },
		Hit3 = { damage = 14, range = 4.5, width = 5, knockback = 38, lift = 22, heavy = true },
	},
	kick = { Hit = { damage = 15, range = 5.5, width = 4, knockback = 52, lift = 28, heavy = true } },
	sword_slash = { Hit = { damage = 22, range = 7, width = 6, knockback = 18, lift = 8, heavy = true } },
}
local SWORD_ONLY = { sword_slash = true }
local MIN_ATTACK_GAP = 0.18 -- seconds between two attack starts, whatever the attack
local MARKER_TOLERANCE = 0.3 -- seconds of latency slack around each marker's expected time
local COMBO_UPGRADE_WINDOW = 0.6 -- a punch may be cancelled into the combo this soon after it starts
local BLOCK_DAMAGE_FACTOR = 0.2
local PARRY_WINDOW = 0.25 -- raising the guard this soon before a hit parries it
local PARRY_COOLDOWN = 1.0 -- only one parry-eligible guard raise per second (no toggle-spam parries)
local MAX_SNEAK_SPEED = 5 -- studs/s: sneak attacks need real crouch speed (WalkSpeed isn't replicated)
local SNEAK_MULTIPLIER = 2

type AttackState = { animation: string, startedAt: number, nextMarker: number }

local current: { [Player]: AttackState } = {}
local lastStart: { [Player]: number } = {}
local blocking: { [Model]: true } = {}
local blockStartedAt: { [Model]: number } = {}
local parryEligible: { [Model]: boolean } = {}
local parryReadyAt: { [Model]: number } = {}
local lastBlockToggle: { [Player]: number } = {}
local crouching: { [Player]: boolean } = {}

local function hitMarkers(animation: string): { { name: string, time: number } }
	local meta = AnimationMeta[animation]
	local list = {}
	if meta then
		for _, marker in meta.markers do
			if string.sub(marker.name, 1, 3) == "Hit" then
				table.insert(list, { name = marker.name, time = marker.time })
			end
		end
	end
	return list
end

local function aliveHumanoid(model: Instance?): Humanoid?
	local humanoid = if model then model:FindFirstChildOfClass("Humanoid") else nil
	if humanoid and humanoid.Health > 0 then
		return humanoid
	end
	return nil
end

-- Returns true if this marker is a legitimate next hit for the player, updating their attack state.
local function acceptMarker(player: Player, animation: string, markerName: string, now: number): boolean
	local markers = hitMarkers(animation)
	if #markers == 0 then
		return false
	end
	local state = current[player]
	local meta = AnimationMeta[animation]
	local length = if meta then meta.length else 1
	if state and state.animation == animation and now - state.startedAt <= length + MARKER_TOLERANCE then
		-- A later hit of the attack already in flight: must be the next marker, on time.
		local expected = markers[state.nextMarker]
		if expected == nil or expected.name ~= markerName then
			return false
		end
		if math.abs((now - state.startedAt) - expected.time) > MARKER_TOLERANCE then
			return false
		end
		state.nextMarker += 1
		return true
	end
	-- A new attack: only its first marker, after the shared gap, and only once the previous attack is
	-- (nearly) over, except that a punch may be upgraded into the combo.
	if markers[1].name ~= markerName then
		return false
	end
	if now - (lastStart[player] or -math.huge) < MIN_ATTACK_GAP then
		return false
	end
	if state then
		local previousMeta = AnimationMeta[state.animation]
		local previousLength = if previousMeta then previousMeta.length else 0
		local upgrading = state.animation == "punch" and animation == "combo"
			and now - state.startedAt <= COMBO_UPGRADE_WINDOW + markers[1].time + MARKER_TOLERANCE
		if not upgrading and now - state.startedAt < previousLength * 0.75 then
			return false
		end
	end
	local startedAt = now - markers[1].time
	current[player] = { animation = animation, startedAt = startedAt, nextMarker = 2 }
	lastStart[player] = now
	return true
end

attackRemote.OnServerEvent:Connect(function(player: Player, animationName: unknown, markerName: unknown)
	if typeof(animationName) ~= "string" or typeof(markerName) ~= "string" then
		return
	end
	local specs = ATTACKS[animationName]
	local spec = specs and specs[markerName]
	local character = player.Character
	local humanoid = aliveHumanoid(character)
	if spec == nil or character == nil or humanoid == nil or blocking[character] then
		return
	end
	local root = character:FindFirstChild("HumanoidRootPart")
	if root == nil or not root:IsA("BasePart") then
		return
	end
	-- Attacking ends your own spawn shield.
	local ownShield = character:FindFirstChildOfClass("ForceField")
	if ownShield then
		ownShield:Destroy()
	end
	local tool = character:FindFirstChildOfClass("Tool")
	local holdingSword = tool ~= nil and tool.Name == "Sword"
	if (SWORD_ONLY[animationName] == true) ~= holdingSword then
		return
	end
	if not acceptMarker(player, animationName, markerName, os.clock()) then
		return
	end

	local params = OverlapParams.new()
	params.FilterType = Enum.RaycastFilterType.Exclude
	params.FilterDescendantsInstances = { character }
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
		if model:FindFirstChildOfClass("ForceField") then
			continue -- spawn shield: no damage, no knockback, no hit feedback
		end
		local victimRoot = model:FindFirstChild("HumanoidRootPart")
		local victimPlayer = Players:GetPlayerFromCharacter(model)
		local contact = if victimRoot and victimRoot:IsA("BasePart")
			then victimRoot.Position:Lerp(root.Position, 0.35) + Vector3.new(0, 1, 0)
			else root.Position + root.CFrame.LookVector * 2
		local isBlocking = blocking[model] == true
		local isParry = isBlocking and parryEligible[model] == true
			and os.clock() - (blockStartedAt[model] or -math.huge) <= PARRY_WINDOW
		local isSneak = false
		local attackerSpeed = (root.AssemblyLinearVelocity * Vector3.new(1, 0, 1)).Magnitude
		if crouching[player] and attackerSpeed <= MAX_SNEAK_SPEED and victimRoot and victimRoot:IsA("BasePart") then
			-- Behind the victim: the attacker is on the opposite side of where the victim faces.
			local toAttacker = (root.Position - victimRoot.Position) * Vector3.new(1, 0, 1)
			if toAttacker.Magnitude > 0.1 and victimRoot.CFrame.LookVector:Dot(toAttacker.Unit) < -0.3 then
				isSneak = true
			end
		end

		local kind: Feedback.HitKind = if isParry then "parry"
			elseif isBlocking then "blocked"
			elseif isSneak then "sneak"
			elseif spec.heavy then "heavy"
			else "normal"
		local damage = if isParry then 0
			elseif isBlocking then spec.damage * BLOCK_DAMAGE_FACTOR
			elseif isSneak then spec.damage * SNEAK_MULTIPLIER
			else spec.damage

		if damage > 0 then
			GameState.tagHit(victim, player, if isSneak then "sneak" else animationName)
			if victimPlayer == nil and model.Name == "TrainingDummy" then
				GameState.onDummyDamage(player, damage)
			end
			victim:TakeDamage(damage)
			if victimPlayer == nil and model.Name == "TrainingDummy" and GameState.challengeActive() then
				victim.Health = math.max(victim.Health, 1)
			end
		end
		feedbackRemote:FireAllClients("hit", {
			position = contact,
			amount = math.floor(damage + 0.5),
			kind = kind,
			attacker = character,
			victim = model,
		})

		if isParry then
			parryEligible[model] = false -- one parry per guard raise
			-- The attacker is thrown off balance.
			ReplicatedPlay.action(humanoid, "hit_react")
			current[player] = nil
		elseif not isBlocking and victim.Health > 0 then
			ReplicatedPlay.action(victim, "hit_react")
			local push = spec.knockback
			if push and victimRoot and victimRoot:IsA("BasePart") then
				local away = (victimRoot.Position - root.Position) * Vector3.new(1, 0, 1)
				local dir = if away.Magnitude > 0.1 then away.Unit else root.CFrame.LookVector
				local velocity = dir * push + Vector3.new(0, spec.lift or 0, 0)
				if victimPlayer then
					-- Player characters are simulated by their own client, so it applies the push.
					feedbackRemote:FireClient(victimPlayer, "knockback", { velocity = velocity })
				else
					-- Server-owned NPC: hold the velocity briefly so the Humanoid doesn't brake it to zero.
					local started = os.clock()
					local connection: RBXScriptConnection
					connection = RunService.Heartbeat:Connect(function()
						local t = os.clock() - started
						if t > 0.3 or not victimRoot.Parent then
							connection:Disconnect()
							return
						end
						victimRoot.AssemblyLinearVelocity = velocity - Vector3.new(0, workspace.Gravity * t, 0)
					end)
				end
			end
		end
	end
end)

blockRemote.OnServerEvent:Connect(function(player: Player, active: unknown)
	local character = player.Character
	if character == nil or typeof(active) ~= "boolean" then
		return
	end
	local now = os.clock()
	if active then
		if now - (lastBlockToggle[player] or -math.huge) < 0.2 then
			return -- at most 5 guard raises a second (releases are never dropped)
		end
		lastBlockToggle[player] = now
		if not blocking[character] then
			blockStartedAt[character] = now
			parryEligible[character] = now >= (parryReadyAt[character] or 0)
			parryReadyAt[character] = now + PARRY_COOLDOWN
		end
		blocking[character] = true
	else
		blocking[character] = nil
	end
end)

-- Clients report crouch (for sneak attacks). Worst case a cheater claims to crouch: that still requires
-- hitting the target from behind, which the server checks.
stateRemote.OnServerEvent:Connect(function(player: Player, key: unknown, value: unknown)
	if key == "crouch" and typeof(value) == "boolean" then
		crouching[player] = value
	end
end)

-- Sword grip: hold the handle in the fist with the blade pointing forward when the arm hangs,
-- matching the Blender sword used to author sword_slash.
local SWORD_HANDLE_OFFSET = CFrame.new(0, -0.15, -1.6)

local function fitSword(tool: Tool, character: Model)
	local hand = character:FindFirstChild("RightHand")
	local attachment = if hand then hand:FindFirstChild("RightGripAttachment") else nil
	if attachment and attachment:IsA("Attachment") then
		-- RightGrip.C0 = attachment.CFrame and C1 = Tool.Grip, so handle = hand * C0 * Grip:Inverse().
		tool.Grip = SWORD_HANDLE_OFFSET:Inverse() * attachment.CFrame
	end
end

local function onCharacter(player: Player, character: Model)
	local humanoid = character:WaitForChild("Humanoid") :: Humanoid
	humanoid.BreakJointsOnDeath = false
	humanoid.Died:Connect(function()
		current[player] = nil
	end)
	character.ChildAdded:Connect(function(child)
		if child:IsA("Tool") and child.Name == "Sword" then
			fitSword(child, character)
		end
	end)
end

local function onPlayer(player: Player)
	player.CharacterAdded:Connect(function(character)
		onCharacter(player, character)
	end)
	player.CharacterRemoving:Connect(function(character)
		blocking[character] = nil
		blockStartedAt[character] = nil
		parryEligible[character] = nil
		parryReadyAt[character] = nil
		current[player] = nil
		crouching[player] = nil
	end)
	if player.Character then
		task.spawn(onCharacter, player, player.Character)
	end
end

Players.PlayerAdded:Connect(onPlayer)
for _, player in Players:GetPlayers() do
	onPlayer(player)
end

Players.PlayerRemoving:Connect(function(player: Player)
	current[player] = nil
	lastStart[player] = nil
	crouching[player] = nil
	lastBlockToggle[player] = nil
	if player.Character then
		blocking[player.Character] = nil
	end
end)
