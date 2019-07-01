import main, battle, characters, overworld, entities, moves, elements, items
from constants import *
import random
import maptools



# The characters subclasses are how you create enemies.

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


# The entities subclasses are items that will appear in the world.

class Rat(entities.RandWalker, entities.Battler):
	# example basic enemy
	def config(self):
		self.name = 'Rat'
		self.combatants.append(LittleRat(level=20))
		self.char = 'r'
		self.AI = battle.Random_AI

class PackRat(entities.RandWalker, entities.Battler):
	# example basic enemy that gives an item when killed
	def config(self):
		self.name = 'Rat Pack'
		self.combatants.append(LittleRat(level=20))
		self.backpack.store(items.Potion())
		self.char = 'r'
		self.AI = battle.Random_AI

class RatPack(entities.RandWalker, entities.Battler):
	def config(self):
		self.name = 'Rat Pack'
		self.combatants.append(LittleRat(level=20))
		self.combatants.append(LittleRat(level=20))
		self.combatants.append(LittleRat(level=20))
		self.char = 'R'
		self.AI = battle.Random_AI


filename = __file__[:-3] + '.map'
zone = overworld.Zone(filename=filename)

maptools.Random_Map_Insert(zone, RatPack)
maptools.Random_Map_Insert(zone, RatPack)
maptools.Random_Map_Insert(zone, Rat)
maptools.Random_Map_Insert(zone, Rat)
maptools.Random_Map_Insert(zone, Rat)
maptools.Random_Map_Insert(zone, Rat)
maptools.Random_Map_Insert(zone, PackRat)
maptools.Random_Map_Insert(zone, PackRat)

