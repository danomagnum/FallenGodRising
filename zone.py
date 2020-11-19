#!/usr/bin/python
#coding: utf-8 

from main import Entity
from constants import *
import items
import math
import utility
import random
import mobs
import entities
import maps.maptools as maptools


def map_gen(height, width, rooms, minroomsize = 4):
	tiles = [[0 for y in range(height)] for x in range(width)]
	for room in range(rooms):
		room_width = random.randint(minroomsize, max(minroomsize + 1, width/rooms))
		room_height = random.randint(minroomsize, max(minroomsize + 1, height/rooms))
		room_x = random.randint(1, width - room_width - 1)
		room_y = random.randint(1, height - room_height - 1)

		for x in range(room_width):
			for y in range(room_height):
				try:
					tiles[room_x + x][room_y + y] = 1
				except IndexError:
					pass

	#set up walls
	for x in range(width):
		for y in range(height):
			if tiles[x][y] == 1:
				if x > 0:
					if tiles[x-1][y] == 0:
						tiles[x-1][y] = 2
				if x < width:
					if tiles[x+1][y] == 0:
						tiles[x+1][y] = 2
				if y > 0:
					if tiles[x][y-1] == 0:
						tiles[x][y-1] = 2
				if y < height:
					if tiles[x][y+1] == 0:
						tiles[x][y+1] = 2

	return tiles

def showmap(tiles, printout = False):
	lines = []
	for x in tiles:
		line = ''
		for y in x:
			if y == 0:
				line += ' '
			elif y  == 1:
				line += WALKABLE
			elif y == 2:
				line += '#'

		lines.append(line)
		if printout:
			print(line)
	return lines

def savelines(lines, filename):
	f = open(filename, 'w')
	for line in lines:
		f.write(line)
		f.write('\n')
	f.close()
class Zone(object):
	def __init__(self, name, game = None, maps = None):
		self.levels = 0
		self.entry = 0
		self.name = name
		self.music = None
		self.special_music = {}
		self.fogs = []
		if maps is not None:
			self.maps = maps
			self.levels = len(maps)
			self.fog_gen()

		self.grid_width = 1
		self.level = 0

		self.map = self.maps[self.level]
		self.fog = self.fogs[self.level]

		self.fast_travel_found = set()
		self.fast_travel_options = {}

		#self.player = None
		self.level_entities = [[] for level in range(self.levels)]
		self.entities = self.level_entities[self.level]
		self.level_visits = [0 for level in range(self.levels)]

		self.game = game

		self.width = 0
		for line in self.map:
			w = len(line)
			self.width = max(w, self.width)
		#self.width = len(self.map[0])
		self.height = len(self.map)

		self.redraw = []
		#utility.call_all_configs(self)
		utility.call_all('config', self)
		self.biome_map = None

	def fog_gen(self):
		fog_char = '█'
		for level in self.maps:
			wd = len(level[0])
			fog = [[fog_char for col in level[0]] for row in level]
			self.fogs.append(fog)

	def get_music(self):
		return self.music

	def depth(self):
		if self.grid_width == 0:
			return max(abs(self.level - self.entry), 1)
		else:
			y0 = self.entry // self.grid_width
			x0 = self.entry - (self.grid_width * y0)

			y1 = self.level // self.grid_width
			x1 = self.level - (self.grid_width * y1)

			return int(math.sqrt((y0 - y1) ** 2 + (x0 - x1) ** 2))

	def check_clear(self):
		return all([e.passive for e in self.entities])

	def biome(self):
		return self.biome_map

	def config(self):
		pass

	def exit(self, entity, direction):
		x = entity.x
		y = entity.y
		if direction == UP:
			newlevel = self.level + self.grid_width
			if newlevel >= len(self.maps):
				return
			else:
				y = len(self.maps[newlevel]) - 1
				try:
					if self.maps[newlevel][y][x] == WALKABLE:
						newx, newy = x, y
					else:
						newx, newy = self.find_empty_position(level=newlevel, position=DOWN)
				except:
					newx = entity.x
					newy = entity.y
					print('error going up @ ({}, {})'.format(x, y))
		elif direction == DOWN:
			newlevel = self.level - self.grid_width
			if newlevel < 0:
				return
			else:
				y = 0
				if self.maps[newlevel][y][x] == WALKABLE:
					newx, newy = x, y
				else:
					newx, newy = self.find_empty_position(level=newlevel, position=UP)
		elif direction == LEFT:
			newlevel = self.level - 1
			if newlevel < 0:
				return
			else:
				x = len(self.maps[newlevel][y]) - 1
				if self.maps[newlevel][y][x] == WALKABLE:
					newx, newy = x, y
				else:
					newx, newy = self.find_empty_position(level=newlevel, position=RIGHT)
		elif direction == RIGHT:
			newlevel = self.level + 1
			if newlevel >= len(self.maps):
				return
			else:
				x = 0
				try:
					if self.maps[newlevel][y][x] == WALKABLE:
						newx, newy = x, y
					else:
						newx, newy = self.find_empty_position(level=newlevel, position=LEFT)
				except:
					print('Failed at ({}, {}) / ({}, {})'.format(x, y, entity.x, entity.y))
					newx, newy = self.find_empty_position(level=newlevel, position=LEFT)


		entity.x = newx
		entity.y = newy


		if self.game.overworld == self:
			self.game.overworld_y = int(newlevel % self.grid_width)
			self.game.overworld_x = int(newlevel / self.grid_width)
		if entity.is_player:
			self.change_level(newlevel)
		else:
			self.remove_entity(entity)
			self.add_entity(entity, newlevel)
		self.check_fasttravel()

	def check_fasttravel(self):
		if self.level in self.fast_travel_options:
			self.fast_travel_found.add(self.fast_travel_options[self.level])
			print('Found new fast travel location: {}'.format(self.fast_travel_options[self.level].name))
			del(self.fast_travel_options[self.level])
		

	def change_level(self, level):
		if self.game.player is not None:
			self.game.player.target_map = None # cancel any auto-moves if we changed levels
		if level < 0:
			print("Can't go below level 0")
		elif level > (len(self.maps) - 1):
			print("Can't go past end of zone")
		else:
			x = int(level / self.grid_width)
			y = int(level % self.grid_width)
			if self.grid_width > 1:
				if self.game is not None:
					print("{} ({}, {}) / ({}, {}) {}".format(self.name, x, y, self.game.overworld_x, self.game.overworld_y, str(self.game.biome())))
			else:
				if self.game is not None:
					print("{} Level {} / {}".format(self.name, level, self.game.biome()))
			self.level_entities[self.level] = self.entities
			self.level = level
			self.map = self.maps[self.level]
			self.fog = self.fogs[self.level]
			#print(len(self.level_entities), level)
			self.entities = self.level_entities[level]
			#self.width = len(self.map[0])
			self.level_visits[level] += 1


			#you can bind a property "Level_001" to a function that takes a zone as a parameter
			#to get custom level events / population per level
			level_method = 'level_{:03}'.format(level)
			try:
				method = getattr(self, level_method)
			except:
				method = None

			if method is not None:
				try: # if the method was outside of a class, this works
					method(self)
				except:
					#if it was in a class to start with this works
					method()

			else:
				self.level_populate(level, self.level_visits[level])


			self.width = 0
			for line in self.map:
				w = len(line)
				self.width = max(w, self.width)
			self.height = len(self.map)

		self.check_fasttravel()

	def level_populate(self, level, visit_no):
		pass

	def add_entity(self, entity, level=None):
		if entity == self.game.player:
			return
		if level is None:
			level = self.level
		if level < 0:
			return
		if level > self.levels:
			return
		if entity in self.level_entities[level]:
			return
		self.level_entities[level].append(entity)
		self.entities = self.level_entities[self.level]

	def remove_entity(self, entity, level=None):
		if entity == self.game.player:
			return
		if level is None:
			level = self.level
		if level < 0:
			return
		if level > self.levels:
			return
		if entity in self.entities:
			self.level_entities[level].remove(entity)
			self.entities = self.level_entities[self.level]

	def tick(self):
		if self.game.player is not None:
			self.redraw.append([self.game.player.x, self.game.player.y])
			self.game.player.tick(zone=self)
			self.game.player.subtick(zone=self)

		for e in self.entities:
			# first we will mark the positions of the entities as needing redrawn.  This will
			# make sure the map is redrawn if they move or are removed.  If they haven't moved,
			# they will be drawn on top of the map anyway so it's no problem.
			self.redraw.append([e.x, e.y])
			if e.enabled:
				utility.call_all('tick', e, self)
				utility.call_all('subtick', e, self)
				#e.tick(zone=self)
				#e.subtick(zone=self)
		# get rid of any entities that were disabled
		self.entities = [e for e in self.entities if e.enabled] 

	def find_empty_position(self, level=None, position=None):
		if position is None:
			if level == None:
				level = self.level
			while True:
				y = random.randint(0, len(self.maps[level]) - 1)
				x = random.randint(0, len(self.maps[level][y]) - 1)
				if self.maps[level][y][x] == WALKABLE:
					return (x, y)
		elif position == UP:
			y = 0
			options = []
			for cell_x in range(len(self.maps[level][y])):
				if self.maps[level][y][cell_x] == WALKABLE:
					options.append((cell_x, y))
			if len(options) > 0:
				return random.choice(options)
			else:
				print('Could not find a valid position Up')
		elif position == DOWN:
			y = len(self.maps[level]) - 1
			options = []
			for cell_x in range(len(self.maps[level][y])):
				if self.maps[level][y][cell_x] == WALKABLE:
					options.append((cell_x, y))
			if len(options) > 0:
				return random.choice(options)
			else:
				print('Could not find a valid position Down')
		elif position == LEFT:
			x = 0
			options = []
			
			for cell_y in range(len(self.maps[level])):
				if self.maps[level][cell_y][0] == WALKABLE:
					options.append((x, cell_y))

			if len(options) > 0:
				return random.choice(options)
			else:
				print('Could not find a valid position Left')

		elif position == RIGHT:
			options = []
			for cell_y in range(len(self.maps[level])):
				cell_x = len(self.maps[level][cell_y]) - 1
				if self.maps[level][cell_y][cell_x] == WALKABLE:
					options.append((cell_x, cell_y))

			if len(options) > 0:
				return random.choice(options)
			else:
				print('Could not find a valid position Right')

			#while True:
				#y = random.randint(0, len(self.maps[level]) - 1)
				#x = len(self.maps[level][y]) - 1
				#if self.maps[level][y][x] == WALKABLE:
					#return (x, y)
		print('Could not find a valid point')
		return (0, 0)

	def check_pos(self, x, y):
		for e in self.entities:
			if (e.x == x) and (e.y == y):
				return [ENTITY, e]
		if x < 0:
			return [LEFT, None]
		if y < 0:
			return [UP, None]
		if y >= len(self.map):
			return [DOWN, None]
		if x >= len(self.map[y]):
			return [RIGHT, None]

		if (self.game.player.x == x) and (self.game.player.y == y):
			return [PLAYER, self.game.player]

		if self.map[y][x] != WALKABLE:
			return [WALL, None]
		return [EMPTY, None]

	def LOS_check(self, x0, y0, x1, y1):
		"Bresenham's line algorithm"
		pts = set()
		dx = abs(x1 - x0)
		dy = abs(y1 - y0)
		x, y = x0, y0
		sx = -1 if x0 > x1 else 1
		sy = -1 if y0 > y1 else 1
		if dx > dy:
			err = dx / 2.0
			while x != x1:
				pts.add((x, y))
				err -= dy
				if err < 0:
					y += sy
					err += dx
				x += sx
		else:
			err = dy / 2.0
			while y != y1:
				pts.add((x, y))
				err -= dx
				if err < 0:
					x += sx
					err += dy
				y += sy		
		visibilities = [self.check_pos(pt[0], pt[1])[0] for pt in pts]
		return not (WALL in visibilities)

	def dist_map(self, x, y):
		dist_map = [[-1 for x in range(self.width)] for x in range(self.height)]
		x0 = x
		y0 = y
		d = 0
		try:
			dist_map[y0][x0] = d
		except:
			print('error @ ({}, {})'.format(x0, y0))
			return None
		checked = set()
		checked.add((x0,y0))
		to_check = [(x0,y0)]
		checking = []
		i = 0
		while len(to_check) > 0:
			checking = to_check[:]
			to_check = []
			for point in checking:
				d = dist_map[point[1]][point[0]]
				pts = []
				if point[1] > 0:
					up = (point[0], point[1] - 1)
					pts.append(up)
				if point[1] < self.height - 1:
					down = (point[0], point[1] + 1)
					pts.append(down)
				if point[0] > 0:
					left = (point[0] - 1, point[1])
					pts.append(left)
				if point[0] < self.width - 1:
					right = (point[0] + 1, point[1])
					pts.append(right)

				d = d + 1
				for pt in pts:
					if pt not in checked:
						chk_pos = self.check_pos(pt[0], pt[1])
						if chk_pos[0] != WALL:
							if pt[0] == x0 and pt[1] == y0:
								print('error')
							if (dist_map[pt[1]][pt[0]] > d) or (dist_map[pt[1]][pt[0]] < 0):
								dist_map[pt[1]][pt[0]] = d
								to_check.append(pt)
							i = i + 1
							checked.add(pt)
		return dist_map


def overworld_gen(maze):
	#dict key=(up, down, left, right)
	# 0 = open 1 = closed
	dir_char = {(1, 1, 1, 1): ' ',
		    (0, 1, 1, 1): '╨',
	            (1, 0, 1, 1): '╥',
		    (1, 1, 0, 1): '╡',
		    (1, 1, 1, 0): '╞',

		    (0, 0, 1, 1): '║',
		    (0, 1, 0, 1): '╝',
		    (0, 1, 1, 0): '╚',
		    (1, 0, 0, 1): '╗',
		    (1, 0, 1, 0): '╔',
		    (1, 1, 0, 0): '═',

		    (0, 0, 0, 1): '╣',
		    (0, 0, 1, 0): '╠',
		    (0, 1, 0, 0): '╩',
		    (1, 0, 0, 0): '╦',

		    (0, 0, 0, 0): '╬'}

	output = []
	for y in maze:
		line = ''
		for x in y:
			line += dir_char[(x.up, x.down, x.left, x.right)]
		print(line)
		output.append(line)
	return output

class LinearZone(Zone):
	def level_populate(self, level, visit_no):
		gen_level = 1
		if self.game.player is not None:
			gen_level = self.game.player.level

		if visit_no < 2:
			#if I only want to populate on the first visit
			item_count = random.randint(0,2)
			for i in range(item_count):
				chance = random.random()
				if chance < 0.05:
					newitem = items.gen_gear(self.game, gen_level)
				elif chance < 0.3:
					newitem = items.scrolls.gen_movescroll(self.game)
				else:
					newitem = items.gen_base_item(self.game)
				maptools.Random_Map_Insert(self, entities.Treasure(self.game, [newitem,]))
			mob_count = random.randint(0, 6)
			for m in range(mob_count):
				moblist = utility.select_by_level(level, self.mobchoices)
				maptools.Random_Map_Insert(self, mobs.party(self.game, moblist[0], moblist[1], level, moblist[3:], moblist[2]))


