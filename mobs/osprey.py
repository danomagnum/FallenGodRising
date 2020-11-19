from .characters import Character, promote
import moves
import elements
import utility
import random


class Osprey(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()

	def base_stats(self):
		self.base_hp = 40
		self.base_physical_strength = 45 
		self.base_physical_defense = 40
		self.base_arcane_strength = 35
		self.base_arcane_defense = 35
		self.base_speed = 56
		self.base_luck = 100

	def level_18(self):
		promote(self, Hawk)	


class Hawk(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()

	def base_stats(self):
		self.base_hp = 63
		self.base_physical_strength = 60 
		self.base_physical_defense = 55
		self.base_arcane_strength = 50
		self.base_arcane_defense = 50
		self.base_speed = 71
		self.base_luck = 100

	def level_36(self):
		promote(self, Eagle)	


class Eagle(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()

	def base_stats(self):
		self.base_hp = 83
		self.base_physical_strength = 80 
		self.base_physical_defense = 75
		self.base_arcane_strength = 70
		self.base_arcane_defense = 70
		self.base_speed = 91
		self.base_luck = 100





trash = [Osprey]
okay = [Hawk]
good = [Eagle]
