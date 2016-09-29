import random
import math

TARGET_NONE = 0
TARGET_COMBATANT = 1
TARGET_COMMANDER = 2
class Item(object):
	def __init__(self, name, target=TARGET_NONE):
		self.name = name
		self.target_type = target

	def use(target = None):
		pass

class Element(object):
	def __init__(self, name, nominal = 1.0, bonus=1.5):
		self.name = name
		self.nominal_modifier = nominal
		self.special_modifiers = {}
		self.bonus = bonus

	def effectiveness(self, defending_element):
		return self.special_modifiers[defending_element] if (defending_element in self.special_modifiers) else self.nominal_modifier

MULTI_SELF = 4
MULTI_ENEMY = 3
ACTIVE = 2
ENEMY = 1
SELF = 0
class Move(object):
	def __init__(self,name, elements, accuracy, power, mp, effects, default_target):
		self.name = name
		self.mp = mp
		self.max_mp = mp
		self.accuracy = accuracy
		self.power = power
		self.elements = elements
		self.uses = 0
		self.effects = effects
		self.default_target = default_target

	def attack(self, user, targets): # do whatever the attack needs to do
		if (self.mp > 0):
			print user.name, 'used move', self.name
			self.mp -= 1
		else:
			print user.name, 'is out of mp to use move', self.name
			self.mp = 0
			if 0.2 > random.random():
				print user.name, 'used move', self.name
			else:
				return

		for target in targets:
			hit_chance = ((user.speed/target.speed)/9) + user.accuracy/target.evasion * self.accuracy
			val =  user.physical_strength/target.physical_strength

			if hit_chance > random.random():
				if self.power > 0:
					damage = ((user.level/100.0 ) * user.physical_strength/target.physical_defense * self.power)

					for atk_element in self.elements:
						for target_element in target.elements:
							damage *= atk_element.effectiveness(target_element)
						for user_element in user.elements:
							if user_element == atk_element:
								damage *= atk_element.bonus

					self.uses += 1

					damage += ((damage + 1) * 3 * min(self.uses, 100.0) / 100.0 + 5) / 10.0
					damage = random.normalvariate(damage, damage/8.0) # normal distribution with stdev of 8% for randomness
					damage = max(1,damage)

					target.hp -= damage

				for effect, chance in self.effects:
					if chance > random.random():
						target.status.append(effect)
						print target.name, 'was effected by', effect.name
	def __str__(self):
		string = ''
		string += self.name + ' '
		string += '( ' + str(int(self.mp)) + '/' + str(int(self.max_mp)) + ' )'
		return string



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
		effected.status.remove(self)
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
		self._exp = 0
		self.moves = []
		self.elements = []
		self.status = []
		self.coefficients = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
		self._level = 1
		self.level = 1
		self.base_physical_strength = 10
		self.base_physical_defense = 10
		self.base_special_strength = 10
		self.base_special_defense = 10
		self.base_speed = 10
		self.base_hp = 10
		self._hp = self.max_hp

	def __str__(self):
		return self.name

	@property
	def level(self):
		return self._level

	@level.setter
	def level(self, value):
		self._level = value
		print self.name, 'leveled up to ', self.level
		self._exp = self.exp_at_level(self.level)
		self.heal()

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
	def levelup(self):
		pass

class User(object):
	def __init__(self, name, combatants, items=None):
		self.name = name
		self.combatants = combatants
		self.combatant = combatants[0]
		if items is None:
			self.items = []
		else:
			self.items = items
	def get_available(self):
		return [ combatant for combatant in self.combatants if combatant.hp > 0 ] 
	
	def get_standby(self):
		return [ combatant for combatant in self.combatants if (combatant.hp > 0) and combatant != self.combatant ] 
	
