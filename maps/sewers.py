import main, battle, characters, zone, entities, moves, elements, items
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
		#battle AI to use, #world AI to use, name, *mobs
		self.mobchoices = [(1, [battle.Random_AI, entities.BasicAI1, 'rat', mobs.Rat]),
		                   (2, [battle.Random_AI, entities.BasicAI1, 'spider', mobs.Spider]),
		                   (3, [battle.Random_AI, entities.BasicAI1, 'spider', mobs.Spider, mobs.Spider]),
		                   (5, [battle.Random_AI, entities.BasicAI1, 'imp', mobs.Imp]),
		                   (9, [battle.Random_AI, entities.BasicAI1, 'skeleton', mobs.Skeleton]),
		                   (13, [battle.Random_AI, entities.BasicAI1, 'skeleton', mobs.Skeleton, mobs.Spider]),
		                   (17, [battle.Random_AI, entities.BasicAI1, 'skeleton', mobs.Skeleton, mobs.Skeleton, mobs.Spider])]
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
			map = maptools.empty_zone(maze_x)
			map = maptools.flatten(map)
			map_list.append(map)


	zone = ThisZone(ZONENAME, game, maps=map_list)
	zone.grid_width = 5
	zone.change_level(0)

	# Populate zone with entities
	#maptools.Stair_Handler(zone)
	#maptools.Door_Handler(zone)

	# add zone to game
	game.add_zone(zone)

	maptools.overworld_inject(game, zone, newchar='s')

	return zone
