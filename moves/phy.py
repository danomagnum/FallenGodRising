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

class Bite(Move):
	def config(self):
		self.name = 'Bite'
		self.max_mp = 20.0
		self.accuracy = 0.9
		self.physical = (True, True)

	def effect(self, user, target, damage=0):
		target.status.append(effects.poison.Bleeding())

class Swoop(Move):
	def config(self):
		self.name = 'Swoop'
		self.max_mp = 20.0
		self.accuracy = 0.9
		self.power = 1
		self.physical = (True, True)


typed_strikes = gen_Typed_Moves(Strike)
typed_rushes = gen_Typed_Moves(Rush)
basic_moves = [Strike, Rush]
scroll_moves = typed_strikes + typed_rushes
