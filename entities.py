from main import Entity
import battle
import random
from constants import *
import characters

class Battler(Entity):
	def collide(self, entity, zone):
		#self.enabled = False
		if entity.is_player == True: #Is the player if no AI
			my_ai = self.AI(self.combatants)
			battle.Battle(entity, my_ai, zone.display)
			self.enabled = False
			entity.backpack.absorb(self.backpack, message = True)

class Shop(Entity):
	def config(self):
		self.name = 'Shop'
		self.char = '$'
	def collide(self, entity, zone):
		#self.enabled = False
		print('I will be a shop')


class Door(Entity):
	def config(self):
		self.name = 'Door'
		self.char = '+'
		self.key()
	def key(self):
		self.lock = None
	def collide(self, entity, zone):
		#self.enabled = False
		if self.lock is None:
			return WALKABLE
			#self.enabled = False
		elif self.lock in entity.backpack:
			entity.backpack.take_by_name(self.lock)
			#self.enabled = False
			self.lock = None
			return WALKABLE
		else:
			print('Locked.  Key={}'.format(self.lock))



class RandWalker(Entity):
	def tick(self, zone):
		if random.random() > 0.8:
			self.move(zone, random.choice([UP, DOWN, LEFT, RIGHT]))

class Treasure(Entity):
	def collide(self, entity, zone):
		self.enabled = False
		entity.backpack.absorb(self.backpack, message = True)

class Rat(RandWalker, Battler):
	def config(self):
		self.combatants.append(characters.Page(level=20))

class TowardWalker(Entity):
	def tick(self, zone):
		#print('walking towards from {},{}'.format(self.x, self.y))
		#dir = zone.toward_player(self.x, self.y)
		dir = self.toward_entity(zone.player)
		if dir is not None:
			self.move(zone, dir)

class BasicAI1(Entity):
	STANDBY = 1
	AGRESSIVE = 2

	def config(self):
		self.state = self.STANDBY
		self.standby_delay = 2
		self.standby_counter = 0
		self.configured = 1

	def tick(self, zone):
		#print('walking towards from {},{}'.format(self.x, self.y))
		if zone.LOS_check(self.x, self.y, zone.player.x, zone.player.y):
			self.state = self.AGRESSIVE
			self.standby_counter = 0
		else:
			self.standby_counter += 1
			if self.standby_counter > self.standby_delay:
				self.state = self.STANDBY

		if self.state == self.AGRESSIVE:
			#dir = zone.toward_player(self.x, self.y)
			dir = self.toward_entity(zone.player)
			if dir is not None:
				self.move(zone, dir)


