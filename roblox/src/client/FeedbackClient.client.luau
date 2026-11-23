--!strict
-- Renders server-decided feedback (Remotes.Feedback) on this client:
--   "hit"       contact flash, sound, floating damage number or BLOCKED / PARRY! / SNEAK ATTACK x2,
--               hit-stop and a small camera shake when you are the attacker or the victim
--   "knockback" / "launch"  a velocity held for a moment on your own character (you own its physics)
--   "splash"    a splash sized by fall height;  "landing"  a heavy-landing thud and dust
--   "burst"     a high-five clap flash;  "sound"  a positioned sound;  "toast"  kill feed and records
--   "countdown" the dummy challenge timer
-- Effects are functional only (contact points, splashes, dust), per the project's no-decorative-FX rule.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")

local pack = ReplicatedStorage:WaitForChild("AnimationPack")
local Feedback = require(pack:WaitForChild("Feedback"))
local feedbackRemote = pack:WaitForChild("Remotes"):WaitForChild("Feedback") :: RemoteEvent

local player = Players.LocalPlayer

-- Screen UI: kill feed (top right), callouts (centre), countdown -------------------------------
local gui = Instance.new("ScreenGui")
gui.Name = "ArenaFeedback"
gui.ResetOnSpawn = false
gui.IgnoreGuiInset = false
gui.Parent = player:WaitForChild("PlayerGui")

local feedFrame = Instance.new("Frame")
feedFrame.BackgroundTransparency = 1
feedFrame.AnchorPoint = Vector2.new(1, 0)
feedFrame.Position = UDim2.new(1, -16, 0, 60)
feedFrame.Size = UDim2.new(0, 420, 0, 220)
feedFrame.Parent = gui
local feedLayout = Instance.new("UIListLayout")
feedLayout.HorizontalAlignment = Enum.HorizontalAlignment.Right
feedLayout.SortOrder = Enum.SortOrder.LayoutOrder
feedLayout.Padding = UDim.new(0, 4)
feedLayout.Parent = feedFrame

local feedOrder = 0
local function feedLine(text: string)
	feedOrder += 1
	local label = Instance.new("TextLabel")
	label.LayoutOrder = feedOrder
	label.AutomaticSize = Enum.AutomaticSize.X
	label.Size = UDim2.new(0, 0, 0, 26)
	label.BackgroundColor3 = Color3.fromRGB(20, 22, 28)
	label.BackgroundTransparency = 0.25
	label.TextColor3 = Feedback.Colors.feed
	label.Font = Enum.Font.GothamBold
	label.TextSize = 18
	label.Text = "  " .. text .. "  "
	local corner = Instance.new("UICorner")
	corner.CornerRadius = UDim.new(0, 6)
	corner.Parent = label
	label.Parent = feedFrame
	local children = {}
	for _, c in feedFrame:GetChildren() do
		if c:IsA("TextLabel") then
			table.insert(children, c)
		end
	end
	if #children > 6 then
		table.sort(children, function(a, b)
			return a.LayoutOrder < b.LayoutOrder
		end)
		children[1]:Destroy()
	end
	task.delay(8, function()
		if label.Parent then
			TweenService:Create(label, TweenInfo.new(0.4), { TextTransparency = 1, BackgroundTransparency = 1 }):Play()
			task.delay(0.45, function()
				label:Destroy()
			end)
		end
	end)
end

local centre = Instance.new("TextLabel")
centre.AnchorPoint = Vector2.new(0.5, 0)
centre.Position = UDim2.new(0.5, 0, 0.18, 0)
centre.Size = UDim2.new(0.8, 0, 0, 44)
centre.BackgroundTransparency = 1
centre.Font = Enum.Font.GothamBlack
centre.TextSize = 30
centre.TextStrokeTransparency = 0.4
centre.TextColor3 = Feedback.Colors.record
centre.TextTransparency = 1
centre.Text = ""
centre.Parent = gui

local centreToken = 0
local function callout(text: string, color: Color3?)
	centreToken += 1
	local token = centreToken
	centre.Text = text
	centre.TextColor3 = color or Feedback.Colors.record
	centre.TextTransparency = 0
	centre.TextStrokeTransparency = 0.4
	task.delay(2.6, function()
		if token == centreToken then
			TweenService:Create(centre, TweenInfo.new(0.5), { TextTransparency = 1, TextStrokeTransparency = 1 }):Play()
		end
	end)
end

-- World effects --------------------------------------------------------------------------------
local function flash(position: Vector3, color: Color3, size: number)
	local part = Instance.new("Part")
	part.Shape = Enum.PartType.Ball
	part.Anchored = true
	part.CanCollide = false
	part.CanQuery = false
	part.CanTouch = false
	part.CastShadow = false
	part.Material = Enum.Material.Neon
	part.Color = color
	part.Size = Vector3.one * size * 0.4
	part.CFrame = CFrame.new(position)
	part.Parent = workspace
	TweenService:Create(part, TweenInfo.new(0.12, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
		Size = Vector3.one * size,
		Transparency = 1,
	}):Play()
	task.delay(0.15, function()
		part:Destroy()
	end)
end

local function floatingText(position: Vector3, text: string, color: Color3, big: boolean)
	local anchor = Instance.new("Part")
	anchor.Anchored = true
	anchor.CanCollide = false
	anchor.CanQuery = false
	anchor.CanTouch = false
	anchor.Transparency = 1
	anchor.Size = Vector3.new(0.2, 0.2, 0.2)
	anchor.CFrame = CFrame.new(position + Vector3.new(math.random() - 0.5, 1.5, math.random() - 0.5))
	anchor.Parent = workspace
	local billboard = Instance.new("BillboardGui")
	billboard.Size = UDim2.new(0, 220, 0, 60)
	billboard.AlwaysOnTop = true
	billboard.MaxDistance = 90
	billboard.Parent = anchor
	local label = Instance.new("TextLabel")
	label.Size = UDim2.fromScale(1, 1)
	label.BackgroundTransparency = 1
	label.Font = Enum.Font.GothamBlack
	label.TextScaled = false
	label.TextSize = if big then 34 else 24
	label.TextColor3 = color
	label.TextStrokeTransparency = 0.2
	label.Text = text
	label.Parent = billboard
	TweenService:Create(anchor, TweenInfo.new(0.8, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
		CFrame = anchor.CFrame + Vector3.new(0, 3, 0),
	}):Play()
	TweenService:Create(label, TweenInfo.new(0.8, Enum.EasingStyle.Quad, Enum.EasingDirection.In), {
		TextTransparency = 1,
		TextStrokeTransparency = 1,
	}):Play()
	task.delay(0.85, function()
		anchor:Destroy()
	end)
end

local function particleBurst(position: Vector3, color: Color3, count: number, speed: number, size: number)
	local part = Instance.new("Part")
	part.Anchored = true
	part.CanCollide = false
	part.CanQuery = false
	part.CanTouch = false
	part.Transparency = 1
	part.Size = Vector3.new(1, 1, 1)
	part.CFrame = CFrame.new(position)
	part.Parent = workspace
	local emitter = Instance.new("ParticleEmitter")
	emitter.Color = ColorSequence.new(color)
	emitter.Size = NumberSequence.new({ NumberSequenceKeypoint.new(0, size), NumberSequenceKeypoint.new(1, size * 0.3) })
	emitter.Transparency = NumberSequence.new({ NumberSequenceKeypoint.new(0, 0.1), NumberSequenceKeypoint.new(1, 1) })
	emitter.Lifetime = NumberRange.new(0.5, 0.9)
	emitter.Speed = NumberRange.new(speed * 0.6, speed)
	emitter.SpreadAngle = Vector2.new(35, 35)
	emitter.EmissionDirection = Enum.NormalId.Top
	emitter.Acceleration = Vector3.new(0, -workspace.Gravity * 0.25, 0)
	emitter.Rate = 0
	emitter.Parent = part
	emitter:Emit(count)
	task.delay(1.2, function()
		part:Destroy()
	end)
end

-- Hit-stop and camera shake --------------------------------------------------------------------
-- Reference-counted per track, so overlapping hit-stops (one swing hitting two targets, fast hits)
-- never save a speed of 0 and leave a clip frozen.
local frozenCount: { [AnimationTrack]: number } = {}
local frozenSpeed: { [AnimationTrack]: number } = {}
local stoppedThisFrame: { [Instance]: boolean } = {}

local function hitStop(model: Instance?, seconds: number)
	if model == nil or stoppedThisFrame[model] then
		return
	end
	stoppedThisFrame[model] = true
	task.defer(function()
		stoppedThisFrame[model] = nil
	end)
	local humanoid = model:FindFirstChildOfClass("Humanoid")
	local animator = humanoid and humanoid:FindFirstChildOfClass("Animator")
	if animator == nil then
		return
	end
	local tracks = animator:GetPlayingAnimationTracks()
	for _, track in tracks do
		local count = frozenCount[track] or 0
		if count == 0 then
			frozenSpeed[track] = track.Speed
			track:AdjustSpeed(0)
		end
		frozenCount[track] = count + 1
	end
	task.delay(seconds, function()
		for _, track in tracks do
			local count = (frozenCount[track] or 1) - 1
			if count <= 0 then
				frozenCount[track] = nil
				local speed = frozenSpeed[track]
				frozenSpeed[track] = nil
				if track.IsPlaying and speed then
					track:AdjustSpeed(speed)
				end
			else
				frozenCount[track] = count
			end
		end
	end)
end

-- Camera shake through Humanoid.CameraOffset: the camera never accumulates drift.
local shakeUntil, shakeStrength = 0, 0
local function shake(strength: number, seconds: number)
	shakeStrength = math.max(shakeStrength, strength)
	shakeUntil = math.max(shakeUntil, os.clock() + seconds)
end
RunService.RenderStepped:Connect(function()
	local character = player.Character
	local humanoid = character and character:FindFirstChildOfClass("Humanoid")
	if humanoid == nil then
		return
	end
	local now = os.clock()
	if now >= shakeUntil then
		if shakeStrength ~= 0 then
			shakeStrength = 0
			humanoid.CameraOffset = Vector3.zero
		end
		return
	end
	local s = shakeStrength * 0.12 * ((shakeUntil - now) / 0.25)
	humanoid.CameraOffset = Vector3.new((math.random() - 0.5) * s, (math.random() - 0.5) * s, 0)
end)

-- Velocity on your own character (knockback, bench launch) --------------------------------------
local velocityToken = 0
local function holdVelocity(velocity: Vector3, duration: number)
	velocityToken += 1
	local token = velocityToken -- a newer push (knockback during a launch) cancels the older one
	local character = player.Character
	local root = character and character:FindFirstChild("HumanoidRootPart")
	local humanoid = character and character:FindFirstChildOfClass("Humanoid")
	if root == nil or not root:IsA("BasePart") or humanoid == nil then
		return
	end
	humanoid:ChangeState(Enum.HumanoidStateType.Freefall)
	local started = os.clock()
	local connection: RBXScriptConnection
	connection = RunService.Heartbeat:Connect(function()
		local t = os.clock() - started
		local state = humanoid:GetState()
		if token ~= velocityToken or t > duration or not root.Parent or humanoid.Health <= 0
			or (t > 0.15 and (state == Enum.HumanoidStateType.Swimming or state == Enum.HumanoidStateType.Landed)) then
			connection:Disconnect()
			return
		end
		root.AssemblyLinearVelocity = velocity - Vector3.new(0, workspace.Gravity * t, 0)
	end)
end

-- Events ---------------------------------------------------------------------------------------
local CALLOUT_TEXT: { [string]: string } = { blocked = "BLOCKED", parry = "PARRY!", sneak = "SNEAK ATTACK x2", guardbreak = "GUARD BREAK!" }

feedbackRemote.OnClientEvent:Connect(function(kind: string, data: any)
	if kind == "hit" then
		local position = data.position :: Vector3
		local hitKind = data.kind :: string
		local color = Feedback.Colors[hitKind] or Feedback.Colors.normal
		local involved = data.attacker == player.Character or data.victim == player.Character
		if hitKind == "shielded" then
			flash(position, color, 2)
			floatingText(position, "SHIELDED", color, false)
			if involved then
				callout(if data.victim == player.Character then "SPAWN SHIELD (3 s)" else "They just spawned: shielded", color)
			end
			return
		elseif hitKind == "blocked" then
			Feedback.playSound("block", position)
			flash(position, color, 2.2)
			floatingText(position, "BLOCKED", color, false)
		elseif hitKind == "parry" then
			Feedback.playSound("parry", position)
			flash(position, color, 3.2)
			floatingText(position, "PARRY!", color, true)
			hitStop(data.attacker, 0.12)
			hitStop(data.victim, 0.12)
		else
			Feedback.playSound(if hitKind == "normal" then "hit" else "heavyHit", position)
			flash(position, color, if hitKind == "normal" then 1.8 else 2.8)
			local label = if hitKind == "sneak" then `{data.amount}  SNEAK ATTACK!`
				elseif hitKind == "guardbreak" then `{data.amount}  GUARD BREAK!`
				else tostring(data.amount)
			floatingText(position, label, color, hitKind ~= "normal")
			local stop = if hitKind == "normal" then 0.05 else 0.09
			hitStop(data.attacker, stop)
			hitStop(data.victim, stop)
		end
		if involved then
			shake(if hitKind == "normal" or hitKind == "blocked" then 0.6 else 1.4, 0.2)
			local text = CALLOUT_TEXT[hitKind]
			if text then
				callout(text, color)
			end
		end
	elseif kind == "knockback" then
		holdVelocity(data.velocity :: Vector3, 0.35)
	elseif kind == "launch" then
		holdVelocity(data.velocity :: Vector3, (data.duration :: number) + 0.6)
	elseif kind == "splash" then
		local raw = data.size :: number
		if raw ~= raw then
			return -- NaN guard
		end
		local size = math.clamp(raw / 10, 0.6, 5)
		Feedback.playSound("splash", data.position)
		particleBurst((data.position :: Vector3) + Vector3.new(0, 1, 0), Color3.fromRGB(190, 225, 255), math.floor(20 * size), 18 * size, 1.2)
		if size >= 2 then
			floatingText(data.position, `SPLASH {math.floor(data.size)}!`, Color3.fromRGB(150, 210, 255), true)
		end
	elseif kind == "landing" then
		Feedback.playSound("land", data.position)
		particleBurst(data.position :: Vector3, Color3.fromRGB(170, 170, 160), 24, 14, 1.6)
		local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
		if root and root:IsA("BasePart") and (root.Position - (data.position :: Vector3)).Magnitude < 30 then
			shake(1.6, 0.25)
		end
	elseif kind == "burst" then
		flash(data.position :: Vector3, Color3.fromRGB(255, 240, 160), 3)
	elseif kind == "sound" then
		Feedback.playSound(data.name :: string, data.position)
	elseif kind == "toast" then
		if data.style == "feed" then
			feedLine(data.text :: string)
		else
			callout(data.text :: string, Feedback.Colors.record)
		end
	elseif kind == "countdown" then
		local seconds = data.seconds :: number
		task.spawn(function()
			for i = seconds, 1, -1 do
				callout(if i == seconds then `GO! {i}` else tostring(i), Feedback.Colors.heavy)
				task.wait(1)
			end
			callout("TIME!", Feedback.Colors.record)
		end)
	end
end)
