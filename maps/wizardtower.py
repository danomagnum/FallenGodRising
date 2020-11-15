import main, battle, zone, entities, moves, elements
from items import items, gen_gear
from constants import *
import random
import maps.maptools as maptools
import maps.cellular
import maps.buildings
import os
import mobs
import utility
ZONENAME = 'WizardTower'

class ThisZone(zone.LinearZone):
	def config(self):
		self.music = 'wizard.mid'
		#battle AI to use, #world AI to use, name, *mobs
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
		newitem = gen_gear(self.game, gen_level + 3)
		maptools.Random_Map_Insert(self, entities.Treasure(self.game, [newitem,]))

#####################
# populate the zone with entities
#####################

def genzone(game):

	# generate maps
	map_list = []

	for l in range(20):
		game.progress()
		lev = maps.buildings.building_octagon(maptools.MAPSIZE[1], maptools.MAPSIZE[1])
		if l == 0:
			#maptools.add_stairs(lev, down=False)
			#maptools.add_stairs(lev, up=False)
			#maptools.add_stairs(lev)
			maptools.add_stairs(lev, up=False)
		elif l == 19:
			maptools.add_stairs(lev, down=False)
		else:
			maptools.add_stairs(lev)
		lev = maptools.flatten(lev)
		map_list.append(maptools.flatten(lev))
	#maze = maptools.maze(16, 16)
		# Create zone
	zone = ThisZone(ZONENAME, game, maps=map_list)
	#zone.grid_width = 16
	zone.change_level(0)

	alter = entities.Alter(game)
	maptools.Random_Map_Insert(zone, alter, 19)
	game.get_var('Alters').append(alter)


	# Populate zone with entities
	maptools.Stair_Handler(zone)
	maptools.Door_Handler(zone)

	# add zone to game
	game.add_zone(zone)

	maps.maptools.overworld_inject(game, zone, newchar='w', mask=maps.buildings.building_octagon(maptools.MAPSIZE[0], maptools.MAPSIZE[1], padding=5,outside_door=True))
	zone.fast_travel_options[0] = main.FastTravel('Entrance', 0)

	return zone
