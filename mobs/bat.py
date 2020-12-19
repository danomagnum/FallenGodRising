from .characters import Character, promote
import moves
import elements
import utility
import random


class Bat(Character):
	def config(self):
		self.moves = [moves.phy.Swoop(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 20
		self.base_physical_strength = 10 
		self.base_physical_defense = 55
		self.base_arcane_strength = 15
		self.base_arcane_defense = 20
		self.base_speed = 80
		self.base_luck = 100
		self.element_pref = [elements.Fire, elements.Electric, elements.Wind, elements.Dark]

	def level_15(self):
		self.add_move(moves.phy.Bite)

	def level_20(self):
		promote(self, Vampire)	


class Vampire(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game), moves.heal.Absorb(self.game)]
		self.base_stats()

	def base_stats(self):
		self.base_hp = 95
		self.base_physical_strength = 125 
		self.base_physical_defense = 79
		self.base_arcane_strength = 60
		self.base_arcane_defense = 100
		self.base_speed = 81
		self.base_luck = 100
		self.element_pref = [elements.Fire, elements.Electric, elements.Dark]
	
	def level_25(self):
		self.add_move(moves.stat.Drain)
		



trash = [Bat]
good = [Vampire]
underground = [Bat, Vampire]
