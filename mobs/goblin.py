from .characters import Character, promote
import moves
import elements
import utility
import random


class Goblin(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 46
		self.base_physical_strength = 57 
		self.base_physical_defense = 40
		self.base_arcane_strength = 40
		self.base_arcane_defense = 40
		self.base_speed = 50
		self.base_luck = 100

	def level_16(self):
		promote(self, HobGoblin)	


class HobGoblin(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 61
		self.base_physical_strength = 72 
		self.base_physical_defense = 57
		self.base_arcane_strength = 55
		self.base_arcane_defense = 55
		self.base_speed = 65
		self.base_luck = 100

	def level_40(self):
		promote(self, GoblinLord)	


class GoblinLord(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 81
		self.base_physical_strength = 92 
		self.base_physical_defense = 77
		self.base_arcane_strength = 85
		self.base_arcane_defense = 75
		self.base_speed = 85
		self.base_luck = 100




trash = [Goblin]
okay = [HobGoblin]
good = [GoblinLord]
plains = [Goblin, HobGoblin]
