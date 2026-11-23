--!strict
-- Client half of ReplicatedPlay: plays server-requested clips locally when they are not published
-- (Studio testing). Base loops come from the Humanoid's "PackBaseAnimation" attribute (so late joiners
-- see them too); one-shots arrive through Remotes.PlayAnimation.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local AnimationController = require(pack:WaitForChild("AnimationController"))
local playRemote = pack:WaitForChild("Remotes"):WaitForChild("PlayAnimation") :: RemoteEvent

local BASE_ATTRIBUTE = "PackBaseAnimation"
local watched: { [Humanoid]: boolean } = {}

local function applyBase(humanoid: Humanoid)
	local name = humanoid:GetAttribute(BASE_ATTRIBUTE)
	if typeof(name) == "string" then
		AnimationController.new(humanoid):playBase(name, 0.2, 1)
	end
end

local function watch(humanoid: Humanoid)
	if watched[humanoid] then
		return
	end
	watched[humanoid] = true
	humanoid:GetAttributeChangedSignal(BASE_ATTRIBUTE):Connect(function()
		applyBase(humanoid)
	end)
	humanoid.AncestryChanged:Connect(function()
		if not humanoid:IsDescendantOf(game) then
			watched[humanoid] = nil
		end
	end)
	applyBase(humanoid)
end

workspace.DescendantAdded:Connect(function(instance)
	if instance:IsA("Humanoid") then
		watch(instance)
	end
end)
for _, instance in workspace:GetDescendants() do
	if instance:IsA("Humanoid") then
		watch(instance)
	end
end

playRemote.OnClientEvent:Connect(function(humanoid: unknown, name: unknown, stopOthers: unknown)
	if typeof(humanoid) ~= "Instance" or not humanoid:IsA("Humanoid") or typeof(name) ~= "string" then
		return
	end
	local controller = AnimationController.new(humanoid)
	if stopOthers == true then
		controller:stopAll(0.1)
	end
	controller:playAction(name, 0.05, 1)
end)
