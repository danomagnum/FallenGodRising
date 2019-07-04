from main import Character, Entity
import sys
import items
import elements
import moves

def gen_testuser():
	sys.stdout.silent = True
	battleuser = Fighter('Fighter Joe', 55)
	battleuser2 = Wizard('MiniMage', 50)

	user = Entity('playercharacter', combatants=[battleuser, battleuser2], item_list=[items.Potion(), items.Potion(), items.Booster(), items.HealAll()], char='@',is_player=True)

	sys.stdout.silent = False
	return user


class Fighter(Character):
	def config(self):
		self.moves = [moves.Strike(), moves.Buff()]
		self.base_physical_strength = 10 
		self.base_physical_defense = 10
		self.base_special_strength = 10
		self.base_special_defense = 10
		self.base_speed = 10
		self.base_hp = 10
		self.base_luck = 10
		self.movepool = {2: moves.}


class Wizard(Character):
	def config(self):
		self.moves = [moves.Blast(), moves.Focus()]
		self.base_physical_strength = 8 
		self.base_physical_defense = 8
		self.base_special_strength = 12
		self.base_special_defense = 12
		self.base_speed = 10
		self.base_hp = 10
		self.base_luck = 10
		self.movepool = {}

class Cleric(Character):
	def config(self):
		self.moves = [moves.Strike(), moves.Heal()]
		self.base_physical_strength = 8
		self.base_physical_defense = 12
		self.base_special_strength = 8
		self.base_special_defense = 12
		self.base_speed = 8
		self.base_hp = 12
		self.base_luck = 10
		self.movepool = {}

class Knight(Character):
	def config(self):
		self.moves = [moves.Strike(), moves.Taunt()]
		self.base_physical_strength = 12
		self.base_physical_defense = 12
		self.base_special_strength = 8
		self.base_special_defense = 8
		self.base_speed = 10
		self.base_hp = 10
		self.base_luck = 10
		self.movepool = {}

class Paladin(Character):
	def config(self):
		self.moves = [moves.Strike(), moves.LightBlast()]
		self.base_physical_strength = 12
		self.base_physical_defense = 10
		self.base_special_strength = 6
		self.base_special_defense = 12
		self.base_speed = 10
		self.base_hp = 10
		self.base_luck = 10
		self.movepool = {}

class Rogue(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 10
		self.base_physical_defense = 10
		self.base_special_strength = 8
		self.base_special_defense = 10
		self.base_speed = 12
		self.base_hp = 8
		self.base_luck = 12
		self.movepool = {}

class Dragoon(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 12
		self.base_physical_defense = 8
		self.base_special_strength = 10
		self.base_special_defense = 8
		self.base_speed = 12
		self.base_hp = 10
		self.base_luck = 10
		self.movepool = {}

class Juggernaut(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 15
		self.base_physical_defense = 15
		self.base_special_strength = 4
		self.base_special_defense = 4
		self.base_speed = 8
		self.base_hp = 14
		self.base_luck = 10
		self.movepool = {}

class Battlemage(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 8
		self.base_physical_defense = 12
		self.base_special_strength = 11
		self.base_special_defense = 11
		self.base_speed = 10
		self.base_hp = 10
		self.base_luck = 10
		self.movepool = {}

class Nightblade(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 12
		self.base_physical_defense = 8
		self.base_special_strength = 12
		self.base_special_defense = 8
		self.base_speed = 12
		self.base_hp = 8
		self.base_luck = 10
		self.movepool = {}

class Spellsword(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 12
		self.base_physical_defense = 8
		self.base_special_strength = 12
		self.base_special_defense = 8
		self.base_speed = 10
		self.base_hp = 10
		self.base_luck = 10
		self.movepool = {}

class Witchhunter(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 10
		self.base_physical_defense = 8
		self.base_special_strength = 8
		self.base_special_defense = 13
		self.base_speed = 11
		self.base_hp = 10
		self.base_luck = 10
		self.movepool = {}

