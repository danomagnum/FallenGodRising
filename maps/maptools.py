import main
import random
from constants import *

def Random_Map_Insert(zone, entity, level=0):
	pos = zone.find_empty_position(level)
	e1 = entity(x=pos[0], y=pos[1])
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
		e1 = entity(x=result[0], y=result[1])
		zone.add_entity(e1)
		if replace:
			zone.maps[level][entity.y][entity.x] = '.'

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
			
			up = main.UpStairs()
			up.new_x = down_pos[0]
			up.new_y = down_pos[1]
			up.x = up_pos[0]
			up.y = up_pos[1]
			down = main.DownStairs()
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


