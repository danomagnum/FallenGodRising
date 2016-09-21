import curses
import sys
import os
import time
import random
import math

import stdoutCatcher
from StringIO import StringIO

import characters

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

class curses_display(object):
	def __init__(self, user, enemy):
		self.screen = screen
		self.screen.keypad(1)

		YMAX, XMAX = self.screen.getmaxyx()

		self.combatantboxsize = [5, 20]
		self.msgboxsize = [5, XMAX]
		self.nmebox = curses.newwin(self.combatantboxsize[0],self.combatantboxsize[1],0,0)
		self.mybox = curses.newwin(self.combatantboxsize[0],self.combatantboxsize[1],YMAX-(self.combatantboxsize[0] + 5),XMAX-self.combatantboxsize[1])
		self.msgbox   = curses.newwin(self.msgboxsize[0],self.msgboxsize[1],YMAX-self.msgboxsize[0],0)

		self.user = user
		self.enemy = enemy

		self.refresh_full()

	def refresh_full(self):
		self.screen.clear()
		self.nmebox.box()
		self.mybox.box()
		self.msgbox.box()
		self.refresh_combatant()
		self.nmebox.refresh()
		self.mybox.refresh()
		self.msgbox.refresh()
		self.nmebox.overlay(screen)
		self.mybox.overlay(screen)
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
		box.refresh()

	def menu(self, options, cols = 1, selected = 0):
		window = curses.newwin(4, 40, 20, 10)
		try:
			old_cursor = curses.curs_set(0)
		except:
			pass # xterm does not like this

		offset = 0
		ymax, xmax = window.getmaxyx()
		colgap = int(xmax / cols)
		window.keypad(1)
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
			if key == curses.KEY_UP:
				if selected > 0:
					if selected_row == 0:
						offset = 0
					else:
						if ( 1 + selected_row - offset) == 1:
							offset -= 1
				selected = selected - cols
			elif key == curses.KEY_DOWN:
				if selected <= (opt_count - 1):
					if ( 1 + selected_row - offset) == (ymax - 1):
						offset += 1
				selected = selected + cols
			elif key == curses.KEY_LEFT:
				selected = selected - 1
			elif key == curses.KEY_RIGHT:
				selected = selected + 1
			elif key == curses.KEY_ENTER or key == 10:
				loop = False

			if selected < 0:
				selected = 0
			elif selected >= opt_count:
				selected = opt_count - 1

			window.refresh()

		window.clear()
		window.refresh()
		try:
			curses.curs_set(old_cursor)
		except:
			pass # xterm does not like this
		return options[selected]


	def show_messages(self):
		for out in sys.stdout.readlines():
			if out.strip() != '':
				self.msgbox.addstr(1, 1, out)
				self.msgbox.refresh()
				key = self.msgbox.getch()
			self.msgbox.clear()
			self.msgbox.box()
			self.msgbox.refresh()

	def refresh_combatant(self):
		self.show_combatant(self.user, self.mybox)
		self.show_combatant(self.enemy, self.nmebox)
		self.show_messages()

def shutdown():
	curses.endwin()
	sys.stdout = original_stdout
