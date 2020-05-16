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

	def config(self):
		self.prefixes.append('Fire')
	def elements(self, element_list):
		if elements.Fire not in element_list:
			element_list.append(elements.Fire)
		return element_list

