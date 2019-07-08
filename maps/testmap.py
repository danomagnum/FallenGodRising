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
class LittleRat(main.Character):
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

	for i in range(5):
		map = maptools.drunkard_walk()
		maptools.add_entry(map, UP)
		maptools.add_entry(map, DOWN)
		maptools.add_entry(map, LEFT)
		maptools.add_entry(map, RIGHT)
		map = maptools.showmap(map)
		maps.append(map)


	# Create zone
	zone = overworld.Zone(ZONENAME, game, maps=maps)

	# Populate zone with entities
	#maptools.Positional_Map_Insert(zone, MyShop, 1)
	#maptools.Random_Map_Insert(zone, RatPack)
	#maptools.Random_Map_Insert(zone, RatPack)
	#maptools.Random_Map_Insert(zone, Rat)
	#maptools.Random_Map_Insert(zone, Rat)
	#maptools.Random_Map_Insert(zone, Rat)
	#maptools.Random_Map_Insert(zone, Rat)
	#maptools.Random_Map_Insert(zone, PackRat)
	#maptools.Random_Map_Insert(zone, PackRat)
	#maptools.Random_Map_Insert(zone, SeeTest)
	#maptools.Random_Map_Insert(zone, KeyChest)
	#maptools.Random_Map_Insert(zone, Door1)
	#maptools.Random_Map_Insert(zone, Door2)
	#maptools.Stair_Handler(zone)

	# add zone to game
	game.add_zone(zone)

	return zone
