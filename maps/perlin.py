import sys, os, random
from math import *


tiledim = 16   #In nodes
repeats = 1	#number of repetitions on screen

tilesize = 1

height = 16
	
def fade(t):
	return t * t * t * (t * (t * 6 - 15) + 10)
def lerp(t, a, b):
	return a + t * (b - a)
def grad(hash, x, y, z):
	#CONVERT LO 4 BITS OF HASH CODE INTO 12 GRADIENT DIRECTIONS.
	h = hash & 15
	if h < 8: u = x
	else:	 u = y
	if h < 4: v = y
	else:
		if h == 12 or h == 14: v = x
		else:				  v = z
	if h&1 == 0: first = u
	else:		first = -u
	if h&2 == 0: second = v
	else:		second = -v
	return first + second

def initialize():
	p = []
	for x in range(2*tiledim):
		p.append(0)
		
	permutation = []
	for value in range(tiledim):
		permutation.append(value)
	random.shuffle(permutation)

	for i in range(tiledim):
		p[i] = permutation[i]
		p[tiledim+i] = p[i]
	
	def noise(x,y,z):
		#FIND UNIT CUBE THAT CONTAINS POINT.
		X = int(x)&(tiledim-1)
		Y = int(y)&(tiledim-1)
		Z = int(z)&(tiledim-1)
		#FIND RELATIVE X,Y,Z OF POINT IN CUBE.
		x -= int(x)
		y -= int(y)
		z -= int(z)
		#COMPUTE FADE CURVES FOR EACH OF X,Y,Z.
		u = fade(x)
		v = fade(y)
		w = fade(z)
		#HASH COORDINATES OF THE 8 CUBE CORNERS
		A = p[X  ]+Y; AA = p[A]+Z; AB = p[A+1]+Z
		B = p[X+1]+Y; BA = p[B]+Z; BB = p[B+1]+Z
		#AND ADD BLENDED RESULTS FROM 8 CORNERS OF CUBE
		return lerp(w,lerp(v,
						   lerp(u,grad(p[AA  ],x  ,y  ,z  ),
								  grad(p[BA  ],x-1,y  ,z  )),
						   lerp(u,grad(p[AB  ],x  ,y-1,z  ),
								  grad(p[BB  ],x-1,y-1,z  ))),
					  lerp(v,
						   lerp(u,grad(p[AA+1],x  ,y  ,z-1),
								  grad(p[BA+1],x-1,y  ,z-1)),
						   lerp(u,grad(p[AB+1],x  ,y-1,z-1),
								  grad(p[BB+1],x-1,y-1,z-1))))

	return noise
def Generate(maxx,maxy):

	noise = initialize()
	output = [[None for dx in range(maxy)] for y in range(maxx)]
	octaves = 6
	persistence = 0.1
	
	amplitude = 1.0
	maxamplitude = 1.0
	for octave in range(octaves):
		amplitude *= persistence
		maxamplitude += amplitude
	total = maxx + maxy
	for x in range(maxx):
		for y in range(maxy):
			sc = 1
			frequency = 0.9
			amplitude = 1.0
			value = 0.0
			for octave in range(octaves):
				sc *= frequency
				prevalue = noise(sc*float(x)/maxx,sc*float(y)/maxy,0.0)
				prevalue = (prevalue+1.0)/2.0
				prevalue *= amplitude
				value += prevalue
				frequency *= 2.0
				amplitude *= persistence
			value /= maxamplitude
			value = int(value*height)
			output[x][y] = value
		#output.append((x,y,color))
	m = min(map(min,output)) - 1
	return output

def normalize(grid, factors, ints = True):
	values = set()
	for line in grid:
		for item in line:
			values.add(item)
	minval = min(values)
	maxval = max(values)
	delta = maxval - minval
	scale = factors / float(delta)
	
	width = len(grid[0])
	height = len(grid)
	if ints:
		output = [[int(((grid[y][x] - minval) * scale)) for x in range(width)] for y in range(height)]
	else:
		output = [[((grid[y][x] - minval) * scale) for x in range(width)] for y in range(height)]

	return output

def printgrid(grid):
	for y in grid:
		line = ''
		for x in y:
			line += '{0}'.format(int(x))
		print(line)

def gen_biome_map(height, width, biome_count = 7):
	tiles = float(height * width)
	gen = True
	tries = 1
	tries += 1
	grid = Generate(height,width)
	grid2 = normalize(grid, biome_count)

	return grid2
		

def gen_overworld(xmax=16, ymax=16):
	tiles = float(16 * 16)
	gen = True
	tries = 1
	while gen:
		tries += 1
		grid = Generate(16,16)
		grid2 = normalize(grid, 7)
		
		counts = [0,0,0,0,0,0,0,0,0,0]
		for y in grid2:
			for x in y:
				counts[x] += 1

		percentages = [int(100.0 * cnt / tiles) for cnt in counts]
		if all([p > 10 for p in percentages[:7]]):
			gen = False
	return grid2

	
	
def main():
	tiles = float(16 * 16)
	gen = True
	tries = 1
	while gen:
		tries += 1
		grid = Generate(16,16)
		grid2 = normalize(grid, 6)
		
		counts = [0,0,0,0,0,0,0,0,0,0]
		for y in grid2:
			for x in y:
				counts[x] += 1

		percentages = [int(100.0 * cnt / tiles) for cnt in counts]
		if all([p > 10 for p in percentages[:7]]):
			gen = False
		#if percentages[0] < 20 and percentages[0] > 5:
			#gen = False
	print('tries: ', tries)
	print('normalized:')
	printgrid(grid2)
	print(counts)
	print(percentages)

if __name__ == '__main__':
	main()
