import maps.maptools as maptools
import random


class Tree(object):
	def __init__(self,x0, y0, width, height, minsize, pad):
		self.x0 = x0
		self.y0 = y0
		self.width = width
		self.height = height
		self.minsize = minsize
		self.children = []
		self.pad = pad

	def all_nodes(self):
		subchildren = [self]

		for child in self.children:
			subchildren += child.all_nodes()

		return subchildren
	
	def final_nodes(self):
		all = self.all_nodes()
		return [l for l in all if l.children == []]

	def split(self, minimize_ratio=False):
		if self.children == []:
			horizontal = random.choice([True, False])

			if minimize_ratio:
				ratio_vertical = float(self.width) / float(self.height)
				ratio_horizontal = float(self.height) / float(self.width)

				if ratio_vertical > ratio_horizontal:
					horizontal = True
				else:
					horizontal = False

			if horizontal:
				start = self.minsize
				end = self.height - self.minsize
				if start < end:
					pos = random.randint(start, end)

					c0 = Tree(self.x0, self.y0, self.width, pos, self.minsize, self.pad)

					c1 = Tree(self.x0, self.y0 + pos, self.width, self.height - pos, self.minsize, self.pad)

					self.children.append(c0)
					self.children.append(c1)
			else:
				start = self.minsize
				end = self.width - self.minsize
				if start < end:
					pos = random.randint(start, end)

					c0 = Tree(self.x0, self.y0, pos, self.height, self.minsize, self.pad)

					c1 = Tree(self.x0 + pos, self.y0, self.width - pos, self.height, self.minsize, self.pad)

					self.children.append(c0)
					self.children.append(c1)
		else:
			for child in self.children:
				child.split()

	def draw(self, map, door = False):
		for x in range(self.width - 2 * self.pad + 1):
			map[self.y0 + self.pad][self.x0 + x + self.pad] = '#'
			map[self.y0 + self.height - self.pad][self.x0 + x + self.pad] = '#'
		for y in range(self.height - 2 * self.pad + 1):
			map[self.y0 + y + self.pad][self.x0 + self.pad] = '#'
			map[self.y0 + y + self.pad][self.x0 + self.width - self.pad] = '#'

		if door:
			self.door(map)

	def door(self, map):
		y0 = self.y0 + self.pad
		ymax = self.y0 + self.height - self.pad
		x0 = self.x0 + self.pad
		xmax = self.x0 + self.width - self.pad
		#valid positions to keep door from being in a corner
		door_y = random.randint(y0 + 1, ymax - 1)
		door_x = random.randint(x0 + 1, xmax - 1)
		
		horizontal = random.choice([True, False])
		top_or_left = random.choice([True, False])
		
		if horizontal:
			if top_or_left:
				map[y0][door_x] = '+'
			else:
				map[ymax][door_x] = '+'
		else:
			if top_or_left:
				map[door_y][x0] = '+'
			else:
				map[door_y][xmax] = '+'
	
