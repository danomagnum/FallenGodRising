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


	#ov_ht = len(game.overworld_minimap) - 1
	#ov_wd = len(game.overworld_minimap[0]) - 1
	#search = True
	#while search:
		#x = random.randint(0, ov_wd)
		#y = random.randint(0, ov_ht)
		#cell = game.overworld_minimap[y][x]
		#if any([cell.up, cell.down, cell.left, cell.right]):
			#ov_x = x
			#ov_y = y
			#search = False
	#cell.char = 'T'
	#if not cell.up:
		#for x in range(len(lev[0])):
			#lev[0][x] = '#'
	#if not cell.down:
		#for x in range(len(lev[-1])):
			#lev[-1][x] = '#'
	#if not cell.left:
		#for y in range(len(lev)):
			#lev[y][0] = '#'
	#if not cell.right:
		#for y in range(len(lev)):
			#lev[y][-1] = '#'
	#overworld_map = maptools.flatten(lev)
	overworld_map = maptools.flatten(lev)

	#ov_level = ov_x + ov_y * game.overworld.grid_width

	#new_ow_map = maptools.empty_zone_with_mask(cell, overworld_map)
	#game.overworld.maps[ov_level] = overworld_map
	

	#maptools.Door_Handler_onelevel(game.overworld, ov_level)

	ov_level = maptools.overworld_inject(game, None, newchar='T', mask=overworld_map)

	game.overworld.fast_travel_options[ov_level] = main.FastTravel(townname, ov_level)
			
	game.overworld.__dict__['level_{:03}'.format(ov_level)] = town_entry
	game.overworld.special_music[ov_level] = 'town.mid'

