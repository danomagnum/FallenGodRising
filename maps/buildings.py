import random
import math

MINWALL = 5

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


class Wall(object):
	def __init__(self, x0, y0, x1, y1):
		self.x0 = int(x0)
		self.y0 = int(y0)
		self.x1 = int(x1)
		self.y1 = int(y1)
		self.calc_pts()
	def calc_pts(self):
		"Bresenham's line algorithm"
		pts = set()
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
	def draw(self, map, char='#'):
		for pt in self.pts:
			try:
				map[pt[1]][pt[0]] = char
			except:
				#print('({}, {})'.format(pt[0], pt[1]))
				pass
	def normals(self):
		divx = self.x0 - self.x1
		divy = self.y0 - self.y1
		normalization = math.sqrt(divx ** 2 + divy ** 2)
		normal0 = (-divy / normalization, divx / normalization)
		normal1 = (divy / normalization, -divx / normalization)
		return (normal0, normal1)


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
		while search:
			divx, divy = longest.divide()
			#print('({}, {})'.format(divx, divy))
			new_wall_1 = Wall(longest.x0, longest.y0, divx, divy)
			new_wall_2 = Wall(divx, divy, longest.x1, longest.y1)
			#print new_wall_1.length()
			#print new_wall_2.length()
			if new_wall_1.length() >= MINWALL:
				if new_wall_2.length() >= MINWALL:
					search = False

		self.walls.remove(longest)
		search = True
		tp0 = [divx, divy]
		tp1 = [divx, divy]
		#normalization = math.sqrt(divx ** 2 + divy ** 2)
		#normal0 = (-divy / normalization, divx / normalization)
		#normal1 = (divy / normalization, -divx / normalization)
		normal0, normal1 = longest.normals()
		while search:
			tp0[0] += normal0[0]
			tp0[1] += normal0[1]

			tp1[0] += normal1[0]
			tp1[1] += normal1[1]

			#print('({}, {}) / ({}, {})'.format(tp0[0], tp0[1], tp1[0], tp1[1]))

			for wall in self.walls:
				if wall.ison(tp0):
					final_pt = tp0
					search = False
					purgewall = wall
				if wall.ison(tp1):
					final_pt = tp1
					search = False
					purgewall = wall

		print('({}, {})'.format(divx, divy))
		self.walls.remove(purgewall)
		self.walls.append(Wall(purgewall.x0, purgewall.y0, final_pt[0], final_pt[1]))
		self.walls.append(Wall(final_pt[0], final_pt[1], purgewall.x1, purgewall.y1))
		self.walls.append(new_wall_1)
		self.walls.append(new_wall_2)
		self.walls.append(Wall(divx, divy, final_pt[0], final_pt[1]))

	def draw(self, map):
		for wall in self.walls:
			wall.draw(map)


def building_gen(xmax = 30, ymax = 30):
	map = [[' ' for x in range(xmax)] for y in range(ymax)]
	walls = []
	wall0 = Wall(2, 2, xmax - 2, 2)
	wall1 = Wall(2, 2, 2, ymax - 2)
	wall2 = Wall(xmax - 2, 2, xmax - 2, ymax - 2)
	wall3 = Wall(2, ymax - 2, xmax - 2, ymax - 2)
	room = Room([wall0, wall1, wall2, wall3])
	room.divide()
	room.divide()
	room.divide()
	room.divide()
	room.divide()
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
