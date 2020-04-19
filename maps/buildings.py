import random
import math

MINWALL = 3

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

WALL = 10
CLEAR = 9
DOOR = 8

def dist(pt0, pt1):
	dx = pt0[0] - pt1[0]
	dy = pt0[1] - pt1[1]
	return math.sqrt(dx**2 + dy**2)

def err_dist(pt0, pt1, test):
	dx0 = pt0[0] - test[0]
	dy0 = pt0[1] - test[1]

	dx1 = pt1[0] - test[0]
	dy1 = pt1[1] - test[1]

	dx = pt0[0] - pt1[0]
	dy = pt0[1] - pt1[1]

	l0p = math.sqrt(dx0**2 + dy0**2)
	l1p = math.sqrt(dx1**2 + dy1**2)
	l = math.sqrt(dx**2 + dy**2)

	dl = l - l0p - l1p

	return dl

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
		return random.choice(list(self.pts))


	def ison(self, pt):
		if (int(pt[0]), int(pt[1])) in self.pts:
			return True
		for mypt in self.pts:
			if dist(mypt, pt) < 1.0:
			#if err_dist((self.x0, self.y0), (self.x1, self.y1), pt) < 1.0:
				return True
		return False
		
		return (int(pt[0]), int(pt[1])) in self.pts

	def nearest(self, pt):
		pts_with_dist = [(mypt, dist(pt, mypt)) for mypt in self.pts]
		pts_with_dist.sort(key=lambda x: x[1])
		return pts_with_dist[0][0]

	def draw(self, map, wall='#', door='+'):
		for pt in self.pts:
			try:
				map[pt[1]][pt[0]] = wall
			except:
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
			elif self.door[0] == self.x1 and self.door[1] == self.y1:
				self.door = None
			else:
				tries = 0


class Room(object):
	def __init__(self, walls):
		if walls is None:
			self.walls = []
		else:
			self.walls = walls
	def walls_by_length(self):
		return sorted(self.walls, key=lambda wall: wall.length())
			
	def drop_wall(self, bylen=True):
		if bylen:
			for wall in self.walls_by_length():
				if not wall.nodoor:
					self.walls.remove(wall)
					return
		else:
			for i in range(len(self.walls)):
				wall = random.choice(self.walls)
				if not wall.nodoor:
					self.walls.remove(wall)
					return

	def divide(self):
		walls_by_length = self.walls_by_length()
		trigger_len = walls_by_length[-1].length() - 3
		longest_walls = [w for w in walls_by_length if w.length() >= trigger_len ]
		longest = random.choice(longest_walls)
		search = True
		search_time = 10
		for attempt in range(10):
			search_time -= 1
			divx, divy = longest.divide()
			new_wall_1 = Wall(longest.x0, longest.y0, divx, divy, longest.nodoor)
			new_wall_2 = Wall(divx, divy, longest.x1, longest.y1, longest.nodoor)
			if new_wall_1.length() >= MINWALL:
				if new_wall_2.length() >= MINWALL:
					break
		else:
			return

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
				if wall is not longest:
					if wall.ison(tp0):
						final_pt = wall.nearest(tp0)
						search = False
						purgewall = wall
					if wall.ison(tp1):
						final_pt = wall.nearest(tp1)
						search = False
						purgewall = wall


		
		if purgewall.nodoor:
			if longest.nodoor:
				final_nodoor = False
			else:
				final_nodoor = False
				if random.choice((True, False)):
					# both walls need doors
					new_wall_1.hasdoor = True
					new_wall_2.hasdoor = True
				else:
					if random.choice((True, False)):
						#First wall has door
						new_wall_1.hasdoor = True
						new_wall_2.hasdoor = False
					else:
						new_wall_1.hasdoor = False
						new_wall_2.hasdoor = True

		else:
			final_nodoor = True

		new_pwall1 = Wall(purgewall.x0, purgewall.y0, final_pt[0], final_pt[1], purgewall.nodoor)
		new_pwall2 = Wall(final_pt[0], final_pt[1], purgewall.x1, purgewall.y1, purgewall.nodoor)

		if new_pwall1.length() < MINWALL:
			#print('new wall too short')
			return
		if new_pwall2.length() < MINWALL:
			#print('new wall too short')
			return

		# new walls to replace the purged wall
		self.walls.append(new_pwall1)
		self.walls.append(new_pwall2)
		# new walls to replace the long wall
		self.walls.append(new_wall_1)
		self.walls.append(new_wall_2)

		#new intermediate wall
		self.walls.append(Wall(divx, divy, final_pt[0], final_pt[1], final_nodoor))

		self.walls.remove(longest)
		self.walls.remove(purgewall)

	def draw(self, map):
		for wall in self.walls:
			wall.draw(map)
	def door_gen(self):
		for wall in self.walls:
			wall.door_gen()

def walls_from_points(pt_list):
	walls = []
	for i, pt in enumerate(pt_list[1:]):
		wall = Wall(pt_list[i][0], pt_list[i][1], pt[0], pt[1], True)
		walls.append(wall)
	return walls



def building_gen(xmax, ymax, divisions=5, padding=0, drops=0,outside_door=False):
	map = [['.' for x in range(xmax)] for y in range(ymax)]

	maxpad = padding + 1
	ystop = ymax - maxpad
	xstop = xmax - maxpad

	pts = [(padding, padding),
	       (xstop, padding),
	       (xstop, ystop),
	       (padding, ystop),
	       (padding, padding)]

	walls = walls_from_points(pts)

	if outside_door:
		random.choice(walls).nodoor=False

	room = Room(walls)

	for d in range(divisions):
		room.divide()
	room.door_gen()
	for d in range(drops):
		room.drop_wall()

	room.draw(map)
	dmap = calcDistGraph((0, 0), map)
	for y in range(ymax):
		for x in range(xmax):
			if dmap[y][x] >= 0:
				map[y][x] = ' '




	return map

def building_octagon(xmax, ymax,divisions=5,padding=0, drops=0, outside_door=False):
	map = [['.' for x in range(xmax)] for y in range(ymax)]

	maxpad = padding + 1
	ystop = ymax - maxpad
	xstop = xmax - maxpad
	x0 = int(xmax / 3)
	x1 = 2*x0
	y0 = int(ymax / 3)
	y1 = 2*y0


	pts = [(x0, padding),
	       (x1, padding),
	       (xstop, y0),
	       (xstop, y1),
	       (x1, ystop),
	       (x0, ystop),
	       (padding, y1),
	       (padding, y0),
	       (x0, padding)]

	walls = walls_from_points(pts)

	if outside_door:
		random.choice(walls).nodoor=False

	room = Room(walls)

	for d in range(divisions):
		room.divide()

	room.door_gen()
	for d in range(drops):
		room.drop_wall()

	room.draw(map)

	dmap = calcDistGraph((0, 0), map)
	for y in range(ymax):
		for x in range(xmax):
			if dmap[y][x] >= 0:
				map[y][x] = ' '

	dmap = calcDistGraph((xmax - 1, 0), map)
	for y in range(ymax):
		for x in range(xmax):
			if dmap[y][x] >= 0:
				map[y][x] = ' '

	dmap = calcDistGraph((xmax - 1, ymax - 1), map)
	for y in range(ymax):
		for x in range(xmax):
			if dmap[y][x] >= 0:
				map[y][x] = ' '

	dmap = calcDistGraph((0, ymax - 1), map)
	for y in range(ymax):
		for x in range(xmax):
			if dmap[y][x] >= 0:
				map[y][x] = ' '





	return map

def building_twobox(xmax, ymax,padding=0,divisions=5,drops=0, outside_door=False):
	map = [['.' for x in range(xmax)] for y in range(ymax)]
	maxpad = padding + 1
	ystop = ymax - maxpad
	xstop = xmax - maxpad
	xjog0 = int(xmax / 3)
	xjog1 = 2*xjog0
	yjog0 = int(ymax / 3)
	yjog1 = 2*yjog0

	pts = [(padding, padding),
	       (xjog1, padding),
	       (xjog1, yjog0),
	       (xstop, yjog0),
	       (xstop, ystop),
	       (xjog0, ystop),
	       (xjog0, yjog1),
	       (padding, yjog1),
	       (padding, padding)]

	walls = walls_from_points(pts)
	
	if outside_door:
		random.choice(walls).nodoor=False
	room = Room(walls)

	for d in range(divisions):
		room.divide()

	room.door_gen()
	for d in range(drops):
		room.drop_wall()

	room.draw(map)
	dmap = calcDistGraph((29, 0), map)
	for y in range(ymax):
		for x in range(xmax):
			if dmap[y][x] >= 0:
				map[y][x] = ' '
	dmap = calcDistGraph((0, 29), map)
	for y in range(ymax):
		for x in range(xmax):
			if dmap[y][x] >= 0:
				map[y][x] = ' '

	return map


def building_tee(xmax, ymax,divisions=5, padding=0, drops=0, outside_door = False):
	map = [['.' for x in range(xmax)] for y in range(ymax)]

	maxpad = padding + 1
	ystop = ymax - maxpad
	xstop = xmax - maxpad
	xjog0 = int(xmax / 3)
	xjog1 = 2*xjog0
	yjog0 = int(ymax / 2)


	pts = [(padding, padding),
	       (xstop, padding),
	       (xstop, yjog0),
	       (xjog1, yjog0),
	       (xjog1, ystop),
	       (xjog0, ystop),
	       (xjog0, yjog0),
	       (padding, yjog0),
	       (padding, padding)]

	walls = walls_from_points(pts)

	if outside_door:
		random.choice(walls).nodoor=False
	room = Room(walls)

	for d in range(divisions):
		room.divide()

	room.door_gen()
	for d in range(drops):
		room.drop_wall()
	room.draw(map)
	dmap = calcDistGraph((29, 29), map)
	for y in range(ymax):
		for x in range(xmax):
			if dmap[y][x] >= 0:
				map[y][x] = ' '
	dmap = calcDistGraph((0, 29), map)
	for y in range(ymax):
		for x in range(xmax):
			if dmap[y][x] >= 0:
				map[y][x] = ' '

	return map



def add_stairs(map, up=True, down=True):
	ymax = len(map)
	xmax =len(map[0])
	dmap = None
	if up:
		for attempt in range(30):
			y = random.randint(0, ymax - 1)
			x = random.randint(0, xmax - 1)
			if map[y][x] == '.':
				map[y][x] = '<'
				break
		else:
			return
		xup = x
		yup = y
		dmap = calcDistGraph((xup, yup), map)
	if down:
		for attempt in range(30):
			y = random.randint(0, ymax - 1)
			x = random.randint(0, xmax - 1)
			if map[y][x] == '.':
				if dmap is not None:
					if dmap[y][x] > 0:
						map[y][x] = '>'
						break
		else:
			return
		xdown = x
		ydown = y

def flatten(map, printout = False):
	lines = []
	for y in map:
		line = ''.join(y)
		lines.append(line)
		if printout:
			print(line)
	return lines

def calcDistGraph(pt, map, throughdoors = False):
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

	if throughdoors:
		invalid = ['#']
	else:
		invalid = ['#', '+']

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
					if map[pt[1]][pt[0]] not in invalid:
						if (dist_map[pt[1]][pt[0]] > d) or (dist_map[pt[1]][pt[0]] < 0):
							dist_map[pt[1]][pt[0]] = d
							to_check.append(pt)
						i = i + 1
						checked.add(pt)
	return dist_map



if __name__ == '__main__':
	map = building_octagon(outside_door=False)
	#map = building_twobox(outside_door=True)
	#map = building_tee(padding=5,outside_door = True)
	#map = building_gen(padding=2)
	add_stairs(map)

	map = flatten(map)
	for line in map:
		print(line)
