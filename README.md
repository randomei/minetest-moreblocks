# moreblocks and stairsplus

more blocks for [minetest](https://www.minetest.net/), a free and open source infinite
world block sandbox game.

![Screenshot](https://github.com/fluxionary/minetest-moreblocks/raw/bugfixes/screenshot.png)

stairsplus adds a large variety of new shapes for registered nodes:

![Screenshot](https://github.com/fluxionary/minetest-moreblocks/raw/bugfixes/screenshot2.png)

![Screenshot](https://github.com/fluxionary/minetest-moreblocks/raw/bugfixes/screenshot3.png)

this is a fork of the version maintained by the minetest-mods group at https://github.com/minetest-mods/moreblocks.
it provides numerous new features and bugfixes and is designed to reduce the number of registered nodes, to avoid
the node ID limit.

# mods in the pack

## moreblocks

defines a bunch of new kinds of nodes. provides an API for creating variants of some nodes.

## moreblocks_legacy_recipes

provided to keep compatibility w/ recipe changes from older versions of moreblocks. disabled by default.

## stairsplus

allows the creation of 49 new shapes for registered nodes. provides an API for registering new shapes.

## stairsplus_legacy

stairsplus registrations for various mods which were formerly done automatically as part of moreblocks.

## stairs

overrides the stairs mod from minetest_game to use stairsplus behind the scenes, to avoid duplication of nodes.

## invsaw

adds a button in unified_inventory that allows you to use the circular saw interface if you are
playing creatively, or have a circular saw item in your inventory and have the right priv
(`interact`, by default).

invsaw was taken from [cheapie's invsaw mod](https://forum.minetest.net/viewtopic.php?t=14736), which
itself borrowed heavily from an older version of this mod. Flux decided to just add it here because it
needed to be fully rewritten to be compatible w/ their modifications to the stairsplus API.

# documentation

## for players

use of a decent inventory manager (e.g.
[unified_inventory](https://content.minetest.net/packages/RealBadAngel/unified_inventory/) or
[i3](https://content.minetest.net/packages/jp/i3/)) will help you figure out how to craft various nodes.

## for admins

### minetest version compatibility

more blocks is only tested against up-to-date minetest. Issues arising in older versions will generally not be fixed.

### legacy mode

the 2023-02-01 release of moreblocks introduces a "legacy" mode, which is on by default, and is meant to
allow new servers to not commit to creating as many nodes as older versions, while not breaking anything
on existing servers. See `settingtypes.txt` for available settings.

by defaul the 2023-02-01 release disables certain recipe overrides that were part of moreblocks 2.*. to re-enable
them, set `moreblocks_legacy_recipes.enabled = true`.

### settings

see `settingtypes.txt` for available settings.

### dependencies

moreblocks and stairsplus do not have hard dependencies on other mods. invsaw depends on `unified_inventory`
and stairsplus.

### compatability

moreblocks currently supports resources from a number of mods and minetest_game. without these installed,
some things may not be craftable, may have low-quality textures, or may not have "node sounds" registered.
if available, resources will be used from `bucket`, `default`, `rhotator`, `screwdriver`, and `vessels`.

if the `stairsplus_legacy` mod is enabled, stairsplus nodes will automatically be registered for the following
mods, if they are available: `basic_materials`, `default`, `farming`, `gloopblocks`, `prefab`, `technic`,
and `wool`.

## for mod makers

See moreblocks/API.md and stairsplus/API.md.

# license

## moreblocks, stairsplus, stairsplus_legacy, moreblocks_legacy_recipes

* © 2011-2022 Hugo Locurcio and contributors under the zlib license
* © 2023- fluxionary under the AGPL v3+

- unless otherwise specified, textures are licensed under
  [CC BY-SA 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/).
- `moreblocks_copperpatina.png` was created by pithydon, and is licensed under
  [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
- `stairsplus_saw_button.png` CC BY-SA 3.0 Unported

## invsaw

* © 2022 cheapie and contributors under the zlib license
* © 2023- fluxionary under the AGPL v3+
