from .characters import Character
import moves
import elements
import utility
import random


class Priest(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 55
		self.base_physical_strength = 47 
		self.base_physical_defense = 52
		self.base_arcane_strength = 40
		self.base_arcane_defense = 40
		self.base_speed = 41
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.sample(moves.typed_strikes,1)[0])

	def level_16(self):
		promote(self, Cleric)	


class Cleric(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 70
		self.base_physical_strength = 62 
		self.base_physical_defense = 67
		self.base_arcane_strength = 55
		self.base_arcane_defense = 55
		self.base_speed = 56
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.sample(moves.typed_strikes,1)[0])

	def level_36(self):
		promote(self, Paladin)	


class Paladin(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 90
		self.base_physical_strength = 82 
		self.base_physical_defense = 87
		self.base_arcane_strength = 75
		self.base_arcane_defense = 85
		self.base_speed = 76
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.sample(moves.typed_strikes,1)[0])



starters = [Priest]
