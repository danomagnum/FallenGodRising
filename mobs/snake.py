from .characters import Character, promote
import moves
import elements
import utility
import random


class Snake(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 30
		self.base_physical_strength = 40 
		self.base_physical_defense = 70
		self.base_arcane_strength = 70
		self.base_arcane_defense = 25
		self.base_speed = 60
		self.base_luck = 100
		self.element_pref = [elements.Water, elements.Earth, elements.Electric]

	def level_24(self):
		promote(self, Serpent)	


class Serpent(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 55
		self.base_physical_strength = 65 
		self.base_physical_defense = 95
		self.base_arcane_strength = 95
		self.base_arcane_defense = 45
		self.base_speed = 85
		self.base_luck = 100
		self.element_pref = [elements.Water, elements.Earth, elements.Electric]



trash = [Snake]
okay = [Serpent]
forest = [Snake, Serpent]
desert = [Snake, Serpent]
