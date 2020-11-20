from .characters import Character, promote
import moves
import elements
import utility
import random


class Satyr(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 60
		self.base_physical_strength = 55 
		self.base_physical_defense = 50
		self.base_arcane_strength = 40
		self.base_arcane_defense = 55
		self.base_speed = 45
		self.base_luck = 100

	def level_24(self):
		promote(self, Centaur)	


class Centaur(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 70
		self.base_physical_strength = 65 
		self.base_physical_defense = 60
		self.base_arcane_strength = 90
		self.base_arcane_defense = 75
		self.base_speed = 90
		self.base_luck = 100



trash = [Satyr]
okay = [Centaur]
plains = [Satyr, Centaur]
