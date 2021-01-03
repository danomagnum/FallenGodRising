import main, battle, zone, entities, moves, elements
import items
#from items import items, gen_gear, Backpack
from constants import *
import random
import maps.maptools as maptools
import maps.cellular
import os
import mobs
import utility
ZONENAME = 'GoblinCave'

class ThisZone(zone.LinearZone):
	def config(self):
		self.mob_list = [mobs.goblin.Goblin, mobs.goblin.HobGoblin, mobs.goblin.GoblinLord]
		self.mob_list = set(self.mob_list)

	def level_009(self):
		gen_level = 1
		if self.game.player is not None:
			gen_level = self.game.player.level
		newitem = items.gen_gear(self.game, gen_level + 3)
		maptools.Random_Map_Insert(self, entities.Treasure(self.game, [newitem,]))

#####################
# populate the zone with entities
#####################

def genzone(game):

	# generate maps
	map_list = []

	for l in range(10):
		game.progress()
		lev = maps.cellular.gen_cellular(maptools.MAPSIZE[0], maptools.MAPSIZE[1], gens=4)
		if l == 0:
			#maptools.add_stairs(lev, down=False)
			#maptools.add_stairs(lev, up=False)
			#maptools.add_stairs(lev)
			maptools.add_stairs(lev, up=False)
		elif l == 9:
			maptools.add_stairs(lev, down=False)
		else:
			maptools.add_stairs(lev)
		lev = maptools.fix_disjoint_hall(lev)
		maptools.swap_char(lev, '#', '\xDB')
		map_list.append(maptools.flatten(lev))
	#maze = maptools.maze(16, 16)
		# Create zone
	zone = ThisZone(ZONENAME, game, maps=map_list)

	# add an alter at the bottom
	alter = entities.Alter(game)
	backpack = items.Backpack(game)
	for x in range(random.randint(2,6)):
		p = items.boosts.DefBoost(game)
		backpack.store(p)
	alter.backpack = backpack
	game.get_var('Alters').append(alter)
	maptools.Random_Map_Insert(zone, alter, 9)

	#zone.grid_width = 16
	zone.change_level(0)

	# Populate zone with entities
	maptools.Stair_Handler(zone)

	# add zone to game
	game.add_zone(zone)

	maps.maptools.overworld_inject(game, zone, newchar='g')

	zone.fast_travel_options[0] = main.FastTravel('Entrance', 0)
	return zone
