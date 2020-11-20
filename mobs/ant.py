from .characters import Character, promote
import moves
import elements
import utility
import random


class Ant(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 35
		self.base_physical_strength = 70 
		self.base_physical_defense = 55
		self.base_arcane_strength = 45
		self.base_arcane_defense = 55
		self.base_speed = 25
		self.base_luck = 100

	def level_24(self):
		promote(self, FireAnt)	


class FireAnt(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 60
		self.base_physical_strength = 95 
		self.base_physical_defense = 80
		self.base_arcane_strength = 60
		self.base_arcane_defense = 80
		self.base_speed = 30
		self.base_luck = 100



trash = [Ant]
okay = [FireAnt]
desert = [Ant, FireAnt]
