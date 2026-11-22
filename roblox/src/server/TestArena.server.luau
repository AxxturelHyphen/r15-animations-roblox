--!strict
-- Builds a small test arena in Studio play-tests (or when ReplicatedStorage.AnimationPack has the
-- attribute BuildTestArena = true) so every animation state can be tried quickly:
--   a truss to climb, a water pool to swim in, a seat, and a respawning R15 training dummy to hit.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
if not (RunService:IsStudio() or pack:GetAttribute("BuildTestArena") == true) then
	return
end

local AnimationController = require(pack:WaitForChild("AnimationController"))

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

-- Climbing: a tall truss.
local truss = Instance.new("TrussPart")
truss.Name = "ClimbTruss"
truss.Anchored = true
truss.Size = Vector3.new(2, 24, 2)
truss.CFrame = CFrame.new(24, 12, 0)
truss.Parent = arena
anchoredPart("TrussTop", Vector3.new(8, 1, 8), CFrame.new(24, 24.5, 4), Color3.fromRGB(110, 110, 120))

-- Swimming: a block of terrain water inside a low rim.
local POOL_CENTER = Vector3.new(0, 4, 40)
local POOL_SIZE = Vector3.new(28, 8, 28)
workspace.Terrain:FillBlock(CFrame.new(POOL_CENTER), POOL_SIZE, Enum.Material.Water)
for _, side in { Vector3.new(1, 0, 0), Vector3.new(-1, 0, 0), Vector3.new(0, 0, 1), Vector3.new(0, 0, -1) } do
	local alongX = side.X == 0
	local size = if alongX then Vector3.new(POOL_SIZE.X + 2, 8, 1) else Vector3.new(1, 8, POOL_SIZE.Z + 2)
	local offset = Vector3.new(side.X * (POOL_SIZE.X / 2 + 0.5), 0, side.Z * (POOL_SIZE.Z / 2 + 0.5))
	anchoredPart("PoolRim", size, CFrame.new(POOL_CENTER + offset), Color3.fromRGB(200, 200, 205))
end
anchoredPart("PoolSteps", Vector3.new(6, 4, 4), CFrame.new(0, 2, 40 - POOL_SIZE.Z / 2 - 3), Color3.fromRGB(200, 200, 205))

-- Sitting: a bench seat.
local seat = Instance.new("Seat")
seat.Name = "Bench"
seat.Anchored = true
seat.Size = Vector3.new(4, 1, 2)
seat.CFrame = CFrame.new(-18, 1.5, 0)
seat.Parent = arena

-- A respawning training dummy for the combat moves.
local DUMMY_CFRAME = CFrame.new(0, 4, -14) * CFrame.Angles(0, math.pi, 0)

local function spawnDummy()
	local description = Instance.new("HumanoidDescription")
	local dummy = Players:CreateHumanoidModelFromDescription(description, Enum.HumanoidRigType.R15)
	dummy.Name = "TrainingDummy"
	local humanoid = dummy:FindFirstChildOfClass("Humanoid") :: Humanoid
	humanoid.BreakJointsOnDeath = false
	humanoid.MaxHealth = 150
	humanoid.Health = 150
	humanoid.DisplayDistanceType = Enum.HumanoidDisplayDistanceType.Subject
	dummy:PivotTo(DUMMY_CFRAME)
	dummy.Parent = arena
	local controller = AnimationController.new(humanoid)
	controller:playBase("idle", 0, 1)
	humanoid.Died:Connect(function()
		controller:stopAll(0.1)
		controller:playAction("death", 0.1, 1)
		task.delay(4, function()
			dummy:Destroy()
			spawnDummy()
		end)
	end)
end

spawnDummy()
