from main import Entity
import battle
import random
from constants import *
import characters
import curses_interface as graphics_interface

class Battler(Entity):
	def collide(self, entity, zone):
		#self.enabled = False
		if entity.is_player == True: #Is the player if no AI
			my_ai = self.AI(self.combatants)
			result = battle.Battle(entity, my_ai, zone.display)
			if result == USER:
				self.enabled = False
				entity.backpack.absorb(self.backpack, message = True)

class Shop(Entity):
	def config(self):
		self.name = 'Shop'
		self.char = '$'
	def collide(self, entity, zone):
		#self.enabled = False
		if entity == zone.player:
			shopping = True
			zonemode = zone.display.mode

			if len(self.backpack) > 0:
				zone.display.mode = SHOP
			else:
				print('Shop is empty')
			def update_info_box(choice):
				zone.display.display_item_stats(choice, zone.player.backpack)
			while shopping:
				if len(self.backpack) > 0:
					selected_item = graphics_interface.menu(zone.display.storebox, self.backpack.show(), cols=2, callback_on_change=update_info_box)
					if selected_item is not None:
						if zone.player.backpack.gold >= selected_item.cost():
							zone.player.backpack.gold -= selected_item.cost()
							zone.player.backpack.store(selected_item.take())
					else:
						shopping = False
				else:
					shopping = False

			zone.display.mode = zonemode


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
			self.char = '-'
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
	def config(self):
		self.walkchance = 0.75
	def tick(self, zone):
		if random.random() < self.walkchance:
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


class NPC(Entity):
	def config(self):
		self.name = 'NPC'
		self.char = 'N'
	def collide(self, entity, zone):
		if entity == zone.player:
			return self.NPC(zone)
	
	def NPC(self, zone):
		return WALKABLE

class UpStairs(Entity):

	def config(self):
		self.char = '<'
		self.new_x = None
		self.new_y = None

	def collide(self, entity, zone):
		if self.new_x is not None:
			entity.x = self.new_x
			entity.y = self.new_y
		if zone.player == entity:
			zone.change_level(zone.level - 1)
		else:
			zone.remove_entity(entity)
			zone.add_entity(entity, zone.level - 1)

class DownStairs(Entity):

	def config(self):
		self.char = '>'
		self.new_x = None
		self.new_y = None

	def collide(self, entity, zone):
		if self.new_x is not None:
			entity.x = self.new_x
			entity.y = self.new_y
		if zone.player == entity:
			zone.change_level(zone.level + 1)
		else:
			zone.remove_entity(entity)
			zone.add_entity(entity, zone.level + 1)

class ZoneWarp(Entity):
	def config(self):
		self.char = '^'
		self.new_x = None
		self.new_y = None
		self.new_zone = None

	def collide(self, entity, zone):
		if None not in [self.new_zone, self.new_x, self.new_y]:
			zone.player.x = self.new_x
			zone.player.y = self.new_y
			zone.display.zone = self.new_zone


