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

class Key(Item):
	def config(self):
		self.name = 'Key'
		self.weight = 0
		self.value = 100
		self.rarity = 0.5
		self.helptext = 'Opens a generic door'
