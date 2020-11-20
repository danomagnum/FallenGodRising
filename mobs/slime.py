from .characters import Character, promote
import moves
import elements
import utility
import random


class Slime(Character):
	def config(self):
		self.moves = [moves.arc.Blast(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 70
		self.base_physical_strength = 45 
		self.base_physical_defense = 48
		self.base_arcane_strength = 60
		self.base_arcane_defense = 65
		self.base_speed = 35
		self.base_luck = 100

	def level_26(self):
		promote(self, Glob)	


class Glob(Character):
	def config(self):
		self.moves = [moves.arc.Blast(self.game), moves.stat.Focus(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 95
		self.base_physical_strength = 70 
		self.base_physical_defense = 73
		self.base_arcane_strength = 85
		self.base_arcane_defense = 90
		self.base_speed = 60
		self.base_luck = 100



trash = [Slime]
okay = [Glob]
marsh = [Slime, Glob]
plains = [Slime, Glob]
sea = [Slime, Glob]
