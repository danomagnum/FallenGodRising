import main, battle, zone, entities, moves, elements, items, effects
from constants import *
import random
import maps.bsp as bsp
import maps.maptools as maptools
import os
import mobs
import utility

class FinalZone(zone.Zone):

	def config(self):
		self.mob_list = [mobs.sorcerer.Archmage]
		self.mob_list = set(self.mob_list)
		self.music = 'wizard'

def genzone(game):
	game.progress()
	map_list = []

	# generate maps
	hall_options =['barrier.txt',
	               'curly.txt',
		       'defender.txt',
		       'hallway.txt',
		       'nook.txt',
		       'seal.txt',
		       'shift1.txt']

	room_options =['seal.txt',
		       'room1.txt',
		       'room2.txt']

	with open('maps/final_dungeon/entryway.txt') as f:
		lev = [ line.rstrip('\n') for line in f.readlines()]
	map_list.append(lev)

	for room in range(3):
		for x in range(3):
			map_name = random.choice(hall_options)
			with open('maps/final_dungeon/{}'.format(map_name)) as f:
				lev = [ line.rstrip('\n') for line in f.readlines()]
			map_list.append(lev)

		map_name = random.choice(room_options)
		with open('maps/final_dungeon/{}'.format(map_name)) as f:
			lev = [ line.rstrip('\n') for line in f.readlines()]
		map_list.append(lev)


	zone = FinalZone('TheSeal', game, maps=map_list)
	zone.grid_width = 1
	zone.change_level(0)

	maptools.Stair_Handler(zone)
	maptools.Door_Handler(zone)

	game.add_zone(zone)
	ov_level = maptools.overworld_inject(game, zone, newchar='S', entry_level = 5, biome=6)
	game.overworld.entry = ov_level
	game.overworld.change_level(ov_level)
	zone.fast_travel_found.add(main.FastTravel('Entrance', 0))


	return zone

