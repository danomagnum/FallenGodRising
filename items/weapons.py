from constants import *
import random
import elements
import inspect
from .item import Item
from .gear import Gear


class Sword(Gear):
	def config(self):
		self.name = 'Sword'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_LEFT
		self.char = '\x02'
	def physical_strength(self, initial):
		return initial + (self.power * self.power)

class GreatSword(Gear):
	def config(self):
		self.name = 'GreatSword'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_HANDS
		self.char = '\x02'
	def physical_strength(self, initial):
		return initial + (2 * self.power * self.power)

class Axe(Gear):
	def config(self):
		self.name = 'Axe'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_LEFT
		self.char = '\x02'
	def physical_strength(self, initial):
		return initial + (self.power * self.power)
	def speed(self, initial):
		return initial - (self.power * self.power) / 2

class BattleAxe(Gear):
	def config(self):
		self.name = 'BattleAxe'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_HANDS
		self.char = '\x02'
	def physical_strength(self, initial):
		return initial + 2 * self.power * self.power
	def speed(self, initial):
		return initial - (self.power * self.power) / 2

class Wand(Gear):
	def config(self):
		self.name = 'Wand'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_LEFT
		self.char = '\x02'
	def special_strength(self, initial):
		return initial + self.power * self.power

class Staff(Gear):
	def config(self):
		self.name = 'Staff'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_HANDS
		self.char = '\x02'
	def special_strength(self, initial):
		return initial + 2*self.power * self.power



gear_items = {EQUIP_LEFT: [Sword, Wand, Axe],
              EQUIP_HANDS: [GreatSword, Staff, BattleAxe]}
