--!strict
-- Server-side helper for animations the SERVER starts on someone (NPC idle/death, hit reactions).
--
-- With published IDs the server simply plays the track and the Animator replicates it.
-- In Studio, unpublished clips use temporary IDs from KeyframeSequenceProvider, which only work on
-- the machine that registered them, so a server-played track would be invisible to clients.
-- In that case the server instead (a) stores the looping base clip in the Humanoid's
-- "PackBaseAnimation" attribute and (b) broadcasts one-shots through Remotes.PlayAnimation;
-- the AnimationReplicator client script plays both locally.

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local AnimationController = require(pack:WaitForChild("AnimationController"))
local AnimationIds = require(pack:WaitForChild("AnimationIds"))
local playRemote = pack:WaitForChild("Remotes"):WaitForChild("PlayAnimation") :: RemoteEvent

local ReplicatedPlay = {}

ReplicatedPlay.BASE_ATTRIBUTE = "PackBaseAnimation"

local function published(name: string): boolean
	local id = AnimationIds[name]
	return id ~= nil and id ~= 0
end

-- Looping state clip (e.g. an NPC's idle).
function ReplicatedPlay.base(humanoid: Humanoid, name: string)
	if published(name) then
		AnimationController.new(humanoid):playBase(name, 0.2, 1)
		humanoid:SetAttribute(ReplicatedPlay.BASE_ATTRIBUTE, nil)
	else
		humanoid:SetAttribute(ReplicatedPlay.BASE_ATTRIBUTE, name)
	end
end

-- One-shot clip (hit_react, death). stopOthers stops everything else first (used for death).
function ReplicatedPlay.action(humanoid: Humanoid, name: string, stopOthers: boolean?)
	if published(name) then
		local controller = AnimationController.new(humanoid)
		if stopOthers then
			controller:stopAll(0.1)
		end
		controller:playAction(name, 0.05, 1)
	else
		if stopOthers then
			humanoid:SetAttribute(ReplicatedPlay.BASE_ATTRIBUTE, nil)
		end
		playRemote:FireAllClients(humanoid, name, stopOthers == true)
	end
end

return ReplicatedPlay
