from .characters import Character, promote
import moves
import elements
import utility
import random


class Echo(Character):
	def config(self):
		self.moves = [moves.arc.Blast(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 35
		self.base_physical_strength = 55 
		self.base_physical_defense = 30
		self.base_arcane_strength = 50
		self.base_arcane_defense = 40
		self.base_speed = 90
		self.base_luck = 100

	def level_22(self):
		promote(self, Shadow)	


class Shadow(Character):
	def config(self):
		self.moves = [moves.arc.Blast(self.game), moves.stat.Focus(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 60
		self.base_physical_strength = 90 
		self.base_physical_defense = 55
		self.base_arcane_strength = 90
		self.base_arcane_defense = 80
		self.base_speed = 100
		self.base_luck = 100



trash = [Echo]
okay = [Shadow]
