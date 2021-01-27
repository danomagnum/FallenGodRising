import main
import random
import elements
import effects
#from utility import clamp, scale
import utility
import math
from constants import *
from .moves import FixedDmgMove
from .mods import gen_Typed_Moves

class Curse(FixedDmgMove):
	def config(self):
		self.name = 'Curse'
		self.power = 10
		self.max_mp = 10.0
		self.accuracy = 0.9
		self.physical = (True, True)

class Jinx(FixedDmgMove):
	def config(self):
		self.name = 'Jinx'
		self.power = 25
		self.max_mp = 10.0
		self.accuracy = 0.9
		self.physical = (True, True)


class Hex(FixedDmgMove):
	def config(self):
		self.name = 'Hex'
		self.power = 10
		self.max_mp = 10.0
		self.accuracy = 0.9
		self.physical = (True, True)
		self.default_target = MULTI_ENEMY

class Doom(FixedDmgMove):
	def config(self):
		self.name = 'Doom'
		self.power = 50
		self.max_mp = 10.0
		self.accuracy = 0.9
		self.physical = (True, True)


scroll_moves = [Curse, Hex, Doom, Jinx]
