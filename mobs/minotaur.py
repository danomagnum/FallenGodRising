from .characters import Character, promote
import moves
import elements
import utility
import random


class Minotaur(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()

	def base_stats(self):
		self.base_hp = 105
		self.base_physical_strength = 95
		self.base_physical_defense = 80
		self.base_arcane_strength = 40
		self.base_arcane_defense = 80
		self.base_speed = 90
		self.base_luck = 100



okay = [Minotaur]
