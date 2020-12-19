from .characters import Character, promote
import moves
import elements
import utility
import random


class Wanderer(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()

	def base_stats(self):
		self.base_hp = 40
		self.base_physical_strength = 45 
		self.base_physical_defense = 35
		self.base_arcane_strength = 40
		self.base_arcane_defense = 40
		self.base_speed = 90
		self.base_luck = 100

	def level_19(self):
		promote(self, Highwayman)	


class Highwayman(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 65
		self.base_physical_strength = 70 
		self.base_physical_defense = 60
		self.base_arcane_strength = 65
		self.base_arcane_defense = 65
		self.base_speed = 115
		self.base_luck = 100



trash = [Wanderer]
okay = [Highwayman]
plains = [Wanderer, Highwayman]
forest = [Wanderer, Highwayman]
mountains = [Wanderer, Highwayman]
