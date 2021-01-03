import main, battle, zone, entities, moves, elements, items
from constants import *
import random
import maps.maptools as maptools
import maps.cellular
import maps.buildings
import os
import mobs
import utility
ZONENAME = 'Sewers'

class ThisZone(zone.LinearZone):
	def config(self):
		self.mob_list = [mobs.rat.LittleRat,
		                 mobs.rat.Rat,
		                 mobs.skeleton.Skeleton,
				 mobs.orc.Orc,
				 mobs.orc.Troll,
				 mobs.snake.Snake,
				 mobs.snake.Serpent,
				 mobs.zombie.Zombie,
				 mobs.imp.Imp,
				 mobs.echo.Echo,
				 mobs.echo.Shadow]

		self.mob_list = set(self.mob_list)

	def level_019(self):
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
	maze = maptools.maze(5, 5)
	
	for maze_y in maze:
		x = 0
		for maze_x in maze_y:
			game.progress()
			map = maptools.empty_zone( maze_x, maptools.MAPSIZE[0], maptools.MAPSIZE[1])
			map = maptools.flatten(map)
			map_list.append(map)


	zone = ThisZone(ZONENAME, game, maps=map_list)
	zone.grid_width = 5
	zone.change_level(0)


	# add an alter somewhere
	alter = entities.Alter(game)
	backpack = items.Backpack(game)
	for x in range(random.randint(2,6)):
		p = items.boosts.ArcDefBoost(game)
		backpack.store(p)
	alter.backpack = backpack
	game.get_var('Alters').append(alter)
	maptools.Random_Map_Insert(zone, alter, random.randint(0,24))

	# Populate zone with entities
	#maptools.Stair_Handler(zone)
	#maptools.Door_Handler(zone)

	# add zone to game
	game.add_zone(zone)

	maptools.overworld_inject(game, zone, newchar='s')

	zone.fast_travel_options[0] = main.FastTravel('Entrance', 0)

	return zone
