import main
import random
import elements
import effects
#from utility import clamp, scale
import utility
import math
from constants import *

MOVE_CUTOFF = 4
MOVE_NERF_AFTER_CUTOFF = 0.9

class Move(utility.Serializable):
	def __init__(self,game, name = None, element_list = None, accuracy = None, power = None, mp = None,  default_target = None):
		self.game = game
		self.prefixes = []
		self.suffixes = []
		if name is None:
			name = 'MISSINGNAME'
		self._name = name
		if mp is None:
			mp = 10.0
		self.max_mp = mp
		if accuracy is None:
			accuracy = 0.99
		self.accuracy = accuracy
		if power is None:
			power = 10
		self.power = power
		if element_list is None:
			element_list = [elements.Normal]
		self.elements = element_list
		self.uses = 0
		self.physical = (True, True) # Attack stat to use, def stat to use
		if default_target is None:
			default_target=ACTIVE
		self.default_target = default_target
	
		self.helptext = ''

		utility.call_all('config', self)
		utility.call_all('postconfig', self)

		self.ticks = 0
		self._mp = self.max_mp

	@property
	def mp(self):
		return self._mp
	
	@mp.setter
	def mp(self, value):
		self._mp = utility.clamp(value, 0, self.max_mp)

	@property
	def name(self):
		namestr = ''
		namestr = ' '.join(self.prefixes)
		if namestr != '':
			namestr += ' '
		namestr += self._name
		if self.suffixes != []:
			namestr += ' '
		namestr += ' '.join(self.suffixes)
		return namestr

	@name.setter
	def name(self, value):
		self._name = value

	def config(self):
		pass
	def postconfig(self):
		pass

	def attack(self, user, targets): # do whatever the attack needs to do
		if (self.mp > 0):
			self.mp -= 1
		else:
			msg = '{} is out of MP to use move {}'.format(user.name,self.name)
			self.mp = 0
			if 0.2 * user.luck > random.random():
				msg += ' but still attacks.'
				print(msg)
			else:
				print(msg)
				return
		target_coefficient = 1.1 / len(targets)

		for target in targets:
			# figure out if the move hits.
			hit_chance = ((user.speed/target.speed)/9) + user.accuracy/target.evasion * self.accuracy
			damage = 0
			randval = random.random()

			if hit_chance * user.luck > randval:

				# calculate whether it is a critical hit:
				crit_metric = CRIT_RATE * (user.luck / target.luck) * (user.speed / target.speed)
				if random.random() < crit_metric:
					crit_factor = 2 # crit
					print('Crit!')
				else:
					crit_factor = 1

				if self.power != 0: # zero power moves are status only
					if self.physical[0]:
						attack_str = user.physical_strength
					else:
						attack_str = user.arcane_strength
					if self.physical[1]:
						attack_def = target.physical_defense
					else:
						attack_def = target.arcane_defense

					if DAMAGE_CALC == 0:
						damage = ((user.level/100.0 ) * attack_str/(attack_def/crit_factor) * self.power + 2) * target_coefficient
					elif DAMAGE_CALC == 1:
						hp_ratio = (target.virtual_hp / 6.0) # virtual hp is the health of a neutrally 
						strdef_ratio = attack_str / (attack_def / crit_factor)
						power_ratio = self.power / 10.0
						level_factor1 =  utility.clamp((1 + (user.level - target.level) / 10), 0.9, 4)
						level_factor1 = math.sqrt(level_factor1)

						damage = hp_ratio * strdef_ratio * power_ratio * level_factor1

					user_attack_count = len(user.moves)
					if user_attack_count > MOVE_CUTOFF:
						# If the user has more than MOVE_CUTOFF moves, start nerfing all their moves
						# Jack of all trades, master of none kind of thing.
						# causes a tradeoff between move coverage and move power
						power_factor = MOVE_NERF_AFTER_CUTOFF ** (user_attack_count - MOVE_CUTOFF)
						power = power * power_factor



					# Do elemental effects
					for atk_element in self.elements:
						for target_element in target.elements:
							damage *= atk_element.effectiveness(target_element, self.game.biome())
						for user_element in user.elements:
							if user_element == atk_element:
								damage *= atk_element.bonus


					self.uses += 1

					# This makes athe attacks do more damage as you've got more experience using them
					if damage > 0:
						damage += ((damage + 1) * 3 * min(self.uses, 100.0) / 100.0 + 5) / 10.0
					else:
						damage -= ((-damage + 1) * 3 * min(self.uses, 100.0) / 100.0 + 5) / 10.0

					#use the attacker and defender item attack and defend checks.
					for item in user.equipment.all_items():
						damage = item.attack(damage, user, target)
					for item in target.equipment.all_items():
						damage = item.attack(damage, target, user)

					# final damage randomization and adjustment based on luck
					if NEWDIST:
						# Using the triangle distribution now so the mean can be off-center
						low = damage - (damage/8.0)
						high = damage + (damage/8.0)
						mode = max(min(high, damage * user.luck), low)
						damage = random.triangular(low, high, mode)# normal distribution with stdev of 8% for randomness
						#print low, high, mode, damage
					else:
						damage = random.normalvariate(damage, damage/8.0) # normal distribution with stdev of 8% for randomness
					if damage >= 0:
						damage = max(1,damage)
					else:
						damage = min(-1,damage)

					#apply the damage
					target.hp -= int(damage)

					if user == target:
						print('{} used move {} on themself for {}'.format(user.name,self.name, int(damage)))
					else:
						print('{} used move {} on {} for {}'.format(user.name,self.name, target.name, int(damage)))

				else:
					if user == target:
						print('{} used move {} on themself'.format(user.name,self.name, target.name))
					else:
						print('{} used move {} on {}'.format(user.name,self.name, target.name))

				utility.call_all('effect', self, user, target, damage)
			else:
				print('{} missed with move {} against {}'.format(user.name, self.name, target.name))

	def effect(self, user, target, damage=0):
		pass

	def __str__(self):
		string = ''
		string += self.name + ' '
		string += '( ' + str(int(self.mp)) + '/' + str(int(self.max_mp)) + ' )'
		return string

	def tick(self, user):
		tick_rate = MOVE_REGEN_TICKS * self.max_mp
		self.ticks += 1
		if self.ticks > tick_rate:
			self.ticks = 0
			if self.mp < self.max_mp:
				self.mp += 1

class SelfDestruct(Move):
	def config(self):
		self.name = 'Self Destruct'
		self.max_mp = 1.0
		self.accuracy = 0.9
		self.physical = (True, True)
		self.power = 50
		self.default_target = MULTI_ALL

	def attack(self, user, targets): # do whatever the attack needs to do
		Move.attack(self, user, targets)
		print('{} was obliterated'.format(user.name))
		user.hp = 0




basic_moves = [SelfDestruct]
