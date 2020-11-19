from .characters import Character, promote
import moves
import elements
import utility
import random


class Lechen(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 60
		self.base_physical_strength = 40 
		self.base_physical_defense = 80
		self.base_arcane_strength = 60
		self.base_arcane_defense = 45
		self.base_speed = 40
		self.base_luck = 100

	def level_24(self):
		promote(self, FlyTrap)	


class FlyTrap(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 95
		self.base_physical_strength = 95 
		self.base_physical_defense = 85
		self.base_arcane_strength = 125
		self.base_arcane_defense = 65
		self.base_speed = 55
		self.base_luck = 100



trash = [Lechen]
okay = [FlyTrap]
