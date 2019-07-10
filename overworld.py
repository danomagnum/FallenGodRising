import random
from main import Entity
from constants import *


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
		self.name = name
		if maps is not None:
			self.maps = maps
			self.levels = len(maps)

		self.grid_width = 1
		self.level = 0
		self.map = self.maps[self.level]

		self.player = None
		self.level_entities = [[] for level in range(self.levels)]
		self.entities = self.level_entities[self.level]

		self.game = game

		self.width = 0
		for line in self.map:
			w = len(line)
			self.width = max(w, self.width)
		#self.width = len(self.map[0])
		self.height = len(self.map)

		self.redraw = []
		self.config()

	def config(self):
		pass

	def exit(self, entity, direction):
		if direction == UP:
			newlevel = self.level + self.grid_width
			if newlevel >= len(self.maps):
				return
			else:
				newx, newy = self.find_empty_position(level=newlevel, position=DOWN)
		elif direction == DOWN:
			newlevel = self.level - self.grid_width
			if newlevel < 0:
				return
			else:
				newx, newy = self.find_empty_position(level=newlevel, position=UP)
		elif direction == LEFT:
			newlevel = self.level - 1
			if newlevel < 0:
				return
			else:
				newx, newy = self.find_empty_position(level=newlevel, position=RIGHT)
		elif direction == RIGHT:
			newlevel = self.level + 1
			if newlevel >= len(self.maps):
				return
			else:
				newx, newy = self.find_empty_position(level=newlevel, position=LEFT)


		entity.x = newx
		entity.y = newy
		if entity.is_player:
			self.change_level(newlevel)
		else:
			self.remove_entity(entity)
			self.add_entity(entity, newlevel)
		

	def change_level(self, level):
		if level < 0:
			print("Can't go below level 0")
		elif level > (len(self.maps) - 1):
			print("Can't go past end of zone")
		else:
			print("Level {}".format(level))
			self.level_entities[self.level] = self.entities
			self.level = level
			self.map = self.maps[self.level]
			print(len(self.level_entities), level)
			self.entities = self.level_entities[level]
			#self.width = len(self.map[0])

			self.width = 0
			for line in self.map:
				w = len(line)
				self.width = max(w, self.width)
			self.height = len(self.map)

	def add_entity(self, entity, level=None):
		if entity == self.player:
			return
		if level is None:
			level = self.level
		if level < 0:
			return
		if level > self.levels:
			return
		if entity in self.level_entities[level]:
			print 'in list already'
			return
		self.level_entities[level].append(entity)
		self.entities = self.level_entities[self.level]

	def remove_entity(self, entity, level=None):
		if entity == self.player:
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

	def set_player(self, entity):
		self.player = entity
	
	def tick(self):
		if self.player is not None:
			self.redraw.append([self.player.x, self.player.y])
			self.player.tick(zone=self)
		for e in self.entities:
			# first we will mark the positions of the entities as needing redrawn.  This will
			# make sure the map is redrawn if they move or are removed.  If they haven't moved,
			# they will be drawn on top of the map anyway so it's no problem.
			self.redraw.append([e.x, e.y])
			if e.enabled:
				e.tick(zone=self)
				e.subtick(zone=self)
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
			while True:
				x = random.randint(0, len(self.maps[level][y]) - 1)
				if self.maps[level][y][x] == WALKABLE:
					return (x, y)
		elif position == DOWN:
			y = len(self.maps[level]) - 1
			while True:
				x = random.randint(0, len(self.maps[level][y]) - 1)
				if self.maps[level][y][x] == WALKABLE:
					return (x, y)
		elif position == LEFT:
			x = 0
			while True:
				y = random.randint(0, len(self.maps[level]) - 1)
				if self.maps[level][y][x] == WALKABLE:
					return (x, y)
		elif position == RIGHT:
			while True:
				y = random.randint(0, len(self.maps[level]) - 1)
				x = len(self.maps[level][y]) - 1
				if self.maps[level][y][x] == WALKABLE:
					return (x, y)

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

		if (self.player.x == x) and (self.player.y == y):
			return [PLAYER, self.player]

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
