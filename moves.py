import main
import random
import elements
import effects
#from utility import clamp, scale
import utility
import math
from constants import *

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
			default_target=ENEMY
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
						print('{} used move {} on themself for {}'.format(user.name,self.name, target.name, int(damage)))
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
		
class FireMove(Move):
	def config(self):
		self.prefixes.append('Fire')
		if elements.Fire not in self.elements:
			self.elements.append(elements.Fire)
class WaterMove(Move):
	def config(self):
		self.prefixes.append('Water')
		if elements.Water not in self.elements:
			self.elements.append(elements.Water)
class EarthMove(Move):
	def config(self):
		self.prefixes.append('Earth')
		if elements.Earth not in self.elements:
			self.elements.append(elements.Earth)
class ElectricMove(Move):
	def config(self):
		self.prefixes.append('Electric')
		if elements.Electric not in self.elements:
			self.elements.append(elements.Electric)
class WindMove(Move):
	def config(self):
		self.prefixes.append('Wind')
		if elements.Wind not in self.elements:
			self.elements.append(elements.Wind)
class LightMove(Move):
	def config(self):
		self.prefixes.append('Light')
		if elements.Light not in self.elements:
			self.elements.append(elements.Light)
class DarkMove(Move):
	def config(self):
		self.prefixes.append('Dark')
		if elements.Dark not in self.elements:
			self.elements.append(elements.Dark)

class Strike(Move):
	def config(self):
		self.name = 'Strike'
		self.max_mp = 20.0
		self.accuracy = 0.9
		self.physical = (True, True)

class Rush(Move):
	def config(self):
		self.name = 'Rush'
		self.max_mp = 10.0
		self.accuracy = 0.9
		self.physical = (True, True)
		self.default_target = MULTI_ENEMY



class Buff(Move):
	def config(self):
		self.name = 'Buff'
		self.accuracy = 1
		self.power = 0
		self.default_target = ALLY

	def effect(self, user, target, damage=0):
		target.status.append(effects.StatMod(1.15, PHYSTR))

class Taunt(Move):
	def config(self):
		self.name = 'Taunt'
		self.accuracy = 1
		self.power = 0
		self.default_target = ENEMY

	def effect(self, user, target, damage=0):
		target.status.append(effects.StatMod(0.85, PHYSTR))


class Focus(Move):
	def config(self):
		self.name = 'Focus'
		self.accuracy = 1
		self.power = 0
		self.default_target = ALLY

	def effect(self, user, target, damage=0):
		target.status.append(effects.StatMod(1.15, SPCSTR))

class Guard(Move):
	def config(self):
		self.name = 'Guard'
		self.accuracy = 1
		self.power = 0
		self.default_target = ALLY

	def effect(self, user, target, damage=0):
		target.status.append(effects.StatMod(1.15, PHYDEF))
		
class Protect(Move):
	def config(self):
		self.name = 'Protect'
		self.accuracy = 1
		self.power = 0
		self.default_target = ALLY

	def effect(self, user, target, damage=0):
		target.status.append(effects.StatMod(1.15, SPCDEF))

class Smoke(Move):
	def config(self):
		self.name = 'Smoke'
		self.accuracy = 1
		self.power = 0
		self.default_target = ALLY

	def effect(self, user, target, damage=0):
		target.status.append(effects.StatMod(1.15, EVASION))

class Haste(Move):
	def config(self):
		self.name = 'Haste'
		self.accuracy = 1
		self.power = 0
		self.default_target = ALLY

	def effect(self, user, target, damage=0):
		target.status.append(effects.StatMod(1.15, SPEED))

stat_moves = [Haste, Smoke, Protect, Guard, Focus, Taunt, Buff]

class Heal(Move):
	def config(self):
		self.name = 'Heal'
		self.accuracy = 0.9
		self.power = -10
		self.default_target = ALLY
		self.physical = (False, False)

class Transfuse(Move):
	def config(self):
		self.name = 'Transfuse'
		self.accuracy = 0.9
		self.power = -10
		self.default_target = ALLY
		self.physical = (False, False)

	def effect(self, user, target, damage=0):
		user.hp -= damage


class Piercing(Move):
	def config(self):
		self.prefixes.append('Piercing')

	def effect(self, user, target, damage=0):
		randval = random.random()
		# for starters, effect 20% of the time.  Once the move is more used, effect 95%
		prob = utility.scale(self.uses, 0, 1000, 0.2, 0.95)
		if self.game.get_var('effect_override'):
			prob = 1.0
		#if randval < prob:
		if True:
			print('{} has been wounded'.format(target.name))
			target.status.append(effects.poison.Bleeding())


class Multi(Move):
	def config(self):
		self.prefixes.append('Multi')
		self.multimove_inprogress = False
	def postconfig(self):
		self.max_mp = self.max_mp / 2

	def effect(self, user, target, damage=0):
		randval = random.random()
		multimove = False
		initial_multimove = not self.multimove_inprogress
		#75% chance to get 2 moves.
		#6% chance to get 3.
		#0.48% chance to get 4 and so on
		if not self.multimove_inprogress:
			if randval < 0.75:
				multimove = True
		elif randval < 0.08:
			multimove = True

		if multimove:
			self.multimove_inprogress = True
			self.attack(user, [target])
			self.mp += 1
			if initial_multimove:
				self.multimove_inprogress = False


#enemy-target move with poison effect
class Poison(Move):
	def config(self):
		self.prefixes.append('Poison')

	def effect(self, user, target, damage=0):
		randval = random.random()
		# for starters, poison minorly 20% of the time.  Once the move is more used, poison minorly 95%
		minor_range = utility.scale(self.uses, 0, 1000, 0.2, 0.95)
		# for starters, poison majorly 5% of the time.  Once the move is more used, poison major 50%
		major_range = utility.scale(self.uses, 0, 1000, 0.05, 0.5)
		if randval < major_range:
			print('{} has major poisoning'.format(target.name))
			target.status.append(effects.poison.Poison_Major())
		elif randval < minor_range:
			print('{} has minor poisoning'.format(target.name))
			target.status.append(effects.poison.Poison_Minor())

class Absorb(Move):
	def config(self):
		self.prefixes.append('Absorbing')

	def effect(self, user, target, damage=0):
		high = damage/1.5
		low = damage/3
		mode = max(min(high, damage * user.luck), low)
		regain = random.triangular(low, high, mode)
		user.hp += regain
		print("{} gained {} hp".format(user.name, regain))
		

#self-target healing move
class Cure(Move):
	def config(self):
		self.name = 'Cure'
		self.max_mp = 2.0
		self.accuracy = 1
		self.power = 0
		self.default_target = ALLY
		self.physical = (False, False)

	def effect(self, user, target, damage=0):
		if len(target.status) > 0:
			to_remove = random.choice(target.status)
			target.status.remove(to_remove)

#single snemy arcane move
class Blast(Move):
	def config(self):
		self.name = 'Blast'
		self.max_mp = 20.0
		self.accuracy = 0.9
		self.physical = (False, False)

#multi snemy arcane move
class Wave(Move):
	def config(self):
		self.name = 'Wave'
		self.max_mp = 10.0
		self.accuracy = 0.9
		self.physical = (False, False)
		self.default_target = MULTI_ENEMY

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



def mod_move(move, mod):
	return utility.add_class(move, mod)

def gen_Typed_Moves(move):
	typed_moves = []
	type_mods = [FireMove, WaterMove, EarthMove, ElectricMove, WindMove, LightMove, DarkMove, Poison, Piercing]
	for mod in type_mods:
		typed_moves.append(mod_move(move, mod))
	return typed_moves



typed_blasts = gen_Typed_Moves(Blast)
typed_waves = gen_Typed_Moves(Wave)
typed_strikes = gen_Typed_Moves(Strike)
typed_rushes = gen_Typed_Moves(Rush)

heal_moves = [Heal, Transfuse, Cure,]
effect_moves = [Haste, Smoke, Protect, Guard, Focus, Taunt, Buff]
basic_moves = [Strike, Blast, Rush, Wave, SelfDestruct]

all_moves = typed_strikes + typed_blasts + typed_rushes + typed_waves + basic_moves + heal_moves
