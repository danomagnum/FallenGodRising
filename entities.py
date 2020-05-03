from main import Entity
import battle
import random
from constants import *
import characters
import sys
#import curses_interface as graphics_interface
import bearlib_interface as graphics_interface

class Battler(Entity):
	def collide(self, entity, zone):
		#self.enabled = False
		if entity.is_player == True: #Is the player if no AI
			result = battle.Battle(self.game, entity, self)
			if result == USER:
				self.enabled = False
				entity.backpack.absorb(self.backpack, message = True)

	def tick(self, zone):
		if len(self.get_available()) == 0:
			self.enabled = False
			print('{}: {}'.format(self.name,self.defeated_text))
			#TODO: drop the backpack
			if len(self.backpack) > 0:
				t = Treasure(backpack=self.backpack)
				t.x = self.x
				t.y = self.y
				zone.add_entity(t)



class Shop(Entity):
	def config(self):
		self.name = 'Shop'
		self.char = '$'
		self.passive = True
	def collide(self, entity, zone):
		#self.enabled = False
		if entity.is_player:
			shopping = True
			zonemode = self.game.display.mode

			if len(self.backpack) > 0:
				self.game.display.mode = SHOP
			else:
				print('Shop is empty')
			def update_info_box(choice):
				self.game.display.display_item_stats(choice, entity.backpack)
			while shopping:
				if len(self.backpack) > 0:
					update_info_box(self.backpack.show()[0])
					selected_item = graphics_interface.menu(self.game.display.storebox, self.backpack.show(), cols=2, callback_on_change=update_info_box)
					if selected_item is not None:
						if entity.backpack.gold >= selected_item.cost():
							entity.backpack.gold -= selected_item.cost()
							entity.backpack.store(selected_item.take())
					else:
						shopping = False
				else:
					shopping = False

			self.game.display.mode = zonemode


class Door(Entity):
	def config(self):
		self.name = 'Door'
		self.char = '+'
		self.key()
		self.passive = True
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
	def __init__(self,game = None, item_list = None, backpack = None):
		Entity.__init__(self, game, name=None, combatants = None, item_list=None, x=0, y=0, char='?', AI=None, is_player = False)
		if backpack is not None:
			self.backpack = backpack
		if item_list is None:
			item_list = []
		for i in item_list:
			self.backpack.store(i)
		if len(self.backpack) > 1:
			self.char = '\x92'
		else:
			if len(self.backpack) > 0:
				self.char = self.backpack.all_items()[0].char

	def config(self):
		self.passive = True

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
			dir = self.toward_entity(self.game.player)
			if dir is not None:
				self.move(zone, dir)

class BasicAI1(Battler):
	STANDBY = 1
	AGRESSIVE = 2
	FLEE = 3

	def config(self):
		self.state = self.STANDBY
		self.standby_delay = 2
		self.standby_counter = 0
		self.configured = 1

	def tick(self, zone):
		#print('walking towards from {},{}'.format(self.x, self.y))
		if zone.LOS_check(self.x, self.y, self.game.player.x, self.game.player.y):
			self.standby_counter = 0
		else:
			self.standby_counter += 1

		if self.state == self.STANDBY:
			if self.standby_counter < 1:
				self.state = self.AGRESSIVE
		elif self.state == self.AGRESSIVE:
			#dir = zone.toward_player(self.x, self.y)
			dir = self.toward_entity(self.game.player)
			if dir is not None:
				self.move(zone, dir)

			if self.standby_counter > self.standby_delay:
				self.state = self.STANDBY
		elif self.state == self.FLEE:
			#dir = zone.toward_player(self.x, self.y)
			dir = self.flee_entity(self.game.player)
			if dir is not None:
				self.move(zone, dir)

			if self.standby_counter < 1:
				self.state = self.STANDBY

class NPC(Entity):
	def config(self):
		self.name = 'NPC'
		self.char = 'N'
		self.passive = True
	def collide(self, entity, zone):
		if entity.is_player:
			return self.NPC(zone)
	
	def NPC(self, zone):
		return WALKABLE

class UpStairs(Entity):

	def config(self):
		self.char = '<'
		self.new_x = None
		self.new_y = None
		self.passive = True

	def collide(self, entity, zone):
		if self.new_x is not None:
			entity.x = self.new_x
			entity.y = self.new_y
		if entity.is_player:
			zone.change_level(zone.level - 1)
		else:
			zone.remove_entity(entity)
			zone.add_entity(entity, zone.level - 1)

class DownStairs(Entity):

	def config(self):
		self.char = '>'
		self.new_x = None
		self.new_y = None
		self.passive = True

	def collide(self, entity, zone):
		if self.new_x is not None:
			entity.x = self.new_x
			entity.y = self.new_y
		if entity.is_player:
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
		self.new_level = None
		self.passive = True

	def collide(self, entity, zone):
		if entity.is_player:
			if self.new_zone is not None:
				self.game.change_zone(self.new_zone, self.new_x, self.new_y, self.new_level)
				self.game.zone.check_fasttravel()

