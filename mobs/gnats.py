from .characters import Character, promote
import moves
import elements
import utility
import random


class Gnats(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()

	def base_stats(self):
		self.base_hp = 40
		self.base_physical_strength = 35 
		self.base_physical_defense = 30
		self.base_arcane_strength = 20
		self.base_arcane_defense = 20
		self.base_speed = 50
		self.base_luck = 100

	def level_8(self):
		promote(self, Skeeters)	

class Skeeters(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 45
		self.base_physical_strength = 25 
		self.base_physical_defense = 50
		self.base_arcane_strength = 25
		self.base_arcane_defense = 25
		self.base_speed = 35
		self.base_luck = 100

	def level_15(self):
		promote(self, Locusts)	

class Locusts(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Taunt(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 65
		self.base_physical_strength = 80
		self.base_physical_defense = 40
		self.base_arcane_strength = 45
		self.base_arcane_defense = 80
		self.base_speed = 75
		self.base_luck = 100


trash = [Gnats]
okay = [Skeeters]
good = [Locusts]
marsh = [Gnats, Skeeters, Locusts]
desert = [Locusts]
forest = [Skeeters]
