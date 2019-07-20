import main
import entities
import random
from constants import *

def Random_Map_Insert(zone, entity, level=0):
	pos = zone.find_empty_position(level)
	e1 = entity(zone.game, x=pos[0], y=pos[1])
	zone.add_entity(e1)

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

def showmap(map, printout = False):
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
			check = __builtins__.map(isfloor, check)
			if all(check):
				map[y][x] = '.'


