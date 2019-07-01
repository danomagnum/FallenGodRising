from main import Character, Entity
import sys
import items
import elements
import moves


class Fighter(Character):
	def config(self):
		self.moves = [moves.Pound(), moves.Slam(), moves.Buff()]
		self.elements = [elements.Normal]
		self.status = []
		self.coefficients = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
		self.base_physical_strength = 10
		self.base_physical_defense = 10
		self.base_special_strength = 10
		self.base_special_defense = 10
		self.base_speed = 10
		self.base_hp = 10

class Page(Character):
	def config(self):
		self.moves = [moves.Pound(), moves.Poison(), moves.Spray()]
		self.elements = [elements.Fire]
		self.status = []
		self.coefficients = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
		self.base_physical_strength = 8
		self.base_physical_defense = 8
		self.base_special_strength = 12
		self.base_special_defense = 12
		self.base_speed = 10
		self.base_hp = 10

class Cleric(Character):
	def config(self):
		self.moves = [moves.Pound(), moves.Heal()]
		self.elements = [elements.Water]
		self.status = []
		self.coefficients = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
		self.base_physical_strength = 8
		self.base_physical_defense = 12
		self.base_special_strength = 8
		self.base_special_defense = 12
		self.base_speed = 8
		self.base_hp = 12

def gen_testuser():
	sys.stdout.silent = True
	battleuser = Fighter('Fighter Joe', 55)
	battleuser2 = Page('MiniMage', 50)

	user = Entity('playercharacter', combatants=[battleuser, battleuser2], item_list=[items.Potion(), items.Potion(), items.Booster(), items.HealAll()], char='@')

	sys.stdout.silent = False
	return user


