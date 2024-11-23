-- luacheck: read globals unified_inventory

if not stairsplus.has.unified_inventory then
	return
end

local S = stairsplus.S

local in_creative_inventory = stairsplus.settings.in_creative_inventory

local api = stairsplus.api

unified_inventory.register_craft_type("stairsplus:circular_saw", {
	description = S("Stairs+ circular saw"),
	icon = "stairsplus_saw_button.png",
	width = 1,
	height = 1,
	uses_crafting_grid = false,
})

unified_inventory.register_category("stairsplus:cuttable", {
	symbol = "stairsplus:circular_saw",
	label = S("Cuttable in the circular saw"),
	index = 0,
	items = {},
})

if in_creative_inventory then
	unified_inventory.register_category("stairsplus:cut_node", {
		symbol = "stairsplus:circular_saw",
		label = S("Nodes cut in the circular saw"),
		index = 0,
		items = {},
	})
end

local function on_register_single(node, shaped_name)
	unified_inventory.register_craft({
		output = shaped_name,
		type = "stairsplus:circular_saw",
		items = { node },
		width = 1,
	})

	unified_inventory.add_category_item("stairsplus:cuttable", node)
	if in_creative_inventory then
		unified_inventory.add_category_item("stairsplus:cut_node", shaped_name)
	end
end

for _, single in ipairs(api.registered_singles) do
	local node, shaped_name = unpack(single)
	on_register_single(node, shaped_name)
end

api.register_on_register_single(on_register_single)
