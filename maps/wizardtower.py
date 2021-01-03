import main, battle, zone, entities, moves, elements, items
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
		self.music = 'wizard'
		self.mob_list = [mobs.imp.Imp, mobs.sorcerer.Sorcerer, mobs.sorcerer.Wizard, mobs.sorcerer.Archmage]
		self.mob_list = set(self.mob_list)
		#battle AI to use, #world AI to use, name, *mobs

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
	backpack = items.Backpack(game)
	for x in range(random.randint(2,6)):
		p = items.boosts.ArcStrBoost(game)
		backpack.store(p)
	alter.backpack = backpack
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
