from main import Character, Entity
import sys
import items
import elements
import moves

def gen_testuser():
	sys.stdout.silent = True
	battleuser = Fighter('Fighter Joe', 55)
	battleuser2 = Wizard('MiniMage', 50)

	user = Entity('playercharacter', combatants=[battleuser, battleuser2], item_list=[items.Potion(self.game), items.Potion(self.game), items.Booster(self.game), items.HealAll(self.game)], char='@',is_player=True)

	sys.stdout.silent = False
	return user


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
		#self.movepool = {2: moves.}


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
		self.movepool = {}

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
		self.movepool = {}

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
		self.movepool = {}

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
		self.movepool = {}

class Rogue(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 100
		self.base_physical_defense = 100
		self.base_special_strength = 80
		self.base_special_defense = 100
		self.base_speed = 120
		self.base_hp = 80
		self.base_luck = 120
		self.movepool = {}

class Dragoon(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 120
		self.base_physical_defense = 80
		self.base_special_strength = 100
		self.base_special_defense = 80
		self.base_speed = 120
		self.base_hp = 120
		self.base_luck = 100
		self.movepool = {}

class Juggernaut(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 140
		self.base_physical_defense = 140
		self.base_special_strength = 60
		self.base_special_defense = 60
		self.base_speed = 60
		self.base_hp = 140
		self.base_luck = 100
		self.movepool = {}

class Battlemage(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 80
		self.base_physical_defense = 120
		self.base_special_strength = 100
		self.base_special_defense = 100
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100
		self.movepool = {}

class Nightblade(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 120
		self.base_physical_defense = 80
		self.base_special_strength = 120
		self.base_special_defense = 80
		self.base_speed = 100
		self.base_hp = 80
		self.base_luck = 100
		self.movepool = {}

class Witchhunter(Character):
	def config(self):
		self.moves = []
		self.base_physical_strength = 100
		self.base_physical_defense = 100
		self.base_special_strength = 60
		self.base_special_defense = 140
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100
		self.movepool = {}

