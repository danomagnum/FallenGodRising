import random

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
				line += '.'
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

class Entity(object):
	def __init__(self, x=0, y=0, char='@'):
		self.x = x
		self.y = y
		self.char = char

class Zone(object):
	def __init__(self, display, filename=None):
		if filename is None:
			self.map = showmap(map_gen(40, 40, 10, 8))
		else:
			self.map = readmap('maps/test0.map')
		self.Player = Entity()

		Others = []

		self.display = display

		self.width = len(self.map[0])
		self.height = len(self.map)
		self.display = display

	def move(self, direction):
		UP = 1
		DOWN = 2
		LEFT = 3
		RIGHT = 4


		if direction == UP:
			if self.map[self.Player.y - 1][self.Player.x] == '.':
				self.display.mappad.addch(self.Player.y, self.Player.x, '.')
				self.display.mappad.addch(self.Player.y - 1, self.Player.x, self.Player.char)
				self.Player.y -= 1
				self.display.y = max(0, self.display.y -1)
		elif direction == DOWN:
			if self.map[self.Player.y + 1][self.Player.x] == '.':
				self.display.mappad.addch(self.Player.y, self.Player.x, '.')
				self.display.mappad.addch(self.Player.y + 1, self.Player.x, '@')
				self.Player.y += 1
				self.display.y = min((self.display.mappad.getmaxyx()[0]  - self.display.mapbox.getmaxyx()[0]), self.display.y + 1)
		elif direction == LEFT:
			if self.map[self.Player.y][self.Player.x - 1] == '.':
				self.display.mappad.addch(self.Player.y, self.Player.x, '.')
				self.display.mappad.addch(self.Player.y, self.Player.x - 1, '@')
				self.Player.x -= 1
				self.display.x = max(0, self.display.x -1)
		elif direction == RIGHT:
			if self.map[self.Player.y][self.Player.x + 1] == '.':
				self.display.mappad.addch(self.Player.y, self.Player.x, '.')
				self.display.mappad.addch(self.Player.y, self.Player.x + 1, '@')
				self.Player.x += 1
				self.display.x = min((self.display.mappad.getmaxyx()[1]  - self.display.mapbox.getmaxyx()[1]), self.display.x + 1)

	def find_empty_position(self):
		while True:
			x = random.randint(0, len(self.map[0]) - 1)
			y = random.randint(0, len(self.map) - 1)
			if self.map[y][x] == '.':
				return (x, y)


