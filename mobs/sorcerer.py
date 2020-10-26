from .characters import Character, promote
import moves
import elements
import utility
import random


class Sorcerer(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 25
		self.base_physical_strength = 20 
		self.base_physical_defense = 15
		self.base_arcane_strength = 105
		self.base_arcane_defense = 55
		self.base_speed = 90
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.choice(moves.typed_strikes))

	def level_16(self):
		promote(self, Wizard)	

class Wizard(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 40
		self.base_physical_strength = 35 
		self.base_physical_defense = 30
		self.base_arcane_strength = 120
		self.base_arcane_defense = 70
		self.base_speed = 105
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.choice(moves.typed_strikes))

	def level_36(self):
		promote(self, Archmage)	

class Archmage(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 55
		self.base_physical_strength = 50 
		self.base_physical_defense = 45
		self.base_arcane_strength = 135
		self.base_arcane_defense = 85
		self.base_speed = 120
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.choice(moves.typed_strikes))




starters = [Sorcerer]
