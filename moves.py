import main
import random
import elements
import effects
#from utility import clamp, scale
import utility
import math
from constants import *

class Move(object):
	def __init__(self,game, name = None, element_list = None, accuracy = None, power = None, mp = None,  default_target = None):
		self.game = game
		if name is None:
			name = 'MISSINGNAME'
		self.name = name
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
			default_target=ENEMY
		self.default_target = default_target
	
		self.helptext = ''

		utility.call_all('config', self)
		#utility.call_all_configs(self)

		self.ticks = 0
		self.mp = self.max_mp

	def config(self):
		pass

	def attack(self, user, targets): # do whatever the attack needs to do
		if (self.mp > 0):
			self.mp -= 1
		else:
			print('{} is out of MP to use move {}'.format(user.name,self.name))
			self.mp = 0
			if 0.2 * user.luck > random.random():
				print('{} used move {}'.format(user.name,self.name))
			else:
				return
		target_coefficient = 1.1 / len(targets)

		for target in targets:
			# figure out if the move hits.
			hit_chance = ((user.speed/target.speed)/9) + user.accuracy/target.evasion * self.accuracy

			if hit_chance * user.luck > random.random():


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
						attack_str = user.special_strength
					if self.physical[1]:
						attack_def = target.physical_defense
					else:
						attack_def = target.special_defense

					if DAMAGE_CALC == 0:
						damage = ((user.level/100.0 ) * attack_str/(attack_def/crit_factor) * self.power + 2) * target_coefficient
					elif DAMAGE_CALC == 1:
						hp_ratio = (target.virtual_hp / 6.0) # virtual hp is the health of a neutrally 
						strdef_ratio = attack_str / (attack_def / crit_factor)
						power_ratio = self.power / 10.0
						level_factor1 =  utility.clamp((1 + (user.level - target.level) / 10), 0.9, 4)
						level_factor1 = math.sqrt(level_factor1)

						damage = hp_ratio * strdef_ratio * power_ratio * level_factor1

					# Do elemental effects
					for atk_element in self.elements:
						for target_element in target.elements:
							damage *= atk_element.effectiveness(target_element)
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

					print('{} used move {} on {} for {}'.format(user.name,self.name, targets[0].name, int(damage)))

				self.effect(target)
			else:
				print('miss!')
	def effect(self, target):
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
		




class Strike(Move):
	def config(self):
		self.name = 'Strike'
		self.max_mp = 20.0
		self.accuracy = 0.9
		self.physical = (True, True)

class FireStrike(Strike):
	def config(self):
		self.name = 'Fire Strike'
		self.elements = [elements.Fire]


class WaterStrike(Strike):
	def config(self):
		self.name = 'Water Strike'
		self.elements = [elements.Water]

class EarthStrike(Strike):
	def config(self):
		self.name = 'Earth Strike'
		self.elements = [elements.Earth]

class ElectricStrike(Strike):
	def config(self):
		self.name = 'Electric Strike'
		self.elements = [elements.Electric]

class WindStrike(Strike):
	def config(self):
		self.name = 'Wind Strike'
		self.elements = [elements.Wind]

class LightStrike(Strike):
	def config(self):
		self.name = 'Light Strike'
		self.elements = [elements.Light]

class DarkStrike(Strike):
	def config(self):
		self.name = 'Dark Strike'
		self.elements = [elements.Dark]

typed_strikes = [FireStrike, WaterStrike, EarthStrike, WindStrike, LightStrike, DarkStrike]

class Buff(Move):
	def config(self):
		self.name = 'Buff'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, PHYSTR))

class Taunt(Move):
	def config(self):
		self.name = 'Taunt'
		self.accuracy = 1
		self.power = 0
		self.default_target = ENEMY

	def effect(self, target):
		target.status.append(effects.StatMod(0.85, PHYSTR))


class Focus(Move):
	def config(self):
		self.name = 'Focus'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, SPCSTR))

class Guard(Move):
	def config(self):
		self.name = 'Guard'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, PHYDEF))
		
class Protect(Move):
	def config(self):
		self.name = 'Protect'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, SPCDEF))

class Smoke(Move):
	def config(self):
		self.name = 'Smoke'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, EVASION))

class Haste(Move):
	def config(self):
		self.name = 'Haste'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, SPEED))


class Heal(Move):
	def config(self):
		self.name = 'Heal'
		self.accuracy = 0.9
		self.power = -10
		self.default_target = SELF
		self.physical = (False, False)

class Poison(Move):
	def config(self):
		self.name = 'Poison'
		self.power = 2.0
		self.elements = [elements.Normal]
		self.physical = (True, True)

	def effect(self, target):
		randval = random.random()
		# for starters, poison minorly 20% of the time.  Once the move is more used, poison minorly 95%
		minor_range = utility.scale(self.uses, 0, 1000, 0.2, 0.95)
		# for starters, poison majorly 5% of the time.  Once the move is more used, poison major 50%
		major_range = utility.scale(self.uses, 0, 1000, 0.05, 0.5)
		if randval < major_range:
			print('{} has major poisoning'.format(target.name))
			target.status.append(effects.Poison_Major())
		elif randval < minor_range:
			print('{} has minor poisoning'.format(target.name))
			target.status.append(effects.Poison_Minor())


class Cure(Move):
	def config(self):
		self.name = 'Cure'
		self.max_mp = 2.0
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF
		self.physical = (False, False)

	def effect(self, target):
		if len(target.status) > 0:
			to_remove = random.choice(target.status)
			target.status.remove(to_remove)


class Blast(Move):
	def config(self):
		self.name = 'Blast'
		self.max_mp = 20.0
		self.accuracy = 0.9
		self.physical = (False, False)

class FireBlast(Blast):
	def config(self):
		self.name = 'Fire Blast'
		self.elements = [elements.Fire]


class WaterBlast(Blast):
	def config(self):
		self.name = 'Water Blast'
		self.elements = [elements.Water]

class EarthBlast(Blast):
	def config(self):
		self.name = 'Earth Blast'
		self.elements = [elements.Earth]

class ElectricBlast(Blast):
	def config(self):
		self.name = 'Electric Blast'
		self.elements = [elements.Electric]

class WindBlast(Blast):
	def config(self):
		self.name = 'Wind Blast'
		self.elements = [elements.Wind]

class LightBlast(Blast):
	def config(self):
		self.name = 'Light Blast'
		self.elements = [elements.Light]

class DarkBlast(Blast):
	def config(self):
		self.name = 'Dark Blast'
		self.elements = [elements.Dark]


typed_blasts = [FireBlast, WaterBlast, EarthBlast, ElectricBlast, WindBlast, LightBlast, DarkBlast]

all_moves = typed_strikes + typed_blasts + [Strike, Blast]
