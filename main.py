import random
import math
import utility
import items
import elements
from targets import *

class GameOver(Exception):
	pass

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


class Equipment(object):
	def __init__(self):
		self.Head = None
		self.Body = None
		self.Legs = None
		self.Left = None
		self.Right = None
		self.Hands = None
		self.Token = None
	
	def equip(self, item):
		return_items = []
		if item.target_type == EQUIP_HEAD:
			if self.Head is not None:
				return_items.append(self.Head)
			self.Head = item
		elif item.target_type == EQUIP_BODY:
			if self.Body is not None:
				return_items.append(self.Body)
			self.Body = item
		elif item.target_type == EQUIP_LEGS:
			if self.Legs is not None:
				return_items.append(self.Legs)
			self.Legs = item
		elif item.target_type == EQUIP_RIGHT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Right is not None:
				return_items.append(self.Right)
			self.Right = item
		elif item.target_type == EQUIP_LEFT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Left is not None:
				return_items.append(self.Left)
			self.Left = item
		elif item.target_type == EQUIP_HANDS:
			if self.Hands is not None:
				return_items.append(self.Hands)
			if self.Left is not None:
				return_items.append(self.Left)
				self.Left = None
			if self.Right is not None:
				return_items.append(self.Right)
				self.Right = None
			self.Hands = item
		elif item.target_type == EQUIP_TOKEN:
			if self.Token is not None:
				return_items.append(self.Token)
			self.Token = item

		return return_items
	def unequip(self, target):
		return_items = []
		if target == EQUIP_HEAD:
			if self.Head is not None:
				return_items.append(self.Head)
				self.Head = None
		elif target == EQUIP_BODY:
			if self.Body is not None:
				return_items.append(self.Body)
				self.Body = None
		elif target == EQUIP_LEGS:
			if self.Legs is not None:
				return_items.append(self.Legs)
				self.Legs = None
		elif target == EQUIP_RIGHT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Right is not None:
				return_items.append(self.Right)
				self.Right = None
		elif target == EQUIP_LEFT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Left is not None:
				return_items.append(self.Left)
				self.Left = None
		elif target == EQUIP_HANDS:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Left is not None:
				return_items.append(self.Left)
				self.Left = None
			if self.Right is not None:
				return_items.append(self.Right)
				self.Right = None
		elif target == EQUIP_TOKEN:
			if self.Token is not None:
				return_items.append(self.Token)
				self.Token = None
		return return_items
	def purge(self, target):
		return_items = []
		if self.Head is not None:
			return_items.append(self.Head)
			self.Head = None
		if self.Body is not None:
			return_items.append(self.Body)
			self.Body = None
		if self.Legs is not None:
			return_items.append(self.Legs)
			self.Legs = None
		if self.Hands is not None:
			return_items.append(self.Hands)
			self.Hands = None
		if self.Right is not None:
			return_items.append(self.Right)
			self.Right = None
		if self.Hands is not None:
			return_items.append(self.Hands)
			self.Hands = None
		if self.Left is not None:
			return_items.append(self.Left)
			self.Left = None
		if self.Hands is not None:
			return_items.append(self.Hands)
			self.Hands = None
		if self.Left is not None:
			return_items.append(self.Left)
			self.Left = None
		if self.Right is not None:
			return_items.append(self.Right)
			self.Right = None
		if self.Token is not None:
			return_items.append(self.Token)
			self.Token = None
		return return_items

	def physical_strength(self, initial): # passive stat boosts take effect on these routines
		if self.Head is not None:
			initial = self.Head.physical_strength(initial)
		if self.Body is not None:
			initial = self.Body.physical_strength(initial)
		if self.Legs is not None:
			initial = self.Legs.physical_strength(initial)
		if self.Hands is not None:
			initial = self.Hands.physical_strength(initial)
		if self.Right is not None:
			initial = self.Right.physical_strength(initial)
		if self.Hands is not None:
			initial = self.Hands.physical_strength(initial)
		if self.Left is not None:
			initial = self.Left.physical_strength(initial)
		if self.Hands is not None:
			initial = self.Hands.physical_strength(initial)
		if self.Left is not None:
			initial = self.Left.physical_strength(initial)
		if self.Right is not None:
			initial = self.Right.physical_strength(initial)
		if self.Token is not None:
			initial = self.Token.physical_strength(initial)
		return initial

	def physical_defense(self, initial):
		if self.Head is not None:
			initial = self.Head.physical_defense(initial)
		if self.Body is not None:
			initial = self.Body.physical_defense(initial)
		if self.Legs is not None:
			initial = self.Legs.physical_defense(initial)
		if self.Hands is not None:
			initial = self.Hands.physical_defense(initial)
		if self.Right is not None:
			initial = self.Right.physical_defense(initial)
		if self.Hands is not None:
			initial = self.Hands.physical_defense(initial)
		if self.Left is not None:
			initial = self.Left.physical_defense(initial)
		if self.Hands is not None:
			initial = self.Hands.physical_defense(initial)
		if self.Left is not None:
			initial = self.Left.physical_defense(initial)
		if self.Right is not None:
			initial = self.Right.physical_defense(initial)
		if self.Token is not None:
			initial = self.Token.physical_defense(initial)
		return initial

	def special_strength(self, initial):
		if self.Head is not None:
			initial = self.Head.special_strength(initial)
		if self.Body is not None:
			initial = self.Body.special_strength(initial)
		if self.Legs is not None:
			initial = self.Legs.special_strength(initial)
		if self.Hands is not None:
			initial = self.Hands.special_strength(initial)
		if self.Right is not None:
			initial = self.Right.special_strength(initial)
		if self.Hands is not None:
			initial = self.Hands.special_strength(initial)
		if self.Left is not None:
			initial = self.Left.special_strength(initial)
		if self.Hands is not None:
			initial = self.Hands.special_strength(initial)
		if self.Left is not None:
			initial = self.Left.special_strength(initial)
		if self.Right is not None:
			initial = self.Right.special_strength(initial)
		if self.Token is not None:
			initial = self.Token.special_strength(initial)
		return initial

	def special_defense(self, initial):
		if self.Head is not None:
			initial = self.Head.special_defense(initial)
		if self.Body is not None:
			initial = self.Body.special_defense(initial)
		if self.Legs is not None:
			initial = self.Legs.special_defense(initial)
		if self.Hands is not None:
			initial = self.Hands.special_defense(initial)
		if self.Right is not None:
			initial = self.Right.special_defense(initial)
		if self.Hands is not None:
			initial = self.Hands.special_defense(initial)
		if self.Left is not None:
			initial = self.Left.special_defense(initial)
		if self.Hands is not None:
			initial = self.Hands.special_defense(initial)
		if self.Left is not None:
			initial = self.Left.special_defense(initial)
		if self.Right is not None:
			initial = self.Right.special_defense(initial)
		if self.Token is not None:
			initial = self.Token.special_defense(initial)
		return initial


	def speed(self, initial):
		if self.Head is not None:
			initial = self.Head.speed(initial)
		if self.Body is not None:
			initial = self.Body.speed(initial)
		if self.Legs is not None:
			initial = self.Legs.speed(initial)
		if self.Hands is not None:
			initial = self.Hands.speed(initial)
		if self.Right is not None:
			initial = self.Right.speed(initial)
		if self.Hands is not None:
			initial = self.Hands.speed(initial)
		if self.Left is not None:
			initial = self.Left.speed(initial)
		if self.Hands is not None:
			initial = self.Hands.speed(initial)
		if self.Left is not None:
			initial = self.Left.speed(initial)
		if self.Right is not None:
			initial = self.Right.speed(initial)
		if self.Token is not None:
			initial = self.Token.speed(initial)
		return initial


	def hp(self, initial):
		if self.Head is not None:
			initial = self.Head.hp(initial)
		if self.Body is not None:
			initial = self.Body.hp(initial)
		if self.Legs is not None:
			initial = self.Legs.hp(initial)
		if self.Hands is not None:
			initial = self.Hands.hp(initial)
		if self.Right is not None:
			initial = self.Right.hp(initial)
		if self.Hands is not None:
			initial = self.Hands.hp(initial)
		if self.Left is not None:
			initial = self.Left.hp(initial)
		if self.Hands is not None:
			initial = self.Hands.hp(initial)
		if self.Left is not None:
			initial = self.Left.hp(initial)
		if self.Right is not None:
			initial = self.Right.hp(initial)
		if self.Token is not None:
			initial = self.Token.hp(initial)
		return initial


	def max_hp(self, initial):
		if self.Head is not None:
			initial = self.Head.max_hp(initial)
		if self.Body is not None:
			initial = self.Body.max_hp(initial)
		if self.Legs is not None:
			initial = self.Legs.max_hp(initial)
		if self.Hands is not None:
			initial = self.Hands.max_hp(initial)
		if self.Right is not None:
			initial = self.Right.max_hp(initial)
		if self.Hands is not None:
			initial = self.Hands.max_hp(initial)
		if self.Left is not None:
			initial = self.Left.max_hp(initial)
		if self.Hands is not None:
			initial = self.Hands.max_hp(initial)
		if self.Left is not None:
			initial = self.Left.max_hp(initial)
		if self.Right is not None:
			initial = self.Right.max_hp(initial)
		if self.Token is not None:
			initial = self.Token.max_hp(initial)
		return initial

	def evasion(self, initial):
		if self.Head is not None:
			initial = self.Head.evasion(initial)
		if self.Body is not None:
			initial = self.Body.evasion(initial)
		if self.Legs is not None:
			initial = self.Legs.evasion(initial)
		if self.Hands is not None:
			initial = self.Hands.evasion(initial)
		if self.Right is not None:
			initial = self.Right.evasion(initial)
		if self.Hands is not None:
			initial = self.Hands.evasion(initial)
		if self.Left is not None:
			initial = self.Left.evasion(initial)
		if self.Hands is not None:
			initial = self.Hands.evasion(initial)
		if self.Left is not None:
			initial = self.Left.evasion(initial)
		if self.Right is not None:
			initial = self.Right.evasion(initial)
		if self.Token is not None:
			initial = self.Token.evasion(initial)
		return initial

	def accuracy(self, initial):
		if self.Head is not None:
			initial = self.Head.accuracy(initial)
		if self.Body is not None:
			initial = self.Body.accuracy(initial)
		if self.Legs is not None:
			initial = self.Legs.accuracy(initial)
		if self.Hands is not None:
			initial = self.Hands.accuracy(initial)
		if self.Right is not None:
			initial = self.Right.accuracy(initial)
		if self.Hands is not None:
			initial = self.Hands.accuracy(initial)
		if self.Left is not None:
			initial = self.Left.accuracy(initial)
		if self.Hands is not None:
			initial = self.Hands.accuracy(initial)
		if self.Left is not None:
			initial = self.Left.accuracy(initial)
		if self.Right is not None:
			initial = self.Right.accuracy(initial)
		if self.Token is not None:
			initial = self.Token.accuracy(initial)
		return initial

class Character(object):
	def __init__(self, name=None, level=1):
		if name is None:
			#self.name = 'MissingNo'
			self.name = self.__class__.__name__
		else:
			self.name = name
		self._exp = 0
		self.elements = [elements.Normal]
		self.status = []
		self.equipment = Equipment()
		# stat growth rate for p.str, p.def, s.str, s.def, speed, maxhp
		self.coefficients = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
		self.config()
		self._level = level
		self.level = level
		self._hp = self.max_hp
		self.full_heal()

	def config(self):
		self.moves = []
		self.base_physical_strength = 10
		self.base_physical_defense = 10
		self.base_special_strength = 10
		self.base_special_defense = 10
		self.base_speed = 10
		self.base_hp = 10


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
		stat = self.equipment.physical_strength(stat)
		return utility.clamp(stat, 1, 3* self.base_physical_strength)
	@property
	def physical_defense(self):
		stat = (self.base_physical_defense + self.coefficients[1]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.physical_defense(stat)
		stat = self.equipment.physical_defense(stat)
		return utility.clamp(stat, 1, 3* self.base_physical_defense)
	@property
	def special_strength(self):
		stat = (self.base_special_strength + self.coefficients[2]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.special_strength(stat)
		stat = self.equipment.special_strength(stat)
		return utility.clamp(stat, 1, 3* self.base_special_strength)
	@property
	def special_defense(self):
		stat = (self.base_special_defense + self.coefficients[3]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.special_defense(stat)
		stat = self.equipment.special_defense(stat)
		return utility.clamp(stat, 1, 3* self.base_special_defense)
	@property
	def speed(self):
		stat = (self.base_speed + self.coefficients[4]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.speed(stat)
		stat = self.equipment.speed(stat)
		return utility.clamp(stat, 1, 3* self.base_speed)

	@property
	def hp(self):
		stat = self._hp
		for status in self.status:
			stat = status.hp(stat)
		stat = self.equipment.hp(stat)
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
		stat = self.equipment.max_hp(stat)
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
	
