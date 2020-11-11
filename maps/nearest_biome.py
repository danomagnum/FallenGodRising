import sys, os, random
from math import *

def generate(width=16, height=16, zones=7):
	biome_map = [[0 for x in range(width)] for y in range(height)]

	zone_centers = []
	while len(zone_centers) < zones:
		x = random.randint(0, width)
		y = random.randint(0, height)
		if (x, y) not in zone_centers:
			zone_centers.append((x, y))
	
	
	for x in range(width):
		for y in range(height):
			nearest_val = 2000000
			nearest_no = 0
			for zone_no in range(zones):
				dx = x - zone_centers[zone_no][0]
				dy = y - zone_centers[zone_no][1]
				metric = dx * dx + dy * dy
				if metric < nearest_val:
					nearest_val = metric
					nearest_no = zone_no
			biome_map[y][x] = nearest_no

	return biome_map

def printgrid(grid):
	for y in grid:
		line = ''
		for x in y:
			line += '{0}'.format(int(x))
		print(line)


	
if __name__ == '__main__':
	printgrid(generate())
