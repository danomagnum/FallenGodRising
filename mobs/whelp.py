from .characters import Character, promote
import moves
import elements
import utility
import random


class Whelp(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()

	def base_stats(self):
		self.base_hp = 41
		self.base_physical_strength = 64 
		self.base_physical_defense = 45
		self.base_arcane_strength = 50
		self.base_arcane_defense = 50
		self.base_speed = 50
		self.base_luck = 100

	def level_30(self):
		promote(self, Drake)	

class Drake(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 61
		self.base_physical_strength = 84 
		self.base_physical_defense = 65
		self.base_arcane_strength = 70
		self.base_arcane_defense = 70
		self.base_speed = 70
		self.base_luck = 100

	def level_55(self):
		promote(self, Dragon)	

class Dragon(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Taunt(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 91
		self.base_physical_strength = 134
		self.base_physical_defense = 95
		self.base_arcane_strength = 100
		self.base_arcane_defense = 100
		self.base_speed = 80
		self.base_luck = 100



okay = [Whelp, Drake]
good = [Dragon]
marsh = [Whelp]
desert = [Drake]
sky = [Dragon]
