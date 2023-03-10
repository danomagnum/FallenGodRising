from .characters import Character, promote
import moves
import elements
import utility
import random

class Spider(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.mods.Poison(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 50
		self.base_physical_defense = 50
		self.base_arcane_strength = 50
		self.base_arcane_defense = 50
		self.base_speed = 50
		self.base_hp = 20
		self.base_luck = 100

class Ogre(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 120
		self.base_physical_defense = 120
		self.base_arcane_strength = 80
		self.base_arcane_defense = 80
		self.base_speed = 90
		self.base_hp = 130
		self.base_luck = 90

class Highwayman(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 90
		self.base_physical_defense = 90
		self.base_arcane_strength = 90
		self.base_arcane_defense = 90
		self.base_speed = 90
		self.base_hp = 90
		self.base_luck = 120

class Skeleton(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 90
		self.base_physical_defense = 90
		self.base_arcane_strength = 10
		self.base_arcane_defense = 50
		self.base_speed = 90
		self.base_hp = 90
		self.base_luck = 90

class Zombie(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 90
		self.base_physical_defense = 90
		self.base_arcane_strength = 10
		self.base_arcane_defense = 50
		self.base_speed = 10
		self.base_hp = 90
		self.base_luck = 90

class Mimic(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 90
		self.base_physical_defense = 90
		self.base_arcane_strength = 90
		self.base_arcane_defense = 90
		self.base_speed = 130
		self.base_hp = 90
		self.base_luck = 90


class Centaur(Character):
	def config(self):
		self.moves = [moves.Blast(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 80
		self.base_physical_defense = 80
		self.base_arcane_strength = 100
		self.base_arcane_defense = 100
		self.base_speed = 110
		self.base_hp = 110
		self.base_luck = 90


class Demon(Character):
	def config(self):
		self.moves = [moves.Blast(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 80
		self.base_physical_defense = 80
		self.base_arcane_strength = 120
		self.base_arcane_defense = 120
		self.base_speed = 90
		self.base_hp = 130
		self.base_luck = 90


#mods: giant, lesser, greater, captain, elements
