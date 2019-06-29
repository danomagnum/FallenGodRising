import curses
import sys
import os
import time
import random
import math
import sayings
import keys

import stdoutCatcher
from StringIO import StringIO

import characters

DEBUG = True

screen = None
original_stdout = sys.stdout

def initialize():
	global screen
	global original_stdout
	screen = curses.initscr()
	curses.start_color()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)
	curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)

	curses.init_pair(11, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(13, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(14, curses.COLOR_BLUE, curses.COLOR_BLACK)

	curses.noecho()

	original_stdout = sys.stdout
	sys.stdout = stdoutCatcher.ioCatcher()

def map_gen(height, width, rooms, minroomsize = 4):
	tiles = [[0 for y in range(height)] for x in range(width)]
	for room in range(rooms):
		room_width = random.randint(minroomsize, max(minroomsize + 1, width/rooms))
		room_height = random.randint(minroomsize, max(minroomsize + 1, height/rooms))
		room_x = random.randint(1, width - room_width - 1)
		room_y = random.randint(1, height - room_height - 1)

		for x in range(room_width):
			for y in range(room_height):
				try:
					tiles[room_x + x][room_y + y] = 1
				except IndexError:
					pass

	#set up walls
	for x in range(width):
		for y in range(height):
			if tiles[x][y] == 1:
				if x > 0:
					if tiles[x-1][y] == 0:
						tiles[x-1][y] = 2
				if x < width:
					if tiles[x+1][y] == 0:
						tiles[x+1][y] = 2
				if y > 0:
					if tiles[x][y-1] == 0:
						tiles[x][y-1] = 2
				if y < height:
					if tiles[x][y+1] == 0:
						tiles[x][y+1] = 2

	return tiles

def showmap(tiles, printout = False):
	lines = []
	for x in tiles:
		line = ''
		for y in x:
			if y == 0:
				line += ' '
			elif y  == 1:
				line += '.'
			elif y == 2:
				line += '#'

		lines.append(line)
		if printout:
			print line
	return lines

def savelines(lines, filename):
	f = open(filename, 'w')
	for line in lines:
		f.write(line)
		f.write('\n')
	f.close()

def readmap(filename):
	f = open(filename, 'r')
	content = f.readlines()
	return content

def find_valid_position(area):
	while True:
		x = random.randint(0, len(area[0]))
		y = random.randint(0, len(area[1]))
		if area[y][x] == '.':
			return (x, y)

class curses_display(object):
	def __init__(self, area_map):
		self.area_map = area_map
		self.area_size = (len(area_map), len(area_map[0]))
		self.screen = screen
		self.screen.keypad(1)
		YMAX, XMAX = self.screen.getmaxyx()

		self.mapbox = curses.newwin(YMAX-2, XMAX - 2, 1, 1)
		self.mappad = curses.newpad(self.area_size[0] + 1, self.area_size[1] + 1)
		self.x = 0
		self.y = 0
		
		self.char_x = 0
		self.char_y = 0
	
	def move(self, direction):
		UP = 1
		DOWN = 2
		LEFT = 3
		RIGHT = 4
		if direction == UP:
			if self.area_map[self.char_y - 1][self.char_x] == '.':
				self.mappad.addch(self.char_y, self.char_x, '.')
				self.mappad.addch(self.char_y - 1, self.char_x, '@')
				self.char_y -= 1
				display.y = max(0, display.y -1)
		elif direction == DOWN:
			if self.area_map[self.char_y + 1][self.char_x] == '.':
				self.mappad.addch(self.char_y, self.char_x, '.')
				self.mappad.addch(self.char_y + 1, self.char_x, '@')
				self.char_y += 1
				display.y = min((display.mappad.getmaxyx()[0]  - display.mapbox.getmaxyx()[0]), display.y + 1)
		elif direction == LEFT:
			if self.area_map[self.char_y][self.char_x - 1] == '.':
				self.mappad.addch(self.char_y, self.char_x, '.')
				self.mappad.addch(self.char_y, self.char_x - 1, '@')
				self.char_x -= 1
				display.x = max(0, display.x -1)
		elif direction == RIGHT:
			if self.area_map[self.char_y][self.char_x + 1] == '.':
				self.mappad.addch(self.char_y, self.char_x, '.')
				self.mappad.addch(self.char_y, self.char_x + 1, '@')
				self.char_x += 1
				display.x = min((display.mappad.getmaxyx()[1]  - display.mapbox.getmaxyx()[1]), display.x + 1)

	def recenter(self, x = None, y = None):
		if x is None:
			x = self.char_x
		if y is None:
			y = self.char_y

		display.x = max(1, x - self.mapbox.getmaxyx()[1]/2)
		display.y = max(1, y - self.mapbox.getmaxyx()[0]/2)

	def update_pad(self):
		i = 0
		for line in self.area_map:
			self.mappad.addstr(i, 0, line)
			i += 1
		self.mappad.addch(self.char_y, self.char_x, '@')

	def refresh_full(self):
		self.screen.clear()
		self.mapbox.box()
		self.mapbox.refresh()
		self.mapbox.overlay(self.screen)
		y0, x0 = self.mapbox.getbegyx()
		ya, xa = self.mapbox.getmaxyx()
		self.mappad.move(self.char_y, self.char_x)
		self.mappad.refresh(self.y, self.x, y0 + 1, x0 + 1, y0+ya - 2, x0+xa - 2)

	def show_map(self):
		pass


if __name__ == '__main__':
	initialize()
	#zone = readmap('maps/test7.map')
	zone = showmap(map_gen(40, 40, 10, 8))
	x, y = find_valid_position(zone)
	display = curses_display(zone)
	display.char_x = x
	display.char_y = y
	display.recenter()
	display.update_pad()
	display.refresh_full()
	display.mapbox.keypad(1)
	loop = True
	while loop:
		key = display.mapbox.getch()
		if key in keys.UP:
			display.move(1)
		elif key in keys.DOWN:
			display.move(2)
		elif key in keys.LEFT:
			display.move(3)
		elif key in keys.RIGHT:
			display.move(4)
		display.refresh_full()
