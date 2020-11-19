from .characters import Character, promote
import moves
import elements
import utility
import random


class Zombie(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 65
		self.base_physical_strength = 95 
		self.base_physical_defense = 57
		self.base_arcane_strength = 100
		self.base_arcane_defense = 85
		self.base_speed = 93
		self.base_luck = 100



good = [Zombie]
