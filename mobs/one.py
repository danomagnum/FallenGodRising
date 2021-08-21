from .characters import Character, promote
import moves
import elements
import utility
import random


class TheOne(Character):
	def config(self):
		self.moves = [moves.arc.Blast(self.game),
		              moves.phy.Rush(self.game),
			      moves.heal.Heal(self.game),
			      moves.stat.Focus(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 106
		self.base_physical_strength = 110 
		self.base_physical_defense = 90
		self.base_arcane_strength = 154
		self.base_arcane_defense = 90
		self.base_speed = 130
		self.base_luck = 120
		self.element_pref = [elements.Light]

