import random
import math
import utility
import items
import elements
import battle
import keys
from constants import *


class GameOver(Exception):
	pass

class Game(object):
	def __init__(self):
		self.overworld = None
		self.biome_map = None
		self.overworld_x = 0
		self.overworld_y = 0
		self.overworld_minimap = None

		self.zone = None
		self.zones = {}
		self.display = None
		self.player = None
		self.game_vars = {}
		self.fast_travel = set()
		self.fast_travel.add('Overworld')

	def biome(self):
		if self.zone == self.overworld:
			if self.biome_map is not None:
				#TODO: fix this
				return elements.biomes[self.biome_map[self.overworld_x][self.overworld_y]]
				#return elements.biomes[self.biome_map[self.overworld_y][self.overworld_x]]
			else:
				return ''
		else:
			return self.zone.biome()

	def add_zone(self, zone):
		if zone.name not in self.zones:
			self.zones[zone.name] = zone
		if self.zone is None:
			self.zone = zone

	def change_zone(self, zonename, newx = None, newy = None, newlevel=None):
		if zonename in self.zones:
			self.zone = self.zones[zonename]
			if newx is not None:
				self.player.x = newx
			if newy is not None:
				self.player.y = newy
			if newlevel is not None:
				self.zone.change_level(newlevel)
			self.display.change_zone(self.zone)
			self.fast_travel.add(zonename)

		else:
			print('Zone {} does not exist'.format(zonename))

	def get_var(self, variable):
		return self.game_vars.get(variable, 0)

	def set_var(self, variable, value):
		self.game_vars[variable] = value
	
	def get_confirm(self):
		key = self.display.msgbox.getch()
		if key in keys.SELECT:
			return True
		else:
			return False
	
	def debug(self, command):
		exec(command)

class Equipment(object):
	def __init__(self, game):
		self.game = game
		self.Head = None
		self.Body = None
		self.Left = None
		self.Right = None
		self.Hands = None
		self.Token = None
		self.helptext = ''
	
	def equip(self, item):
		return_items = []
		if item.target_type == EQUIP_HEAD:
			if self.Head is not None:
				return_items.append(self.Head)
			self.Head = item
		elif item.target_type == EQUIP_BODY:
			if self.Body is not None:
				return_items.append(self.Body)
			self.Body = item
		elif item.target_type == EQUIP_RIGHT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Right is not None:
				return_items.append(self.Right)
			self.Right = item
		elif item.target_type == EQUIP_LEFT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Left is not None:
				return_items.append(self.Left)
			self.Left = item
		elif item.target_type == EQUIP_HANDS:
			if self.Hands is not None:
				return_items.append(self.Hands)
			if self.Left is not None:
				return_items.append(self.Left)
				self.Left = None
			if self.Right is not None:
				return_items.append(self.Right)
				self.Right = None
			self.Hands = item
		elif item.target_type == EQUIP_TOKEN:
			if self.Token is not None:
				return_items.append(self.Token)
			self.Token = item

		return return_items
	def unequip(self, target):
		return_items = []
		if target == EQUIP_HEAD:
			if self.Head is not None:
				return_items.append(self.Head)
				self.Head = None
		elif target == EQUIP_BODY:
			if self.Body is not None:
				return_items.append(self.Body)
				self.Body = None
		elif target == EQUIP_RIGHT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Right is not None:
				return_items.append(self.Right)
				self.Right = None
		elif target == EQUIP_LEFT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Left is not None:
				return_items.append(self.Left)
				self.Left = None
		elif target == EQUIP_HANDS:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Left is not None:
				return_items.append(self.Left)
				self.Left = None
			if self.Right is not None:
				return_items.append(self.Right)
				self.Right = None
		elif target == EQUIP_TOKEN:
			if self.Token is not None:
				return_items.append(self.Token)
				self.Token = None
		return return_items
	def purge(self, target):
		return_items = []
		if self.Head is not None:
			return_items.append(self.Head)
			self.Head = None
		if self.Body is not None:
			return_items.append(self.Body)
			self.Body = None
		if self.Hands is not None:
			return_items.append(self.Hands)
			self.Hands = None
		if self.Right is not None:
			return_items.append(self.Right)
			self.Right = None
		if self.Hands is not None:
			return_items.append(self.Hands)
			self.Hands = None
		if self.Left is not None:
			return_items.append(self.Left)
			self.Left = None
		if self.Hands is not None:
			return_items.append(self.Hands)
			self.Hands = None
		if self.Left is not None:
			return_items.append(self.Left)
			self.Left = None
		if self.Right is not None:
			return_items.append(self.Right)
			self.Right = None
		if self.Token is not None:
			return_items.append(self.Token)
			self.Token = None
		return return_items
	
	def all_items(self):
		items = [self.Head, self.Body, self.Hands, self.Right, self.Left, self.Token]
		return [item for item in items if item is not None]

	def physical_strength(self, initial): # passive stat boosts take effect on these routines
		for item in self.all_items():
			initial = utility.call_all_recursive(initial, 'physical_strength', item)
		return initial

	def physical_defense(self, initial):
		for item in self.all_items():
			initial = utility.call_all_recursive(initial, 'physical_defense', item)
		return initial

	def special_strength(self, initial):
		for item in self.all_items():
			initial = utility.call_all_recursive(initial, 'special_strength', item)
		return initial

	def special_defense(self, initial):
		for item in self.all_items():
			initial = utility.call_all_recursive(initial, 'special_defense', item)
		return initial
		
	def speed(self, initial):
		for item in self.all_items():
			initial = utility.call_all_recursive(initial, 'speed', item)
		return initial

	def hp(self, initial):
		for item in self.all_items():
			initial = utility.call_all_recursive(initial, 'hp', item)
		return initial

	def max_hp(self, initial):
		for item in self.all_items():
			initial = utility.call_all_recursive(initial, 'max_hp', item)
		return initial

	def evasion(self, initial):
		for item in self.all_items():
			initial = utility.call_all_recursive(initial, 'evasion', item)
		return initial

	def accuracy(self, initial):
		for item in self.all_items():
			initial = utility.call_all_recursive(initial, 'accuracy', item)
		return initial

	def luck(self, initial):
		for item in self.all_items():
			initial = utility.call_all_recursive(initial, 'luck', item)
		return initial

class Entity(object):
	def __init__(self,game, name=None, combatants = None, item_list=None, x=0, y=0, char=None, AI=None, is_player = False):
		self.game = game
		self.defeated_text = None
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


	def attack(self, enemy_ai):
		move = random.choice(self.combatant.moves)
		enemy = random.choice(enemy_ai.combatants)
		target = [self.combatant, enemy][move.default_target]
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
			action = random.choice([ATTACK, ATTACK, ATTACK, ATTACK, ATTACK, RUN])
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


