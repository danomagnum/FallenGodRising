from constants import *
import random
import effects
import elements
import utility
import inspect
import moves
import sys

from .item import Item
from .gear import Gear


class MoveScroll(Item):
	def __init__(self, game=None, move=None):
		if move is None:
			return
		self.move = move(game)
		name = 'Scroll of'
		level = 1
		Item.__init__(self, game, level,  name, target=ALLY, uses=None)
		self.char = '\x01'
		self.suffixes.append(self.move.name)

	def use(self, target):
		target_moves = [move.name for move in target.moves]
		if self.move.name not in target_moves:
			target.moves.append(self.move)
			print('{} learned {}'.format(target.name,self.move.name))
		else:
			print('{} already knows {}'.format(target.name,self.move.name))


def gen_movescroll(game):
	move = random.sample(moves.all_moves,1)[0]
	return MoveScroll(game, move)

