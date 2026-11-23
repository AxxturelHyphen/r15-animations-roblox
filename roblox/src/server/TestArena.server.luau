--!strict
-- Builds the playtest arena in Studio play-tests (or when ReplicatedStorage.AnimationPack has the
-- attribute BuildTestArena = true):
--   spawn with a 3 s shield, a sign with the controls and goals, and a records board;
--   a truss with a climb race (start pad at the bottom, bell at the top);
--   a pool with a splash zone (biggest-splash record);
--   a bench with a launch lever aimed at the pool;
--   a respawning training dummy with a visible health bar and a 10-second damage challenge pad.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
if not (RunService:IsStudio() or pack:GetAttribute("BuildTestArena") == true) then
	return
end

local ReplicatedPlay = require(pack:WaitForChild("ReplicatedPlay"))
local GameState = require(script.Parent:WaitForChild("GameState"))
local feedbackRemote = pack:WaitForChild("Remotes"):WaitForChild("Feedback") :: RemoteEvent

local arena = Instance.new("Folder")
arena.Name = "AnimationTestArena"
arena.Parent = workspace

local function anchoredPart(name: string, size: Vector3, cframe: CFrame, color: Color3): Part
	local part = Instance.new("Part")
	part.Name = name
	part.Anchored = true
	part.Size = size
	part.CFrame = cframe
	part.Color = color
	part.TopSurface = Enum.SurfaceType.Smooth
	part.BottomSurface = Enum.SurfaceType.Smooth
	part.Parent = arena
	return part
end

local function sign(name: string, cframe: CFrame, size: Vector2, text: string, textSize: number): TextLabel
	local board = anchoredPart(name, Vector3.new(size.X, size.Y, 0.4), cframe, Color3.fromRGB(28, 30, 36))
	local gui = Instance.new("SurfaceGui")
	gui.Face = Enum.NormalId.Front
	gui.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud
	gui.PixelsPerStud = 40
	gui.Parent = board
	local label = Instance.new("TextLabel")
	label.Size = UDim2.fromScale(1, 1)
	label.BackgroundTransparency = 1
	label.TextColor3 = Color3.fromRGB(240, 240, 245)
	label.Font = Enum.Font.GothamBold
	label.TextSize = textSize
	label.TextScaled = true -- shrink to fit, up to textSize
	local limit = Instance.new("UITextSizeConstraint")
	limit.MaxTextSize = textSize
	limit.MinTextSize = 10
	limit.Parent = label
	label.TextWrapped = true
	label.TextXAlignment = Enum.TextXAlignment.Left
	label.TextYAlignment = Enum.TextYAlignment.Top
	label.Text = text
	local padding = Instance.new("UIPadding")
	padding.PaddingLeft = UDim.new(0, 24)
	padding.PaddingTop = UDim.new(0, 18)
	padding.Parent = label
	label.Parent = gui
	return label
end

local function prompt(parent: BasePart, action: string, object: string): ProximityPrompt
	local p = Instance.new("ProximityPrompt")
	p.ActionText = action
	p.ObjectText = object
	p.HoldDuration = 0
	p.MaxActivationDistance = 10
	p.RequiresLineOfSight = false
	p.Parent = parent
	return p
end

-- Spawn: a short shield so nobody gets spawn-killed, plus the sign and the board ----------------
local spawnLocation: SpawnLocation? = nil
for _, d in workspace:GetDescendants() do
	if d:IsA("SpawnLocation") then
		spawnLocation = d
		d.Duration = 3
	end
end
if spawnLocation == nil then
	local s = Instance.new("SpawnLocation")
	s.Anchored = true
	s.Size = Vector3.new(6, 1, 6)
	s.CFrame = CFrame.new(0, 0.5, 0)
	s.Duration = 3
	s.Parent = arena
end

-- Signs face the spawn: a part's Front face is its -Z side, which CFrame.lookAt points at the target.
sign("ControlsSign", CFrame.lookAt(Vector3.new(-8, 4, 8), Vector3.new(0, 4, 0)), Vector2.new(9, 6),
	"CONTROLS\nClick: punch (click again fast: combo)\nQ: kick (knocks people flying)\nHold F: block (tap right before a hit: PARRY)\nC: crouch (hit from behind: SNEAK ATTACK x2)\n1: sword\n/e highfive with a friend, /e dance, laugh, ...",
	26)
local boardLabel = sign("RecordsBoard", CFrame.lookAt(Vector3.new(8, 4, 8), Vector3.new(0, 4, 0)), Vector2.new(9, 6), "RECORDS", 28)
GameState.setBoard(boardLabel)

-- Climb race: touch the start pad, climb, ring the bell ------------------------------------------
local truss = Instance.new("TrussPart")
truss.Name = "ClimbTruss"
truss.Anchored = true
truss.Size = Vector3.new(2, 24, 2)
truss.CFrame = CFrame.new(24, 12, 0)
truss.Parent = arena
anchoredPart("TrussTop", Vector3.new(8, 1, 8), CFrame.new(24, 24.5, 4), Color3.fromRGB(110, 110, 120))
local startPad = anchoredPart("ClimbStart", Vector3.new(6, 0.4, 6), CFrame.new(24, 0.2, -4), Color3.fromRGB(70, 200, 120))
startPad.CanCollide = false
local bell = anchoredPart("ClimbBell", Vector3.new(2, 2, 2), CFrame.new(24, 26.5, 6.5), Color3.fromRGB(240, 200, 60))
bell.Shape = Enum.PartType.Ball
bell.Material = Enum.Material.Metal

local climbStart: { [Player]: number } = {}
local MIN_CLIMB_SECONDS = 1.8 -- faster than physically possible on a 24-stud truss
local function playerFromPart(hit: BasePart): Player?
	local model = hit:FindFirstAncestorOfClass("Model")
	return if model then Players:GetPlayerFromCharacter(model) else nil
end
startPad.Touched:Connect(function(hit)
	local player = playerFromPart(hit)
	if player and climbStart[player] == nil then
		climbStart[player] = os.clock()
		GameState.announce("Climb race! Ring the bell at the top", player)
	elseif player then
		climbStart[player] = os.clock() -- standing on the pad keeps the clock at zero
	end
end)
bell.Touched:Connect(function(hit)
	local player = playerFromPart(hit)
	local started = player and climbStart[player]
	if player == nil or started == nil then
		return
	end
	-- Server-side checks: really at the bell, and not impossibly fast.
	local character = player.Character
	local root = character and character:FindFirstChild("HumanoidRootPart")
	local elapsed = os.clock() - started
	if root == nil or not root:IsA("BasePart") or (root.Position - bell.Position).Magnitude > 6 or elapsed < MIN_CLIMB_SECONDS then
		return
	end
	climbStart[player] = nil
	feedbackRemote:FireAllClients("sound", { name = "record", position = bell.Position })
	GameState.submit("climb", player, elapsed)
end)
Players.PlayerRemoving:Connect(function(player: Player)
	climbStart[player] = nil
end)

-- Pool with a splash zone ---------------------------------------------------------------------
-- Terrain uses a 4-stud voxel grid, so the pool is grid-aligned (x -16..16, y 0..8, z 24..56).
local POOL_CENTER = Vector3.new(0, 4, 40)
local POOL_SIZE = Vector3.new(32, 8, 32)
workspace.Terrain:FillBlock(CFrame.new(POOL_CENTER), POOL_SIZE, Enum.Material.Water)
for _, side in { Vector3.new(1, 0, 0), Vector3.new(-1, 0, 0), Vector3.new(0, 0, 1), Vector3.new(0, 0, -1) } do
	local alongX = side.X == 0
	local size = if alongX then Vector3.new(POOL_SIZE.X + 2, 8, 1) else Vector3.new(1, 8, POOL_SIZE.Z + 2)
	local offset = Vector3.new(side.X * (POOL_SIZE.X / 2 + 0.5), 0, side.Z * (POOL_SIZE.Z / 2 + 0.5))
	anchoredPart("PoolRim", size, CFrame.new(POOL_CENTER + offset), Color3.fromRGB(200, 200, 205))
end
anchoredPart("PoolSteps", Vector3.new(6, 4, 4), CFrame.new(0, 2, 40 - POOL_SIZE.Z / 2 - 3), Color3.fromRGB(200, 200, 205))
local poolZone = anchoredPart("PoolZone", POOL_SIZE, CFrame.new(POOL_CENTER), Color3.new(0, 0, 0))
poolZone.Transparency = 1
poolZone.CanCollide = false
poolZone.CanTouch = false
poolZone.CanQuery = false

-- Launch bench: sit, and anyone can pull the lever to fling the sitter into the pool -------------
local seat = Instance.new("Seat")
seat.Name = "Bench"
seat.Anchored = true
seat.Size = Vector3.new(4, 1, 2)
seat.CFrame = CFrame.lookAt(Vector3.new(-18, 1.5, 0), Vector3.new(0, 1.5, 40))
seat.Parent = arena
local lever = anchoredPart("LaunchLever", Vector3.new(0.6, 3, 0.6), seat.CFrame * CFrame.new(3, 1, 0), Color3.fromRGB(220, 60, 60))
local launchPrompt = prompt(lever, "Launch!", "Bench")

local LAUNCH_FLIGHT_TIME = 1.4 -- seconds to the pool centre; peaks about 49 studs up
launchPrompt.Triggered:Connect(function(puller: Player)
	local occupant = seat.Occupant
	local riderModel = occupant and occupant:FindFirstAncestorOfClass("Model")
	local rider = riderModel and Players:GetPlayerFromCharacter(riderModel)
	if occupant == nil or rider == nil then
		GameState.announce("Someone has to sit on the bench first", puller)
		return
	end
	local root = occupant.Parent and occupant.Parent:FindFirstChild("HumanoidRootPart")
	if root == nil or not root:IsA("BasePart") then
		return
	end
	-- Disable the seat for the launch so the rider isn't re-seated before the push arrives.
	seat.Disabled = true
	task.delay(2.5, function()
		seat.Disabled = false
	end)
	local weld = seat:FindFirstChild("SeatWeld")
	if weld then
		weld:Destroy()
	end
	occupant.Sit = false
	local target = POOL_CENTER + Vector3.new(0, 2, 0)
	local delta = target - root.Position
	local g = workspace.Gravity
	local velocity = Vector3.new(delta.X / LAUNCH_FLIGHT_TIME, (delta.Y + 0.5 * g * LAUNCH_FLIGHT_TIME ^ 2) / LAUNCH_FLIGHT_TIME, delta.Z / LAUNCH_FLIGHT_TIME)
	feedbackRemote:FireAllClients("sound", { name = "launch", position = seat.Position })
	feedbackRemote:FireClient(rider, "launch", { velocity = velocity, duration = LAUNCH_FLIGHT_TIME })
	if puller == rider then
		GameState.feed(`{rider.DisplayName} launched themselves into the pool`)
	else
		GameState.feed(`{puller.DisplayName} launched {rider.DisplayName} into the pool`)
	end
end)

-- Training dummy with a visible health bar and a 10-second challenge pad -----------------------
local DUMMY_CFRAME = CFrame.new(0, 4, -14) * CFrame.Angles(0, math.pi, 0)
local currentDummy: Humanoid? = nil

local function spawnDummy()
	local description = Instance.new("HumanoidDescription")
	local dummy = Players:CreateHumanoidModelFromDescription(description, Enum.HumanoidRigType.R15)
	dummy.Name = "TrainingDummy"
	local humanoid = dummy:FindFirstChildOfClass("Humanoid") :: Humanoid
	humanoid.BreakJointsOnDeath = false
	humanoid.MaxHealth = 150
	humanoid.Health = 150
	humanoid.DisplayName = "Training Dummy"
	humanoid.DisplayDistanceType = Enum.HumanoidDisplayDistanceType.Viewer
	humanoid.HealthDisplayType = Enum.HumanoidHealthDisplayType.AlwaysOn
	humanoid.HealthDisplayDistance = 60
	humanoid.NameDisplayDistance = 60
	dummy:PivotTo(DUMMY_CFRAME)
	dummy.Parent = arena
	local dummyRoot = dummy:FindFirstChild("HumanoidRootPart")
	if dummyRoot and dummyRoot:IsA("BasePart") then
		-- Keep physics on the server, so server-side knockback isn't overwritten by a nearby client.
		dummyRoot:SetNetworkOwner(nil)
	end
	currentDummy = humanoid
	GameState.watch(humanoid, "the Training Dummy", false)
	ReplicatedPlay.base(humanoid, "idle")
	humanoid.Died:Connect(function()
		ReplicatedPlay.action(humanoid, "death", true)
		task.delay(4, function()
			dummy:Destroy()
			spawnDummy()
		end)
	end)
end

local challengePad = anchoredPart("ChallengePad", Vector3.new(5, 0.4, 3), CFrame.new(0, 0.2, -9), Color3.fromRGB(240, 140, 50))
local challengePrompt = prompt(challengePad, "10 s damage challenge", "Training Dummy")
challengePrompt.Triggered:Connect(function(player: Player)
	local dummy = currentDummy
	if dummy and dummy.Parent and dummy.Health > 0 then
		GameState.startChallenge(player, function()
			return currentDummy
		end)
	end
end)

-- Kicks knock the dummy away; walk it back home once it has settled for a moment.
task.spawn(function()
	while arena.Parent do
		task.wait(1)
		local dummy = currentDummy
		local model = dummy and dummy.Parent
		local root = model and model:FindFirstChild("HumanoidRootPart")
		if dummy and dummy.Health > 0 and model and model:IsA("Model") and root and root:IsA("BasePart") then
			local lastHit = dummy:GetAttribute("LastHitAt")
			local settled = typeof(lastHit) ~= "number" or os.clock() - lastHit > 2
			if settled and (root.Position - DUMMY_CFRAME.Position).Magnitude > 3 then
				model:PivotTo(DUMMY_CFRAME)
			end
		end
	end
end)

spawnDummy()
