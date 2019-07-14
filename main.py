import random
import math
import utility
import items
import elements
import battle
import keys
from constants import *

NEWDIST = True
DAMAGE_CALC = 1

MOVE_REGEN_TICKS = 1000


class GameOver(Exception):
	pass

class Game(object):
	def __init__(self):
		self.overworld = None
		self.biome_map = None
		self.overworld_x = 0
		self.overworld_y = 0

		self.zone = None
		self.zones = {}
		self.display = None
		self.player = None
		self.game_vars = {}

	def biome(self):
		if self.zone == self.overworld:
			return elements.biomes[self.biome_map[self.overworld_y][self.overworld[x]]]
		else:
			return zone.biome()

	def add_zone(self, zone):
		if zone.name not in self.zones:
			self.zones[zone.name] = zone
		if self.zone is None:
			self.zone = zone

	def change_zone(self, zonename, newx = None, newy = None):
		if zonename in self.zones:
			self.zone = self.zones[zonename]
			if newx is not None:
				self.player.x = newx
			if newy is not None:
				self.player.y = newy

		else:
			print('Zone {} does not exist'.format(zonename))

	def get_var(self, variable):
		self.game_vars.get(variable, 0)

	def set_var(self, variable, value):
		self.game_vars[variable] = value
	
	def get_confirm(self):
		key = self.display.msgbox.getch()
		if key in keys.SELECT:
			return True
		else:
			return False
	

class Move(object):
	def __init__(self,game, name = None, element_list = None, accuracy = None, power = None, mp = None,  default_target = None):
		self.game = game
		if name is None:
			name = 'MISSINGNAME'
		self.name = name
		if mp is None:
			mp = 10.0
		self.max_mp = mp
		if accuracy is None:
			accuracy = 0.99
		self.accuracy = accuracy
		if power is None:
			power = 10
		self.power = power
		if element_list is None:
			element_list = [elements.Normal]
		self.elements = element_list
		self.uses = 0
		self.physical = (True, True) # Attack stat to use, def stat to use
		if default_target is None:
			default_target=ENEMY
		self.default_target = default_target
	
		self.helptext = ''

		utility.call_all_configs(self)

		self.ticks = 0
		self.mp = self.max_mp

	def config(self):
		pass

	def attack(self, user, targets): # do whatever the attack needs to do
		if (self.mp > 0):
			self.mp -= 1
		else:
			print('{} is out of MP to use move {}'.format(user.name,self.name))
			self.mp = 0
			if 0.2 * user.luck > random.random():
				print('{} used move {}'.format(user.name,self.name))
			else:
				return
		target_coefficient = 1.1 / len(targets)

		for target in targets:
			# figure out if the move hits.
			hit_chance = ((user.speed/target.speed)/9) + user.accuracy/target.evasion * self.accuracy

			if hit_chance * user.luck > random.random():


				# calculate whether it is a critical hit:
				crit_metric = CRIT_RATE * (user.luck / target.luck) * (user.speed / target.speed)
				if random.random() < crit_metric:
					crit_factor = 2 # crit
					print('Crit!')
				else:
					crit_factor = 1

				if self.power != 0: # zero power moves are status only
					if self.physical[0]:
						attack_str = user.physical_strength
					else:
						attack_str = user.special_strength
					if self.physical[1]:
						attack_def = target.physical_defense
					else:
						attack_def = target.special_defense

					if DAMAGE_CALC == 0:
						damage = ((user.level/100.0 ) * attack_str/(attack_def/crit_factor) * self.power + 2) * target_coefficient
					elif DAMAGE_CALC == 1:
						hp_ratio = (target.virtual_hp / 6.0) # virtual hp is the health of a neutrally 
						strdef_ratio = attack_str / (attack_def / crit_factor)
						power_ratio = self.power / 10.0
						level_factor1 =  utility.clamp((1 + (user.level - target.level) / 10), 0.9, 4)
						level_factor1 = math.sqrt(level_factor1)

						damage = hp_ratio * strdef_ratio * power_ratio * level_factor1

					# Do elemental effects
					for atk_element in self.elements:
						for target_element in target.elements:
							damage *= atk_element.effectiveness(target_element)
						for user_element in user.elements:
							if user_element == atk_element:
								damage *= atk_element.bonus


					self.uses += 1

					# This makes athe attacks do more damage as you've got more experience using them
					if damage > 0:
						damage += ((damage + 1) * 3 * min(self.uses, 100.0) / 100.0 + 5) / 10.0
					else:
						damage -= ((-damage + 1) * 3 * min(self.uses, 100.0) / 100.0 + 5) / 10.0

					#use the attacker and defender item attack and defend checks.
					for item in user.equipment.all_items():
						damage = item.attack(damage, user, target)
					for item in target.equipment.all_items():
						damage = item.attack(damage, target, user)

					# final damage randomization and adjustment based on luck
					if NEWDIST:
						# Using the triangle distribution now so the mean can be off-center
						low = damage - (damage/8.0)
						high = damage + (damage/8.0)
						mode = max(min(high, damage * user.luck), low)
						damage = random.triangular(low, high, mode)# normal distribution with stdev of 8% for randomness
						#print low, high, mode, damage
					else:
						damage = random.normalvariate(damage, damage/8.0) # normal distribution with stdev of 8% for randomness
					if damage >= 0:
						damage = max(1,damage)
					else:
						damage = min(-1,damage)

					#apply the damage
					target.hp -= int(damage)

					print('{} used move {} on {} for {}'.format(user.name,self.name, targets[0].name, int(damage)))

				self.effect(target)
			else:
				print('miss!')
	def effect(self, target):
		pass
	def __str__(self):
		string = ''
		string += self.name + ' '
		string += '( ' + str(int(self.mp)) + '/' + str(int(self.max_mp)) + ' )'
		return string
	def tick(self, user):
		tick_rate = MOVE_REGEN_TICKS * self.max_mp
		self.ticks += 1
		if self.ticks > tick_rate:
			self.ticks = 0
			if self.mp < self.max_mp:
				self.mp += 1
		


class Equipment(object):
	def __init__(self, game):
		self.game = game
		self.Head = None
		self.Body = None
		self.Legs = None
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
		elif item.target_type == EQUIP_LEGS:
			if self.Legs is not None:
				return_items.append(self.Legs)
			self.Legs = item
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
		elif target == EQUIP_LEGS:
			if self.Legs is not None:
				return_items.append(self.Legs)
				self.Legs = None
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
		if self.Legs is not None:
			return_items.append(self.Legs)
			self.Legs = None
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
		items = [self.Head, self.Body, self.Legs, self.Hands, self.Right, self.Left, self.Token]
		return [item for item in items if item is not None]

	def physical_strength(self, initial): # passive stat boosts take effect on these routines
		for item in self.all_items():
			initial = item.physical_strength(initial)
		return initial

	def physical_defense(self, initial):
		for item in self.all_items():
			initial = item.physical_defense(initial)
		return initial

	def special_strength(self, initial):
		for item in self.all_items():
			initial = item.special_strength(initial)
		return initial

	def special_defense(self, initial):
		for item in self.all_items():
			initial = item.special_defense(initial)
		return initial
		
	def speed(self, initial):
		for item in self.all_items():
			initial = item.speed(initial)
		return initial

	def hp(self, initial):
		for item in self.all_items():
			initial = item.hp(initial)
		return initial

	def max_hp(self, initial):
		for item in self.all_items():
			initial = item.max_hp(initial)
		return initial

	def evasion(self, initial):
		for item in self.all_items():
			initial = item.evasion(initial)
		return initial

	def accuracy(self, initial):
		for item in self.all_items():
			initial = item.accuracy(initial)
		return initial

	def luck(self, initial):
		for item in self.all_items():
			initial = item.luck(initial)
		return initial

class Character(object):
	def __init__(self, game,  name=None, level=1):
		self.game = game
		self.initialized = False
		if name is None:
			#self.name = 'MissingNo'
			self.name = self.__class__.__name__
		else:
			self.name = name
		self._hp = 1
		self._exp = 0
		self._elements = [elements.Normal]
		self.status = []
		self.equipment = Equipment(game)
		# stat growth rate for p.str, p.def, s.str, s.def, speed, maxhp
		self.coefficients = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
		self.helptext = ''
		self.moves = []
		self._level = 1

		utility.call_all_configs(self)

		self.level = level
		self.full_heal()
		self._exp = self.exp_at_level(self.level)
		self.initialized = True

	@property
	def elements(self):
		e_list = self._elements
		for item in self.equipment.all_items():
			e_list = item.elements(e_list)
		return e_list

	@elements.setter
	def elements(self, value):
		self._elements = value

	def config(self):
		self.moves = []
		self.base_physical_strength = 10
		self.base_physical_defense = 10
		self.base_special_strength = 10
		self.base_special_defense = 10
		self.base_speed = 10
		self.base_hp = 10
		self.base_luck = 10
		self.physical = True
	
	def tick(self):
		pass

	def subtick(self):
		for item in self.equipment.all_items():
			item.subtick(self)
			item.tick(self)
		for move in self.moves:
			move.tick(self)
		for stat in self.status:
			stat.tick(self)

	def __str__(self):
		return self.name

	@property
	def level(self):
		return self._level

	@level.setter
	def level(self, value):
		if self.initialized:
			print('{} leveled up from {} to {}'.format(self.name, self._level, value))
		if value > self._level:
			for lvl in range(self._level + 1, value + 1):
				self._level = lvl
				self._exp = self.exp_at_level(self.level)
				self.levelup()
				level_method = 'level_{:02}'.format(lvl)
				try:
					method = getattr(self, level_method)
				except:
					method = None
				if method is not None:
					method()
		self.full_heal()
	
	def add_move(self, move):
		m = move(self.game)
		if self.initialized:
			print('{} Gained The Skill {}'.format(self.name, m.name))
		self.moves.append(m)

	@property
	def exp(self):
		return self._exp

	@exp.setter
	def exp(self, value):
		self._exp = value
		check_level = True
		while check_level:
			if self._exp > self.exp_at_level(self.level + 1):
				self.level += 1
			else:
				check_level = False

	@property
	def exp_value(self):
		val = self.physical_strength + self.physical_defense
		val += self.special_strength + self.special_defense
		val += self.speed + self.max_hp
		val *= self.level / 6
		return int(val)

	def exp_at_level(self, level):
		return (level ) ** 3

	def exp_progress(self):
		return (float(self.exp) - float(self.exp_at_level(self.level)) ) / float(self.exp_at_level(self.level + 1))
	@property
	def physical_strength(self):
		stat = (self.base_physical_strength + self.coefficients[0]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.physical_strength(stat)
		stat = self.equipment.physical_strength(stat)
		return utility.clamp(stat, 1, 3* self.base_physical_strength)
	@property
	def physical_defense(self):
		stat = (self.base_physical_defense + self.coefficients[1]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.physical_defense(stat)
		stat = self.equipment.physical_defense(stat)
		return utility.clamp(stat, 1, 3* self.base_physical_defense)
	@property
	def special_strength(self):
		stat = (self.base_special_strength + self.coefficients[2]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.special_strength(stat)
		stat = self.equipment.special_strength(stat)
		return utility.clamp(stat, 1, 3* self.base_special_strength)
	@property
	def special_defense(self):
		stat = (self.base_special_defense + self.coefficients[3]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.special_defense(stat)
		stat = self.equipment.special_defense(stat)
		return utility.clamp(stat, 1, 3* self.base_special_defense)

	@property
	def speed(self):
		stat = (self.base_speed + self.coefficients[4]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.speed(stat)
		stat = self.equipment.speed(stat)
		return utility.clamp(stat, 1, 3* self.base_speed)

	@property
	def hp(self):
		stat = self._hp
		for status in self.status:
			stat = status.hp(stat)
		stat = self.equipment.hp(stat)
		return  min(max(0,stat), self.max_hp)
	
	@property
	def luck(self):
		stat = (self.base_luck + 40) / 50.0 # One point of luck is a 2% change. Will need balanced.
		for status in self.status:
			stat = status.luck(stat)
		stat = self.equipment.luck(stat)
		return utility.clamp(stat, 1, 3* self.base_speed)

	@hp.setter
	def hp(self, value):
		self._hp = min(max(0,value), self.max_hp)

	def heal(self, amount):
		if self.hp > 0:
			self._hp = min(max(0,self._hp + amount), self.max_hp)

	@property
	def max_hp(self):
		stat = int((self.base_hp + self.coefficients[5]) * 10 * self.level / 100.0 + 5)
		for status in self.status:
			stat = status.max_hp(stat)
		stat = self.equipment.max_hp(stat)
		return stat

	@property
	def virtual_hp(self):
		stat = int((100 + self.coefficients[5]) * 10 * self.level / 100.0 + 5)
		return stat


	@property
	def evasion(self):
		stat = 1.0
		for status in self.status:
			stat = status.evasion(stat)
		stat = self.equipment.evasion(stat)
		return stat

	@property
	def accuracy(self):
		stat = 1.0
		for status in self.status:
			stat = status.accuracy(stat)
		stat = self.equipment.accuracy(stat)
		return stat

	def full_heal(self):
		for move in self.moves:
			move.mp = move.max_mp
		if self.hp > 0:
			self.hp = self.max_hp

	def levelup(self): # override this with sub classes to do fancy things
		pass

	def revive(self):
		if self.hp <= 0:
			self.hp = 1

class Entity(object):
	def __init__(self,game, name=None, combatants = None, item_list=None, x=0, y=0, char=None, AI=None, is_player = False):
		self.game = game
		if name is None:
			name = ''
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
		
		utility.call_all_configs(self)

		if self.is_player:
			self.priority = 10
		else:
			self.priority = 100

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


