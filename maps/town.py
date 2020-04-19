import main, battle, characters, zone, entities, moves, elements, items
from constants import *
import random
import maps.bsp as bsp
import maps.maptools as maptools
import os
import mobs
import utility

SPLITS = 8

def town_entry(zone):
	print('Welcome To Town')
	if zone.level_visits[zone.level] == 1:
		print('First Visit')
		#first visit to town. populate NPCs
		e = entities.Shop(zone.game)
		gen_level = zone.game.player.level
		e.backpack.gold = 100

		e.backpack.store(items.gen_gear(zone.game, gen_level))
		e.backpack.store(items.gen_movescroll(zone.game))
		e.backpack.store(items.gen_base_item(zone.game))
		for potion in range(10):
			e.backpack.store(items.Potion(zone.game))
			e.backpack.store(items.HealAll(zone.game))

		maptools.Random_Map_Insert(zone, e)

def genzone(game, townname):
	game.progress()

	# generate maps

	lev = [['.' for x in range(maptools.MAPSIZE[0])] for y in range(maptools.MAPSIZE[1])]
	buildings = bsp.Tree(0, 0, maptools.MAPSIZE[0] - 1, maptools.MAPSIZE[1] - 1, 8, 2)

	for split in range(SPLITS):
		buildings.split(True)
	for building in buildings.final_nodes():
		building.draw(lev, True)

	overworld_map = maptools.flatten(lev)


	ov_ht = len(game.overworld_minimap) - 1
	ov_wd = len(game.overworld_minimap[0]) - 1
	search = True
	while search:
		y = random.randint(0, ov_wd)
		x = random.randint(0, ov_ht)
		cell = game.overworld_minimap[y][x]
		if any([cell.up, cell.down, cell.left, cell.right]):
			ov_x = x
			ov_y = y
			search = False
	cell.char = 'T'
	ov_level = ov_x + ov_y * game.overworld.grid_width

	#new_ow_map = maptools.empty_zone_with_mask(cell, overworld_map)
	game.overworld.maps[ov_level] = overworld_map
	

	maptools.Door_Handler_onelevel(game.overworld, ov_level)
	game.overworld.fast_travel_options[ov_level] = main.FastTravel(townname, ov_level)

			
	game.overworld.__dict__['level_{:03}'.format(ov_level)] = town_entry

