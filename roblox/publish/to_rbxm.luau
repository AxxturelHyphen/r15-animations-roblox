-- Converts every output/rbxmx/<clip>.rbxmx KeyframeSequence into a binary .rbxm (what the Open Cloud
-- Assets API accepts for animations), re-serialized by Lune's Roblox library so the file is well formed.
--   lune run roblox/publish/to_rbxm.luau <out_dir>
local fs = require("@lune/fs")
local process = require("@lune/process")
local roblox = require("@lune/roblox")

local outDir = process.args[1] or "build/rbxm"
fs.writeDir(outDir)
local count = 0
for _, name in fs.readDir("output/rbxmx") do
	if string.sub(name, -6) == ".rbxmx" then
		local instances = roblox.deserializeModel(fs.readFile("output/rbxmx/" .. name))
		assert(#instances == 1 and instances[1].ClassName == "KeyframeSequence", name .. ": expected one KeyframeSequence")
		local clip = string.sub(name, 1, -7)
		fs.writeFile(outDir .. "/" .. clip .. ".rbxm", roblox.serializeModel(instances))
		count += 1
	end
end
print(`converted {count} clips to {outDir}`)
