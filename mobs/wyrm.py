from .characters import Character, promote
import moves
import elements
import utility
import random


class Wyrm(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 75
		self.base_physical_strength = 100 
		self.base_physical_defense = 95
		self.base_arcane_strength = 40
		self.base_arcane_defense = 70
		self.base_speed = 110
		self.base_luck = 100



good = [Wyrm]
sky = [Wyrm]
