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

def find_valid_position(area):
	while True:
		x = random.randint(0, len(area[0]) - 1)
		y = random.randint(0, len(area) - 1)
		if area[y][x] == '.':
			return (x, y)


def move(direction, display):
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4
	if direction == UP:
		if display.area_map[display.char_y - 1][display.char_x] == '.':
			display.mappad.addch(display.char_y, display.char_x, '.')
			display.mappad.addch(display.char_y - 1, display.char_x, '@')
			display.char_y -= 1
			display.y = max(0, display.y -1)
	elif direction == DOWN:
		if display.area_map[display.char_y + 1][display.char_x] == '.':
			display.mappad.addch(display.char_y, display.char_x, '.')
			display.mappad.addch(display.char_y + 1, display.char_x, '@')
			display.char_y += 1
			display.y = min((display.mappad.getmaxyx()[0]  - display.mapbox.getmaxyx()[0]), display.y + 1)
	elif direction == LEFT:
		if display.area_map[display.char_y][display.char_x - 1] == '.':
			display.mappad.addch(display.char_y, display.char_x, '.')
			display.mappad.addch(display.char_y, display.char_x - 1, '@')
			display.char_x -= 1
			display.x = max(0, display.x -1)
	elif direction == RIGHT:
		if display.area_map[display.char_y][display.char_x + 1] == '.':
			display.mappad.addch(display.char_y, display.char_x, '.')
			display.mappad.addch(display.char_y, display.char_x + 1, '@')
			display.char_x += 1
			display.x = min((display.mappad.getmaxyx()[1]  - display.mapbox.getmaxyx()[1]), display.x + 1)


