import battle
import random
import utility
from constants import *
#import characters
import mobs
import sys
from copy import deepcopy
#import curses_interface as graphics_interface
import bearlib_interface as graphics_interface
import settings
import items


class Entity(object):
	def __init__(self,game, name=None, combatants = None, item_list=None, x=0, y=0, char=None, AI=None, is_player = False):
		self.game = game
		self.defeated_text = None
		self.music = None
		if name is None:
			name = ''
		self._level = 1
		self.name = name
		self.dist_map = None
		if combatants is None:
			self.combatants = []
			self.combatant = None
		else:
			self.combatants = combatants
			self.combatant = combatants[0]
		self.backpack = items.Backpack(game)
		if item_list is not None:
			for item in item_list:
				self.backpack.store(item)

		self.AI = AI
		self.x = x
		self.y = y
		self.char = char

		self.enabled = True

		self.is_player = is_player
		self.helptext = ''

		self.passive = False
		self.blocking = False
		self.vis_blocking = True

		self.action_points = 0
		
		#utility.call_all_configs(self)
		utility.call_all('config', self)

		if self.combatant is None:
			if len(self.combatants) > 0:
				self.combatant = self.combatants[0]

		if self.is_player:
			self.priority = 10
		else:
			self.priority = 100

		if self.defeated_text is None:
			self.defeated_text = '{} was defeated'.format(self.name)

	def action_accumulate(self):
		return 0

	def attack(self, enemy_ai):
		move = random.choice(self.combatant.moves)
		enemy = random.choice(enemy_ai.combatants)
		if move.default_target == ENEMY:
			target = enemy
		else:
			target = self.combatant
		return [move, [target]]
	
	def purge_dead(self):
		newcombatants = []
		for c in self.combatants:
			if c.hp > 0:
				newcombatants.append(c)
			else:
				pass
		self.combatants = newcombatants

	def change(self, enemy):
		standby = self.get_standby()
		available = self.get_available()
		if standby:
			self.combatant = random.choice(standby)
			return self.combatant
		elif available:
			self.combatant = random.choice(available)
			return self.combatant
		else:
			return None
	
	def action(self, enemy_ai):
		if self.get_standby():
			return random.choice([ATTACK, SWITCH])
		else:
			action = random.choice([ATTACK, ATTACK, ATTACK, ATTACK, ATTACK])
		return action
	
	def get_available(self):
		return [ combatant for combatant in self.combatants if combatant.hp > 0 ] 
	
	def get_standby(self):
		return [ combatant for combatant in self.combatants if (combatant.hp > 0) and combatant != self.combatant ] 



	@property
	def level(self):
		l = self._level
		for c in self.combatants:
			l = max(l, c.level)
		return l
	def config(self):
		pass

	def get_available(self):
		return [ combatant for combatant in self.combatants if combatant.hp > 0 ] 
	
	def get_standby(self):
		return [ combatant for combatant in self.combatants if (combatant.hp > 0) and combatant != self.combatant ] 
	
	def tick(self, zone):
		pass

	def subtick(self, zone):
		for combatant in self.combatants:
			combatant.tick()
			combatant.subtick()

	def collide(self, entity, zone):
		pass

	def move(self, zone, direction):
		test_x = self.x
		test_y = self.y

		if direction == UP:
			test_y -= 1
		elif direction == DOWN:
			test_y += 1
		elif direction == LEFT:
			test_x -= 1
		elif direction == RIGHT:
			test_x += 1

		at_pos = zone.check_pos(test_x, test_y)
		if at_pos[0] == EMPTY:
			self.x = test_x
			self.y = test_y
			self.calcDistGraph(zone)
		elif (at_pos[0] == ENTITY) or (at_pos[0] == PLAYER):
			self.collide(at_pos[1], zone)
			walk_over = at_pos[1].collide(self, zone)
			if walk_over == WALKABLE:
				self.x = test_x
				self.y = test_y
		elif at_pos[0] == UP:
			zone.exit(self, UP)
		elif at_pos[0] == DOWN:
			zone.exit(self, DOWN)
		elif at_pos[0] == LEFT:
			zone.exit(self, LEFT)
		elif at_pos[0] == RIGHT:
			zone.exit(self, RIGHT)

	def calcDistGraph(self, zone):
		self.dist_map = [[-1 for x in range(zone.width)] for x in range(zone.height)]
		x0 = self.x
		y0 = self.y
		d = 0
		self.dist_map[y0][x0] = d
		checked = set()
		checked.add((x0,y0))
		to_check = [(x0,y0)]
		checking = []
		i = 0
		while len(to_check) > 0:
			checking = to_check[:]
			to_check = []
			for point in checking:
				d = self.dist_map[point[1]][point[0]]
				pts = []
				if point[1] > 0:
					up = (point[0], point[1] - 1)
					pts.append(up)
				if point[1] < zone.height - 2:
					down = (point[0], point[1] + 1)
					pts.append(down)
				if point[0] > 0:
					left = (point[0] - 1, point[1])
					pts.append(left)
				if point[0] < zone.width - 2:
					right = (point[0] + 1, point[1])
					pts.append(right)

				d = d + 1
				for pt in pts:
					if pt not in checked:
						chk_pos = zone.check_pos(pt[0], pt[1])
						if chk_pos[0] != WALL:
							if pt[0] == x0 and pt[1] == y0:
								print('error')
							if (self.dist_map[pt[1]][pt[0]] > d) or (self.dist_map[pt[1]][pt[0]] < 0):
								#print('error 2 {} {}'.format(d,self.dist_map[pt[1]][pt[0]] ))
								self.dist_map[pt[1]][pt[0]] = d
								to_check.append(pt)
							i = i + 1
							checked.add(pt)
	def follow_distmap(self, dmap):
		y = self.y
		x = self.x
		current = dmap[y][x]
		up = current + 1
		down = current + 1
		left = current + 1
		right = current + 1

		ymax = len(dmap) - 1
		xmax = len(dmap[0]) - 1
		if y > 0:
			up = dmap[y - 1][x]
		if y < ymax:
			down = dmap[y + 1][x]
		if x > 0:
			left = dmap[y][x - 1]
		if x < xmax:
			right = dmap[y][x + 1]

		options = [up, down, left, right]

		options = [opt for opt in options if (opt <= current) and (opt >= 0)]

		if options:
			minval = min(options)

			if up == minval:
				return UP
			elif down == minval:
				return DOWN 
			elif left==minval:
				return LEFT
			elif right==minval:
				return RIGHT
		return None



	def toward_entity(self, entity):
		y = self.y
		x = self.x
		up = -1
		down = -1
		left = -1
		right = -1
		if entity.dist_map:
			ymax = len(entity.dist_map) - 1
			xmax = len(entity.dist_map[0]) - 1
			if y > 0:
				up = entity.dist_map[y - 1][x]
			if y < ymax:
				down = entity.dist_map[y + 1][x]
			if x > 0:
				left = entity.dist_map[y][x - 1]
			if x < xmax:
				right = entity.dist_map[y][x + 1]

			options = [up, down, left, right]

			options = [opt for opt in options if opt >= 0]

			if options:
				minval = min(options)

				if up == minval:
					return UP
				elif down == minval:
					return DOWN 
				elif left==minval:
					return LEFT
				elif right==minval:
					return RIGHT
		return None



	def toward_entity(self, entity):
		y = self.y
		x = self.x
		up = -1
		down = -1
		left = -1
		right = -1
		if entity.dist_map:
			ymax = len(entity.dist_map) - 1
			xmax = len(entity.dist_map[0]) - 1
			if y > 0:
				up = entity.dist_map[y - 1][x]
			if y < ymax:
				down = entity.dist_map[y + 1][x]
			if x > 0:
				left = entity.dist_map[y][x - 1]
			if x < xmax:
				right = entity.dist_map[y][x + 1]

			options = [up, down, left, right]

			options = [opt for opt in options if opt >= 0]

			if options:
				minval = min(options)

				if up == minval:
					return UP
				elif down == minval:
					return DOWN 
				elif left==minval:
					return LEFT
				elif right==minval:
					return RIGHT
		return None

	def flee_entity(self, entity):
		y = self.y
		x = self.x
		up = -1
		down = -1
		left = -1
		right = -1
		if entity.dist_map:
			ymax = len(entity.dist_map) - 1
			xmax = len(entity.dist_map[0]) - 1
			if y > 0:
				up = entity.dist_map[y - 1][x]
			if y < ymax:
				down = entity.dist_map[y + 1][x]
			if x > 0:
				left = entity.dist_map[y][x - 1]
			if x < xmax:
				right = entity.dist_map[y][x + 1]

			options = [up, down, left, right]

			options = [opt for opt in options if opt >= 0]

			if options:
				maxval = max(options)

				if up == maxval:
					return UP
				elif down == maxval:
					return DOWN 
				elif left==maxval:
					return LEFT
				elif right==maxval:
					return RIGHT
		return None


	def flee_distmap(self, dmap):
		y = self.y
		x = self.x
		up = -1
		down = -1
		left = -1
		right = -1
		if dmap:
			ymax = len(dmap) - 1
			xmax = len(dmap[0]) - 1
			if y > 0:
				up = dmap[y - 1][x]
			if y < ymax:
				down = dmap[y + 1][x]
			if x > 0:
				left = dmap[y][x - 1]
			if x < xmax:
				right = dmap[y][x + 1]

			options = [up, down, left, right]

			options = [opt for opt in options if opt >= 0]

			if options:
				maxval = max(options)

				if up == maxval:
					return UP
				elif down == maxval:
					return DOWN 
				elif left==maxval:
					return LEFT
				elif right==maxval:
					return RIGHT
		return None


class ActingEntity(Entity):
	def action_accumulate(self):
		combatantspeed = sum([combatant.speed for combatant in self.combatants]) / len(self.combatants)
		self.action_points += combatantspeed
		return self.action_points




class Battler(ActingEntity):
	def config(self):
		self.music = 'battle'
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
		entity.backpack.absorb(self.backpack, message = True)

		global_level_offset = self.game.get_var('GLO')
		self.game.set_var('GLO', global_level_offset + 1)

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



class PassiveTillClose(Battler):
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
			if utility.dist_from_entity(self, self.game.player) < 3:
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


class Inn(Entity):
	def config(self):
		self.name = 'Inn'
		self.char = '\x16'
		self.blocking = True
		self.passive = False
	def collide(self, entity, zone):
		modifier = self.game.get_var('GLO')
		
		cost = 100 * modifier

		cost = max(100, cost)


		#If you look like you've got money, it might cost more
		# Add up the value of all equipped items of the combatants
		# and then use some fraction of that as a minimum cost
		equip_value = 0
		for dude in entity.combatants:
			for item in dude.equipment.all_items():
				equip_value += item.value

		print('Equip Value: {}'.format(equip_value))

		equip_cost = equip_value / 3

		cost = max(equip_cost, cost)

		if entity.is_player:
			choice = self.game.display.popup('Sleep at the Inn? Cost: {}'.format(cost), ['Sleep', 'Leave'])
			if choice == 'Sleep':
				if cost <= entity.backpack.gold:
					entity.backpack.gold -= cost
					for c in entity.combatants:
						c.full_heal()
				else:
					print('Not Enough Money')



