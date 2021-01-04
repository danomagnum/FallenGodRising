from constants import *
import random
import elements
import inspect
from .item import Item
from .gear import Gear

class Helm(Gear):
	def config(self):
		self.name = 'Helm'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_HEAD
		self.char = '\x03'
	def physical_defense(self, initial):
		return initial + (self.power * self.power / 5.0)

class Hood(Gear):
	def config(self):
		self.name = 'Hood'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_HEAD
		self.char = '\x03'
	def arcane_defense(self, initial):
		return initial + (self.power * self.power / 5.0)

class Mail(Gear):
	def config(self):
		self.name = 'Mail'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_BODY
		self.char = '\x03'
	def physical_defense(self, initial):
		return initial + (self.power * self.power / 2.0)

class Robe(Gear):
	def config(self):
		self.name = 'Robe'
		self.weight = 2
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_BODY
		self.char = '\x03'
	def arcane_defense(self, initial):
		return initial + (self.power * self.power / 2.0)

class BattleRobe(Gear):
	def config(self):
		self.name = 'BattleRobe'
		self.weight = 2
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_BODY
		self.char = '\x03'
	def arcane_defense(self, initial):
		return initial + (self.power * self.power)
	def physical_defense(self, initial):
		return initial - (self.power * self.power / 3.0)

class Plate(Gear):
	def config(self):
		self.name = 'Plate'
		self.weight = 2
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_BODY
		self.char = '\x03'
	def physical_defense(self, initial):
		return initial + (self.power * self.power)
	def arcane_defense(self, initial):
		return initial - (self.power * self.power / 3.0)

class Shield(Gear):
	def config(self):
		self.name = 'Shield'
		self.weight = 2
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_RIGHT
		self.char = '\x03'
	def evasion(self, initial):
		return initial + (self.power * self.power / 5.0)

class Amulet(Gear):
	def config(self):
		self.name = 'Amulet'
		self.weight = 0
		self.value = 500
		self.rarity = 0.1
		self.target_type = EQUIP_TOKEN
		self.char = '\x03'

gear_items = {EQUIP_HEAD:[Helm],
              EQUIP_BODY: [Plate, Mail, Robe, BattleRobe],
              EQUIP_RIGHT: [Shield],
              EQUIP_TOKEN: [Amulet]}
