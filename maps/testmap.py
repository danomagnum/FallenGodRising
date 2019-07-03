import main, battle, characters, overworld, entities, moves, elements, items
from constants import *
import random
import maptools


#####################
# The characters subclasses are how you create enemies.
# You can used "canned" ones or creat your own.
#####################
class LittleRat(main.Character):
	def config(self):
		self.moves = [moves.Slam()]
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
# You can used "canned" ones or creat your own.
# This is also where you set up battle groups by inheriting entities.Battler and
# assigning combatants
#####################
class Rat(entities.RandWalker, entities.Battler):
	# example basic enemy
	def config(self):
		self.name = 'Rat'
		self.combatants.append(LittleRat(level=20))
		self.char = 'r'
		self.AI = battle.Random_AI

class PackRat(entities.TowardWalker, entities.Battler):
	# example basic enemy that gives an item when killed
	def config(self):
		self.name = 'Rat Pack'
		self.combatants.append(LittleRat(level=20))
		self.backpack.store(items.Potion())
		self.char = 'F'
		self.AI = battle.Random_AI

class RatPack(entities.RandWalker, entities.Battler):
	def config(self):
		self.name = 'Rat Pack'
		self.combatants.append(LittleRat(level=20))
		self.combatants.append(LittleRat(level=20))
		self.combatants.append(LittleRat(level=20))
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
# load the map file and create the zone
#####################

filename = __file__[:-3] + '.map'
zone = overworld.Zone(filename=filename)


#####################
# populate the zone with entities
#####################

maptools.Positional_Map_Insert(zone, entities.Shop, 1)
maptools.Random_Map_Insert(zone, RatPack)
maptools.Random_Map_Insert(zone, RatPack)
maptools.Random_Map_Insert(zone, Rat)
maptools.Random_Map_Insert(zone, Rat)
maptools.Random_Map_Insert(zone, Rat)
maptools.Random_Map_Insert(zone, Rat)
maptools.Random_Map_Insert(zone, PackRat)
maptools.Random_Map_Insert(zone, PackRat)
maptools.Random_Map_Insert(zone, SeeTest)
maptools.Random_Map_Insert(zone, KeyChest)
maptools.Random_Map_Insert(zone, Door1)
maptools.Random_Map_Insert(zone, Door2)
