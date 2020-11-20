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


typed_blasts = gen_Typed_Moves(Blast)
typed_waves = gen_Typed_Moves(Wave)
basic_moves = [Blast, Wave]
scroll_moves = typed_blasts + typed_waves
