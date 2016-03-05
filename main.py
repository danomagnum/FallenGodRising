import random

class Element(object):
	def __init__(self, name, nominal = 1.0, bonus=1.5):
		self.name = name
		self.nominal_modifier = nominal
		self.special_modifiers = {}
		self.bonus = bonus

	def effectiveness(self, defending_element):
		return self.special_modifiers[defending_element] if (defending_element in self.special_modifiers) else self.nominal_modifier


class Move(object):
	def __init__(self,name, elements, accuracy, mp):
		self.name = name
		self.mp = mp
		self.max_mp = mp
		self.mp_cost = cost
		self.accuracy = accuracy
		self.elements = elements
		self.uses = 0

	def attack(self, user, target): # do whatever the attack needs to do
		self.uses += 1
		pass

class Status(object):
	def __init__(self, name=None):
		if name is None:
			self.name = 'Status'
		else:
			self.name = name
		self.expired = False
	def pre_battle(self, effected):
		pass
	def pre_turn(self, effected):
		pass
	def pre_attack(self, effected):
		pass
	def allow_attack(self, effected): # something like paralyze would use this to prevent attacking.
		return True
	def post_attack(self, effected): # things like poison should happen here.
		pass
	def post_turn(self, effected):
		pass
	def post_battle(self, effected):
		pass
	def physical_strength(self, initial): # passive stat boosts take effect on these routines
		return initial
	def physical_defense(self, initial):
		return initial
	def special_strength(self, initial):
		return initial
	def special_defense(self, initial):
		return initial
	def speed(self, initial):
		return initial
	def hp(self, initial):
		return initial
	def max_hp(self, initial):
		return initial
	def evasion(self, initial):
		return initial
	def accuracy(self, initial):
		return initial

class Character(object):
	def __init__(self):
		self.setup('')

	def setup(self, name=None):
		if name is None:
			self.name = 'MissingNo'
		else:
			self.name = name
		self.moves = []
		self.elements = []
		self.status = []
		self.coefficients = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
		self.level = 1
		self.base_physical_strength = 10
		self.base_physical_defense = 10
		self.base_special_strength = 10
		self.base_special_defense = 10
		self.base_speed = 10
		self.base_hp = 10
		self._hp = self.max_hp

	@property
	def physical_strength(self):
		stat = (self.base_physical_strength + self.coefficients[0]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.physical_strength(stat)
		print 'strength: ', stat
		return stat
	@property
	def physical_defense(self):
		stat = (self.base_physical_defense + self.coefficients[1]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.physical_defense(stat)
		return stat
	@property
	def special_strength(self):
		stat = (self.base_special_strength + self.coefficients[2]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.special_strength(stat)
		return stat
	@property
	def special_defense(self):
		stat = (self.base_special_defense + self.coefficients[3]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.special_defense(stat)
		return stat
	@property
	def speed(self):
		stat = (self.base_speed + self.coefficients[4]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.speed(stat)
		return stat

	@property
	def hp(self):
		stat = self._hp
		for status in self.status:
			stat = status.hp(stat)
		return  min(max(0,stat), self.max_hp)
	
	@hp.setter
	def hp(self, value):
		self._hp = min(max(0,value), self.max_hp)

	@property
	def max_hp(self):
		stat = int((self.base_hp + self.coefficients[5]) * 10 * self.level / 100.0 + 5)
		for status in self.status:
			stat = status.max_hp(stat)
		return stat

	@property
	def evasion(self):
		stat = 1.0
		for status in self.status:
			stat = status.evasion(stat)
		return stat

	@property
	def accuracy(self):
		stat = 1.0
		for status in self.status:
			stat = status.accuracy(stat)
		return stat

	def heal(self):
		for move in self.moves:
			move.mp = move.max_mp
			self.hp = self.max_hp


class Battle(object):
	pass
