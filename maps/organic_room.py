import random
import math

def printmap(map):
	for line in map:
		print line



def makeroom(xmax, ymax):
	rad = math.sqrt((xmax / 2)**2 + (ymax / 2)**2)
	radius = rad
	theta = 0
	window = math.pi / 4
	alpha_zero = math.pi / 2
	alpha_range = (alpha_zero - window, alpha_zero + window)
	alpha = random.triangular(alpha_range[0], alpha_range[1], alpha_zero)
	pts = set()

	x0 = math.acos(theta) * radius
	y0 = math.asin(theta) * radius

	pts.add((x0, y0))

	loop = True
	quadrant = 1

	while loop:
		x0 = math.cos(theta) * radius
		y0 = math.sin(theta) * radius
		
		alpha1 = alpha + theta
		d = random.triangular(0,5,3)

		dx = math.cos(alpha1) * d
		dy = math.sin(alpha1) * d

		x1 = x0 + dx
		y1 = y0 + dy

		pts.add((x1, y1))

		theta1 = math.atan(y1 / x1)

		#if theta1 < 0:
			#theta1 = theta1 + math.pi
		if theta1 < theta:
			quadrant += 1
			theta1 = theta1 + (math.pi / 2) * quadrant

		if quadrant > 4:
			loop = False
		theta = theta1
		radius = math.sqrt(y1 ** 2 + x1 ** 2)
		print theta

	pts = [(int(pt[0]), int(pt[1])) for pt in pts]

	xs = [pt[0] for pt in pts]
	ys = [pt[1] for pt in pts]

	minx = min(xs)
	maxx = max(xs)
	rangex = maxx - minx

	miny = min(ys)
	maxy = max(ys)
	rangey = maxy - miny

	map = [[' ' for x in range(rangex + 1)] for y in range(rangey + 1)]

	for pt in pts:
		x = pt[0] - minx
		y = pt[1] - miny
		map[y][x] = '#'

	return map


if __name__ == '__main__':
	printmap(makeroom(20, 20))
