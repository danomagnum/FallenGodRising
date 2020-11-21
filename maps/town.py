import main, battle, zone, entities, moves, elements
import items
from constants import *
import random
import maps.bsp as bsp
import maps.maptools as maptools
import os
import mobs
import utility

SPLITS = 8

def town_entry(zone):
	zone.game.set_music('town.mid')
	if zone.level_visits[zone.level] == 1:
		#first visit to town. populate NPCs
		e = entities.Shop(zone.game)
		gen_level = zone.game.player.level
		e.backpack.gold = 100

		e.backpack.store(items.gen_gear(zone.game, gen_level))
		e.backpack.store(items.scrolls.gen_movescroll(zone.game))
		e.backpack.store(items.gen_base_item(zone.game))
		for potion in range(10):
			e.backpack.store(items.status.Potion(zone.game))
			e.backpack.store(items.status.HealAll(zone.game))

		maptools.Random_Map_Insert(zone, e)

def genzone(game, townname):
	game.progress()

	# generate maps

	lev = [[' ' for x in range(maptools.MAPSIZE[0])] for y in range(maptools.MAPSIZE[1])]
	buildings = bsp.Tree(0, 0, maptools.MAPSIZE[0] - 1, maptools.MAPSIZE[1] - 1, 8, 2)

	for split in range(SPLITS):
		buildings.split(True)
	buildings = buildings.final_nodes()
	for b in range(5):
		buildings.remove(random.choice(buildings))
	for building in buildings:
		building.draw(lev, True)

	overworld_map = maptools.flatten(lev)

	ov_level = maptools.overworld_inject(game, None, newchar='T', mask=overworld_map)

	game.overworld.fast_travel_options[ov_level] = main.FastTravel(townname, ov_level)
			
	game.overworld.__dict__['level_{:03}'.format(ov_level)] = town_entry
	game.overworld.special_music[ov_level] = 'town.mid'

