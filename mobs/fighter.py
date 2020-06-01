from .characters import Character, promote
import moves
import elements
import utility
import random


class Fighter(Character):
	def config(self):
		self.moves = [moves.Strike(self.game), moves.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 70
		self.base_physical_strength = 80 
		self.base_physical_defense = 50
		self.base_special_strength = 35
		self.base_special_defense = 35
		self.base_speed = 35
		self.base_luck = 100


	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.choice(moves.typed_strikes))
	
	def level_16(self):
		promote(self, Squire)	

class Squire(Character):
	def config(self):
		self.moves = [moves.Strike(self.game), moves.Buff(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 80
		self.base_physical_strength = 100 
		self.base_physical_defense = 70
		self.base_special_strength = 50
		self.base_special_defense = 60
		self.base_speed = 45
		self.base_luck = 100

	def level_36(self):
		promote(self, Knight)	

class Knight(Character):
	def config(self):
		self.moves = [moves.Strike(self.game), moves.Taunt(self.game)]
		self.base_stats()
	def base_stats(self):
		self.base_hp = 90
		self.base_physical_strength = 130
		self.base_physical_defense = 80
		self.base_special_strength = 65
		self.base_special_defense = 85
		self.base_speed = 55
		self.base_luck = 100



starters = [Fighter]
