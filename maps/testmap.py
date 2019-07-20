import main, battle, characters, overworld, entities, moves, elements, items
from constants import *
import random
import maps.maptools as maptools
import os
ZONENAME = 'test'

#####################
# The characters subclasses are how you create enemies.
# You can used "canned" ones or create your own.
#####################
class LittleRat(characters.Character):
	def config(self):
		self.moves = [moves.Strike(self.game)]
		self.elements = [elements.Normal]
		self.status = []
		self.coefficients = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
		self.base_physical_strength = 50
		self.base_physical_defense = 50
		self.base_special_strength = 50
		self.base_special_defense = 50
		self.base_speed = 50
		self.base_hp = 50
		self.base_luck = 100

#####################
# The entities subclasses are items that will appear in the world.
# You can used "canned" ones or create your own.
# This is also where you set up battle groups by inheriting entities.Battler and
# assigning combatants
#####################
class Rat(entities.RandWalker, entities.Battler):
	# example basic enemy
	def config(self):
		self.name = 'Rat'
		self.combatants.append(LittleRat(self.game, level=1))
		self.char = 'r'
		self.AI = battle.Random_AI

class PackRat(entities.TowardWalker, entities.Battler):
	# example basic enemy that gives an item when killed
	def config(self):
		self.name = 'Rat Pack'
		self.combatants.append(LittleRat(self.game, level=1))
		self.backpack.store(items.Potion(self.game))
		self.char = 'F'
		self.AI = battle.Random_AI

class RatPack(entities.RandWalker, entities.Battler):
	def config(self):
		self.name = 'Rat Pack'
		self.combatants.append(LittleRat(self.game, level=1))
		self.combatants.append(LittleRat(self.game, level=1))
		self.combatants.append(LittleRat(self.game, level=1))
		self.char = 'R'
		self.AI = battle.Random_AI

class SeeTest(entities.BasicAI1):
	def config(self):
		self.name = 'See Test'
		self.char = 'S'
		self.standby_delay = 10


class KeyChest(entities.Treasure):
	# example basic enemy that gives an item when killed
	def config(self):
		self.name = 'Key Chest'
		self.backpack.store(items.Key(self.game))
		self.char = 'k'

class SwordChest(entities.Treasure):
	# example basic enemy that gives an item when killed
	def config(self):
		self.name = 'Sword Chest'
		#self.backpack.store(items.FireSword(self.game))
		item = items.Sword(self.game)
		items.add_item_mod(item, random.choice(items.general_gear_mods))
		items.add_item_mod(item, random.choice(items.base_gear_mods))
		items.add_item_mod(item, random.choice(items.special_gear_mods))
		self.backpack.store(item)
		self.char = '/'

class Door1(entities.Door):
	pass
class Door2(entities.Door):
	def key(self):
		self.lock='Key'

class MyShop(entities.Shop):
	def config(self):
		self.backpack.store(items.Potion(self.game))
		self.backpack.store(items.Potion(self.game))
		self.backpack.store(items.Potion(self.game))
		self.backpack.store(items.Potion(self.game))
		self.backpack.store(items.Potion(self.game))

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
		


#####################
# populate the zone with entities
#####################

def genzone(game):

	# generate maps
	maps = []
	for file in files:
		maps.append(maptools.readmap(file))
	
	maps = []
	maze = maptools.maze(16, 16)
	y = 0
	x = 0
	maxentries = 0
	start = 0
	for maze_y in maze:
		for maze_x in maze_y:
			map = maptools.drunkard_walk()
			#up and down are swapped because of the zone map list goes from bottom to top but the 
			#maze y order is top to bottom
			entries = 0
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
			map = maptools.showmap(map)
			maps.append(map)

			if entries > maxentries:
				maxentries = entries
				start = y * 16 + x
			x += 1
		y += 1
	


	# Create zone
	zone = overworld.Zone(ZONENAME, game, maps=maps)
	zone.grid_width = 16
	zone.level = start

	# Populate zone with entities
	#maptools.Positional_Map_Insert(zone, MyShop, 1)
	#maptools.Random_Map_Insert(zone, RatPack)
	#maptools.Random_Map_Insert(zone, RatPack)
	maptools.Random_Map_Insert(zone, Rat)
	maptools.Random_Map_Insert(zone, Rat)
	maptools.Random_Map_Insert(zone, Rat)
	maptools.Random_Map_Insert(zone, Rat)
	#maptools.Random_Map_Insert(zone, PackRat)
	#maptools.Random_Map_Insert(zone, PackRat)
	#maptools.Random_Map_Insert(zone, SeeTest)
	maptools.Random_Map_Insert(zone, SwordChest)
	#maptools.Random_Map_Insert(zone, Door1)
	#maptools.Random_Map_Insert(zone, Door2)
	#maptools.Stair_Handler(zone)

	# add zone to game
	game.add_zone(zone)

	return zone
