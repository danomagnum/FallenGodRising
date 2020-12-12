import main, battle, zone, entities, moves, elements, items
from constants import *
import random
import maps.maptools as maptools
import maps.cellular
import maps.maze
import os
import mobs
import utility
ZONENAME = 'Pyramid'

class ThisZone(zone.LinearZone):
	def config(self):
		#battle AI to use, #world AI to use, name, *mobs
		self.music = 'Purgatory.mid'
		self.mobchoices = [(1, [battle.Random_AI, entities.BasicAI1, 'imp', mobs.imp.Imp]),
		                   (2, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Sorcerer]),
		                   (3, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Sorcerer, mobs.imp.Imp]),
		                   (5, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Sorcerer, mobs.sorcerer.Wizard]),
		                   (9, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Wizard, mobs.sorcerer.Sorcerer, mobs.sorcerer.Sorcerer]),
		                   (13, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Sorcerer, mobs.sorcerer.Sorcerer, mobs.sorcerer.Wizard]),
		                   (17, [battle.Random_AI, entities.BasicAI1, 'wizard', mobs.sorcerer.Wizard, mobs.sorcerer.Wizard, mobs.sorcerer.Archmage])]
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

	for l in range(10):
		game.progress()
		#lev = maps.buildings.building_octagon(maptools.MAPSIZE[1], maptools.MAPSIZE[1])
		lev = maps.maze.maze_map(12 - l, 12 -  l)
		#print('lev created')
		if l == 0:
			#maptools.add_stairs(lev, down=False)
			#maptools.add_stairs(lev, up=False)
			#maptools.add_stairs(lev)
			maptools.add_stairs(lev, up=False)
		elif l == 9:
			maptools.add_stairs(lev, down=False)
		else:
			maptools.add_stairs(lev)
		#lev = maptools.flatten(lev)
		#print('flattening')
		map_list.append(maptools.flatten(lev))
		#print('flattened')
	#maze = maptools.maze(16, 16)
		# Create zone
	zone = ThisZone(ZONENAME, game, maps=map_list)
	#zone.grid_width = 16
	zone.change_level(0)

	alter = entities.Alter(game)
	backpack = items.Backpack(game)
	for x in range(random.randint(2,6)):
		p = items.boosts.SpdBoost(game)
		backpack.store(p)
	alter.backpack = backpack
	maptools.Random_Map_Insert(zone, alter, 9)
	game.get_var('Alters').append(alter)


	# Populate zone with entities
	maptools.Stair_Handler(zone)
	#maptools.Door_Handler(zone)

	# add zone to game
	game.add_zone(zone)

	maps.maptools.overworld_inject(game, zone, newchar='p', mask=maps.buildings.building_octagon(maptools.MAPSIZE[0], maptools.MAPSIZE[1], padding=5,outside_door=True), biome=3)
	zone.fast_travel_options[0] = main.FastTravel('Entrance', 0)

	return zone
