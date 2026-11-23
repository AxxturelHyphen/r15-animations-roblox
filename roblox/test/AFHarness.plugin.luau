-- AFHarness: automated play-test harness for this project (a Studio plugin).
--
-- It does nothing unless the open place has ReplicatedStorage.__AFTest (only the test builds made by
-- roblox/test/run_tests.py have it), so it is safe to leave installed.
--
--   edit DataModel    starts a solo or 2-player test with StudioTestService and prints the result
--   server DataModel  runs the scenarios (orchestrator) and ends the test with a JSON report
--   client DataModel  executes commands from the server: real key presses and clicks through
--                     VirtualInputManager (so CombatInput and Animate are exercised as they are
--                     played), teleports, emotes, prompts, and reports what it sees
--
-- Every line it prints starts with "[AFH]" so run_tests.py can pick it out of the Studio log.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")
local LogService = game:GetService("LogService")

local marker = ReplicatedStorage:FindFirstChild("__AFTest")
if marker == nil then
	return
end

local StudioTestService = game:GetService("StudioTestService")

local function log(...)
	local parts = {}
	for i = 1, select("#", ...) do
		table.insert(parts, tostring((select(i, ...))))
	end
	print("[AFH] " .. table.concat(parts, " "))
end

local function waitFor(cond, timeout)
	local deadline = os.clock() + (timeout or 5)
	while os.clock() < deadline do
		local ok, v = pcall(cond)
		if ok and v then
			return v
		end
		task.wait(0.05)
	end
	return nil
end

local function logProblems()
	-- Errors and warnings from the whole session, including those before the plugin loaded.
	local errs, warns = {}, {}
	for _, entry in LogService:GetLogHistory() do
		local text = entry.message
		if not string.find(text, "[AFH]", 1, true) then
			if entry.messageType == Enum.MessageType.MessageError then
				table.insert(errs, text)
			elseif entry.messageType == Enum.MessageType.MessageWarning then
				table.insert(warns, text)
			end
		end
	end
	return { errors = errs, warnings = warns }
end

local CLIPS = {
	"idle", "walk", "run", "jump", "fall", "climb", "swim", "swim_idle", "sit",
	"punch", "sword_slash", "hit_react", "block", "kick", "combo", "death",
	"wave", "dance", "cheer", "point", "laugh", "clap", "salute",
	"crouch_idle", "crouch_walk", "high_five", "land_heavy",
}

---------------------------------------------------------------------------------------------------
-- EDIT: launcher
---------------------------------------------------------------------------------------------------
if RunService:IsEdit() then
	local mode = marker:GetAttribute("Mode") or "solo"
	task.wait(5)
	log("LAUNCH", mode)
	local ok, result = pcall(function()
		if mode == "multi" then
			return StudioTestService:ExecuteMultiplayerTestAsync(2, { mode = mode })
		end
		return StudioTestService:ExecutePlayModeAsync({ mode = mode })
	end)
	if not ok then
		log("RESULT_ERROR", result)
	elseif typeof(result) == "string" then
		-- Long reports are printed in chunks: the log truncates very long lines.
		local n = math.ceil(#result / 800) -- Studio truncates log lines at ~1020 chars
		for i = 1, n do
			log(string.format("RESULT_CHUNK %d/%d %s", i, n, string.sub(result, (i - 1) * 800 + 1, i * 800)))
		end
	else
		log("RESULT_OTHER", typeof(result))
	end
	log("FINISHED")
	return
end

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local remotes = pack:WaitForChild("Remotes")
local feedbackRemote = remotes:WaitForChild("Feedback")

---------------------------------------------------------------------------------------------------
-- CLIENT: driver
---------------------------------------------------------------------------------------------------
if RunService:IsClient() then
	local player = Players.LocalPlayer
	local rf = ReplicatedStorage:WaitForChild("__AFTestRF", 60)
	if rf == nil then
		log("client: no RF")
		return
	end
	local events = {}
	local errors = {}
	feedbackRemote.OnClientEvent:Connect(function(kind, data)
		local e = { kind = kind, t = os.clock() }
		if typeof(data) == "table" then
			e.text = data.text
			e.style = data.style
			e.hitKind = data.kind
			e.amount = data.amount
			e.size = data.size
			e.height = data.height
			e.name = data.name
			if typeof(data.victim) == "Instance" then
				e.victim = data.victim.Name
			end
		end
		table.insert(events, e)
	end)
	LogService.MessageOut:Connect(function(message, messageType)
		if messageType == Enum.MessageType.MessageError then
			table.insert(errors, message)
		elseif messageType == Enum.MessageType.MessageWarning and not string.find(message, "%[AFH%]") then
			table.insert(errors, "WARN: " .. message)
		end
	end)

	local vim = nil
	local vimOk, vimErr = pcall(function()
		vim = game:GetService("VirtualInputManager")
		vim:SendKeyEvent(false, Enum.KeyCode.F13, false, game)
	end)
	if not vimOk then
		vim = nil
	end
	-- Without VirtualInputManager, drive the game's ContextActionService actions (same handlers the
	-- keyboard, gamepad and touch buttons use).
	local KEY_ACTIONS = { C = "PackCrouch", LeftControl = "PackCrouch", Q = "PackKick", F = "PackBlock" }
	local function callAction(action, down)
		-- ContextActionService:CallFunction is Roblox-internal, so use the PackAction hooks that
		-- CombatInput and Animate expose (they run the same handlers as the bound keys).
		local holder
		if action == "PackCrouch" then
			holder = player.Character and player.Character:FindFirstChild("Animate")
		else
			local ps = player:FindFirstChild("PlayerScripts")
			holder = ps and ps:FindFirstChild("CombatInput")
		end
		local fn = holder and holder:FindFirstChild("PackAction")
		if not fn then
			log("no PackAction for", action)
			return false
		end
		local ok, err = pcall(function()
			fn:Invoke(action, down)
		end)
		if not ok then
			log("PackAction failed", action, err)
		end
		return ok
	end

	local moveDir = nil
	RunService:BindToRenderStep("AFHMove", Enum.RenderPriority.Character.Value + 5, function()
		local character = player.Character
		local humanoid = character and character:FindFirstChildOfClass("Humanoid")
		if humanoid and moveDir then
			humanoid:Move(moveDir, false)
		end
	end)

	local function humanoidOf(target)
		local model
		if target == nil or target == "self" then
			model = player.Character
		elseif target == "dummy" then
			local arena = workspace:FindFirstChild("AnimationTestArena")
			model = arena and arena:FindFirstChild("TrainingDummy")
		else
			local other = Players:FindFirstChild(target)
			model = other and other.Character
		end
		return model and model:FindFirstChildOfClass("Humanoid"), model
	end

	local function playing(target)
		local humanoid = humanoidOf(target)
		local animator = humanoid and humanoid:FindFirstChildOfClass("Animator")
		local names = {}
		if animator then
			for _, track in animator:GetPlayingAnimationTracks() do
				local name = track.Animation and track.Animation.Name or "?"
				table.insert(names, string.format("%s@%.2f/%.2f", name, track.TimePosition, track.Length))
			end
		end
		return names
	end

	local commands = {}
	function commands.ping()
		return { vim = vim ~= nil, vimErr = if vimOk then nil else tostring(vimErr), name = player.Name }
	end
	function commands.water()
		-- Is there water at the pool on this client, and what state is the humanoid in?
		local region = Region3.new(Vector3.new(-4, 0, 36), Vector3.new(4, 8, 44)):ExpandToGrid(4)
		local materials = workspace.Terrain:ReadVoxels(region, 4)
		local counts = {}
		for x = 1, materials.Size.X do
			for y = 1, materials.Size.Y do
				for z = 1, materials.Size.Z do
					local m = materials[x][y][z].Name
					counts[m] = (counts[m] or 0) + 1
				end
			end
		end
		local humanoid = humanoidOf("self")
		return { voxels = counts, state = humanoid and humanoid:GetState().Name }
	end
	function commands.state()
		local humanoid, model = humanoidOf("self")
		local root = model and model:FindFirstChild("HumanoidRootPart")
		if not humanoid or not root then
			return { alive = false }
		end
		return {
			alive = humanoid.Health > 0,
			health = humanoid.Health,
			walkSpeed = humanoid.WalkSpeed,
			state = humanoid:GetState().Name,
			pos = { root.Position.X, root.Position.Y, root.Position.Z },
			shield = model:FindFirstChildOfClass("ForceField") ~= nil,
			sit = humanoid.Sit,
			tool = (model:FindFirstChildOfClass("Tool") or {}).Name,
		}
	end
	function commands.anims(target)
		return playing(target)
	end
	function commands.loadall()
		local humanoid = humanoidOf("self")
		local animator = humanoid and humanoid:FindFirstChildOfClass("Animator")
		local folder = pack:WaitForChild("KeyframeSequences")
		local out = {}
		for _, name in CLIPS do
			local seq = folder:FindFirstChild(name)
			local entry = { name = name, ok = false }
			if seq and animator then
				local ok, err = pcall(function()
					local id = game:GetService("KeyframeSequenceProvider"):RegisterKeyframeSequence(seq)
					local anim = Instance.new("Animation")
					anim.AnimationId = id
					local track = animator:LoadAnimation(anim)
					waitFor(function()
						return track.Length > 0
					end, 5)
					entry.length = track.Length
					entry.ok = track.Length > 0
					track:Destroy()
				end)
				if not ok then
					entry.err = tostring(err)
				end
			end
			table.insert(out, entry)
		end
		return out
	end
	function commands.pivot(cf)
		local character = player.Character
		local root = character and character:FindFirstChild("HumanoidRootPart")
		if not root then
			return false
		end
		character:PivotTo(cf)
		root.AssemblyLinearVelocity = Vector3.zero
		root.AssemblyAngularVelocity = Vector3.zero
		return true
	end
	function commands.key(keyName, down)
		if not vim then
			return callAction(KEY_ACTIONS[keyName], down)
		end
		vim:SendKeyEvent(down, Enum.KeyCode[keyName], false, game)
		return true
	end
	function commands.tap(keyName)
		if not vim then
			callAction(KEY_ACTIONS[keyName], true)
			task.wait(0.05)
			return callAction(KEY_ACTIONS[keyName], false)
		end
		vim:SendKeyEvent(true, Enum.KeyCode[keyName], false, game)
		task.wait(0.05)
		vim:SendKeyEvent(false, Enum.KeyCode[keyName], false, game)
		return true
	end
	function commands.click()
		if not vim then
			callAction("PackPrimary", true)
			task.wait(0.03)
			return callAction("PackPrimary", false)
		end
		local camera = workspace.CurrentCamera
		local size = camera.ViewportSize
		local x, y = size.X / 2, size.Y / 2
		vim:SendMouseButtonEvent(x, y, 0, true, game, 0)
		task.wait(0.03)
		vim:SendMouseButtonEvent(x, y, 0, false, game, 0)
		return true
	end
	function commands.move(dir, seconds)
		moveDir = dir
		if seconds then
			task.wait(seconds)
			moveDir = nil
		end
		return true
	end
	function commands.stop()
		moveDir = nil
		return true
	end
	function commands.equip(name)
		local humanoid = humanoidOf("self")
		local tool = player.Backpack:FindFirstChild(name)
		if humanoid and tool then
			humanoid:EquipTool(tool)
			return waitFor(function()
				return player.Character:FindFirstChild(name) ~= nil
			end, 3) ~= nil
		end
		return false
	end
	function commands.unequip()
		local humanoid = humanoidOf("self")
		if humanoid then
			humanoid:UnequipTools()
		end
		return true
	end
	function commands.toolGrip()
		local character = player.Character
		local hand = character and character:FindFirstChild("RightHand")
		local tool = character and character:FindFirstChildOfClass("Tool")
		local handle = tool and tool:FindFirstChild("Handle")
		if not (hand and handle) then
			return nil
		end
		local rel = hand.CFrame:ToObjectSpace(handle.CFrame)
		local look = handle.CFrame.LookVector
		return {
			offset = { rel.Position.X, rel.Position.Y, rel.Position.Z },
			handleLook = { look.X, look.Y, look.Z },
			grip = tostring(tool.Grip),
		}
	end
	function commands.emote(name)
		local character = player.Character
		local animate = character and character:FindFirstChild("Animate")
		local fn = animate and animate:FindFirstChild("PlayEmote")
		if not fn then
			return "no PlayEmote"
		end
		return fn:Invoke(name)
	end
	function commands.chatCommands()
		-- TextChannel:SendAsync blocks inside a Studio test, so check the wiring instead: the pack's
		-- /e command is registered and Roblox's built-in emote command is disabled.
		local TextChatService = game:GetService("TextChatService")
		local commandsFolder = TextChatService:FindFirstChild("TextChatCommands")
		local builtIn = commandsFolder and commandsFolder:FindFirstChild("RBXEmoteCommand")
		local ours = TextChatService:FindFirstChild("AnimationPackEmote", true)
		return {
			chatVersion = TextChatService.ChatVersion.Name,
			packCommand = ours ~= nil and ours:IsA("TextChatCommand") and ours.PrimaryAlias == "/e",
			builtInDisabled = builtIn == nil or not builtIn.Enabled,
		}
	end
	function commands.prompt(partName)
		local arena = workspace:FindFirstChild("AnimationTestArena")
		local part = arena and arena:FindFirstChild(partName)
		local prompt = part and part:FindFirstChildOfClass("ProximityPrompt")
		if not prompt then
			return "no prompt"
		end
		-- Wait until the prompt system shows it (the player has to be in range first).
		local shown = false
		local conn = game:GetService("ProximityPromptService").PromptShown:Connect(function(p)
			if p == prompt then
				shown = true
			end
		end)
		waitFor(function()
			return shown
		end, 2)
		conn:Disconnect()
		local ok, err = pcall(function()
			prompt:InputHoldBegin()
			task.wait(0.1)
			prompt:InputHoldEnd()
		end)
		return if ok then true else tostring(err)
	end
	function commands.dive(cf, speed)
		-- Teleport and shoot straight down for a few frames (like a hard bench launch).
		local character = player.Character
		local root = character and character:FindFirstChild("HumanoidRootPart")
		if not root then
			return false
		end
		character:PivotTo(cf)
		local t0 = os.clock()
		while os.clock() - t0 < 0.25 do
			root.AssemblyLinearVelocity = Vector3.new(0, -speed, 0)
			RunService.Heartbeat:Wait()
		end
		return true
	end
	function commands.jump()
		local humanoid = humanoidOf("self")
		if humanoid then
			humanoid.Jump = true
		end
		return true
	end
	function commands.events(since)
		local out = {}
		for i = (since or 0) + 1, #events do
			table.insert(out, events[i])
		end
		return { list = out, count = #events }
	end
	function commands.errors()
		return logProblems()
	end
	function commands.gui()
		-- Text currently shown by FeedbackClient (feed and callouts).
		local texts = {}
		local pg = player:FindFirstChild("PlayerGui")
		if pg then
			for _, d in pg:GetDescendants() do
				if d:IsA("TextLabel") and d.Visible and d.Text ~= "" then
					table.insert(texts, d.Text)
				end
			end
		end
		return texts
	end
	function commands.boardText()
		local arena = workspace:FindFirstChild("AnimationTestArena")
		local board = arena and arena:FindFirstChild("RecordsBoard")
		local label = board and board:FindFirstChildWhichIsA("TextLabel", true)
		return label and label.Text
	end

	rf.OnClientInvoke = function(name, ...)
		local fn = commands[name]
		if not fn then
			return { error = "unknown command " .. tostring(name) }
		end
		local ok, result = pcall(fn, ...)
		if not ok then
			return { error = tostring(result) }
		end
		return result
	end
	log("client ready", player.Name, "vim", vim ~= nil)
	return
end

---------------------------------------------------------------------------------------------------
-- SERVER: orchestrator
---------------------------------------------------------------------------------------------------
local args = StudioTestService:GetTestArgs()
local mode = (typeof(args) == "table" and args.mode) or marker:GetAttribute("Mode") or "solo"
local expectedPlayers = if mode == "multi" then 2 else 1

local rf = Instance.new("RemoteFunction")
rf.Name = "__AFTestRF"
rf.Parent = ReplicatedStorage

local serverErrors = {}
LogService.MessageOut:Connect(function(message, messageType)
	if messageType == Enum.MessageType.MessageError then
		table.insert(serverErrors, message)
	elseif messageType == Enum.MessageType.MessageWarning and not string.find(message, "%[AFH%]") then
		table.insert(serverErrors, "WARN: " .. message)
	end
end)

local socialProbe = {}
remotes:WaitForChild("Social").OnServerEvent:Connect(function(player, kind, value)
	local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
	local entry = string.format("%s %s=%s rootY=%.1f t=%.2f", player.Name, tostring(kind), tostring(value), root and root.Position.Y or -1, os.clock())
	table.insert(socialProbe, entry)
	log("probe social", entry)
end)

local results = {}
local function record(status, name, detail)
	local entry = { status = status, name = name, detail = detail }
	table.insert(results, entry)
	log(status, name, detail and HttpService:JSONEncode(detail) or "")
end
local function check(name, cond, detail)
	record(if cond then "PASS" else "FAIL", name, detail)
	return cond
end
local function info(name, detail)
	record("INFO", name, detail)
end

local function invoke(player, ...)
	local packed = table.pack(...)
	local done, res = false, nil
	task.spawn(function()
		local ok, r = pcall(function()
			return rf:InvokeClient(player, table.unpack(packed, 1, packed.n))
		end)
		res = if ok then r else { error = tostring(r) }
		done = true
	end)
	local deadline = os.clock() + 25
	while not done and os.clock() < deadline do
		task.wait(0.05)
	end
	if not done then
		return { error = "timeout " .. tostring(packed[1]) }
	end
	return res
end

local function arena()
	return workspace:FindFirstChild("AnimationTestArena")
end
local function dummy()
	local a = arena()
	local model = a and a:FindFirstChild("TrainingDummy")
	return model and model:FindFirstChildOfClass("Humanoid"), model
end
local function hasAnim(list, name)
	if typeof(list) ~= "table" then
		return false
	end
	for _, s in list do
		if typeof(s) == "string" and string.sub(s, 1, #name + 1) == name .. "@" then
			return true
		end
	end
	return false
end
local function waitAnim(player, target, name, timeout)
	local last
	local found = waitFor(function()
		last = invoke(player, "anims", target)
		return hasAnim(last, name)
	end, timeout or 3)
	return found ~= nil, last
end

-- Events seen by a client. Fetched events wait in `pending` until a waitEvent consumes them, so an
-- event that arrives in the same batch as the one being waited for is not lost.
local cursors = {}
local pending = {}
local function fetch(player)
	local r = invoke(player, "events", cursors[player] or 0)
	local list = pending[player] or {}
	pending[player] = list
	if typeof(r) == "table" and r.list ~= nil then
		cursors[player] = r.count
		for _, e in r.list do
			table.insert(list, e)
		end
	end
	return list
end
-- Everything not yet consumed (and clears it): used to start a fresh window.
local function newEvents(player)
	local list = fetch(player)
	pending[player] = {}
	return list
end
local function findEvent(list, pred)
	for _, e in list do
		if pred(e) then
			return e
		end
	end
	return nil
end
-- Collects events until pred matches (or timeout); returns the match and everything seen.
local function waitEvent(player, pred, timeout)
	local seen = {}
	local deadline = os.clock() + (timeout or 3)
	repeat
		local list = fetch(player)
		while #list > 0 do
			local e = table.remove(list, 1)
			table.insert(seen, e)
			if pred(e) then
				return e, seen
			end
		end
		task.wait(0.1)
	until os.clock() > deadline
	return nil, seen
end
local function toastMatching(pattern)
	return function(e)
		return e.kind == "toast" and typeof(e.text) == "string" and string.find(e.text, pattern) ~= nil
	end
end
local function summarize(list)
	local out = {}
	for _, e in list do
		table.insert(out, e.kind .. ":" .. tostring(e.text or e.hitKind or e.name or e.size or ""))
	end
	return out
end

local function rootOf(player)
	local c = player.Character
	return c and c:FindFirstChild("HumanoidRootPart")
end
local function humanoidOf(player)
	local c = player.Character
	return c and c:FindFirstChildOfClass("Humanoid")
end
local function stat(player, name)
	local ls = player:FindFirstChild("leaderstats")
	local v = ls and ls:FindFirstChild(name)
	return v and v.Value
end

local function place(player, position, lookAt)
	return invoke(player, "pivot", CFrame.lookAt(position, Vector3.new(lookAt.X, position.Y, lookAt.Z)))
end

local function waitShieldGone(player)
	return waitFor(function()
		local c = player.Character
		return c and c:FindFirstChildOfClass("ForceField") == nil
	end, 6)
end

local function respawnWait(player)
	return waitFor(function()
		local h = humanoidOf(player)
		return h and h.Health > 0 and rootOf(player)
	end, 15)
end

local function dummyHome()
	local h, model = dummy()
	local root = model and model:FindFirstChild("HumanoidRootPart")
	return h and h.Health > 0 and root and (root.Position - Vector3.new(0, 3, -14)).Magnitude < 3
end

local DUMMY_FRONT = Vector3.new(0, 3, -11)
local DUMMY_POS = Vector3.new(0, 3, -14)

-- Attack the dummy and measure the health change.
local function attackDummy(player, label, action, expected, vimOk)
	waitFor(dummyHome, 8)
	local h, model = dummy()
	if not h then
		check(label, false, { reason = "no dummy" })
		return
	end
	if h.Health < 60 then
		h.Health = h.MaxHealth
	end
	place(player, DUMMY_FRONT, DUMMY_POS)
	task.wait(0.4)
	newEvents(player)
	local before = h.Health
	local rootBefore = model.HumanoidRootPart.Position
	action()
	task.wait(1.6)
	local after = h.Health
	local seen = {}
	for _, e in newEvents(player) do
		table.insert(seen, e)
	end
	local hits = {}
	for _, e in seen do
		if e.kind == "hit" then
			table.insert(hits, (e.hitKind or "?") .. ":" .. tostring(e.amount))
		end
	end
	local moved = (model.HumanoidRootPart.Position - rootBefore).Magnitude
	check(label, math.abs((before - after) - expected) < 0.01 and vimOk, {
		damage = before - after,
		expected = expected,
		hitEvents = hits,
		dummyMoved = math.floor(moved * 10) / 10,
	})
	return moved
end

local function runSolo(p)
	local ping = invoke(p, "ping")
	local vimOk = typeof(ping) == "table" and ping.error == nil
	info("client.input_mode", ping)

	-- Structure ---------------------------------------------------------------------------------
	local kfs = pack:FindFirstChild("KeyframeSequences")
	check("structure.keyframe_sequences", kfs and #kfs:GetChildren() == 27, { count = kfs and #kfs:GetChildren() })
	local remoteNames = {}
	for _, r in remotes:GetChildren() do
		table.insert(remoteNames, r.Name)
	end
	check("structure.remotes", #remoteNames == 6, remoteNames)
	local a = arena()
	local expectedParts = { "ControlsSign", "RecordsBoard", "ClimbTruss", "TrussTop", "ClimbStart", "ClimbBell",
		"PoolZone", "PoolSteps", "Bench", "LaunchLever", "ChallengePad", "TrainingDummy" }
	local missing = {}
	for _, n in expectedParts do
		if not (a and a:FindFirstChild(n)) then
			table.insert(missing, n)
		end
	end
	check("arena.built", a ~= nil and #missing == 0, { missing = missing })
	local dh = dummy()
	check("arena.dummy_health", dh ~= nil and dh.MaxHealth == 150, { max = dh and dh.MaxHealth })
	check("player.leaderstats", stat(p, "KOs") == 0 and stat(p, "High Fives") == 0,
		{ kos = stat(p, "KOs"), fives = stat(p, "High Fives") })
	local h = humanoidOf(p)
	check("player.r15", h ~= nil and h.RigType == Enum.HumanoidRigType.R15, { rig = h and h.RigType.Name })
	check("player.spawn_shield", p.Character:FindFirstChildOfClass("ForceField") ~= nil
		or waitShieldGone(p) ~= nil, nil)

	-- Every clip loads on the client --------------------------------------------------------------
	local loaded = invoke(p, "loadall")
	local bad = {}
	if typeof(loaded) == "table" then
		for _, e in loaded do
			if not e.ok then
				table.insert(bad, e.name .. (e.err and (": " .. e.err) or ""))
			end
		end
	end
	check("clips.all_27_load_on_client", typeof(loaded) == "table" and #loaded == 27 and #bad == 0,
		{ failed = bad, error = typeof(loaded) == "table" and loaded.error or nil })

	-- Animate: idle, run, walk ------------------------------------------------------------------
	place(p, Vector3.new(-30, 3, -30), Vector3.new(-30, 3, -40))
	task.wait(1)
	local okIdle, list = waitAnim(p, "self", "idle", 3)
	check("animate.idle", okIdle, list)
	invoke(p, "move", Vector3.new(0, 0, -1))
	local okRun, runList = waitAnim(p, "self", "run", 3)
	invoke(p, "stop")
	check("animate.run_at_16", okRun, runList)
	task.wait(0.8)
	local okBack = waitAnim(p, "self", "idle", 3)
	check("animate.back_to_idle", okBack, nil)

	-- Jump and fall
	invoke(p, "jump")
	local okJump, jumpList = waitAnim(p, "self", "jump", 2)
	check("animate.jump", okJump, jumpList)
	task.wait(1.5)

	-- Crouch (real C key) -------------------------------------------------------------------------
	invoke(p, "tap", "C")
	local okCrouch, crouchList = waitAnim(p, "self", "crouch_idle", 2)
	local st = invoke(p, "state")
	check("animate.crouch_idle_on_C", okCrouch, { anims = crouchList, walkSpeed = st and st.walkSpeed })
	invoke(p, "move", Vector3.new(1, 0, 0))
	local okCW, cwList = waitAnim(p, "self", "crouch_walk", 3)
	invoke(p, "stop")
	check("animate.crouch_walk", okCW, cwList)
	task.wait(0.5)
	invoke(p, "tap", "C")
	task.wait(0.4)
	st = invoke(p, "state")
	check("animate.uncrouch_restores_speed", st and st.walkSpeed == 16, { walkSpeed = st and st.walkSpeed })

	-- Emotes --------------------------------------------------------------------------------------
	for _, name in { "wave", "dance", "cheer", "point", "laugh", "clap", "salute" } do
		task.wait(0.3)
		local r = invoke(p, "emote", name)
		local ok, l = waitAnim(p, "self", name, 2)
		check("emote." .. name, r == true and ok, { invoke = r, anims = l })
	end
	-- An emote is cancelled by moving.
	invoke(p, "emote", "dance")
	task.wait(0.3)
	invoke(p, "move", Vector3.new(0, 0, 1))
	task.wait(0.8)
	invoke(p, "stop")
	local afterMove = invoke(p, "anims", "self")
	check("emote.cancelled_by_moving", not hasAnim(afterMove, "dance"), afterMove)
	task.wait(0.6)
	-- Chat command path
	local chatR = invoke(p, "chatCommands")
	check("emote.chat_/e_command_registered", typeof(chatR) == "table" and chatR.packCommand == true
		and chatR.builtInDisabled == true, chatR)
	local unknown = invoke(p, "emote", "flex")
	check("emote.unknown_returns_false", unknown == false, { invoke = unknown })
	-- Left hanging
	newEvents(p)
	invoke(p, "emote", "highfive")
	local hang, hangSeen = waitEvent(p, toastMatching("left hanging"), 5)
	check("social.left_hanging", hang ~= nil, summarize(hangSeen))

	-- Combat on the dummy (real clicks and keys) ---------------------------------------------------
	waitShieldGone(p)
	task.wait(1)
	local okDummyIdle, dummyList = waitAnim(p, "dummy", "idle", 3)
	check("dummy.idle_replicated_to_client", okDummyIdle, dummyList)

	attackDummy(p, "combat.punch_dummy_10", function()
		invoke(p, "click")
	end, 10, vimOk)
	task.wait(0.8)
	attackDummy(p, "combat.combo_dummy_30", function()
		-- The second click must land before the punch's Hit marker (0.30 s); later than that, the
		-- punch hit counts too (10 + 30), which is also correct play.
		invoke(p, "click")
		task.wait(0.08)
		invoke(p, "click")
	end, 30, vimOk)
	local okHR = waitAnim(p, "dummy", "hit_react", 0.5)
	info("dummy.hit_react_seen_after_combo", { seen = okHR })
	task.wait(1)
	local kickMoved = attackDummy(p, "combat.kick_dummy_15", function()
		invoke(p, "tap", "Q")
	end, 15, vimOk)
	check("combat.kick_knocks_dummy_back", (kickMoved or 0) > 4, { moved = kickMoved })
	local home = waitFor(dummyHome, 8)
	check("dummy.walks_back_home", home ~= nil, nil)

	-- Block animation (hold F)
	invoke(p, "key", "F", true)
	local okBlock, blockList = waitAnim(p, "self", "block", 2)
	invoke(p, "key", "F", false)
	task.wait(0.5)
	local afterBlock = invoke(p, "anims", "self")
	check("combat.block_hold_F", okBlock and not hasAnim(afterBlock, "block"), { holding = blockList, released = afterBlock })

	-- Sword
	local equipped = invoke(p, "equip", "Sword")
	check("sword.equip", equipped == true, { result = equipped })
	task.wait(0.5)
	local grip = invoke(p, "toolGrip")
	info("sword.grip", grip)
	attackDummy(p, "combat.sword_slash_dummy_22", function()
		invoke(p, "click")
	end, 22, vimOk)
	attackDummy(p, "combat.kick_with_sword_15", function()
		invoke(p, "tap", "Q")
	end, 15, vimOk)
	invoke(p, "unequip")
	task.wait(0.5)

	-- Kill the dummy: feed line, death clip, respawn
	waitFor(dummyHome, 8)
	local dh2, dmodel = dummy()
	if dh2 then
		dh2.Health = 5
	end
	place(p, DUMMY_FRONT, DUMMY_POS)
	task.wait(0.4)
	newEvents(p)
	invoke(p, "click")
	local napE, napSeen = waitEvent(p, toastMatching("Training Dummy into a nap"), 3)
	check("dummy.ko_feed_line", napE ~= nil, summarize(napSeen))
	local okDeath, deathList = waitAnim(p, "dummy", "death", 2)
	check("dummy.death_clip_on_client", okDeath, deathList)
	check("dummy.ko_does_not_count", stat(p, "KOs") == 0, { kos = stat(p, "KOs") })
	local respawned = waitFor(function()
		local nh, nm = dummy()
		return nh and nm ~= dmodel and nh.Health == 150
	end, 8)
	check("dummy.respawns", respawned ~= nil, nil)

	-- Dummy challenge
	task.wait(1)
	place(p, Vector3.new(0, 3, -9), DUMMY_POS)
	task.wait(1.2) -- let ProximityPromptService notice the prompt in range
	newEvents(p)
	local pr = invoke(p, "prompt", "ChallengePad")
	local cd, cdSeen = waitEvent(p, function(e)
		return e.kind == "countdown"
	end, 2)
	check("challenge.starts_with_prompt", cd ~= nil, { prompt = pr, seen = summarize(cdSeen) })
	if cd then
		place(p, DUMMY_FRONT, DUMMY_POS)
		local t0 = os.clock()
		while os.clock() - t0 < 9.3 do
			invoke(p, "click")
			task.wait(0.75)
		end
		local rec, recSeen = waitEvent(p, toastMatching("challenge"), 4)
		check("challenge.result_and_record", rec ~= nil, { toast = rec and rec.text, seen = summarize(recSeen) })
		local dh3 = dummy()
		check("challenge.dummy_alive_after", dh3 ~= nil and dh3.Health > 0, nil)
	end

	-- Heavy landing -------------------------------------------------------------------------------
	place(p, Vector3.new(-40, 40, -40), Vector3.new(-40, 40, -50))
	newEvents(p)
	local okLand, landList = waitAnim(p, "self", "land_heavy", 5)
	local landE, landSeen = waitEvent(p, function(e)
		return e.kind == "landing"
	end, 2)
	check("landing.superhero_clip", okLand, landList)
	check("landing.server_dust_event", landE ~= nil, { height = landE and landE.height, seen = summarize(landSeen) })
	info("landing.fall_clip_seen", { note = "checked indirectly" })
	task.wait(1)

	-- Pool: splash and swim -----------------------------------------------------------------------
	place(p, Vector3.new(0, 34, 40), Vector3.new(0, 34, 50))
	newEvents(p)
	local splashE, splashSeen = waitEvent(p, function(e)
		return e.kind == "splash"
	end, 5)
	check("pool.splash_event", splashE ~= nil, { size = splashE and splashE.size, seen = summarize(splashSeen) })
	local recE = findEvent(splashSeen, toastMatching("splash")) or waitEvent(p, toastMatching("splash"), 2)
	check("pool.splash_record", recE ~= nil, { toast = recE and recE.text })
	local okSwim, swimList = waitAnim(p, "self", "swim", 3)
	if not okSwim then
		okSwim, swimList = waitAnim(p, "self", "swim_idle", 2)
	end
	check("pool.swim_clip", okSwim, swimList)
	info("pool.client_water_probe", invoke(p, "water"))
	info("pool.position", invoke(p, "state"))
	invoke(p, "move", Vector3.new(0, 0, 1))
	local okSwimMove, swimMoveList = waitAnim(p, "self", "swim", 3)
	invoke(p, "stop")
	check("pool.swim_moving", okSwimMove, swimMoveList)
	task.wait(0.5)

	-- A hard dive reaches the pool floor before swimming starts: it must still be a splash.
	local diveResults = {}
	local diveOk = true
	for i = 1, 3 do
		task.wait(1.2)
		newEvents(p)
		invoke(p, "dive", CFrame.new(-4 + i * 2, 30, 44), 140)
		local diveSplash, diveSeen = waitEvent(p, function(e)
			return e.kind == "splash" or e.kind == "landing"
		end, 4)
		table.insert(diveResults, summarize(diveSeen))
		if not (diveSplash and diveSplash.kind == "splash") then
			diveOk = false
		end
	end
	check("pool.hard_dive_is_a_splash_not_a_landing", diveOk, diveResults)
	task.wait(0.5)

	-- Climb race ------------------------------------------------------------------------------------
	place(p, Vector3.new(24, 3, -4), Vector3.new(24, 3, 0))
	task.wait(0.6)
	newEvents(p)
	invoke(p, "move", Vector3.new(0, 0, 1))
	local okClimb, climbList = waitAnim(p, "self", "climb", 4)
	check("climb.clip", okClimb, climbList)
	local top = waitFor(function()
		local r = rootOf(p)
		return r and r.Position.Y > 25
	end, 12)
	check("climb.reaches_top", top ~= nil, { y = rootOf(p) and math.floor(rootOf(p).Position.Y) })
	local climbRec, climbSeen = waitEvent(p, toastMatching("climb"), 6)
	invoke(p, "stop")
	check("climb.race_time_recorded", climbRec ~= nil and string.find(climbRec.text, "RECORD") ~= nil,
		{ toast = climbRec and climbRec.text, seen = summarize(climbSeen) })
	-- Jump off the tower: heavy landing from a real fall.
	invoke(p, "move", Vector3.new(1, 0, 0))
	task.wait(0.6)
	invoke(p, "stop")
	local okTowerLand = waitAnim(p, "self", "land_heavy", 5)
	check("climb.jump_off_tower_heavy_landing", okTowerLand, invoke(p, "state"))
	task.wait(1)

	-- Launch bench ----------------------------------------------------------------------------------
	local seat = arena():FindFirstChild("Bench")
	place(p, seat.Position + seat.CFrame.LookVector * 2 + Vector3.new(0, 2, 0), seat.Position)
	task.wait(0.4)
	seat:Sit(humanoidOf(p))
	local okSit, sitList = waitAnim(p, "self", "sit", 3)
	check("bench.sit_clip", okSit, sitList)
	newEvents(p)
	local leverR = invoke(p, "prompt", "LaunchLever")
	local launchE, launchSeen = waitEvent(p, function(e)
		return e.kind == "launch"
	end, 3)
	check("bench.lever_launches", launchE ~= nil, { prompt = leverR, seen = summarize(launchSeen) })
	local selfFeed = findEvent(launchSeen, toastMatching("launched themselves"))
		or waitEvent(p, toastMatching("launched themselves"), 2)
	check("bench.feed_line", selfFeed ~= nil, nil)
	local benchSplash, benchSeen = waitEvent(p, function(e)
		return e.kind == "splash"
	end, 5)
	local r = rootOf(p)
	check("bench.lands_in_pool_with_splash", benchSplash ~= nil,
		{ size = benchSplash and benchSplash.size, pos = r and { math.floor(r.Position.X), math.floor(r.Position.Y), math.floor(r.Position.Z) }, seen = summarize(benchSeen) })

	-- Records board
	local board = invoke(p, "boardText")
	check("board.shows_records", typeof(board) == "string" and string.find(board, "splash") ~= nil, { text = board })

	-- Death of the player: death clip, fell / nap feed
	task.wait(1)
	place(p, Vector3.new(-30, 3, -30), Vector3.new(-30, 3, -40))
	task.wait(0.5)
	newEvents(p)
	humanoidOf(p).Health = 0
	local okPDeath, pDeathList = waitAnim(p, "self", "death", 2)
	check("player.death_clip", okPDeath, pDeathList)
	local napSelf, napSelfSeen = waitEvent(p, toastMatching("took a nap"), 3)
	check("player.death_feed", napSelf ~= nil, summarize(napSelfSeen))
	check("player.respawns", respawnWait(p) ~= nil, nil)
end

-- Two players ------------------------------------------------------------------------------------
local function runMulti(a, b)
	local pa, pb = invoke(a, "ping"), invoke(b, "ping")
	check("multi.both_clients_ready", typeof(pa) == "table" and typeof(pb) == "table" and pa.error == nil and pb.error == nil, { a = pa, b = pb })

	-- Spawn shield message
	local A0 = Vector3.new(-30, 3, -30)
	local B0 = Vector3.new(-30, 3, -33)
	local shielded = rootOf(b) and b.Character:FindFirstChildOfClass("ForceField")
	if shielded then
		place(b, B0, A0)
		place(a, A0, B0)
		task.wait(0.3)
		newEvents(a)
		invoke(a, "click")
		local sh, shSeen = waitEvent(a, function(e)
			return e.kind == "hit" and e.hitKind == "shielded"
		end, 2)
		check("multi.spawn_shield_says_shielded", sh ~= nil, summarize(shSeen))
	else
		info("multi.spawn_shield_says_shielded", { skipped = "shield already gone" })
	end
	waitShieldGone(a)
	waitShieldGone(b)
	task.wait(1)

	local function reset()
		for _, p in { a, b } do
			local h = humanoidOf(p)
			if h and h.Health > 0 then
				h.Health = h.MaxHealth
			end
		end
		place(b, B0, A0)
		place(a, A0, B0)
		task.wait(0.5)
	end

	local function attackB(label, action, expected, kind)
		reset()
		local hb = humanoidOf(b)
		local before = hb.Health
		newEvents(a)
		action()
		local e, seen = waitEvent(a, function(ev)
			return ev.kind == "hit" and ev.hitKind == kind
		end, 2.5)
		task.wait(0.3)
		local dmg = before - hb.Health
		check(label, e ~= nil and math.abs(dmg - expected) < 0.01, { damage = dmg, expected = expected, seen = summarize(seen) })
	end

	attackB("multi.punch_player_10", function()
		invoke(a, "click")
	end, 10, "normal")
	local okHR, hrList = waitAnim(b, "self", "hit_react", 1)
	check("multi.victim_hit_react", okHR, hrList)

	-- Block: hold F well before the hit.
	attackB("multi.blocked_2", function()
		invoke(b, "key", "F", true)
		task.wait(1.3)
		invoke(a, "click")
	end, 2, "blocked")
	invoke(b, "key", "F", false)
	task.wait(1.2)

	-- Parry: raise the guard just before the punch's Hit marker.
	local AnimationMeta = require(pack:WaitForChild("AnimationMeta"))
	local hitTime = 0.25
	for _, m in AnimationMeta.punch.markers do
		if m.name == "Hit" then
			hitTime = m.time
		end
	end
	attackB("multi.parry_0", function()
		task.spawn(function()
			task.wait(math.max(hitTime - 0.15, 0))
			invoke(b, "key", "F", true)
		end)
		invoke(a, "click")
	end, 0, "parry")
	local okStagger, staggerList = waitAnim(a, "self", "hit_react", 1)
	check("multi.parry_staggers_attacker", okStagger, staggerList)
	task.wait(0.3)
	invoke(b, "key", "F", false)
	task.wait(1.2)

	-- Guard break: combo finisher through the block.
	reset()
	invoke(b, "key", "F", true)
	task.wait(1.2)
	newEvents(a)
	local hb = humanoidOf(b)
	local before = hb.Health
	invoke(a, "click")
	task.wait(0.2)
	invoke(a, "click")
	local gb, gbSeen = waitEvent(a, function(e)
		return e.kind == "hit" and e.hitKind == "guardbreak"
	end, 3)
	check("multi.combo_guard_break", gb ~= nil, { damage = before - hb.Health, seen = summarize(gbSeen) })
	invoke(b, "key", "F", false)
	task.wait(1.5)

	-- Sneak attack: crouched, from behind.
	reset()
	invoke(a, "tap", "C")
	task.wait(0.4)
	-- B faces away from A.
	place(b, B0, B0 + (B0 - A0))
	task.wait(0.3)
	attackB("multi.sneak_attack_20", function()
		place(b, B0, B0 + (B0 - A0))
		task.wait(0.3)
		invoke(a, "click")
	end, 20, "sneak")
	invoke(a, "tap", "C")
	task.wait(0.5)

	-- KOs, taunt, set win
	local okSet = false
	for i = 1, 5 do
		respawnWait(b)
		waitShieldGone(b)
		reset()
		humanoidOf(b).Health = 5
		newEvents(a)
		invoke(a, "click")
		local ko, koSeen = waitEvent(a, toastMatching("into a nap"), 3)
		check("multi.ko_" .. i, ko ~= nil and stat(a, "KOs") == i, { kos = stat(a, "KOs"), seen = summarize(koSeen) })
		if i == 1 then
			local okBDeath, bDeathList = waitAnim(b, "self", "death", 2)
			check("multi.victim_death_clip", okBDeath, bDeathList)
			task.wait(0.5)
			invoke(a, "emote", "laugh")
			local taunt, tauntSeen = waitEvent(a, toastMatching("laughed at"), 3)
			check("multi.taunt_after_ko", taunt ~= nil, summarize(tauntSeen))
		end
		if i == 5 then
			local win = findEvent(koSeen, toastMatching("WINS THE SET")) or waitEvent(a, toastMatching("WINS THE SET"), 3)
			okSet = win ~= nil
			check("multi.set_win_callout", okSet, summarize(koSeen))
			local okCheer = waitAnim(a, "self", "cheer", 2)
			check("multi.winner_cheers", okCheer, nil)
		end
	end

	-- Animation replication between clients (expected to need published IDs)
	respawnWait(b)
	waitShieldGone(b)
	reset()
	invoke(a, "emote", "dance")
	task.wait(0.6)
	local seenFromB = invoke(b, "anims", a.Name)
	info("multi.a_dance_visible_on_b_client", { tracksOnB = seenFromB, note = "unpublished clips use temporary IDs; see GUIA 7.1" })

	-- High five
	task.wait(1)
	reset()
	newEvents(a)
	invoke(a, "emote", "highfive")
	task.wait(0.5)
	invoke(b, "emote", "highfive")
	local hf, hfSeen = waitEvent(a, toastMatching("high%-fived"), 3)
	check("multi.high_five_feed", hf ~= nil, summarize(hfSeen))
	check("multi.high_five_stats", stat(a, "High Fives") == 1 and stat(b, "High Fives") == 1,
		{ a = stat(a, "High Fives"), b = stat(b, "High Fives") })
	local okHFa = waitAnim(a, "self", "high_five", 1.5)
	check("multi.high_five_clip", okHFa, nil)
	task.wait(2)

	-- Dance party
	reset()
	newEvents(a)
	invoke(a, "emote", "dance")
	task.wait(0.4)
	invoke(b, "emote", "dance")
	local party, partySeen = waitEvent(a, toastMatching("Dance party"), 3)
	check("multi.dance_party", party ~= nil, summarize(partySeen))
	task.wait(1)

	-- Bench: B sits, A pulls the lever.
	local seat = arena():FindFirstChild("Bench")
	place(b, seat.Position + seat.CFrame.LookVector * 2 + Vector3.new(0, 2, 0), seat.Position)
	place(a, seat.Position + seat.CFrame.RightVector * 4 + Vector3.new(0, 2, 0), seat.Position)
	task.wait(0.4)
	seat:Sit(humanoidOf(b))
	task.wait(0.6)
	newEvents(a)
	invoke(a, "prompt", "LaunchLever")
	local launched, lSeen = waitEvent(a, toastMatching("launched " .. b.DisplayName), 3)
	check("multi.friend_launches_friend", launched ~= nil, summarize(lSeen))
	task.wait(3)

	-- Dunk: kick B off a ledge into the pool.
	local ledge = Instance.new("Part")
	ledge.Anchored = true
	ledge.Size = Vector3.new(10, 1, 8)
	ledge.CFrame = CFrame.new(0, 8.5, 19)
	ledge.Name = "AFHTestLedge"
	ledge.Parent = workspace
	respawnWait(b)
	local hbb = humanoidOf(b)
	hbb.Health = hbb.MaxHealth
	place(b, Vector3.new(0, 12, 21.5), Vector3.new(0, 12, 40))
	place(a, Vector3.new(0, 12, 18.5), Vector3.new(0, 12, 40))
	task.wait(0.8)
	newEvents(a)
	invoke(a, "tap", "Q")
	local dunk, dunkSeen = waitEvent(a, toastMatching("dunked"), 5)
	check("multi.kick_into_pool_is_a_dunk", dunk ~= nil, summarize(dunkSeen))
	ledge:Destroy()

	local board = invoke(a, "boardText")
	check("multi.board_shows_rivalry", typeof(board) == "string" and string.find(board, a.DisplayName) ~= nil, { text = board })
end

task.spawn(function()
	local ok, err = pcall(function()
		local ready = waitFor(function()
			if #Players:GetPlayers() < expectedPlayers then
				return false
			end
			for _, p in Players:GetPlayers() do
				local r = invoke(p, "ping")
				if typeof(r) ~= "table" or r.error then
					return false
				end
				if not (p.Character and rootOf(p)) then
					return false
				end
			end
			return true
		end, 90)
		if not ready then
			record("FAIL", "setup.players_ready", { players = #Players:GetPlayers() })
			return
		end
		task.wait(2)
		local list = Players:GetPlayers()
		if mode == "multi" then
			runMulti(list[1], list[2])
		else
			runSolo(list[1])
		end
	end)
	if not ok then
		record("FAIL", "harness.crashed", { error = tostring(err) })
	end
	-- Errors and warnings from game scripts (server and clients).
	for _, p in Players:GetPlayers() do
		local problems = invoke(p, "errors")
		local errs = typeof(problems) == "table" and problems.errors
		check("client_script_errors." .. p.Name, typeof(errs) == "table" and #errs == 0, problems)
	end
	local serverProblems = logProblems()
	check("server_script_errors", #serverProblems.errors == 0, serverProblems)
	info("social_reports_received", socialProbe)
	local pass, fail = 0, 0
	for _, r in results do
		if r.status == "PASS" then
			pass += 1
		elseif r.status == "FAIL" then
			fail += 1
		end
	end
	log("SUMMARY", mode, "pass", pass, "fail", fail)
	local report = HttpService:JSONEncode({ mode = mode, pass = pass, fail = fail, results = results })
	task.wait(0.5)
	StudioTestService:EndTest(report)
end)
