#!/usr/bin/python
#coding: utf-8 
import main
import entities
import random
from constants import *

def Random_Map_Insert(zone, entity, level=None):
	try:
		entity = entity(zone.game)
	except:
		pass

	if level is None:
		level = zone.level

	pos = zone.find_empty_position(level)
	#e1 = entity(zone.game, x=pos[0], y=pos[1])
	entity.x = pos[0]
	entity.y = pos[1]
	zone.add_entity(entity)

def map_search(zone, id, level=0):
	for y in range(len(zone.maps[level]) - 2):
		for x in range(len(zone.maps[level][0]) - 2):
			if zone.maps[level][y][x] == str(id):
				return x, y
	return None, None

def Positional_Map_Insert(zone, entity, id, level=0, replace=True):
	result = map_search(zone, id, level)
	if result[0] is not None:
		e1 = entity(zone.game, x=result[0], y=result[1])
		if e1.x is not None:
			if e1.y is not None:
				zone.add_entity(e1)
				if replace:
					line0 = zone.maps[level][e1.y][:e1.x]
					line1 = zone.maps[level][e1.y][e1.x + 1:]
					zone.maps[level][e1.y] = line0 + '.' + line1
					#zone.maps[level][e1.y][e1.x] = '.'

def Stair_Handler(zone, dir=0):
	levels = len(zone.maps)
	if levels > 1:
		for level in range(levels - 1):
			if dir == 0:
				down_pos = map_search(zone, '>', level)
				up_pos = map_search(zone, '<', level + 1)
			else:
				down_pos = map_search(zone, '>', level + 1)
				up_pos = map_search(zone, '<', level)
			
			up = entities.UpStairs(zone.game)
			up.new_x = down_pos[0]
			up.new_y = down_pos[1]
			up.x = up_pos[0]
			up.y = up_pos[1]
			down = entities.DownStairs(zone.game)
			down.new_x = up_pos[0]
			down.new_y = up_pos[1]
			down.x = down_pos[0]
			down.y = down_pos[1]

			if dir == 0:
				zone.level_entities[level].append(down)
				zone.level_entities[level + 1].append(up)
			else:
				zone.level_entities[level].append(up)
				zone.level_entities[level + 1].append(down)


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

def flatten(map, printout = False):
	lines = []
	for y in map:
		line = ''.join(y)
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

def readmap(filename):
	f = open(filename, 'r')
	content = f.readlines()
	return content


def debug_map():
	showmap(mt.map_gen(70, 40, 20, 8))

def drunkard_walk(xmax = 30, ymax = 30, percentage = 0.3):
	map = [['#' for x in range(xmax)] for y in range(ymax)]
	x, y = (int(xmax / 2), int(ymax/2))
	remove_target = percentage * xmax * ymax
	removed = 0

	dirs = [(0, 1), (1, 0), (-1, 0), (0, -1)]

	while removed < remove_target:
		if map[y][x] == '#':
			removed += 1
			map[y][x] = '.'
		dir = random.choice(dirs)

		x1 = x + dir[0]
		y1 = y + dir[1]

		if x1 < (xmax - 1) and x1 > 0:
			if y1 < (ymax - 1) and y1 > 0:
				x = x1
				y = y1
	return map

def add_entry(map, entry_dir, tries = 2):
	xmax = len(map[0]) - 1
	ymax = len(map) - 1

	dirs = [(0, 1), (1, 0),(-1, 0),(0, -1)]
	for trial in range(tries):
		if entry_dir == UP:
			y = 0
			x = random.choice(range(1, xmax))
			#print 'setting new xy start at {}, {}'.format(x, y)
		elif entry_dir == DOWN:
			y = ymax
			x = random.choice(range(1, xmax))
			#print 'setting new xy start at {}, {}'.format(x, y)
		elif entry_dir == LEFT:
			y = random.choice(range(1,ymax))
			x = 0
			#print 'setting new xy start at {}, {}'.format(x, y)
		elif entry_dir == RIGHT:
			y = random.choice(range(1,ymax))
			x = xmax
			#print 'setting new xy start at {}, {}'.format(x, y)


		while map[y][x] != '.':
			if map[y][x] == '#':
				#print 'writing to {}, {}'.format(x, y)
				map[y][x] = '!'
			dir = random.choice(dirs)

			x1 = x + dir[0]
			y1 = y + dir[1]

			if x1 < (xmax) and x1 > 0:
				if y1 < (ymax) and y1 > 0:
					x = x1
					y = y1
	if entry_dir == UP:
		for x in range(xmax):
			map[0][x] = map[1][x]
	elif entry_dir == DOWN:
		for x in range(xmax):
			map[ymax][x] = map[ymax - 1][x]
	elif entry_dir == LEFT:
		for y in range(ymax):
			map[y][0] = map[y][1]
	elif entry_dir == RIGHT:
		for y in range(ymax):
			map[y][xmax] = map[y][xmax - 1]

	for y in range(ymax + 1):
		for x in range(xmax + 1):
			if map[y][x] == '!':
				map[y][x] = '.'

	map[0][0] = '#'
	map[0][xmax] = '#'
	map[ymax][0] = '#'
	map[ymax][xmax] = '#'

	return map


def noise_prune(map):
	xmax = len(map[0]) - 1
	ymax = len(map) - 1

	def isfloor(coord):
		if map[coord[1]][coord[0]] == '.':
			return True
		else:
			return False

	for y in range(ymax):
		for x in range(xmax):
			check = [ (x, y-1), (x, y+1), (x-1, y), (x+1, y)]
			check = __builtins__['map'](isfloor, check)
			#check = __builtins__.map(isfloor, check)
			if all(check):
				map[y][x] = '.'


class Cell(object):
	def __init__(self, x, y):
		self.up = 1
		self.down = 1
		self.left = 1
		self.right = 1
		self.x = x
		self.y = y
		self.map = None
		self.visited = False

	def box(self):
		output = [[' ', ' ', ' '],[' ', ' ', ' '],[' ', ' ', ' ']]
		if self.up:
			output[0] = ['#', '#', '#']
		if self.down:
			output[2] = ['#', '#', '#']
		if self.left:
			output[0][0] = '#'
			output[1][0] = '#'
			output[2][0] = '#'
		if self.right:
			output[0][2] = '#'
			output[1][2] = '#'
			output[2][2] = '#'
		return output
	def __str__(self):

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

		return dir_char[(self.down, self.up, self.left, self.right)] #these are correct for showing the minimap.
		#return dir_char[(self.up, self.down, self.left, self.right)] #these are correct in general



def maze(width, height, clear_percent = 0.99):
	map = [[Cell(x, y) for x in range(width)] for y in range(height)]
	potential_cleared = width * height
	cleared = 0

	# block edges
	for y in range(height):
		for x in range(width):
			if y == 0:
				map[y][x].up = 1
			if x == 0:
				map[y][x].left = 1
			if x == (width - 1):
				map[y][x].right = 1
			if y == (height - 1):
				map[y][x].down = 1

	percent = 0.0
	x = random.randint(0, width - 1)
	y = random.randint(0, height - 1)
	while percent < clear_percent:
		map[y][x].visited = True
		opts = []
		if y > 0:
			if not map[y - 1][x].visited:
				opts.append(UP)
		if x > 0:
			if not map[y][x - 1].visited:
				opts.append(LEFT)
		if y < height - 1:
			if not map[y + 1][x].visited:
				opts.append(DOWN)
		if x < width - 1:
			if not map[y][x + 1].visited:
				opts.append(RIGHT)
		#print('({}, {}) / {}'.format(x, y, len(opts)))
		if len(opts) > 0:
			dir = random.choice(opts)
		else:
			for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
				testx = x + dx
				testy = y + dy
				if testx > 0 and testx < width - 1:
					if testy > 0 and testy < height - 1:
						subtestx = testx
						subtesty = testy - 1
						if subtestx > 0 and subtestx < width - 1:
							if subtesty > 0 and subtesty < height - 1:
								map[testy][testx].up = 0
								map[subtesty][subtestx].down = 0
								if not map[testy][testx].visited:
									cleared += 1

						subtestx = testx
						subtesty = testy + 1
						if subtestx > 0 and subtestx < width - 1:
							if subtesty > 0 and subtesty < height - 1:
								map[testy][testx].down = 0
								map[subtesty][subtestx].up = 0
								if not map[testy][testx].visited:
									cleared += 1

						subtestx = testx + 1
						subtesty = testy
						if subtestx > 0 and subtestx < width - 1:
							if subtesty > 0 and subtesty < height - 1:
								map[testy][testx].left = 0
								map[subtesty][subtestx].right = 0
								if not map[testy][testx].visited:
									cleared += 1
						subtestx = testx - 1
						subtesty = testy
						if subtestx > 0 and subtestx < width - 1:
							if subtesty > 0 and subtesty < height - 1:
								map[testy][testx].right = 0
								map[subtesty][subtestx].left = 0
								if not map[testy][testx].visited:
									cleared += 1

			x = random.randint(0, width - 1)
			y = random.randint(0, height - 1)

		if dir == UP and y > 0:
			map[y][x].up = 0
			map[y - 1][x].down = 0
			y -= 1
			cleared += 1
		if dir == DOWN and y < height - 1:
			map[y][x].down = 0
			map[y + 1][x].up = 0
			y += 1
			cleared += 1
		if dir == LEFT and x > 0:
			map[y][x].left = 0
			map[y][x - 1].right = 0
			x -= 1
			cleared += 1
		if dir == RIGHT and x < width - 1:
			map[y][x].right = 0
			map[y][x + 1].left = 0
			x += 1
			cleared += 1

		percent = cleared / float(potential_cleared)

	return map

def swap_char(map, old_char, new_chars):
	ymax = len(map)
	xmax = len(map[0])
	for y in range(ymax):
		for x in range(xmax):
			if map[y][x] == old_char:
				map[y][x] = random.choice(new_chars)


def calcDistGraph(pt, map):
	height = len(map)
	width = len(map[0])
	dist_map = [[-1 for x in range(width)] for x in range(height)]
	x0 = pt[0]
	y0 = pt[1]
	d = 0
	dist_map[y0][x0] = d
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
			if point[1] < height - 1:
				down = (point[0], point[1] + 1)
				pts.append(down)
			if point[0] > 0:
				left = (point[0] - 1, point[1])
				pts.append(left)
			if point[0] < width - 1:
				right = (point[0] + 1, point[1])
				pts.append(right)

			d = d + 1
			for pt in pts:
				if pt not in checked:
					if map[pt[1]][pt[0]] != '#':
						if (dist_map[pt[1]][pt[0]] > d) or (dist_map[pt[1]][pt[0]] < 0):
							dist_map[pt[1]][pt[0]] = d
							to_check.append(pt)
						i = i + 1
						checked.add(pt)
	return dist_map




def add_stairs(map, up=True, down=True):
	ymax = len(map)
	xmax =len(map[0])
	dmap = None
	if up:
		search = True
		while search:
			y = random.randint(0, ymax - 1)
			x = random.randint(0, xmax - 1)
			if map[y][x] == '.':
				map[y][x] = '<'
				search = False
		xup = x
		yup = y
		dmap = calcDistGraph((xup, yup), map)
	if down:
		search = True
		while search:
			y = random.randint(0, ymax - 1)
			x = random.randint(0, xmax - 1)
			if map[y][x] == '.':
				if dmap is not None:
					if dmap[y][x] > 0:
						map[y][x] = '>'
						search = False
		xdown = x
		ydown = y


