from main import Entity, ActingEntity
import battle
import random
from constants import *
#import characters
import mobs
import sys
from copy import deepcopy
#import curses_interface as graphics_interface
import bearlib_interface as graphics_interface
import settings

class Battler(ActingEntity):
	def config(self):
		self.music = 'battle.mid'
		self.blocking = True
	def collide(self, entity, zone):
		#self.enabled = False
		if entity.is_player == True: #Is the player if no AI
			result = battle.Battle(self.game, entity, self)

			if result == USER:
				self.enabled = False
				entity.backpack.absorb(self.backpack, message = True)
	def battle_run(self):
		pass

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


class Alter(Entity):
	def config(self):
		name = self.game.generate_name()
		self.name = 'Alter of {}'.format(name)
		self.char = '\x91'
		self.passive = True
		self.blocking = True
		self.recharge = 10

	def collide(self, entity, zone):
		#self.enabled = False
		if entity.is_player:
			choice = self.game.display.popup('Encountered {}'.format(self.name), ['Pray', 'Destroy', 'Leave'])
			if choice == 'Pray':
				self.pray(entity, zone)
			elif choice == 'Destroy':
				self.destroy(entity, zone)
			elif choice == 'Leave':
				self.leave(entity, zone)
		else:
			pass

	def pray(self, entity, zone):
		var_name = '{}_ticks'.format(self.name)
		time = self.game.ticks - self.game.get_var(var_name)
		if time > self.recharge:
			self.game.set_var(var_name, self.game.ticks)
			print('You pray at the {} and it grants you its blessing'.format(self.name))
		else:
			print('The alter has no charge')

	def destroy(self, entity, zone):
		print('You have destoryed the {}'.format(self.name))
		self.enabled = False
		self.game.get_var('Alters').remove(self)

	def leave(self, entity, zone):
		pass
			


class Shop(Entity):
	def config(self):
		self.name = 'Shop'
		self.char = '$'
		self.blocking = True
		self.passive = False
	def collide(self, entity, zone):
		SELLRATIO = 0.5
		#self.enabled = False
		if entity.is_player:
			shopping = True
			zonemode = self.game.display.mode

			def update_info_box(choice):
				self.game.display.display_item_stats(choice, entity.backpack)

			def update_info_box2(choice):
				self.game.display.display_item_stats(choice, entity.backpack, cost_mult = SELLRATIO)

			choice = self.game.display.popup('Shop {}'.format(self.name), ['Buy', 'Sell', 'Leave'])
			while shopping:

				if choice == 'Sell':
					self.game.display.mode = SHOP
					if len(entity.backpack) > 0:
						update_info_box(entity.backpack.show()[0])
						selected_item = graphics_interface.menu(self.game.display.storebox, entity.backpack.show(), cols=2, callback_on_change=update_info_box2, opaque=True)
						if selected_item is not None:
							entity.backpack.gold += selected_item.cost() * SELLRATIO
							self.backpack.store(selected_item.take())
						else:
							shopping = False
					else:
						shopping = False



				elif choice == 'Buy':
					if len(self.backpack) > 0:
						self.game.display.mode = SHOP

					else:
						print('Shop is empty')
						break
					
					if len(self.backpack) > 0:
						update_info_box(self.backpack.show()[0])
						selected_item = graphics_interface.menu(self.game.display.storebox, self.backpack.show(), cols=2, callback_on_change=update_info_box, opaque=True)
						if selected_item is not None:
							if entity.backpack.gold >= selected_item.cost():
								entity.backpack.gold -= selected_item.cost()
								entity.backpack.store(selected_item.take())
						else:
							shopping = False
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
			self.vis_blocking = False
			return WALKABLE
			#self.enabled = False
		elif self.lock in entity.backpack:
			entity.backpack.take_by_name(self.lock)
			#self.enabled = False
			self.lock = None
			self.vis_blocking = False
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
		elif len(self.backpack) == 0:
			self.char = '\x0B'
		else:
			self.char = self.backpack.all_items()[0].char

	def config(self):
		self.passive = True
		self.blocking = False
		self.vis_blocking = False

	def collide(self, entity, zone):
		self.enabled = False
		entity.backpack.absorb(self.backpack, message = True)

class Rat(RandWalker, Battler):
	def config(self):
		self.combatants.append(mobs.characters.Page(level=20))

class TowardWalker(Entity):
	def config(self):
		self.walkchance = 0.75
	def tick(self, zone):
		if random.random() < self.walkchance:
			dir = self.toward_entity(self.game.player)
			if dir is not None:
				self.move(zone, dir)


class DoomAI(Battler):
	def config(self):
		self.state = self.standby
		self.standby_delay = 2
		self.standby_counter = 0
		self.flee_counter = 0
		self.configured = 1
		self.movingdir = None
		self.target_map  = None

	def standby(self, zone):
		if zone.LOS_check(self.x, self.y, self.game.player.x, self.game.player.y):
			self.standby_counter = 0
			self.state = self.advancing

	def battle_run(self):
		self.state = self.flee

	def advancing(self, zone):
		dir = None
		if zone.LOS_check(self.x, self.y, self.game.player.x, self.game.player.y):
			dir = self.toward_entity(self.game.player)

		if dir is not None:
			self.move(zone, dir)
			self.target_map = self.game.player.dist_map
		else:
			if self.target_map is not None:
				dir = self.follow_distmap(self.target_map)
				if dir is None:
					self.target_map = None
					self.state = self.standby
				else:
					self.move(zone, dir)
			else:
				self.state = self.standby
			
	def flee(self, zone):
		dir = None
		if zone.LOS_check(self.x, self.y, self.game.player.x, self.game.player.y):
			dir = self.flee_entity(self.game.player)

		if dir is not None:
			self.move(zone, dir)
			self.target_map = self.game.player.dist_map
		else:
			self.flee_counter += 1
			if self.target_map is not None:
				dir = self.flee_distmap(self.target_map)
				if dir is None:
					self.target_map = None
					self.state = self.standby
				else:
					self.move(zone, dir)
			else:
				self.state = self.standby

			if self.flee_counter > 5:
				self.state = self.standby

	def tick(self, zone):
		self.state(zone)

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

