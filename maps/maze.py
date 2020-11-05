import random
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

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

	def box(self, nullchar = None):
		if nullchar == None:
			nullchar = ' '
		output = [[nullchar, nullchar, nullchar],[nullchar, nullchar, nullchar],[nullchar, nullchar, nullchar]]
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
						map[testy][testx].up = 0
						map[testy][testx].down = 0
						map[testy][testx].left = 0
						map[testy][testx].right = 0
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


def maze_map(width, height, clear_percent = 0.99):
	map = maze(width, height, clear_percent)
	out_map = []

	for y in map:
		line = ['', '', '']
		row = ''
		for x in y:
			disp = x.box(nullchar='.')
			for c in disp[0]:
				line[0] += c
			for c in disp[1]:
				line[1] += c
			for c in disp[2]:
				line[2] += c
		for spot in line:
			#row += spot
			out_map.append(list(spot))
		#out_map.append(row)

	return out_map


if __name__ == '__main__':
	map = maze(16, 16)

	for y in map:
		line = ['', '', '']
		for x in y:
			disp = x.box()
			for c in disp[0]:
				line[0] += c
			for c in disp[1]:
				line[1] += c
			for c in disp[2]:
				line[2] += c
		for spot in line:
			print(spot)
