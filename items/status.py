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

class HealAll(Item):
	def config(self):
		self.name = 'Heal All'
		self.target_type = MULTI_ALLY
		self.weight = 1
		self.value = 500
		self.rarity = 0.1
		self.helptext = 'Clear All Status'
		self.char = '\x04'

	def use(self, target):
		target.heal(20)
		print('{} used {}'.format(target.name,self.name))

class Potion(Item):
	def config(self):
		self.name = 'Potion'
		self.target_type = ANY

		self.weight = 1
		self.value = 300
		self.rarity = 0.3

		self.effects = []

		multieffect_roll = random.random()

		if multieffect_roll < 0.1:
			effect_count = 3
			self.value *= 3
			self.rarity /= 5

		elif multieffect_roll < 0.3:
			effect_count = 2
			self.value *= 2
			self.rarity /= 2

		else:
			effect_count = 1

		for x in range(effect_count):
			target_effect = random.choice([PHYSTR, PHYDEF, SPCSTR, SPCDEF, SPEED, HP, MAXHP, ACCURACY, EVASION, LUCK, 'Poison'])
			target_power = random.randrange(85, 115)/ 100.0

			if target_effect == HP:
				self.effects.append(effects.Recovery())
			elif target_effect == 'Poison':
				self.effects.append(effects.Poison_Minor())
			else:
				self.effects.append(effects.StatMod(target_power, target_effect))

		self.prefixes = [e.name for e in self.effects]

		self.helptext = 'Status Effect Potion'
		self.char = '\x04'

	def use(self, target):
		for effect in self.effects:
			target.status.append(effect)
		print('{} used {}'.format(target.name,self.name))

def x_potion(*effects):
	p = Potion()
	p.effects = effects
	p.prefixes = [e.name for e in self.effects]
	return p

def potion_of(potion, *effects):
	potion.effects += effects
	p.postfixes = [e.name for e in effects]
	return potion


base_items = [Potion, HealAll]

