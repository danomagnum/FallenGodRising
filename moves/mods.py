import main
import random
import elements
import effects
#from utility import clamp, scale
import utility
import math
from constants import *
from .moves import Move
		
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

class Absorbing(Move):
	def config(self):
		self.prefixes.append('Absorbing')

	def effect(self, user, target, damage=0):
		high = damage/1.5
		low = damage/3
		mode = max(min(high, damage * user.luck), low)
		regain = random.triangular(low, high, mode)
		user.hp += regain
		print("{} gained {} hp".format(user.name, regain))
		

def mod_move(move, mod):
	return utility.add_class(move, mod)

def gen_Typed_Moves(move, type_mods = None):
	typed_moves = []
	if type_mods is None:
		type_mods = [FireMove, WaterMove, EarthMove, ElectricMove, WindMove, LightMove, DarkMove, Poison, Piercing, Absorbing]
	for mod in type_mods:
		typed_moves.append(mod_move(move, mod))
	return typed_moves


