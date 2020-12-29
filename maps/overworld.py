#!/usr/bin/python
#coding: utf-8 

import main, battle, zone, entities, moves, elements
import mobs
import items
#from items import items
from constants import *
import random
import maps.maptools as maptools
import maps.perlin as perlin
import maps.nearest_biome as biomegen
import maps.bezier as bezier
import os
import sys
import math
ZONENAME = 'Overworld'

USE_SYMBOLS = True
#####################
# load the map file(s)
#####################

filename = os.path.split(__file__)[-1]
#__file__[:-3]
path = os.path.dirname(os.path.realpath(__file__))
#+ '.map'

files = []
for i in os.listdir(path):
	if os.path.isfile(os.path.join(path,i)) and filename[:-3] in i:
		if i[-3:] == 'map':
			files.append(os.path.join(path, i))
		

music_per_biome = {elements.Sea: 'calm',
                   elements.Marsh: 'odd',
		   elements.Plains: 'alone',
		   elements.Desert: 'desert',
		   elements.Forest: 'forest',
		   elements.Mountains: 'mountains',
		   elements.Sky: 'Winter Frost',
		   elements.Underground: 'overworld1'}


moblist         = {elements.Sea: mobs.sea,
                   elements.Marsh: mobs.marsh,
		   elements.Plains: mobs.plains,
		   elements.Desert: mobs.desert,
		   elements.Forest: mobs.forest,
		   elements.Mountains: mobs.mountain,
		   elements.Sky: mobs.sky,
		   elements.Underground: mobs.underground}



class OverworldZone(zone.Zone):
	def level_populate(self, level, visit_no):
		gen_level = 1
		if self.game.player is not None:
			gen_level = self.game.player.combatants[0].level

		gen_level += self.game.get_var('GLO')

		if visit_no < 2:
			#if I only want to populate on the first visit
			item_count = random.randint(0,2)
			for i in range(item_count):
				chance = random.random()
				if chance < 0.3:
					newitem = items.gen_gear(self.game, gen_level)
				elif chance < 0.6:
					newitem = items.scrolls.gen_movescroll(self.game)
				else:
					newitem = items.gen_base_item(self.game)
				maptools.Random_Map_Insert(self, entities.Treasure(self.game, [newitem,]))
			gold_count = random.randint(0,2)
			for i in range(gold_count):
				g0 = random.randint(5,100)
				g2 = random.randint(5,100)
				g3 = random.randint(5,100)

				gtotal = g0 + g2 + g3
				bp = items.Backpack()
				bp.gold = gtotal
				maptools.Random_Map_Insert(self, entities.Treasure(self.game, backpack=bp))

			mob_count = random.randint(0, 10)
			for m in range(mob_count):
				#party = mobs.party(self.game, Battle_AI, Entity_AI, mob_level, mobs_list, 'name')
				try:
					#this array is the probabilities of getting 1, 2, or 3 mobs in a spawned party
					probabilities = [1] * 30 + [2] * 3 + [3]
					partysize = random.choice(probabilities)
					available_mobs = mobs.trash & moblist[self.game.biome()]

					chosen_mobs = []

					for mobno in range(partysize):
						chosen_mobs.append(random.sample(available_mobs,1)[0])

					#parties = []
					mob_level = random.choice([gen_level, self.depth()])
					maptools.Random_Map_Insert(self, mobs.party(self.game, battle.Random_AI, entities.BasicAI1, mob_level, chosen_mobs))
				except:
					pass

		self.game.set_music(self.get_music())
		#b = self.game.biome()
		#if b in music_per_biome:
			#self.game.set_music(music_per_biome[b])

	def get_music(self):
		print('music check for level {}'.format(self.level))
		if self.level in self.special_music:
			return self.special_music[self.level]

		b = self.game.biome()
		if b in music_per_biome:
			return music_per_biome[b]


#####################
# populate the zone with entities
#####################

def genzone(game):

	# generate maps
	maps = []
	for file in files:
		maps.append(maptools.readmap(file))

	
	#this defines the biomes
	#biome_map = perlin.gen_overworld(16, 16)
	biome_map = biomegen.generate()
	
	maps = []
	maze = maptools.maze(16, 16)
	y = 0
	x = 0
	maxentries = 0
	start = 0
	valid_positions = []
	for maze_y in maze:
		x = 0
		for maze_x in maze_y:
			game.progress()
			biome = biome_map[y][x]
			poke = False
			if biome == 3: # deserts
				percent = 0.8
				map = maptools.drunkard_walk(maptools.MAPSIZE[0], maptools.MAPSIZE[1], percent)
				poke = True
			elif biome == 4: # forest
				map = bezier.generate(maze_x)
				percent = 0.8
			else:
				percent = 0.3
				map = maptools.drunkard_walk(maptools.MAPSIZE[0], maptools.MAPSIZE[1], percent)
				poke = True
			#up and down are swapped because of the zone map list goes from bottom to top but the 
			#maze y order is top to bottom
			entries = 0
			if poke:
				if not maze_x.up:
					maptools.add_entry(map, DOWN)
					entries += 1
				if not maze_x.down:
					maptools.add_entry(map, UP)
					entries += 1
				if not maze_x.left:
					maptools.add_entry(map, LEFT)
					entries += 1
				if not maze_x.right:
					maptools.add_entry(map, RIGHT)
					entries += 1
				maptools.noise_prune(map)
			#if (sys.version_info.major >= 3) and USE_SYMBOLS:
			if True:
				if biome == 0:
					maptools.swap_char(map, '#', '~\x7F\x8D') # Sea
					#maptools.swap_char(map, '#', '≅≊≋≌⋍') # Sea
				elif biome == 1:
					maptools.swap_char(map, '#', '~\xFC') # Marsh
					#maptools.swap_char(map, '#', '≅≊≋≌⋍') # Marsh
				elif biome == 2:
					pass # Plains
				elif biome == 3:
					#pass # desert
					maptools.swap_char(map, '#', '\xA6\xA7') # Desert
				elif biome == 4:
					maptools.swap_char(map, '#', '\x05\x06\x07\x08') # forest
					#maptools.swap_char(map, '#', '♠♣') # forest
				elif biome == 5:
					maptools.swap_char(map, '#', '\xEC\xED') # Mountains
					#maptools.swap_char(map, '#', '▲⏶') # Mountains
				elif biome == 6:
					pass # sky
				elif biome == 7:
					pass # underground
			#map = maptools.flatten(map)
			maps.append(map)

			if entries > 0:
				valid_positions.append((x, y))

			if entries > maxentries:
				maxentries = entries
				start = y * 16 + x
			x += 1
		y += 1

	maps = maptools.entry_match(maps, maze, game, 16)
	
	maps = [maptools.flatten(map) for map in maps]
	
	# Create zone
	zone = OverworldZone(ZONENAME, game, maps=maps)
	zone.grid_width = 16
	zone.change_level(start)

	maptools.Stair_Handler(zone)

	# add zone to game
	game.add_zone(zone)

	return zone, biome_map, maze
