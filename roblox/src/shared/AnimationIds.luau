--!strict
-- Published animation asset IDs, one per clip. 0 = not published yet.
--
-- To publish: open the clip's KeyframeSequence (ReplicatedStorage.AnimationPack.KeyframeSequences)
-- in the Animation Editor on an R15 rig, choose Publish to Roblox, and paste the number here.
-- Until a clip is published, Studio play-tests load it straight from its KeyframeSequence
-- (see AnimationLoader). Live servers need the published IDs.

local AnimationIds: { [string]: number } = {
	-- locomotion
	idle = 0,
	walk = 0,
	run = 0,
	jump = 0,
	fall = 0,
	climb = 0,
	swim = 0,
	swim_idle = 0,
	sit = 0,
	crouch_idle = 0,
	crouch_walk = 0,
	-- combat
	punch = 0,
	combo = 0,
	kick = 0,
	sword_slash = 0,
	block = 0,
	hit_react = 0,
	death = 0,
	-- emotes
	wave = 0,
	dance = 0,
	cheer = 0,
	point = 0,
	laugh = 0,
	clap = 0,
	salute = 0,
	-- social / juice
	high_five = 0,
	land_heavy = 0,
}

return AnimationIds
