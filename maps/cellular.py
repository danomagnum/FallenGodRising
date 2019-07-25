import random

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

def cellular(xmax = 30, ymax = 30, percentage = 0.3, gens = 6):
	map = [['#' for x in range(xmax)] for y in range(ymax)]
	x, y = (int(xmax / 2), int(ymax/2))

	total_cells = xmax * ymax
	removals = int(total_cells * percentage)
	print removals

	for r in range(removals):

		xsel = random.choice(range(xmax))
		ysel = random.choice(range(xmax))

		map[ysel][xsel] = '.'

	for line in showmap(map):
		print line

	def neighbors(x, y, diags=True):
		if diags:
			offsets = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
		else:
			offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)]
		check_cells = [(x + o[0], y+o[1]) for o in offsets]
		neighbor_cells = []
		for cell in check_cells:
			if cell[0] >= 0 and cell[0] < xmax:
				if cell[1] >= 0 and cell[1] < ymax:
					neighbor_cells.append(cell)
		return neighbor_cells

	def neighbors2(x, y, diags=True):
		offsets = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
		offsets += [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, -2), (-1, 2) , (0, -2), (0, 2), (1, -2), (1, 2), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]
		check_cells = [(x + o[0], y+o[1]) for o in offsets]
		neighbor_cells = []
		for cell in check_cells:
			if cell[0] >= 0 and cell[0] < xmax:
				if cell[1] >= 0 and cell[1] < ymax:
					neighbor_cells.append(cell)
		return neighbor_cells

	def iswall(x, y):
		return map[y][x] == '#'
	def isfloor(x, y):
		return map[y][x] == '.'

	for gen in range(gens):
		for y in range(ymax):
			for x in range(xmax):
				n1= neighbors(x, y)
				n2= neighbors2(x, y)
				w1s = [w for w in n1 if iswall(w[0], w[1])]
				w2s = [w for w in n2 if iswall(w[0], w[1])]

				if len(w1s) >= 5 or len(w2s) <= 7:
					map[y][x] = '#'
				else:
					map[y][x] = '.'
		
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
	map = cellular()
	#add_entry2(map, UP)
	#add_entry2(map, DOWN)
	#add_entry2(map, LEFT)
	#add_entry2(map, RIGHT)
	#noise_prune(map)
	map = showmap(map)
	for line in map:
		print line
