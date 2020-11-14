from .characters import Character, promote
import moves
import elements
import utility
import random


class Dromedary(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 35
		self.base_physical_strength = 60 
		self.base_physical_defense = 44
		self.base_arcane_strength = 40
		self.base_arcane_defense = 54
		self.base_speed = 55
		self.base_luck = 100

	def level_22(self):
		promote(self, Bactrian)	


class Bactrian(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 60
		self.base_physical_strength = 85 
		self.base_physical_defense = 69
		self.base_arcane_strength = 65
		self.base_arcane_defense = 79
		self.base_speed = 80
		self.base_luck = 100



trash = [Dromedary]
okay = [Bactrian]
