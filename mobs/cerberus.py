from .characters import Character, promote
import moves
import elements
import utility
import random


class Cerberus(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 80
		self.base_physical_strength = 85 
		self.base_physical_defense = 95
		self.base_arcane_strength = 30
		self.base_arcane_defense = 30
		self.base_speed = 25
		self.base_luck = 100

	def level_42(self):
		promote(self, Chimera)	


class Chimera(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 105
		self.base_physical_strength = 130 
		self.base_physical_defense = 120
		self.base_arcane_strength = 45
		self.base_arcane_defense = 45
		self.base_speed = 40
		self.base_luck = 100



okay = [Cerberus]
good = [Chimera]
