import main, battle, zone, entities, moves, elements, items
from constants import *
import random
import maps.bsp as bsp
import maps.maptools as maptools
import os
import mobs
import utility

class HomeZone(zone.Zone):

	def config(self):
		self.music = 'wizard.mid'

	def level_000(self):
		print('Tutorial> Navigate with WASD.  To continue, walk off the screen to the right.')
	def level_001(self):
		print('Tutorial> You can open doors by walking through them')
		print('Tutorial> You can pick up items by touching them')

		if self.level_visits[1] == 1:
			t = entities.Alter(self.game)
			game.get_var('Alters').append(t)
			maptools.Positional_Map_Insert(self, t, '?', level=1)

	def level_002(self):
		if self.level_visits[2] == 1:
			print('Tutorial> Enemies appear as letters on the screen.  Bump into them to start combat')
			print('Tutorial> You can continue by stepping on the stairs')
			first_mob = random.choice(mobs.trash)(self.game)
			maptools.Positional_Map_Insert(self, mobs.party(self.game, battle.Random_AI, entities.BasicAI1, 1, [first_mob], 'rat'), '!', level=2)
	def level_003(self):
		if self.level_visits[3] == 1:
			print('Tutorial> You can get a general idea of what type items are by their apperaance')
			backpack = items.Backpack(self.game)
			backpack.gold = random.randint(20, 200)
			t = entities.Treasure(self.game)
			t.backpack = backpack
			maptools.Positional_Map_Insert(self, t, '$', level=3)


			t = entities.Treasure(self.game, [items.scrolls.gen_movescroll(self.game)])
			maptools.Positional_Map_Insert(self, t, '/', level=3)

			t = entities.Treasure(self.game, [items.gen_gear(self.game, 1)])
			maptools.Positional_Map_Insert(self, t, '%', level=3)

			t = entities.Treasure(self.game, [items.status.Potion(self.game)])
			maptools.Positional_Map_Insert(self, t, '&', level=3)

			second_mob = random.choice(mobs.trash)(self.game)
			maptools.Positional_Map_Insert(self, mobs.party(self.game, battle.Random_AI, entities.BasicAI1, 1, [second_mob], 'rat'), '!', level=3)

	def level_004(self):
		total = 0
		if self.level_visits[4] == 1:
			item_list = []
			while (random.random() > 0.2) and (total < 5):
				total = total + 1
				item_seed = random.random()
				if item_seed < 0.25:
					item_list.append( items.gen_base_item(self.game))
				elif item_seed < 0.50:
					item_list.append(items.gen_gear(self.game, level=1))
				elif item_seed < 0.75:
					item_list.append(items.scrolls.gen_movescroll(self.game))
				else:
					bp = items.Backpack()
					bp.gold = random.randint(5,100)
					maptools.Random_Map_Insert(self, entities.Treasure(self.game, backpack=bp))
			if random.random() < 0.1:
				#10% chance of getting a magic amulet
				amulet = items.armor.Amulet(self.game)
				amulet = utility.add_class_to_instance(amulet, random.choice(items.special_gear_mods))
				item_list.append(amulet)
			for item in item_list:
				maptools.Random_Map_Insert(self, entities.Treasure(self.game, [item,]), level=4)

	def level_005(self):
		print('Tutorial> Touching the castle tile brings you between the overworld and dungeons')
		if self.level_visits[5] == 1:
			total = 0
			item_list = []
			while (random.random() > 0.2) and (total < 5):
				total = total + 1
				item_seed = random.random()
				if item_seed < 0.33:
					item_list.append( items.gen_base_item(self.game))
				elif item_seed < 0.66:
					item_list.append(items.gen_gear(self.game, level=1))
				else:
					item_list.append(items.scrolls.gen_movescroll(self.game))
			for item in item_list:
				maptools.Random_Map_Insert(self, entities.Treasure(self.game, [item,]), level=5)

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

