from .characters import Character, promote
import moves
import elements
import utility
import random


class Hunter(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 39
		self.base_physical_strength = 52 
		self.base_physical_defense = 43
		self.base_arcane_strength = 60
		self.base_arcane_defense = 50
		self.base_speed = 65
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.choice(moves.typed_strikes))

	def level_16(self):
		promote(self, Rogue)	


class Rogue(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 58
		self.base_physical_strength = 64 
		self.base_physical_defense = 58
		self.base_arcane_strength = 80
		self.base_arcane_defense = 65
		self.base_speed = 80
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.choice(moves.typed_strikes))

	def level_36(self):
		promote(self, Ranger)	


class Ranger(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 78
		self.base_physical_strength = 84 
		self.base_physical_defense = 78
		self.base_arcane_strength = 109
		self.base_arcane_defense = 85
		self.base_speed = 100
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.choice(moves.typed_strikes))



starters = [Hunter]
