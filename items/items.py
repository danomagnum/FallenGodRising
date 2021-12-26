from constants import *
import random
import effects
import elements
import utility
import inspect
import moves
import sys
import entities

from .item import Item
from .gear import Gear

class Key(Item):
	def config(self):
		self.name = 'Key'
		self.weight = 0
		self.value = 100
		self.rarity = 0.5
		self._helptext = 'Opens a generic door'

class Tent(entities.Entity):
	def config(self):
		self.name = 'Tent'
		self.char = '\x93'
		self.passive = True
		self.blocking = False
		self.recharge = 10
		self.uses = random.randint(2,6)

	def collide(self, entity, zone):
		#self.enabled = False
		if entity.is_player:
			for c in entity.combatants:
				c.full_heal()
			print('Recovered in the tent')
		self.uses -= 1
		if self.uses <= 0:
			print('The tent has deteriorated and is no longer usable')
			self.enabled = False


class Tent_item(Item):
	def config(self):
		self.name = 'Tent'
		self.weight = 0
		self.value = 1000
		self.rarity = 0.1
		self._helptext = 'A place to recover health'
		self.target_type = WORLD

	def use(self):
		t = Tent(self.game)
		t.x = self.game.player.x
		t.y = self.game.player.y
		self.game.zone.entities.append(t)

