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

		self.dist_map = [[0] * self.width] * self.height

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

	def calcDistGraph(self):
		self.dist_map = [[-1 for x in range(self.width)] for x in range(self.height)]
		#self.dist_map = [[99999] * self.width] * self.height
		x0 = self.player.x
		y0 = self.player.y
		d = 0
		self.dist_map[y0][x0] = d
		#print('init {}, {}, {}'.format(x0, y0, self.dist_map[y0][x0]) )
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
				if point[1] < self.height - 2:
					down = (point[0], point[1] + 1)
					pts.append(down)
				if point[0] > 0:
					left = (point[0] - 1, point[1])
					pts.append(left)
				if point[0] < self.width - 2:
					right = (point[0] + 1, point[1])
					pts.append(right)

				d = d + 1
				#for pt in [up, down, left, right]:
				for pt in pts:
					if pt not in checked:
						chk_pos = self.check_pos(pt[0], pt[1])
						if chk_pos[0] != WALL:
							if pt[0] == x0 and pt[1] == y0:
								print('error')
								print (str(checked))
							if (self.dist_map[pt[1]][pt[0]] > d) or (self.dist_map[pt[1]][pt[0]] < 0):
								#print('error 2 {} {}'.format(d,self.dist_map[pt[1]][pt[0]] ))
								self.dist_map[pt[1]][pt[0]] = d
								to_check.append(pt)
							i = i + 1
							checked.add(pt)


	def toward_player(self, x, y):
		up = self.dist_map[y - 1][x]
		down = self.dist_map[y + 1][x]
		left = self.dist_map[y][x - 1]
		right = self.dist_map[y][x + 1]

		options = [up, down, left, right]

		options = [opt for opt in options if opt >= 0]

		if options:
			minval = min(options)

			if minval == 0:
				print 'targeting hero'
			if up == minval:
				return UP
			elif down == minval:
				return DOWN 
			elif left==minval:
				return LEFT
			elif right==minval:
				return RIGHT
		return None


	def show_distmap(self):
		self.map = []
		for y in range(self.height - 1):
			line = ''
			for x in range(self.width):
				line = line + str(self.dist_map[y][x])[-1]
			self.map.append(line)
			line = None
		print(line)
		#print('{}'.format(self.dist_map[:10]))

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
