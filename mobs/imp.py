from .characters import Character, promote
import moves
import elements
import utility
import random


class Imp(Character):
	def config(self):
		self.moves = [moves.arc.Blast(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 60
		self.base_physical_strength = 48 
		self.base_physical_defense = 45
		self.base_arcane_strength = 43
		self.base_arcane_defense = 90
		self.base_speed = 42
		self.base_luck = 100

	def level_10(self):
		self.add_move(moves.stat.Focus)

	def level_17(self):
		self.add_move(moves.phy.Strike)

	def level_24(self):
		promote(self, Demon)	


class Demon(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.arc.Blast(self.game), moves.stat.Focus(self.game)]
		self.base_stats()

	def base_stats(self):
		self.base_hp = 85
		self.base_physical_strength = 73 
		self.base_physical_defense = 70
		self.base_arcane_strength = 73
		self.base_arcane_defense = 115
		self.base_speed = 67
		self.base_luck = 100
	

	def level_27(self):
		self.add_move(moves.arc.Wave)


trash = [Imp]
okay = [Demon]
mountains = [Imp]
sky = [Demon]
