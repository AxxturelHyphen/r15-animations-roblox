--!strict
-- Two-player and show-off moments, reported by clients through Remotes.Social and validated here:
--   ("emote", name)     /e highfive matches two players into a synced high five (or "left hanging");
--                       any emote right after a KO becomes a taunt in the kill feed.
--   ("splash", height)  landing in the pool: a splash sized by fall height, and the biggest-splash record.
--   ("landing", height) a heavy landing after a big fall: thud and dust for everyone.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local Feedback = require(pack:WaitForChild("Feedback"))
local AnimationMeta = require(pack:WaitForChild("AnimationMeta"))
local ReplicatedPlay = require(pack:WaitForChild("ReplicatedPlay"))
local GameState = require(script.Parent:WaitForChild("GameState"))
local remotes = pack:WaitForChild("Remotes")
local socialRemote = remotes:WaitForChild("Social") :: RemoteEvent
local feedbackRemote = remotes:WaitForChild("Feedback") :: RemoteEvent

local EMOTES = { wave = true, dance = true, cheer = true, point = true, laugh = true, clap = true, salute = true }
local EMOTE_TAUNT_TEXT: { [string]: string } = {
	laugh = "laughed at",
	dance = "danced on",
	point = "pointed at",
	salute = "saluted",
	cheer = "cheered over",
	clap = "slow-clapped",
	wave = "waved bye-bye to",
}

local pendingHighFive: { [Player]: number } = {}
local dancingSince: { [Player]: number } = {}
local lastFeedLine: { [Player]: number } = {}
local lastLanding: { [Player]: number } = {}
local lastDanceParty = -math.huge

-- Server-side height tracking: the highest root Y in the last few seconds, used to check fall heights
-- that clients report for splashes and landings.
type Peak = { y: number, at: number }
local peaks: { [Player]: Peak } = {}
RunService.Heartbeat:Connect(function()
	local now = os.clock()
	for _, p in Players:GetPlayers() do
		local character = p.Character
		local root = character and character:FindFirstChild("HumanoidRootPart")
		if root and root:IsA("BasePart") then
			local y = root.Position.Y
			local peak = peaks[p]
			if peak == nil or y >= peak.y or now - peak.at > 3 then
				peaks[p] = { y = y, at = now }
			end
		end
	end
end)

local function verifiedFall(player: Player, claimed: number, root: BasePart): number?
	if claimed ~= claimed then
		return nil -- NaN
	end
	local peak = peaks[player]
	if peak == nil then
		return nil
	end
	local maxFall = peak.y - root.Position.Y + 3
	return math.floor(math.clamp(math.min(claimed, maxFall), 0, 80)) -- the bench can throw ~65 studs
end

-- One feed line per player every 3 s (taunts and dance parties), so nobody floods the feed.
local function feedFrom(player: Player, text: string)
	local now = os.clock()
	if now - (lastFeedLine[player] or -math.huge) < 3 then
		return
	end
	lastFeedLine[player] = now
	GameState.feed(text)
end
local lastReport: { [Player]: number } = {}

local function rootOf(player: Player): BasePart?
	local character = player.Character
	local root = character and character:FindFirstChild("HumanoidRootPart")
	if root and root:IsA("BasePart") then
		return root
	end
	return nil
end

local function humanoidOf(player: Player): Humanoid?
	local character = player.Character
	local humanoid = character and character:FindFirstChildOfClass("Humanoid")
	if humanoid and humanoid.Health > 0 then
		return humanoid
	end
	return nil
end

local function markerTime(clip: string, marker: string): number
	local meta = AnimationMeta[clip]
	if meta then
		for _, m in meta.markers do
			if m.name == marker then
				return m.time
			end
		end
	end
	return 0.33
end

local function doHighFive(a: Player, b: Player)
	local ra, rb = rootOf(a), rootOf(b)
	local ha, hb = humanoidOf(a), humanoidOf(b)
	local ca, cb = a.Character, b.Character
	if not (ra and rb and ha and hb and ca and cb) then
		return
	end
	-- Only standing players: no snapping someone out of a seat, a ladder or the water.
	for _, h in { ha, hb } do
		local state = h:GetState()
		if h.Sit or state == Enum.HumanoidStateType.Climbing or state == Enum.HumanoidStateType.Swimming then
			return
		end
	end
	-- Square them up: face each other 3.7 studs apart, where the high_five hands meet (critic-measured).
	local mid = (ra.Position + rb.Position) / 2
	local axis = (rb.Position - ra.Position) * Vector3.new(1, 0, 1)
	local dir = if axis.Magnitude > 0.1 then axis.Unit else Vector3.new(0, 0, -1)
	local posA = Vector3.new(mid.X, ra.Position.Y, mid.Z) - dir * 1.85
	local posB = Vector3.new(mid.X, rb.Position.Y, mid.Z) + dir * 1.85
	ca:PivotTo(CFrame.lookAt(posA, posA + dir))
	cb:PivotTo(CFrame.lookAt(posB, posB - dir))
	ReplicatedPlay.action(ha, "high_five")
	ReplicatedPlay.action(hb, "high_five")
	task.delay(markerTime("high_five", "Clap"), function()
		feedbackRemote:FireAllClients("sound", { name = "clap", position = mid + Vector3.new(0, 2.5, 0) })
		feedbackRemote:FireAllClients("burst", { position = mid + Vector3.new(0, 2.5, 0), kind = "clap" })
	end)
	GameState.addHighFive(a, b)
	GameState.feed(`{a.DisplayName} and {b.DisplayName} high-fived!`)
end

local function requestHighFive(player: Player)
	local root = rootOf(player)
	if root == nil then
		return
	end
	local now = os.clock()
	for other, at in pendingHighFive do
		local otherRoot = rootOf(other)
		if other ~= player and otherRoot and now - at <= Feedback.HIGH_FIVE_WINDOW
			and (otherRoot.Position - root.Position).Magnitude <= Feedback.HIGH_FIVE_RANGE then
			pendingHighFive[other] = nil
			pendingHighFive[player] = nil
			doHighFive(other, player)
			return
		end
	end
	pendingHighFive[player] = now
	GameState.announce("Hand up! Your friend has 3 seconds to /e highfive back", player)
	task.delay(Feedback.HIGH_FIVE_WINDOW, function()
		if pendingHighFive[player] == now then
			pendingHighFive[player] = nil
			local humanoid = humanoidOf(player)
			if humanoid then
				ReplicatedPlay.action(humanoid, "high_five")
			end
			GameState.feed(`{player.DisplayName} was left hanging`)
		end
	end)
end

socialRemote.OnServerEvent:Connect(function(player: Player, kind: unknown, value: unknown)
	local now = os.clock()
	if now - (lastReport[player] or 0) < 0.25 then
		return -- rate limit
	end
	lastReport[player] = now
	local root = rootOf(player)
	if root == nil then
		return
	end
	if kind == "emote" and typeof(value) == "string" then
		if value == "highfive" then
			requestHighFive(player)
		elseif EMOTES[value] then
			if value == "dance" then
				-- Dance party: two or more players dancing near each other.
				dancingSince[player] = now
				local crew = { player.DisplayName }
				for other, at in dancingSince do
					local otherRoot = rootOf(other)
					if other ~= player and now - at <= 8 and otherRoot and (otherRoot.Position - root.Position).Magnitude <= 16 then
						table.insert(crew, other.DisplayName)
					end
				end
				if #crew >= 2 and now - lastDanceParty > 8 then
					lastDanceParty = now
					feedFrom(player, `Dance party! {table.concat(crew, " + ")}`)
				end
			end
			local ko = GameState.lastKO(player)
			if ko and now - ko.at <= Feedback.TAUNT_WINDOW then
				feedFrom(player, `{player.DisplayName} {EMOTE_TAUNT_TEXT[value]} {ko.victim}`)
			end
		end
	elseif kind == "splash" and typeof(value) == "number" then
		local arena = workspace:FindFirstChild("AnimationTestArena")
		local pool = arena and arena:FindFirstChild("PoolZone")
		if pool == nil or not pool:IsA("BasePart") then
			return -- no pool in this place
		end
		-- Only count splashes inside the pool zone.
		local localPos = pool.CFrame:PointToObjectSpace(root.Position)
		local half = pool.Size / 2 + Vector3.new(2, 6, 2)
		if math.abs(localPos.X) > half.X or math.abs(localPos.Y) > half.Y or math.abs(localPos.Z) > half.Z then
			return
		end
		local height = verifiedFall(player, value, root)
		if height == nil then
			return
		end
		feedbackRemote:FireAllClients("splash", { position = root.Position, size = height })
		-- Knocked (kick or combo finisher) into the water by someone in the last 3 s: a dunk.
		-- Each knock is credited once (clearing the tag), so re-entering the water doesn't repeat it.
		local humanoid = humanoidOf(player)
		local byId = humanoid and humanoid:GetAttribute("LastKnockBy")
		local at = humanoid and humanoid:GetAttribute("LastKnockAt")
		local dunker = if typeof(byId) == "number" then Players:GetPlayerByUserId(byId) else nil
		if humanoid and dunker and dunker ~= player and typeof(at) == "number" and now - at <= 3 then
			humanoid:SetAttribute("LastKnockAt", nil)
			GameState.feed(`{dunker.DisplayName} dunked {player.DisplayName} into the pool`)
		end
		if height >= 6 then
			GameState.submit("splash", player, height)
		end
	elseif kind == "landing" and typeof(value) == "number" then
		if now - (lastLanding[player] or -math.huge) < 1 then
			return
		end
		local height = verifiedFall(player, value, root)
		if height == nil or height < Feedback.HEAVY_LANDING_STUDS then
			return
		end
		lastLanding[player] = now
		feedbackRemote:FireAllClients("landing", { position = root.Position - Vector3.new(0, 2.8, 0), height = height })
	end
end)

Players.PlayerRemoving:Connect(function(player: Player)
	pendingHighFive[player] = nil
	lastReport[player] = nil
	dancingSince[player] = nil
	lastFeedLine[player] = nil
	lastLanding[player] = nil
	peaks[player] = nil
end)
