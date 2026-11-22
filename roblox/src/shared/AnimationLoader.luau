--!strict
-- Resolves a clip name to an Animation instance.
--   1. A published ID in AnimationIds wins.
--   2. Otherwise, in Studio only, the synced KeyframeSequence is registered with
--      KeyframeSequenceProvider to get a temporary ID, so the whole pack can be play-tested
--      before anything is published.
--   3. Otherwise the clip is missing and a warning explains how to fix it.

local KeyframeSequenceProvider = game:GetService("KeyframeSequenceProvider")
local RunService = game:GetService("RunService")

local pack = script.Parent
local AnimationIds = require(pack:WaitForChild("AnimationIds"))

local AnimationLoader = {}

local cache: { [string]: Animation } = {}
local warned: { [string]: boolean } = {}

local function resolveId(name: string): string?
	local id = AnimationIds[name]
	if id ~= nil and id ~= 0 then
		return "rbxassetid://" .. tostring(id)
	end
	if RunService:IsStudio() then
		local folder = pack:FindFirstChild("KeyframeSequences")
		local sequence = folder and folder:FindFirstChild(name)
		if sequence and sequence:IsA("KeyframeSequence") then
			return KeyframeSequenceProvider:RegisterKeyframeSequence(sequence)
		end
	end
	return nil
end

function AnimationLoader.get(name: string): Animation?
	local cached = cache[name]
	if cached then
		return cached
	end
	local animationId = resolveId(name)
	if animationId == nil then
		if not warned[name] then
			warned[name] = true
			warn(
				`[AnimationPack] "{name}" has no published ID in AnimationIds and no KeyframeSequence `
					.. "fallback (the fallback only works in Studio). Publish it and paste the ID into AnimationIds."
			)
		end
		return nil
	end
	local animation = Instance.new("Animation")
	animation.Name = name
	animation.AnimationId = animationId
	cache[name] = animation
	return animation
end

return AnimationLoader
