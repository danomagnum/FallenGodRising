import main
import random
import elements
import effects
#from utility import clamp, scale
import utility
import math
from constants import *
from .moves import Move
from .mods import gen_Typed_Moves

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

class Absorb(Move):
	def config(self):
		self.name = 'Absorb'

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

heal_moves = [Heal, Transfuse, Cure, Absorb]
scroll_moves = [Heal, Transfuse, Cure, Absorb]
