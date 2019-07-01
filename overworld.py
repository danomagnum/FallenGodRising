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
	def __init__(self, display = None, filename=None):
		if filename is None:
			self.map = showmap(map_gen(40, 40, 10, 8))
		else:
			self.map = readmap(filename)

		self.player = None

		self.entities = []

		self.display = display

		self.width = len(self.map[0])
		self.height = len(self.map)
		self.display = display

		self.redraw = []

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
		# get rid of any entities that were disabled
		self.entities = [e for e in self.entities if e.enabled]


	def find_empty_position(self):
		while True:
			x = random.randint(0, len(self.map[0]) - 1)
			y = random.randint(0, len(self.map) - 1)
			if self.map[y][x] == WALKABLE:
				return (x, y)

	def check_pos(self, x, y):
		for e in self.entities:
			if (e.x == x) and (e.y == y):
				return [ENTITY, e]
		if (self.player.x == x) and (self.player.y == y):
			return [PLAYER, self.player]
		if self.map[y][x] != WALKABLE:
			return [WALL, None]
		return [EMPTY, None]

