import main, battle, zone, entities, moves, elements, items
from constants import *
import random
import maps.bsp as bsp
import maps.maptools as maptools
import os
import mobs
import utility

class HomeZone(zone.Zone):

	def level_000(self):
		print('Tutorial> Navigate with WASD.  To continue, walk off the screen to the right.')
	def level_001(self):
		print('Tutorial> You can open doors by walking through them')
		print('Tutorial> You can pick up items by touching them')
	def level_002(self):
		print('Tutorial> Enemies appear as letters on the screen.  Bump into them to start combat')
		print('Tutorial> You can continue by stepping on the stairs')
	def level_003(self):
		pass
	def level_004(self):
		pass
	def level_005(self):
		print('Tutorial> Touching the castle tile brings you between the overworld and dungeons')
	pass

def genzone(game):
	game.progress()
	map_list = []

	# generate maps

	for x in range(5):
		with open('maps/Tutorial' + str(x) + '.map') as f:
			lev = [ line.rstrip('\n') for line in f.readlines()]

		map_list.append(lev)
	lev = [['#' for x in range(maptools.MAPSIZE[0])] for y in range(maptools.MAPSIZE[1])]

	for x in range(int(maptools.MAPSIZE[0] / 3), int(2* maptools.MAPSIZE[0] / 3)):
		for y in range(int(maptools.MAPSIZE[1] / 3), int(2* maptools.MAPSIZE[1] / 3)):
			lev[y][x] = '.'


	maptools.add_stairs(lev, down=False)
	lev = maptools.flatten(lev)

	map_list.append(lev)



	zone = HomeZone('Home', game, maps=map_list)
	zone.grid_width = 1
	zone.change_level(0)

	maptools.Stair_Handler(zone)
	maptools.Door_Handler(zone)

	game.add_zone(zone)
	ov_level = maptools.overworld_inject(game, zone, newchar='h', entry_level = 5)
	game.overworld.change_level(ov_level)


	#TODO: create and add "tutorial" entities
	#maptools.Positional_Map_Insert(zone, entity, '!', level=2)

	return zone

