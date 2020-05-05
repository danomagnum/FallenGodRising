import random

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

def drunkard_walk(xmax = 30, ymax = 30, percentage = 0.2):
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

def add_entry2(map, entry_dir, tries = 2):
	xmax = len(map[0]) - 1
	ymax = len(map) - 1

	dirs = [(0, 1), (1, 0),(-1, 0),(0, -1)]
	for trial in range(tries):
		if entry_dir == UP:
			y = 0
			x = random.choice(range(1, xmax))
			print 'setting new xy start at {}, {}'.format(x, y)
		elif entry_dir == DOWN:
			y = ymax
			x = random.choice(range(1, xmax))
			print 'setting new xy start at {}, {}'.format(x, y)
		elif entry_dir == LEFT:
			y = random.choice(range(1,ymax))
			x = 0
			print 'setting new xy start at {}, {}'.format(x, y)
		elif entry_dir == RIGHT:
			y = random.choice(range(1,ymax))
			x = xmax
			print 'setting new xy start at {}, {}'.format(x, y)


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

def noise_prune(map_data):
	xmax = len(map_data[0]) - 1
	ymax = len(map_data) - 1

	def isfloor(coord):
		if map_data[coord[1]][coord[0]] == '.':
			return True
		else:
			return False

	for y in range(ymax):
		for x in range(xmax):
			check = [ (x, y-1), (x, y+1), (x-1, y), (x+1, y)]
			check = __builtins__.map(isfloor, check)
			if all(check):
				map_data[y][x] = '.'


def showmap(map, printout = False):
	lines = []
	for y in map:
		line = ''.join(y)
		lines.append(line)
		if printout:
			print(line)
	return lines



if __name__ == '__main__':
	map = drunkard_walk()
	add_entry2(map, UP)
	add_entry2(map, DOWN)
	add_entry2(map, LEFT)
	add_entry2(map, RIGHT)
	noise_prune(map)
	map = showmap(map)
	for line in map:
		print line
