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
			print line
	return lines

def savelines(lines, filename):
	f = open(filename, 'w')
	for line in lines:
		f.write(line)
		f.write('\n')
	f.close()

def readmap(filename):
	f = open(filename, 'r')
	content = f.readlines()
	return content

class Zone(object):
	def __init__(self, display = None, files=None):
		if files is None:
			self.maps = [showmap(map_gen(40, 40, 10, 8))]
			self.levels = 1
		else:
			self.maps = []
			self.levels = len(files)
			for file in files:
				self.maps.append(readmap(file))

		self.level = 0
		self.map = self.maps[self.level]

		self.player = None
		self.level_entities = [[] for level in range(self.levels)]
		self.entities = self.level_entities[self.level]

		self.display = display

		self.width = len(self.map[0])
		self.height = len(self.map)


		self.display = display

		self.redraw = []

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
			print len(self.level_entities), level
			self.entities = self.level_entities[level]
			self.width = len(self.map[0])
			self.height = len(self.map)

	def add_entity(self, entity):
		self.entities.append(entity)

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

	def find_empty_position(self, level=None):
		if level == None:
			level = self.level
		while True:
			x = random.randint(0, len(self.maps[level][0]) - 1)
			y = random.randint(0, len(self.maps[level]) - 1)
			if self.maps[level][y][x] == WALKABLE:
				return (x, y)

	def check_pos(self, x, y):
		for e in self.entities:
			if (e.x == x) and (e.y == y):
				return [ENTITY, e]
		if (self.player.x == x) and (self.player.y == y):
			return [PLAYER, self.player]
		if len(self.map) > y and len(self.map[0]) > x:
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
