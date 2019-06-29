import random
import math
import utility
import items
from targets import *


class Move(object):
	def __init__(self,name, elements, accuracy, power, mp,  default_target):
		self.name = name
		self.mp = mp
		self.max_mp = mp
		self.accuracy = accuracy
		self.power = power
		self.elements = elements
		self.uses = 0
		self.default_target = default_target

	def attack(self, user, targets): # do whatever the attack needs to do
		if (self.mp > 0):
			print('{} used move {}'.format(user.name,self.name))
			self.mp -= 1
		else:
			print('{} is out of MP to use move {}'.format(user.name,self.name))
			self.mp = 0
			if 0.2 > random.random():
				print('{} used move {}'.format(user.name,self.name))
			else:
				return
		target_coefficient = 1.1 / len(targets)

		for target in targets:
			hit_chance = ((user.speed/target.speed)/9) + user.accuracy/target.evasion * self.accuracy
			val =  user.physical_strength/target.physical_strength

			if hit_chance > random.random():
				if self.power > 0:
					damage = ((user.level/100.0 ) * user.physical_strength/target.physical_defense * self.power) * target_coefficient

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

				self.effect(target)
	def effect(self, target):
		pass
	def __str__(self):
		string = ''
		string += self.name + ' '
		string += '( ' + str(int(self.mp)) + '/' + str(int(self.max_mp)) + ' )'
		return string


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
		print('{} leveled up to {}'.format(self.name, self.level))
		self._exp = self.exp_at_level(self.level)
		self.full_heal()

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
		return utility.clamp(stat, 1, 3* self.base_physical_strength)
	@property
	def physical_defense(self):
		stat = (self.base_physical_defense + self.coefficients[1]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.physical_defense(stat)
		return utility.clamp(stat, 1, 3* self.base_physical_defense)
	@property
	def special_strength(self):
		stat = (self.base_special_strength + self.coefficients[2]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.special_strength(stat)
		return utility.clamp(stat, 1, 3* self.base_special_strength)
	@property
	def special_defense(self):
		stat = (self.base_special_defense + self.coefficients[3]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.special_defense(stat)
		return utility.clamp(stat, 1, 3* self.base_special_defense)
	@property
	def speed(self):
		stat = (self.base_speed + self.coefficients[4]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.speed(stat)
		return utility.clamp(stat, 1, 3* self.base_speed)

	@property
	def hp(self):
		stat = self._hp
		for status in self.status:
			stat = status.hp(stat)
		return  min(max(0,stat), self.max_hp)
	
	@hp.setter
	def hp(self, value):
		self._hp = min(max(0,value), self.max_hp)

	def heal(self, amount):
		self._hp = min(max(0,self._hp + amount), self.max_hp)

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

	def full_heal(self):
		for move in self.moves:
			move.mp = move.max_mp
			self.hp = self.max_hp
	def levelup(self):
		pass

class User(object):
	def __init__(self, name, combatants, item_list=None):
		self.name = name
		self.combatants = combatants
		self.combatant = combatants[0]
		self.backpack = items.Backpack()
		if item_list is not None:
			for item in item_list:
				self.backpack.store(item)

	def get_available(self):
		return [ combatant for combatant in self.combatants if combatant.hp > 0 ] 
	
	def get_standby(self):
		return [ combatant for combatant in self.combatants if (combatant.hp > 0) and combatant != self.combatant ] 
	
