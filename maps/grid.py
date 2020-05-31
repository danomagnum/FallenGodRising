#!/usr/bin/python
#coding: utf-8 

import main, battle, zone, entities, moves, elements, items
from constants import *
import random
import maps.maptools as maptools
import maps.perlin as perlin
import os
import sys

def add_vdoor(lev, x, y):
	x = int(x)
	y = int(y)
	if lev[y][x] == '.' or lev[y][x] == '+':
		return True
	lev[y][x] = '+'

	lev[y][x - 1] = '+'
	lev[y][x + 1] = '+'

	lev[y - 1][x - 2] = '#'
	lev[y - 1][x + 2] = '#'
	lev[y - 1][x - 3] = '#'
	lev[y - 1][x + 3] = '#'
	lev[y - 1][x - 4] = '#'
	lev[y - 1][x + 4] = '#'

	lev[y + 1][x - 2] = '#'
	lev[y + 1][x + 2] = '#'
	lev[y + 1][x - 3] = '#'
	lev[y + 1][x + 3] = '#'
	lev[y + 1][x - 4] = '#'
	lev[y + 1][x + 4] = '#'


	return False

def add_hdoor(lev, x, y):
	x = int(x)
	y = int(y)
	#if lev[y][x] == '.':
	if lev[y][x] == '.' or lev[y][x] == '+':
		return True
	lev[y][x] = '+'

	lev[y-1][x] = '+'
	lev[y+1][x] = '+'

	lev[y-2][x-1] = '#'
	lev[y+2][x-1] = '#'
	lev[y-3][x-1] = '#'
	lev[y+3][x-1] = '#'
	lev[y-4][x-1] = '#'
	lev[y+4][x-1] = '#'

	lev[y-2][x+1] = '#'
	lev[y+2][x+1] = '#'
	lev[y-3][x+1] = '#'
	lev[y+3][x+1] = '#'
	lev[y-4][x+1] = '#'
	lev[y+4][x+1] = '#'

	return False

def gridlevel(width = 3, height = 2):

	#horizontal wall Y coordinates
	h = []
	spacing = int(maptools.MAPSIZE[1] / height)
	for y in range(height):
		h.append(y * spacing)
	h.append(maptools.MAPSIZE[1] - 1)

	#vertical wall x coordinates
	v = []
	spacing = int(maptools.MAPSIZE[0] / width)
	for x in range(width):
		v.append(x * spacing)
	v.append(maptools.MAPSIZE[0] - 1)

	#find the room entries
	maze = maptools.maze(width, height)

	#set up the map
	lev = [['.' for x in range(maptools.MAPSIZE[0])] for y in range(maptools.MAPSIZE[1])]

	#set up the wall grid
	for x in range(maptools.MAPSIZE[0] - 1):
		for wall in range(height + 1):
			lev[h[wall]][x] = '#'


	for y in range(maptools.MAPSIZE[1] - 1):
		for wall in range(width + 1):
			lev[y][v[wall]] = '#'
	lev[maptools.MAPSIZE[1] - 1][maptools.MAPSIZE[0] - 1] = '#'


	for x in range(width):
		for y in range(height):
			dirs = [UP, DOWN, LEFT, RIGHT]
			if x == 0:
				dirs.remove(LEFT)
			if y == 0:
				dirs.remove(UP)
			if x == (width - 1):
				dirs.remove(RIGHT)
			if y == (height - 1):
				dirs.remove(DOWN)

			search = True
			while search and dirs:
				exit = random.choice(dirs)
				dirs.remove(exit)
				if exit == RIGHT:
					search = add_hdoor(lev, v[x + 1], h[y] + (h[y + 1] - h[y])/2)
				elif exit == LEFT:
					search = add_hdoor(lev, v[x],     h[y] + (h[y + 1] - h[y])/2)
				elif exit == UP:
					search = add_vdoor(lev, v[x] + (v[x + 1] - v[x])/2, h[y])
				elif exit == DOWN:
					search = add_vdoor(lev, v[x] + (v[x + 1] - v[x])/2, h[y + 1])
	


	return lev


if __name__ == '__main__':
	a = gridlevel()
	maptools.flatten(a, True)
