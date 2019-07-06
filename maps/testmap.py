import main, battle, characters, overworld, entities, moves, elements, items
from constants import *
import random
import maps.maptools as maptools
import os


#####################
# The characters subclasses are how you create enemies.
# You can used "canned" ones or create your own.
#####################
class LittleRat(main.Character):
	def config(self):
		self.moves = [moves.Strike()]
		self.elements = [elements.Normal]
		self.status = []
		self.coefficients = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
		self.base_physical_strength = 6
		self.base_physical_defense = 6
		self.base_special_strength = 6
		self.base_special_defense = 6
		self.base_speed = 6
		self.base_hp = 6
		self.base_luck = 10

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
		self.combatants.append(LittleRat(level=2))
		self.char = 'r'
		self.AI = battle.Random_AI

class PackRat(entities.TowardWalker, entities.Battler):
	# example basic enemy that gives an item when killed
	def config(self):
		self.name = 'Rat Pack'
		self.combatants.append(LittleRat(level=1))
		self.backpack.store(items.Potion())
		self.char = 'F'
		self.AI = battle.Random_AI

class RatPack(entities.RandWalker, entities.Battler):
	def config(self):
		self.name = 'Rat Pack'
		self.combatants.append(LittleRat(level=1))
		self.combatants.append(LittleRat(level=1))
		self.combatants.append(LittleRat(level=1))
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
		self.backpack.store(items.Key())
		self.char = 'k'

class Door1(entities.Door):
	pass
class Door2(entities.Door):
	def key(self):
		self.lock='Key'


#####################
# load the map file(s) and create the zone
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
		
		
zone = overworld.Zone(files=files)

class MyShop(entities.Shop):
	def config(self):
		self.backpack.store(items.Potion())
		self.backpack.store(items.Potion())
		self.backpack.store(items.Potion())
		self.backpack.store(items.Potion())
		self.backpack.store(items.Potion())

#####################
# populate the zone with entities
#####################

maptools.Positional_Map_Insert(zone, MyShop, 1)
#maptools.Random_Map_Insert(zone, RatPack)
#maptools.Random_Map_Insert(zone, RatPack)
#maptools.Random_Map_Insert(zone, Rat)
#maptools.Random_Map_Insert(zone, Rat)
#maptools.Random_Map_Insert(zone, Rat)
#maptools.Random_Map_Insert(zone, Rat)
maptools.Random_Map_Insert(zone, PackRat)
maptools.Random_Map_Insert(zone, PackRat)
#maptools.Random_Map_Insert(zone, SeeTest)
maptools.Random_Map_Insert(zone, KeyChest)
maptools.Random_Map_Insert(zone, Door1)
maptools.Random_Map_Insert(zone, Door2)
#maptools.Positional_Map_Insert(zone, main.UpStairs, '\\')
#maptools.Positional_Map_Insert(zone, main.DownStairs, '/')
maptools.Stair_Handler(zone)
