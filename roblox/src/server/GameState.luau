--!strict
-- Server-side game state for the playtest arena: leaderstats, records, the head-to-head rivalry
-- board, the kill feed and the dummy damage challenge. Required by CombatServer, Social and TestArena.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local Feedback = require(pack:WaitForChild("Feedback"))
local feedbackRemote = pack:WaitForChild("Remotes"):WaitForChild("Feedback") :: RemoteEvent

local GameState = {}

type RecordSpec = { label: string, unit: string, lowerIsBetter: boolean }
type Record = { value: number, holder: string }

local RECORDS: { [string]: RecordSpec } = {
	climb = { label = "Fastest climb", unit = "s", lowerIsBetter = true },
	splash = { label = "Biggest splash", unit = " studs", lowerIsBetter = false },
	challenge = { label = "Dummy challenge (10 s)", unit = " dmg", lowerIsBetter = false },
}
local records: { [string]: Record } = {}
local rivalry: { [string]: number } = {} -- "killer>victim" -> KOs
local highFives = 0
local lastKO: { [Player]: { victim: string, at: number } } = {}
local boardLabel: TextLabel? = nil
local lastRecordAnnounce: { [string]: number } = {}

type Challenge = { startedAt: number, total: number }
local challenges: { [Player]: Challenge } = {}

-- Messaging --------------------------------------------------------------------------------------

function GameState.feed(text: string)
	feedbackRemote:FireAllClients("toast", { text = text, style = "feed" })
end

function GameState.announce(text: string, player: Player?)
	local payload = { text = text, style = "record" }
	if player then
		feedbackRemote:FireClient(player, "toast", payload)
	else
		feedbackRemote:FireAllClients("toast", payload)
	end
end

-- Board -----------------------------------------------------------------------------------------

local function formatValue(key: string, value: number): string
	local spec = RECORDS[key]
	if key == "climb" then
		return string.format("%.2f%s", value, spec.unit)
	end
	return string.format("%d%s", math.floor(value + 0.5), spec.unit)
end

function GameState.refreshBoard()
	local label = boardLabel
	if label == nil then
		return
	end
	local lines = { "RECORDS" }
	for _, key in { "climb", "splash", "challenge" } do
		local r = records[key]
		table.insert(lines, `{RECORDS[key].label}: {if r then formatValue(key, r.value) .. "  " .. r.holder else "-"}`)
	end
	table.insert(lines, `High fives: {highFives}`)
	table.insert(lines, "")
	table.insert(lines, "RIVALRIES")
	local shown: { [string]: boolean } = {}
	for key in rivalry do
		local a, b = string.match(key, "^(.-)>(.+)$")
		if a and b then
			local pairKey = if a < b then a .. "|" .. b else b .. "|" .. a
			if not shown[pairKey] then
				shown[pairKey] = true
				table.insert(lines, `{a} {rivalry[a .. ">" .. b] or 0} - {rivalry[b .. ">" .. a] or 0} {b}`)
			end
		end
	end
	label.Text = table.concat(lines, "\n")
end

function GameState.setBoard(label: TextLabel)
	boardLabel = label
	GameState.refreshBoard()
end

-- Records ---------------------------------------------------------------------------------------

-- Returns true if this is a new record.
function GameState.submit(key: string, player: Player, value: number): boolean
	local spec = RECORDS[key]
	if spec == nil then
		return false
	end
	local current = records[key]
	if current == nil or (if spec.lowerIsBetter then value < current.value else value > current.value) then
		local previous = if current then current.holder else nil
		records[key] = { value = value, holder = player.DisplayName }
		GameState.refreshBoard()
		-- Throttle global callouts per record, so nobody can spam everyone's screen.
		local now = os.clock()
		if now - (lastRecordAnnounce[key] or -math.huge) >= 3 then
			lastRecordAnnounce[key] = now
			local beat = if previous and previous ~= player.DisplayName then ` (beat {previous}!)` else ""
			GameState.announce(`NEW RECORD! {spec.label}: {formatValue(key, value)}{beat}`)
			feedbackRemote:FireAllClients("sound", { name = "record" })
		else
			GameState.announce(`NEW RECORD! {spec.label}: {formatValue(key, value)}`, player)
		end
		return true
	end
	GameState.announce(`{spec.label}: {formatValue(key, value)} (record {formatValue(key, current.value)} by {current.holder})`, player)
	return false
end

function GameState.addHighFive(a: Player, b: Player)
	highFives += 1
	for _, p in { a, b } do
		local stats = p:FindFirstChild("leaderstats")
		local value = stats and stats:FindFirstChild("High Fives")
		if value and value:IsA("IntValue") then
			value.Value += 1
		end
	end
	GameState.refreshBoard()
end

-- KOs and the kill feed -------------------------------------------------------------------------

local HOW_TEXT: { [string]: string } = {
	punch = "punched %s into a nap",
	combo = "comboed %s into a nap",
	kick = "kicked %s into a nap",
	sword_slash = "slashed %s into a nap",
	sneak = "sneak-attacked %s into a nap",
}

-- Called by CombatServer before damage, so a death can be credited.
function GameState.tagHit(victim: Humanoid, attacker: Player, how: string)
	victim:SetAttribute("LastHitBy", attacker.UserId)
	victim:SetAttribute("LastHitAt", os.clock())
	victim:SetAttribute("LastHitHow", how)
end

function GameState.lastKO(player: Player): { victim: string, at: number }?
	return lastKO[player]
end

local function onDied(humanoid: Humanoid, victimName: string, isPlayer: boolean)
	local root = humanoid.Parent and humanoid.Parent:FindFirstChild("HumanoidRootPart")
	local byId = humanoid:GetAttribute("LastHitBy")
	local at = humanoid:GetAttribute("LastHitAt")
	local how = humanoid:GetAttribute("LastHitHow")
	local killer = if typeof(byId) == "number" then Players:GetPlayerByUserId(byId) else nil
	feedbackRemote:FireAllClients("sound", { name = "ko", position = if root and root:IsA("BasePart") then root.Position else nil })
	if killer and typeof(at) == "number" and os.clock() - at < 6 and not isPlayer then
		-- The dummy: a feed line only (no KO, rivalry or taunt window, so it can't be farmed).
		local template = HOW_TEXT[if typeof(how) == "string" then how else ""] or "sent %s to nap"
		GameState.feed(`{killer.DisplayName} {string.format(template, victimName)}`)
	elseif killer and typeof(at) == "number" and os.clock() - at < 6 then
		local stats = killer:FindFirstChild("leaderstats")
		local kos = stats and stats:FindFirstChild("KOs")
		if kos and kos:IsA("IntValue") then
			kos.Value += 1
		end
		local key = killer.DisplayName .. ">" .. victimName
		rivalry[key] = (rivalry[key] or 0) + 1
		lastKO[killer] = { victim = victimName, at = os.clock() }
		local template = HOW_TEXT[if typeof(how) == "string" then how else ""] or "sent %s to nap"
		GameState.feed(`{killer.DisplayName} {string.format(template, victimName)}`)
		GameState.refreshBoard()
	elseif root == nil or (root:IsA("BasePart") and root.Position.Y < -20) then
		-- Parts below FallenPartsDestroyHeight are destroyed, so a missing root means a fall.
		GameState.feed(`{victimName} fell off the world`)
	else
		GameState.feed(`{victimName} took a nap`)
	end
end

function GameState.watch(humanoid: Humanoid, victimName: string, isPlayer: boolean)
	humanoid.Died:Connect(function()
		onDied(humanoid, victimName, isPlayer)
	end)
end

-- Dummy challenge -------------------------------------------------------------------------------

-- getDummy returns the current dummy (it is replaced after every death).
function GameState.startChallenge(player: Player, getDummy: () -> Humanoid?): boolean
	if challenges[player] then
		return false
	end
	challenges[player] = { startedAt = os.clock(), total = 0 }
	local dummy = getDummy()
	if dummy then
		dummy.Health = dummy.MaxHealth
	end
	feedbackRemote:FireClient(player, "countdown", { seconds = Feedback.CHALLENGE_SECONDS })
	task.delay(Feedback.CHALLENGE_SECONDS, function()
		local c = challenges[player]
		challenges[player] = nil
		if c and player.Parent then
			GameState.submit("challenge", player, c.total)
		end
		local current = getDummy()
		if current and current.Parent and current.Health > 0 then
			current.Health = current.MaxHealth
		end
	end)
	return true
end

-- While any challenge runs, the dummy is kept alive so scores aren't capped by its respawn.
function GameState.challengeActive(): boolean
	return next(challenges) ~= nil
end

function GameState.onDummyDamage(player: Player, amount: number)
	local c = challenges[player]
	if c then
		c.total += amount
	end
end

-- Players ---------------------------------------------------------------------------------------

local function setupPlayer(player: Player)
	local stats = Instance.new("Folder")
	stats.Name = "leaderstats"
	local kos = Instance.new("IntValue")
	kos.Name = "KOs"
	kos.Parent = stats
	local fives = Instance.new("IntValue")
	fives.Name = "High Fives"
	fives.Parent = stats
	stats.Parent = player
	local function onCharacter(character: Model)
		local humanoid = character:WaitForChild("Humanoid") :: Humanoid
		GameState.watch(humanoid, player.DisplayName, true)
	end
	player.CharacterAdded:Connect(onCharacter)
	if player.Character then
		task.spawn(onCharacter, player.Character)
	end
end

Players.PlayerAdded:Connect(setupPlayer)
for _, player in Players:GetPlayers() do
	setupPlayer(player)
end
Players.PlayerRemoving:Connect(function(player: Player)
	lastKO[player] = nil
	challenges[player] = nil
end)

return GameState
