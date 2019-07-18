from main import Character, Entity
import sys
import items
import elements
import moves
import random


class Fighter(Character):
	def config(self):
		self.moves = [moves.Strike(self.game), moves.Buff(self.game)]
		self.base_physical_strength = 100 
		self.base_physical_defense = 100
		self.base_special_strength = 100
		self.base_special_defense = 100
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100

	def level_03(self):
		if self.elements[0] in moves.typed_blasts:
			preferred_move = moves.typed_strikes.index(self.element)
			if (random.random() * self.luck) > 50:
				self.add_move(preferred_move)
				return
		self.add_move(random.choice(moves.typed_strikes))

class Wizard(Character):
	def config(self):
		self.moves = [moves.Blast(self.game), moves.Focus(self.game)]
		self.base_physical_strength = 80 
		self.base_physical_defense = 80
		self.base_special_strength = 120
		self.base_special_defense = 120
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100

class Cleric(Character):
	def config(self):
		self.moves = [moves.Strike(self.game), moves.Heal(self.game)]
		self.base_physical_strength = 80
		self.base_physical_defense = 120
		self.base_special_strength = 80
		self.base_special_defense = 120
		self.base_speed = 80
		self.base_hp = 120
		self.base_luck = 100

class Knight(Character):
	def config(self):
		self.moves = [moves.Strike(self.game), moves.Taunt(self.game)]
		self.base_physical_strength = 120
		self.base_physical_defense = 120
		self.base_special_strength = 80
		self.base_special_defense = 80
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100

class Paladin(Character):
	def config(self):
		self.moves = [moves.Strike(self.game), moves.LightBlast(self.game)]
		self.base_physical_strength = 110
		self.base_physical_defense = 110
		self.base_special_strength = 50
		self.base_special_defense = 110
		self.base_speed = 100
		self.base_hp = 110
		self.base_luck = 100

class Rogue(Character):
	def config(self):
		self.moves = [moves.Strike(self.game), moves.Poison(self.game)]
		self.base_physical_strength = 100
		self.base_physical_defense = 100
		self.base_special_strength = 80
		self.base_special_defense = 100
		self.base_speed = 120
		self.base_hp = 80
		self.base_luck = 120

class Dragoon(Character):
	def config(self):
		self.moves = [moves.Strike(self.game), moves.Smoke(self.game)]
		self.base_physical_strength = 120
		self.base_physical_defense = 80
		self.base_special_strength = 100
		self.base_special_defense = 80
		self.base_speed = 120
		self.base_hp = 120
		self.base_luck = 100

class Juggernaut(Character):
	def config(self):
		self.moves = [moves.Strike(self.game)]
		self.base_physical_strength = 140
		self.base_physical_defense = 140
		self.base_special_strength = 60
		self.base_special_defense = 60
		self.base_speed = 60
		self.base_hp = 140
		self.base_luck = 100

class Battlemage(Character):
	def config(self):
		self.moves = [moves.Blast(self.game), moves.Protect(self.game)]
		self.base_physical_strength = 80
		self.base_physical_defense = 120
		self.base_special_strength = 100
		self.base_special_defense = 100
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100

class Nightblade(Character):
	def config(self):
		self.moves = [moves.Strike(self.game), moves.Blast(self.game)]
		self.base_physical_strength = 120
		self.base_physical_defense = 80
		self.base_special_strength = 120
		self.base_special_defense = 80
		self.base_speed = 100
		self.base_hp = 80
		self.base_luck = 100

class Witchhunter(Character):
	def config(self):
		print 'witchhunter'
		self.moves = [moves.Strike(self.game), moves.Haste(self.game)]
		self.base_physical_strength = 100
		self.base_physical_defense = 100
		self.base_special_strength = 60
		self.base_special_defense = 140
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100

