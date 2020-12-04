import main, battle, mobs, zone, entities, moves, elements, items
from constants import *
import maps.grid as grid
import random
import maps.maptools as maptools
import maps.cellular
import maps.buildings
import os
import mobs
import utility
ZONENAME = 'Fortress'

class FortressZone(zone.LinearZone):
	def config(self):
		self.music = 'Adventure.mid'
		#battle AI to use, #world AI to use, name, *mobs
		self.mobchoices = [(1, [battle.Random_AI, entities.BasicAI1, 'barbarian', mobs.barbarian.Barbarian]),
		                   (2, [battle.Random_AI, entities.BasicAI1, 'barbarian', mobs.barbarian.Barbarian, mobs.barbarian.Barbarian]),
		                   (2, [battle.Random_AI, entities.BasicAI1, 'barbarian', mobs.barbarian.Barbarian, mobs.barbarian.Juggernaut]),
		                   (2, [battle.Random_AI, entities.BasicAI1, 'barbarian', mobs.barbarian.Barbarian, mobs.barbarian.Juggernaut, mobs.barbarian.Juggernaut]),
		                   (5, [battle.Random_AI, entities.BasicAI1, 'barbarian', mobs.barbarian.Juggernaut, mobs.barbarian.Warlord])]

#####################
# populate the zone with entities
#####################

def genzone(game):

	# generate maps
	map_list = []

	for l in range(4):
		game.progress()
		#lev = maps.buildings.building_octagon(maptools.MAPSIZE[1], maptools.MAPSIZE[1])
		lev = grid.gridlevel()
		if l == 0:
			maptools.add_stairs(lev, up=False)
		elif l == 3:
			maptools.add_stairs(lev, down=False)
		else:
			maptools.add_stairs(lev)
		lev = maptools.flatten(lev)
		map_list.append(maptools.flatten(lev))
	zone = FortressZone(ZONENAME, game, maps=map_list)
	#zone.grid_width = 16
	zone.change_level(0)

	# add an alter at the end
	alter = entities.Alter(game)
	backpack = items.Backpack(self.game)
	for x in range(random.randint(2,6)):
		p = items.boosts.StrBoost(self.game)
		backpack.store(p)
	alter.backpack = backpack
	game.get_var('Alters').append(alter)
	maptools.Random_Map_Insert(zone, alter, 3)

	# Populate zone with entities
	maptools.Stair_Handler(zone, dir=1)
	maptools.Door_Handler(zone)

	# add zone to game
	game.add_zone(zone)

	maps.maptools.overworld_inject(game, zone, newchar='f', mask=maps.buildings.building_gen(maptools.MAPSIZE[0], maptools.MAPSIZE[1], padding=5,outside_door=True))
	zone.fast_travel_options[0] = main.FastTravel('Entrance', 0)

	return zone
