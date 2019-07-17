import random
import math

MINWALL = 5

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

WALL = 10
CLEAR = 9
DOOR = 8

def floodFill(map, x, y, floodmap = None):
	# The recursive algorithm. Starting at x and y, changes any adjacent
	# characters that match oldChar to newChar.
	width = len(world)
	height = len(world[0])
	if floodmap is None:
		floodmap = [[0 for x in width] for y in height]

	if floodmap[y][x] != 0:
		return

	# Change the character at world[x][y] to newChar
	if map[y][x] == '.':
		floodmap[y][x] = CLEAR
	elif map[y][x] == '+':
		floodmap[y][x] = DOOR
	else:
		floodmap[y][x] = WALL
		return

	# Recursive calls. Make a recursive call as long as we are not on the
	# boundary (which would cause an Index Error.)
	if x > 0: # left
		floodFill(world, x-1, y, floodmap)

	if y > 0: # up
		floodFill(world, x, y-1, floodmap)

	if x < worldWidth-1: # right
		floodFill(world, x+1, y, floodmap)

	if y < worldHeight-1: # down
		floodFill(world, x, y+1, floodmap)
	return floodmap
	

class Wall(object):
	def __init__(self, x0, y0, x1, y1, nodoor = False):
		self.x0 = int(x0)
		self.y0 = int(y0)
		self.x1 = int(x1)
		self.y1 = int(y1)
		self.calc_pts()
		self.door = None
		self.nodoor = nodoor

	def calc_pts(self):
		"Bresenham's line algorithm"
		pts = set()
		pts.add((self.x0, self.y0))
		pts.add((self.x1, self.y1))
		dx = abs(self.x1 - self.x0)
		dy = abs(self.y1 - self.y0)
		x, y = self.x0, self.y0
		sx = -1 if self.x0 > self.x1 else 1
		sy = -1 if self.y0 > self.y1 else 1
		if dx > dy:
			err = dx / 2.0
			while x != self.x1:
				pts.add((x, y))
				err -= dy
				if err < 0:
					y += sy
					err += dx
				x += sx
		else:
			err = dy / 2.0
			while y != self.y1:
				pts.add((x, y))
				err -= dx
				if err < 0:
					x += sx
					err += dy
				y += sy		
		self.pts = pts

	def length(self):
		dx = abs(self.x0 - self.x1)
		dy = abs(self.y0 - self.y1)
		len = math.sqrt(dx**2 + dy ** 2)
		return len

	def divide(self):
		if self.x0 > self.x1:
			by_x = -1
		else:
			by_x = 1
		if self.y0 > self.y1:
			by_y = -1
		else:
			by_y = 1
		xsel = random.choice(range(self.x0, self.x1 + by_x, by_x))
		ysel = random.choice(range(self.y0, self.y1 + by_y, by_y))

		return (xsel, ysel)

	def ison(self, pt):
		return (int(pt[0]), int(pt[1])) in self.pts
	def draw(self, map, wall='#', door='+'):
		for pt in self.pts:
			try:
				map[pt[1]][pt[0]] = wall
			except:
				#print('({}, {})'.format(pt[0], pt[1]))
				pass
		if self.door is not None:
			map[self.door[1]][self.door[0]] = door

	def normals(self):
		divx = self.x0 - self.x1
		divy = self.y0 - self.y1
		normalization = math.sqrt(divx ** 2 + divy ** 2)
		normal0 = (-divy / normalization, divx / normalization)
		normal1 = (divy / normalization, -divx / normalization)
		return (normal0, normal1)

	def door_gen(self):
		tries = 3
		if self.nodoor:
			return
		while tries > 0:
			tries -= 1
			self.door = random.choice(list(self.pts))
			if self.door[0] == self.x0 and self.door[1] == self.y0:
				self.door = None
			elif self.door[0] == self.x0 and self.door[1] == self.y1:
				self.door = None
			else:
				tries = 0


class Room(object):
	def __init__(self, walls):
		if walls is None:
			self.walls = []
		else:
			self.walls = walls
	def divide(self):
		walls_by_length = sorted(self.walls, key=lambda wall: wall.length())
		longest = walls_by_length[-1]
		search = True
		nodoors = 0
		while search:
			divx, divy = longest.divide()
			new_wall_1 = Wall(longest.x0, longest.y0, divx, divy, longest.nodoor)
			new_wall_2 = Wall(divx, divy, longest.x1, longest.y1, longest.nodoor)
			if new_wall_1.length() >= MINWALL:
				if new_wall_2.length() >= MINWALL:
					search = False

		if longest.nodoor:
			nodoors += 1

		self.walls.remove(longest)
		search = True
		tp0 = [divx, divy]
		tp1 = [divx, divy]
		normal0, normal1 = longest.normals()
		while search:
			tp0[0] += normal0[0]
			tp0[1] += normal0[1]

			tp1[0] += normal1[0]
			tp1[1] += normal1[1]


			for wall in self.walls:
				if wall.ison(tp0):
					final_pt = tp0
					search = False
					purgewall = wall
				if wall.ison(tp1):
					final_pt = tp1
					search = False
					purgewall = wall

		self.walls.remove(purgewall)
		
		if purgewall.nodoor:
			nodoors += 1
		self.walls.append(Wall(purgewall.x0, purgewall.y0, final_pt[0], final_pt[1], purgewall.nodoor))
		self.walls.append(Wall(final_pt[0], final_pt[1], purgewall.x1, purgewall.y1, purgewall.nodoor))
		self.walls.append(new_wall_1)
		self.walls.append(new_wall_2)
		if nodoors > 1:
			final_nodoor = False
		else:
			final_nodoor = True

		self.walls.append(Wall(divx, divy, final_pt[0], final_pt[1], final_nodoor))

	def draw(self, map):
		for wall in self.walls:
			wall.draw(map)
	def door_gen(self):
		for wall in self.walls:
			wall.door_gen()


def building_gen(xmax = 30, ymax = 30):
	map = [['.' for x in range(xmax)] for y in range(ymax)]
	walls = []
	wall0 = Wall(0, 0, xmax - 1, 0, True)
	wall1 = Wall(0, 0, 0, ymax - 1, True)
	wall2 = Wall(xmax - 1, 0, xmax - 1, ymax - 1, True)
	wall3 = Wall(0, ymax - 1, xmax - 1, ymax - 1, True)
	room = Room([wall0, wall1, wall2, wall3])
	room.divide()
	room.divide()
	room.divide()
	room.divide()
	room.divide()
	room.door_gen()
	room.draw(map)
	return map

def showmap(map, printout = False):
	lines = []
	for y in map:
		line = ''.join(y)
		lines.append(line)
		if printout:
			print(line)
	return lines


if __name__ == '__main__':
	map = building_gen()

	map = showmap(map)
	for line in map:
		print line
