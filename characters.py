import main
import sys
import items
import elements
import moves
import random
import utility

class Character(object):
	def __init__(self, game,  name=None, level=1):
		self.game = game
		self.initialized = False
		if name is None:
			#self.name = 'MissingNo'
			self.name = self.__class__.__name__
		else:
			self.name = name
		self._hp = 1
		self._exp = 0
		self._elements = [elements.Normal]
		self.status = []
		self.equipment = main.Equipment(game)
		# stat growth rate for p.str, p.def, s.str, s.def, speed, maxhp
		self.coefficients = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
		self.helptext = ''
		self.moves = []
		self._level = 1
		self.stat_randomizer()
		utility.call_all('config', self)
		#utility.call_all_configs(self)

		self.level = level
		self.full_heal()
		self._exp = self.exp_at_level(self.level)
		self.initialized = True

	@property
	def elements(self):
		e_list = self._elements
		for item in self.equipment.all_items():
			e_list = item.elements(e_list)
		return e_list

	@elements.setter
	def elements(self, value):
		self._elements = value

	def stat_randomizer(self):
		# when the entity is created, give it some variety in power
		# nominally 1.0 +- 5%
		BASE = 1.0
		DEV = 0.05
		self.mod_physical_strength = random.normalvariate(BASE, DEV)
		self.mod_physical_defense = random.normalvariate(BASE, DEV)
		self.mod_special_strength = random.normalvariate(BASE, DEV)
		self.mod_special_defense = random.normalvariate(BASE, DEV)
		self.mod_speed = random.normalvariate(BASE, DEV)
		self.mod_hp = random.normalvariate(BASE, DEV)
		self.mod_luck = random.normalvariate(BASE, DEV)


	def config(self):
		self.moves = []
		self.base_physical_strength = 10
		self.base_physical_defense = 10
		self.base_special_strength = 10
		self.base_special_defense = 10
		self.base_speed = 10
		self.base_hp = 10
		self.base_luck = 100
		self.physical = True
	
	def tick(self):
		pass

	def battletick(self):
		for item in self.equipment.all_items():
			item.subtick(self)
			item.tick(self)
		for move in self.moves:
			#sys.stderr.write(str(move))
			move.tick(self)

	def subtick(self):
		for item in self.equipment.all_items():
			utility.call_all('tick', item, self)
			utility.call_all('subtick', item, self)
		for move in self.moves:
			#sys.stderr.write(str(move))
			utility.call_all('tick', move, self)
			#move.tick(self)
		for stat in self.status:
			utility.call_all('tick', stat, self)
			#stat.tick(self)

	def __str__(self):
		return self.name

	@property
	def level(self):
		return self._level

	@level.setter
	def level(self, value):
		if self.initialized:
			print('{} leveled up from {} to {}'.format(self.name, self._level, value))
		if value > self._level:
			for lvl in range(self._level + 1, value + 1):
				self._level = lvl
				self._exp = self.exp_at_level(self.level)
				self.levelup()
				level_method = 'level_{:02}'.format(lvl)
				try:
					method = getattr(self, level_method)
				except:
					method = None
				if method is not None:
					method()
		self.partial_heal()
	
	def add_move(self, move):
		m = move(self.game)
		if self.initialized:
			print('{} Gained The Skill {}'.format(self.name, m.name))
		self.moves.append(m)

	@property
	def exp(self):
		return self._exp

	@exp.setter
	def exp(self, value):
		self._exp = value
		check_level = True
		while check_level:
			if self._exp > self.exp_at_level(self.level + 1):
				self.level += 1
			else:
				check_level = False

	@property
	def exp_value(self):
		val = self.physical_strength + self.physical_defense
		val += self.special_strength + self.special_defense
		val += self.speed + self.max_hp
		val *= self.level / 6
		return int(val)

	def exp_at_level(self, level):
		return (level ) ** 3

	def exp_progress(self):
		return (float(self.exp) - float(self.exp_at_level(self.level)) ) / float(self.exp_at_level(self.level + 1))
	@property
	def physical_strength(self):
		stat = (self.base_physical_strength + self.coefficients[0]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.physical_strength(stat)
		stat = self.equipment.physical_strength(stat)
		stat = stat * self.mod_physical_strength
		return utility.clamp(stat, 1, 3* self.base_physical_strength)
	@property
	def physical_defense(self):
		stat = (self.base_physical_defense + self.coefficients[1]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.physical_defense(stat)
		stat = self.equipment.physical_defense(stat)
		stat = stat * self.mod_physical_defense
		return utility.clamp(stat, 1, 3* self.base_physical_defense)
	@property
	def special_strength(self):
		stat = (self.base_special_strength + self.coefficients[2]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.special_strength(stat)
		stat = self.equipment.special_strength(stat)
		stat = stat * self.mod_special_strength
		return utility.clamp(stat, 1, 3* self.base_special_strength)
	@property
	def special_defense(self):
		stat = (self.base_special_defense + self.coefficients[3]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.special_defense(stat)
		stat = self.equipment.special_defense(stat)
		stat = stat * self.mod_special_defense
		return utility.clamp(stat, 1, 3* self.base_special_defense)

	@property
	def speed(self):
		stat = (self.base_speed + self.coefficients[4]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.speed(stat)
		stat = self.equipment.speed(stat)
		stat = stat * self.mod_speed
		return utility.clamp(stat, 1, 3* self.base_speed)

	def raw_hp(self):
		return self._hp

	@property
	def hp(self):
		stat = self._hp
		for status in self.status:
			stat = status.hp(stat)
		stat = self.equipment.hp(stat)
		return  min(max(0,stat), self.max_hp)
	
	@property
	def luck(self):
		stat = float(self.base_luck) / 100.0 # One point of luck is a 2% change. Will need balanced.
		for status in self.status:
			stat = status.luck(stat)
		stat = self.equipment.luck(stat)
		stat = stat * self.mod_luck
		return utility.clamp(stat, 0.1, 3* self.base_luck)

	@hp.setter
	def hp(self, value):
		self._hp = utility.clamp(value, 0, self.max_hp)

	def heal(self, amount):
		if self.hp > 0:
			self._hp = min(max(0,self._hp + amount), self.max_hp)

	@property
	def max_hp(self):
		stat = int((self.base_hp + self.coefficients[5]) * 10 * self.level / 100.0 + 5)
		for status in self.status:
			stat = status.max_hp(stat)
		stat = self.equipment.max_hp(stat)
		stat = stat * self.mod_hp
		return stat

	@property
	def virtual_hp(self):
		stat = int((100 + self.coefficients[5]) * 10 * self.level / 100.0 + 5)
		return stat


	@property
	def evasion(self):
		stat = 1.0
		for status in self.status:
			stat = status.evasion(stat)
		stat = self.equipment.evasion(stat)
		return stat

	@property
	def accuracy(self):
		stat = 1.0
		for status in self.status:
			stat = status.accuracy(stat)
		stat = self.equipment.accuracy(stat)
		return stat

	def full_heal(self):
		for move in self.moves:
			move.mp = move.max_mp
		if self.hp > 0:
			self.hp = self.max_hp

	def partial_heal(self):
		for move in self.moves:
			move.mp += int(move.max_mp / 5)
		if self.hp > 0:
			self.hp += int(self.max_hp / 5)

	def levelup(self): # override this with sub classes to do fancy things
		pass

	def revive(self):
		if self.hp <= 0:
			self.hp = 1



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
		#self.moves = [moves.Strike(self.game), moves.LightBlast(self.game)]
		self.moves = [moves.Strike(self.game), moves.mod_move(moves.Blast, moves.LightMove)(self.game)]
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
		self.moves = [moves.Strike(self.game), moves.Haste(self.game)]
		self.base_physical_strength = 100
		self.base_physical_defense = 100
		self.base_special_strength = 60
		self.base_special_defense = 140
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100


class Debug(Character):
	def config(self):
		self.moves = [moves.Strike(self.game),
		              moves.Haste(self.game),
		              moves.Wave(self.game),
		              moves.SelfDestruct(self.game),
		              moves.Transfuse(self.game),
			      moves.mod_move(moves.Strike, moves.Piercing)(self.game),
			      moves.mod_move(moves.mod_move(moves.Strike, moves.Piercing), moves.Multi)(self.game),
			      moves.mod_move(moves.Strike, moves.Poison)(self.game),
			      moves.mod_move(moves.mod_move(moves.Strike, moves.Poison), moves.Piercing)(self.game)]
		self.base_physical_strength = 100
		self.base_physical_defense = 100
		self.base_special_strength = 60
		self.base_special_defense = 140
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100

