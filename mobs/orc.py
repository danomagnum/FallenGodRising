from .characters import Character, promote
import moves
import elements
import utility
import random


class Orc(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 50
		self.base_physical_strength = 50 
		self.base_physical_defense = 95
		self.base_arcane_strength = 40
		self.base_arcane_defense = 50
		self.base_speed = 35
		self.base_luck = 100

	def level_25(self):
		promote(self, Troll)	


class Troll(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 60
		self.base_physical_strength = 80 
		self.base_physical_defense = 110
		self.base_arcane_strength = 50
		self.base_arcane_defense = 80
		self.base_speed = 45
		self.base_luck = 100



trash = [Orc]
okay = [Troll]
plains = [Orc]
mountains = [Troll, Orc]
