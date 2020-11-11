#import scipy.interpolate
import random
import time

import numpy as np
from scipy.special import comb
#from scipy.misc import comb

def bernstein_poly(i, n, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * ( t**(n-i) ) * (1 - t)**i


def bezier_curve(points, nTimes=1000):
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1], 
                 [2,3], 
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t) for i in range(0, nPoints)   ])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals, yvals

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
			#check = __builtins__.map(isfloor, check)
			check = map(isfloor, check)
			if all(check):
				map_data[y][x] = '.'



def grow_cellular(lvl, gens = 5):
	map = lvl

	xmax = len(lvl[0]) - 1
	ymax = len(lvl) - 1


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

	def iswall(m, x, y):
		return map[y][x] == '#'
	def isfloor(m, x, y):
		return map[y][x] == '.'

	for gen in range(gens):
		nextmap = [[map[y][x] for x in range(xmax + 1)] for y in range(ymax + 1)]
		lastpass = gen == gens - 1

		for y in range(1,ymax - 1):
			for x in range(1,xmax - 1):
				n1= neighbors(x, y)
				n2= neighbors2(x, y)
				w1s = [w for w in n1 if iswall(map, w[0], w[1])]
				w2s = [w for w in n2 if iswall(map, w[0], w[1])]

				if map[y][x] == '#':
					if lastpass:
						if len(w1s) < 8:
							nextmap[y][x] = '.'
						if len(n2) < 24:
							nextmap[y][x] = '#'
							#pass
					else:
						if len(w1s) < 6:
							nextmap[y][x] = random.choice(('.', '#'))
						if len(w1s) < 5:
							nextmap[y][x] = '.'
						#if len(n2) < 24:
						#	nextmap[y][x] = '#'


				else:
					if len(w1s) > 7:
						#nextmap[y][x] = '#'
						pass
					if len(w2s) > 18:
						nextmap[y][x] = '#'
						#pass
					#if len(n2) < 24:
						#nextmap[y][x] = '#'
				

		map = nextmap
		
	return map


def grow_cellular2(lvl, gens = 5):
	map = lvl

	xmax = len(lvl[0]) - 1
	ymax = len(lvl) - 1


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

	def iswall(m, x, y):
		return map[y][x] == '#'
	def isfloor(m, x, y):
		return map[y][x] == '.'

	for gen in range(gens):
		nextmap = [[map[y][x] for x in range(xmax + 1)] for y in range(ymax + 1)]
		lastpass = gen == gens - 1

		for y in range(1,ymax - 1):
			for x in range(1,xmax - 1):
				n1= neighbors(x, y)
				n2= neighbors2(x, y)
				w1s = [w for w in n1 if iswall(map, w[0], w[1])]
				w2s = [w for w in n2 if iswall(map, w[0], w[1])]

				if map[y][x] == '#':
					if lastpass:
						if len(w1s) < 8:
							nextmap[y][x] = '.'
						#if len(n2) < 24:
							#nextmap[y][x] = '#'
							#pass
					else:
						if len(w1s) < 6:
							nextmap[y][x] = random.choice(('.', '#'))
						if len(w1s) < 5:
							nextmap[y][x] = '.'
						#if len(n2) < 24:
						#	nextmap[y][x] = '#'


				else:
					if len(w1s) > 7:
						#nextmap[y][x] = '#'
						pass
					if len(w2s) > 18:
						#nextmap[y][x] = '#'
						pass
					#if len(n2) < 24:
						#nextmap[y][x] = '#'
				

		map = nextmap
		
	return map


def grow_neighbors(lvl):
	map = lvl

	xmax = len(lvl[0]) - 1
	ymax = len(lvl) - 1


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

	def iswall(m, x, y):
		return map[y][x] == '#'
	def isfloor(m, x, y):
		return map[y][x] == '.'

	nextmap = [[map[y][x] for x in range(xmax + 1)] for y in range(ymax + 1)]

	for y in range(ymax):
		for x in range(xmax):
			n1= neighbors(x, y)
			w1s = [w for w in n1 if isfloor(map, w[0], w[1])]

			if map[y][x] == '#':
				if len(w1s) >= 1:
					nextmap[y][x] = '.'
	return nextmap






    


def add_path(lvl, start, end, leadin = 3, curvitude = 4):
	x0, y0 = start
	x3, y3 = end

	width = len(lvl[0]) - 1
	height = len(lvl) - 1

	if x0 < x3:
		x1 = x0 + leadin
		x2 = x0 - leadin
	elif x0 == x3:
		#not sure what to do here
		x1 = x0 - leadin
		x2 = x0 - leadin
	else:
		x1 = x0 - leadin
		x2 = x0 + leadin


	if y0 < y3:
		y1 = y0 + leadin
		y2 = y0 - leadin
	elif y0 == y3:
		#not sure what to do here
		y1 = y0 - leadin
		y2 = y0 - leadin
	else:
		y1 = y0 - leadin
		y2 = y0 + leadin

	coords = [(x0, y0), (x1, y1)]

	for coord in range(curvitude):
		coords.append((random.randint(leadin, width - leadin), random.randint(leadin, height - leadin)))

	coords.append((x2, y2))
	coords.append((x3, y3))

	xvals, yvals = bezier_curve(coords, nTimes=1000)
	final = zip(xvals, yvals)
	for pt in final:
		try:
			lvl[int(pt[1])][int(pt[0])] = '.'
		except:
			pass

def or_map(lvl1, lvl2, truechar = '.'):
	width = len(lvl[0])
	height = len(lvl)
	newmap = [['#' for x in range(width)] for y in range(height)]

	for x in range(width):
		for y in range(height):
			newmap[y][x] = lvl1[y][x]
			if lvl2[y][x] == truechar:
				newmap[y][x] = truechar

	return newmap


def print_map(lvl):
	#print()
	print(chr(27)+'[2j')
	print('\033c')
	print('\x1bc')
	for row in lvl:
		print(''.join(row))

def generate(entries):

if __name__ == '__main__':
	DEMOMAPCOUNT = 5
	for maptogen in range(DEMOMAPCOUNT):
		lvl = [['#' for x in range(60)] for y in range(36)] 

		entry_left = (0, random.randint(8, 28))
		entry_top = (random.randint(10, 50), 0)
		entry_bottom = (random.randint(10, 50), 35)
		entry_right = (59, random.randint(8, 28))
		#add_path(lvl, e0, e1)

		possible = [entry_left, entry_top, entry_bottom, entry_right]

		paths = random.randint(5,10)

		used = set()

		for path in range(paths):
			pts = random.sample(possible, 2)
			used.add(pts[0])
			used.add(pts[1])
			add_path(lvl, pts[0], pts[1])
			print_map(lvl)
			time.sleep(0.2)
	
		time.sleep(0.2)
		for pt in used:
			if pt[0] == 0 or pt[0] == 59:
				lvl[pt[1] + 1][pt[0]] = '.'
				lvl[pt[1] - 1][pt[0]] = '.'
			if pt[1] == 0 or pt[1] == 35:
				lvl[pt[1]][pt[0] + 1] = '.'
				lvl[pt[1]][pt[0] - 1] = '.'

		print_map(lvl)
		time.sleep(0.2)

		lvl2 = grow_neighbors(lvl)
		#lvl2 = grow_cellular2(lvl, gens=2)

		print_map(lvl2)
		noise_prune(lvl2)
		time.sleep(0.2)

		lvl3 = or_map(lvl, lvl2)
		print_map(lvl3)
		time.sleep(0.5)
