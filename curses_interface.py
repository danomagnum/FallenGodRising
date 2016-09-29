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


def progress_bar(actual, maxvalue, length):
	percent = float(actual) / float(maxvalue)
	filled = int(percent * length)
	unfilled = length - filled
	filled_char = ' '
	unfilled_char = ''
	return filled_char * filled + unfilled_char * unfilled

def menu(window, options, cols = 1, selected = None):
	#window = curses.newwin(4, 40, 20, 10)
	#YMAX, XMAX = self.screen.getmaxyx()
	#window = curses.newwin(self.msgboxsize[0],self.msgboxsize[1],YMAX-self.msgboxsize[0],0)
	try:
		old_cursor = curses.curs_set(0)
	except:
		pass # xterm does not like this
	window.keypad(1)
	for opt_id in xrange(len(options)):
		if selected == options[opt_id]:
			selected = opt_id
			break
	offset = 0
	ymax, xmax = window.getmaxyx()
	colgap = int(xmax / cols)
	selected_row = 0
	opt_count = len(options)

	if selected < 0:
		selected = 0
	elif selected > (opt_count - 1):
		selected = opt_count - 1
		
	maxrow = opt_count / cols

	loop = True
	while loop:
		window.clear()
		window.box()
		count = 0
		col = 0
		row = 0
		for option in options:
			yposition = 1 + row - offset
			xposition = 1 + col * colgap
			if (yposition <= (ymax - 2)) and (yposition >= 1):
				if count == selected:
					selected_row = row
					color = curses.color_pair(1)
				else:
					color = curses.color_pair(11)
				window.addstr(yposition, xposition, str(option), color)
			else:
				if (yposition > (ymax - 2)):
					window.addstr(ymax - 1, 1, '...')
				if (yposition < 1):
					window.addstr(0, 1, '...')
			count += 1
			col += 1
			if col >= cols:
				col = 0
				row += 1
		key = window.getch()
		if key in keys.UP:
			if selected > 0:
				if selected_row == 0:
					offset = 0
				else:
					if ( 1 + selected_row - offset) == 1:
						offset -= 1
			selected = selected - cols
		elif key in keys.DOWN:
			if selected < (opt_count - 1):
				if ( 1 + selected_row - offset) == (ymax - 2):
					offset += 1
			selected = selected + cols
		elif key in keys.LEFT:
			selected = selected - 1
		elif key in keys.RIGHT:
			selected = selected + 1
		elif key in keys.SELECT:
			loop = False
			#sys.exit(key)
		elif key in keys.BACK:
			#sys.exit(key)
			return None #escape key

		if selected < 0:
			selected = 0
		elif selected >= opt_count:
			selected = opt_count - 1

		if DEBUG:
			#options += str(key)
			#print str(key)
			pass
		window.refresh()

	window.clear()
	window.refresh()
	try:
		curses.curs_set(old_cursor)
	except:
		pass # xterm does not like this
	return options[selected]



MAX_COMBATANTS = 3

class curses_display(object):
	def __init__(self, user, enemy):
		self.screen = screen
		self.screen.keypad(1)

		YMAX, XMAX = self.screen.getmaxyx()

		self.combatantboxsize = [5, XMAX/MAX_COMBATANTS]
		self.msgboxsize = [5, XMAX]
		self.nmebox = []
		self.mybox = []
		for i in xrange(MAX_COMBATANTS):
			self.nmebox.append(curses.newwin(self.combatantboxsize[0],self.combatantboxsize[1],0,self.combatantboxsize[1]*i))
			self.mybox.append(curses.newwin(self.combatantboxsize[0],self.combatantboxsize[1],YMAX-(self.combatantboxsize[0] + 5),self.combatantboxsize[1]*i))
		self.msgbox   = curses.newwin(self.msgboxsize[0],self.msgboxsize[1],YMAX-self.msgboxsize[0],0)

		self.user = user
		self.enemy = enemy

		self.refresh_full()

	def refresh_full(self):
		self.screen.clear()
		for i in xrange(MAX_COMBATANTS):
			if i < len(self.user.combatants):
				self.mybox[i].box()
				self.mybox[i].refresh()
				self.mybox[i].overlay(screen)
			if i < len(self.enemy.combatants):
				self.nmebox[i].box()
				self.nmebox[i].refresh()
				self.nmebox[i].overlay(screen)
		self.msgbox.box()
		self.refresh_combatant()
		self.msgbox.refresh()
		self.msgbox.overlay(screen)
		self.screen.refresh()

	def show_combatant(self, combatant, box, hideexp=False):
		box.clear()
		box.box()
		box.addstr(0, 1, combatant.name)
		box.addstr(1, 1, progress_bar(combatant.hp, combatant.max_hp, self.combatantboxsize[1] - 2), curses.color_pair(1))
		box.addstr(2, 1, str(int(math.ceil(combatant.hp))) + ' / ' + str(int(math.ceil(combatant.max_hp))), curses.color_pair(11))
		if not hideexp:
			box.addstr(3, 1, progress_bar(combatant.exp - combatant.exp_at_level(combatant.level), combatant.exp_at_level(combatant.level + 1) - combatant.exp_at_level(combatant.level), self.combatantboxsize[1] - 2), curses.color_pair(4))
		if (combatant == self.user.combatant) or (combatant == self.enemy.combatant):
			box.addstr(4, 1, 'Active')
		box.refresh()

	def menu(self, options, cols = 1, selected = None):
		#window = curses.newwin(4, 40, 20, 10)
		YMAX, XMAX = self.screen.getmaxyx()
		window = curses.newwin(self.msgboxsize[0],self.msgboxsize[1],YMAX-self.msgboxsize[0],0)
		return menu(window, options, cols, selected)
	
	def show_messages(self):
		for out in sys.stdout.readlines():
			if out.strip() != '':
				self.msgbox.addstr(1, 1, out)
				self.msgbox.addstr(4, 1, sayings.press_to_continue)
				self.msgbox.refresh()
				waiting = True
				while waiting:
					key = self.msgbox.getch()
					if key in keys.SELECT + keys.BACK:
						waiting = False
			self.msgbox.clear()
			self.msgbox.box()
			self.msgbox.refresh()

	def refresh_combatant(self):
		for i in xrange(MAX_COMBATANTS):
			if i < len(self.user.combatants):
				self.show_combatant(self.user.combatants[i], self.mybox[i])
			if i < len(self.enemy.combatants):
				self.show_combatant(self.enemy.combatants[i], self.nmebox[i])
		self.show_messages()

def shutdown():
	curses.endwin()
	sys.stdout = original_stdout
