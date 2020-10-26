from .characters import Character, promote
import moves
import elements
import utility
import random


class Spirit(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 90
		self.base_physical_strength = 65 
		self.base_physical_defense = 65
		self.base_arcane_strength = 40
		self.base_arcane_defense = 40
		self.base_speed = 15
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.choice(moves.typed_strikes))

	def level_16(self):
		promote(self, Spectre)	


class Spectre(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 95
		self.base_physical_strength = 75 
		self.base_physical_defense = 110
		self.base_arcane_strength = 100
		self.base_arcane_defense = 80
		self.base_speed = 30
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.choice(moves.typed_strikes))

	def level_36(self):
		promote(self, Ghoul)	


class Ghoul(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 95
		self.base_physical_strength = 75 
		self.base_physical_defense = 80
		self.base_arcane_strength = 100
		self.base_arcane_defense = 110
		self.base_speed = 30
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.choice(moves.typed_strikes))



#starters = [Spirit]
