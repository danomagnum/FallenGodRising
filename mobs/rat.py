from .characters import Character, promote
import moves
import elements
import utility
import random


class LittleRat(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 30
		self.base_physical_strength = 56 
		self.base_physical_defense = 35
		self.base_arcane_strength = 25
		self.base_arcane_defense = 35
		self.base_speed = 72
		self.base_luck = 100

	def level_20(self):
		promote(self, Rat)	


class Rat(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 55
		self.base_physical_strength = 81 
		self.base_physical_defense = 60
		self.base_arcane_strength = 50
		self.base_arcane_defense = 70
		self.base_speed = 97
		self.base_luck = 100



trash = [LittleRat]
