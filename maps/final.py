import main, battle, zone, entities, moves, elements, items, effects
from constants import *
import random
import maps.bsp as bsp
import maps.maptools as maptools
import os
import mobs
import utility

class FinalZone(zone.LinearZone):

	def config(self):
		self.mob_list = [mobs.sorcerer.Archmage]
		self.mob_list = set(self.mob_list)
		self.music = 'wizard'

	def level_018(self):
		if self.level_visits[18] == 1:
			final_boss = mobs.one.TheOne(self.game)
			maptools.Positional_Map_Insert(self, mobs.party(self.game, battle.Random_AI, entities.BasicAI1, 1, [final_boss]), '!', level=100)


def treasure_level(zone):
	t = entities.Treasure(zone.game)
	backpack = items.Backpack(zone.game)
	for x in range(3):
		p = items.status.HealAll(zone.game)
		backpack.store(p)
	tent = items.items.Tent_item(zone.game)
	backpack.store(tent)
	backpack.gold = random.randint(20, 200)
	t.backpack = backpack
	t.char = '\x92'
	maptools.Random_Map_Insert(zone, t)

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

	final_room = 'final.txt'

	treasure_levels = []

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
		treasure_levels.append(len(map_list) - 1)

	for x in range(5):
		map_name = random.choice(hall_options)
		with open('maps/final_dungeon/{}'.format(map_name)) as f:
			lev = [ line.rstrip('\n') for line in f.readlines()]
		map_list.append(lev)
		if random.random() < 0.3:
			treasure_levels.append(len(map_list) - 1)

	map_name = final_room
	with open('maps/final_dungeon/{}'.format(map_name)) as f:
		lev = [line.rstrip('\n') for line in f.readlines()]
	map_list.append(lev)


	zone = FinalZone('TheSeal', game, maps=map_list)
	zone.grid_width = 1
	zone.change_level(0)

	maptools.Stair_Handler(zone)
	maptools.Door_Handler(zone)

	#TODO: put seals in as &'s.
	#TODO: put defender in as *'s.

	game.add_zone(zone)
	ov_level = maptools.overworld_inject(game,
	                                     zone,
					     newchar='S',
					     entry_level = 0,
					     biome=6,
					     inject_char='!')
	game.overworld.entry = ov_level
	game.overworld.change_level(ov_level)
	zone.fast_travel_found.add(main.FastTravel('Entrance', 0))


	for level in treasure_levels:
		zone.__dict__['level_{:03}'.format(level)] = treasure_level


	return zone

