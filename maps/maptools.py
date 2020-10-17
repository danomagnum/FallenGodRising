#!/usr/bin/python
#coding: utf-8 
import main
import entities
import random
from constants import *
import sys

#MAPSIZE = [48, 36]
MAPSIZE = [60, 36]

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
	zone.add_entity(entity, level)

def map_search(zone, id, level=0):
	for y in range(len(zone.maps[level]) - 2):
		for x in range(len(zone.maps[level][0]) - 2):
			if zone.maps[level][y][x] == str(id):
				return x, y
	return None, None

def Positional_Map_Insert(zone, entity, id, level=0, replace=True):
	result = map_search(zone, id, level)
	if result[0] is not None:
		try:
			e1 = entity(zone.game, x=result[0], y=result[1])
		except:
			e1 = entity
			e1.x = result[0]
			e1.y = result[1]
		if e1.x is not None:
			if e1.y is not None:
				zone.add_entity(e1, level)
				if replace:
					line0 = zone.maps[level][e1.y][:e1.x]
					line1 = zone.maps[level][e1.y][e1.x + 1:]
					zone.maps[level][e1.y] = line0 + '.' + line1
					#zone.maps[level][e1.y][e1.x] = '.'
		return True
	else:
		return False

def Door_Handler(zone):
	levels = len(zone.maps)
	doors = 0
	for level in range(levels):
		while Positional_Map_Insert(zone, entities.Door, '+', level):
			doors += 1
	zone.doors_added = doors

def Door_Handler_onelevel(zone, level):
	doors = 0
	while Positional_Map_Insert(zone, entities.Door, '+', level):
		doors += 1



def Stair_Handler(zone, dir=0):
	levels = len(zone.maps)
	if levels > 1:
		for level in range(levels - 1):
			up = entities.UpStairs(zone.game)
			down = entities.DownStairs(zone.game)
			down_pos = map_search(zone, '>', level)
			up_pos = map_search(zone, '<', level + 1)

			if dir == 0:
				pass
			else:
				up.char = '>'
				down.char = '<'
			
			up.new_x = down_pos[0]
			up.new_y = down_pos[1]
			up.x = up_pos[0]
			up.y = up_pos[1]
			down.new_x = up_pos[0]
			down.new_y = up_pos[1]
			down.x = down_pos[0]
			down.y = down_pos[1]

			zone.level_entities[level].append(down)
			zone.level_entities[level + 1].append(up)


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

def drunkard_walk(xmax, ymax, percentage = 0.3):
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
		self.char = None

	def close(self):
		self.visited = False
		self.up = 1
		self.down = 1
		self.left = 1
		self.right = 1

	def open(self, dir):
		self.visited = True
		width = len(self.map[0])
		height = len(self.map)
		if dir == UP:
			if self.y > 0:
				self.up = 0
				if inbounds(self.x, self.y - 1, width, height):
					self.map[self.y - 1][self.x].down = 0
					self.map[self.y - 1][self.x].visited = True
					return self.map[self.y - 1][self.x]
		elif dir == DOWN:
			if self.y < (height - 1):
				self.down = 0
				if inbounds(self.x, self.y + 1, width, height):
					self.map[self.y + 1][self.x].up = 0
					self.map[self.y + 1][self.x].visited = True
					return self.map[self.y + 1][self.x]
		elif dir == LEFT:
			if self.x > 0:
				self.left = 0
				if inbounds(self.x - 1, self.y, width, height):
					self.map[self.y][self.x - 1].right = 0
					self.map[self.y][self.x - 1].visited = True
					return self.map[self.y][self.x - 1]
		elif dir == RIGHT:
			if self.x < width - 1:
				self.right = 0
				if inbounds(self.x + 1, self.y, width, height):
					self.map[self.y][self.x + 1].left = 0
					self.map[self.y][self.x + 1].visited = True
					return self.map[self.y][self.x + 1]
		return None
	
	def grow(self):
		width = len(self.map[0])
		height = len(self.map)
		if (self.y > 0) and (inbounds(self.x, self.y - 1, width, height)):
			if self.map[self.y - 1][self.x].visited == False:
				self.open(UP)
				return self.map[self.y-1][self.x]
		if (self.y < (height - 1)) and (inbounds(self.x, self.y + 1, width, height)):
			if self.map[self.y + 1][self.x].visited:
				self.open(DOWN)
				return self.map[self.y+1][self.x]
		if (self.x > 0) and inbounds(self.x - 1, self.y, width, height):
			if self.map[self.y][self.x - 1].visited:
				self.open(LEFT)
				return self.map[self.y][self.x - 1]
		if (self.x < width - 1) and inbounds(self.x + 1, self.y, width, height):
			if self.map[self.y][self.x + 1].visited:
				self.open(RIGHT)
				return self.map[self.y][self.x + 1]
		return None

	def unvisited_neighbors(self):
		width = len(self.map[0])
		height = len(self.map)
		count = 0
		if inbounds(self.x, self.y - 1, width, height):
			if self.map[self.y - 1][self.x].visited:
				count += 1
		if inbounds(self.x, self.y + 1, width, height):
			if self.map[self.y + 1][self.x].visited:
				count += 1
		if inbounds(self.x - 1, self.y, width, height):
			if self.map[self.y][self.x - 1].down:
				count += 1
		if inbounds(self.x + 1, self.y, width, height):
			if self.map[self.y][self.x + 1].down:
				count += 1

		return count


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

		if self.char is not None:
			return self.char

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

		dir_char2= {(1, 1, 1, 1): ' ',
			    (0, 1, 1, 1): '╵',
			    (1, 0, 1, 1): '╷',
			    (1, 1, 0, 1): '╴',
			    (1, 1, 1, 0): '╶',

			    (0, 0, 1, 1): '│',
			    (0, 1, 0, 1): '┘',
			    (0, 1, 1, 0): '└',
			    (1, 0, 0, 1): '┐',
			    (1, 0, 1, 0): '┌',
			    (1, 1, 0, 0): '─',

			    (0, 0, 0, 1): '┤',
			    (0, 0, 1, 0): '├',
			    (0, 1, 0, 0): '┴',
			    (1, 0, 0, 0): '┬',

			    (0, 0, 0, 0): '┼'}



		return dir_char2[(self.down, self.up, self.left, self.right)] #these are correct for showing the minimap.
		#return dir_char[(self.up, self.down, self.left, self.right)] #these are correct in general

def inbounds(x,y,width,height):
	if x >= 0 and x <= width - 1:
		if y >= 0 and y <= height - 1:
			return True
	return False

def inbound_padded(x,y,width,height):
	if x > 0 and x < width - 1:
		if y > 0 and y < height - 1:
			return True
	return False



def maze2(width, height, clear_percent=0.99):
	map = [[Cell(x, y) for x in range(width)] for y in range(height)]

	#tell all the cells what map they are a part of
	for row in map:
		for cell in row:
			cell.map = map


	toclear = int(clear_percent * height * width)

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

	# start right in the middle
	# with a cell open on all sides
	x = int(width / 2)
	y = int(height / 2)

	firstcell = map[y][x]

	newtestcells = []
	newtestcells.append(firstcell.open(UP))
	newtestcells.append(firstcell.open(DOWN))
	newtestcells.append(firstcell.open(LEFT))
	newtestcells.append(firstcell.open(RIGHT))

	cleared = 5


	while cleared < toclear:
		cleared += 1
		testcells = newtestcells
		newtestcells = []
		if testcells == []:
			# if we don't have a good cell to use, pick one that has an empty neighbor
			# but is already visited.  This way they are for sure on the main path
			while True:
				x = random.randint(0,width - 1)
				y = random.randint(0,height - 1)
				c = map[y][x]
				nextcell = c.grow()
				if nextcell is not None:
					testcells.append(nextcell)
					break

		for cell in testcells:
			if cell is not None:
				if cell.unvisited_neighbors() > 0:
					# there are cells next to this one we can investigate
					# decide how many exits to poke holes for
					exits = random.choice([1,1,2,2,2,2,2])
					for exit in range(exits):
						dir = random.choice([UP, DOWN, LEFT, RIGHT])
						nextcell = cell.open(dir)
						if nextcell is not None:
							if not nextcell.visited:
								newtestcells.append(nextcell)
								cleared += 1

	
	return map
		


def maze(width, height, clear_percent = 0.99):
	return maze2(width, height, clear_percent)


def maze_original(width, height, clear_percent = 0.99):
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
		if len(opts) > 0:
			dir = random.choice(opts)
		else:
			for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
				testx = x + dx
				testy = y + dy
				if inbound_padded(testx, testy, width, height):
					subtestx = testx
					subtesty = testy - 1
					if inbound_padded(subtestx, subtesty, width, height):
						map[testy][testx].up = 0
						map[subtesty][subtestx].down = 0
						if not map[testy][testx].visited:
							cleared += 1

					subtestx = testx
					subtesty = testy + 1
					if inbound_padded(subtestx, subtesty, width, height):
						map[testy][testx].down = 0
						map[subtesty][subtestx].up = 0
						if not map[testy][testx].visited:
							cleared += 1

					subtestx = testx + 1
					subtesty = testy
					if inbound_padded(subtestx, subtesty, width, height):
						map[testy][testx].left = 0
						map[subtesty][subtestx].right = 0
						if not map[testy][testx].visited:
							cleared += 1
					subtestx = testx - 1
					subtesty = testy
					if inbound_padded(subtestx, subtesty, width, height):
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
				else:
					map[y][x] = '>'
					search = False

		xdown = x
		ydown = y


def overworld_inject(game, zone, entry_level = 0, newchar=None, mask=None):
	ov_ht = len(game.overworld_minimap) - 1
	ov_wd = len(game.overworld_minimap[0]) - 1
	search = True
	while search:
		y = random.randint(0, ov_wd)
		x = random.randint(0, ov_ht)
		cell = game.overworld_minimap[y][x]
		if any([not cell.up, not cell.down, not cell.left, not cell.right]):
			ov_x = x
			ov_y = y
			ov_level = ov_x + ov_y * game.overworld.grid_width
			if not (ov_level in game.overworld.fast_travel_options):
				search = False
	cell.char = newchar
	if mask is not None:
		new_ow_map = empty_zone_with_mask(cell, mask)
		game.overworld.maps[ov_level] = new_ow_map
	

	#Door_Handler(zone)

	ov_x2, ov_y2 = game.overworld.find_empty_position(level=ov_level)

	z_x, z_y = zone.find_empty_position(level=entry_level)
	z_entity = entities.ZoneWarp(game)
	z_entity.x = z_x
	z_entity.y = z_y
	z_entity.new_x = ov_x2
	z_entity.new_y = ov_y2
	z_entity.new_zone = 'Overworld'
	zone.add_entity(z_entity, entry_level)

	ov_entity = entities.ZoneWarp(game)
	ov_entity.x = ov_x2
	ov_entity.y = ov_y2
	ov_entity.new_x = z_x
	ov_entity.new_y = z_y
	ov_entity.new_zone = zone.name
	game.overworld.add_entity(ov_entity, ov_level)


	Door_Handler_onelevel(game.overworld, ov_level)

	game.overworld.fast_travel_options[ov_level] = main.FastTravel(zone.name, level=ov_level)

	return ov_level


def empty_zone(cell, xmax, ymax):
	map = [['.' for x in range(xmax + 1)] for y in range(ymax + 1)]
	if cell.down:
		for x, c in enumerate(map[0]):
			map[0][x] = '#'

	if cell.up:
		for x, c in enumerate(map[ymax]):
			map[ymax][x] = '#'

	if cell.left:
		for y, line in enumerate(map):
			map[y][0] = '#'

	if cell.right:
		for y, line in enumerate(map):
			map[y][xmax] = '#'

	return flatten(map)

def empty_zone_with_mask(cell, mask):
	xmax = len(mask[0]) - 1
	ymax = len(mask) - 1
	map = [['.' for x in range(xmax + 1)] for y in range(ymax + 1)]
	if cell.down:
		for x, c in enumerate(map[0]):
			map[0][x] = '#'

	if cell.up:
		for x, c in enumerate(map[ymax]):
			map[ymax][x] = '#'

	if cell.left:
		for y, line in enumerate(map):
			map[y][0] = '#'

	if cell.right:
		for y, line in enumerate(map):
			map[y][xmax] = '#'
	
	for y, line in enumerate(map):
		for x, char in enumerate(line):
			if mask[y][x] != ' ':
				map[y][x] = mask[y][x]
	return flatten(map)

def flatten(map, printout = False):
	lines = []
	for y in map:
		line = ''.join(y)
		lines.append(line)
		if printout:
			print(line)
	return lines

def wall_or(list1, list2, char_false='#', char_true='.'):
	result = [char_false]*(len(list1) - 1)
	for i in range(len(list1)):
		if list1[i] == char_true or list2[i] == char_true:
			result[i] = char_true
	return result

def wall_and(list1, list2, char_false='#', char_true='.'):
	result = [char_false]*(len(list1) - 1)
	for i in range(len(list1)):
		if list1[i] == char_true and list2[i] == char_true:
			result[i] = char_true

def wall_any(list1, char_true='.'):
	for x in list1:
		if x == char_true:
			return True
	return False

def entry_match(map_list, maze, game=None, grid_width = 1):
	zone_width = grid_width
	zone_height = int(len(map_list) / grid_width)
	mapwidth = len(map_list[0][0])
	mapheight = len(map_list[0])
	firstrow = 0
	lastrow = mapheight - 1
	firstcol = 0
	lastcol = mapwidth - 1

	mirror_depth = 4

	for grid_x in range(zone_width):
		for grid_y in range(zone_height):
			if game is not None:
				game.progress()
			index = grid_x + grid_y * zone_width
			above = index + zone_width
			right = index + 1
			cell = maze[grid_y][grid_x]


			if (not cell.up) and (grid_y < zone_height - 1):
				replacement = ['.'] * mapwidth
				for line in range(mirror_depth):
				#while wall_any(replacement)
					for map_x in range(1,mapwidth - 1):
						change = False
						if map_list[index][firstrow + line][map_x] == '.':
							change = True
						if map_list[above][lastrow - line][map_x] == '.':
							change = True
						if change and replacement[map_x] == '.':
							map_list[above][lastrow - line][map_x] = '.'
							map_list[index][firstrow + line][map_x] = '.'
						else:
							replacement[map_x] = '#'

			if (not cell.right) and (grid_x < zone_width - 1):
				replacement = ['.'] * mapheight
				for line in range(mirror_depth):
					for map_y in range(1,mapheight - 1):
						change = False
						if map_list[index][map_y][lastcol - line] == '.':
							change = True
						if map_list[right][map_y][firstcol + line] == '.':
							change = True
						if change and replacement[map_y] == '.':
							map_list[index][map_y][lastcol - line] = '.'
							map_list[right][map_y][firstcol + line] = '.'
						else:
							replacement[map_y] = '#'


	
	return map_list



