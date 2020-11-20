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

class Drain(Move):
	def config(self):
		self.name = 'Drain'
		self.accuracy = 1
		self.power = 0
		self.default_target = ENEMY

	def effect(self, user, target, damage=0):
		target.status.append(effects.poison.Drain())



stat_moves = [Haste, Smoke, Protect, Guard, Focus, Taunt, Buff]
effect_moves = [Haste, Smoke, Protect, Guard, Focus, Taunt, Buff]
scroll_moves = [Haste, Smoke, Protect, Guard, Focus, Taunt, Buff]
