import curses
import sys
import os
import time
import random
import math
import sayings
import keys

MAP = 0
COMBAT = 1
STATS = 2

import stdoutCatcher
#from StringIO import StringIO

import characters

DEBUG = True

DEBUG_STDOUT = False

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
	if not DEBUG_STDOUT:
		sys.stdout = stdoutCatcher.ioCatcher()



def progress_bar(actual, maxvalue, length):
	percent = float(actual) / float(maxvalue)
	filled = int(percent * length)
	unfilled = length - filled
	filled_char = ' '
	unfilled_char = ''
	return filled_char * filled + unfilled_char * unfilled

#TODO: add a "helptext" function where you can hit "?" on a menu to get more
# information on the entry you've selected before going back to the menu right
# where you left off.  Some items could even give better help info (on monsters, etc...)
def menu(window, options, cols = 1, selected = None):
	#window = curses.newwin(4, 40, 20, 10)
	#YMAX, XMAX = self.screen.getmaxyx()
	#window = curses.newwin(self.msgboxsize[0],self.msgboxsize[1],YMAX-self.msgboxsize[0],0)
	try:
		old_cursor = curses.curs_set(0)
	except:
		pass # xterm does not like this
	window.keypad(1)
	for opt_id in range(len(options)):
		if selected == options[opt_id]:
			selected = opt_id
			break
	else:
		selected = 0
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
	def __init__(self, user=None, enemy=None, zone=None):
		self.screen = screen
		self.screen.keypad(1)

		YMAX, XMAX = self.screen.getmaxyx()

		self.combatantboxsize = [5, int(XMAX/MAX_COMBATANTS)]
		self.statboxsize = [10, int(XMAX/MAX_COMBATANTS)]
		self.msgboxsize = [5, int(XMAX)]
		self.nmebox = []
		self.mybox = []
		for i in range(MAX_COMBATANTS):
			self.nmebox.append(curses.newwin(self.combatantboxsize[0],self.combatantboxsize[1],0,self.combatantboxsize[1]*i))
			self.mybox.append(curses.newwin(self.combatantboxsize[0],self.combatantboxsize[1],YMAX-(self.combatantboxsize[0] + 5),self.combatantboxsize[1]*i))
		self.msgbox   = curses.newwin(self.msgboxsize[0],self.msgboxsize[1],YMAX-self.msgboxsize[0],0)

		self.user = user
		self.enemy = enemy


		self.zone = zone
		self.mapbox = curses.newwin(YMAX-1 - self.msgboxsize[0], XMAX - 2, 0, 0)
		self.mappad = curses.newpad(zone.height + 1, zone.width + 1)
		self.x = 0
		self.y = 0

		self.statbox = []
		for i in range(MAX_COMBATANTS):
			self.statbox.append(curses.newwin(self.statboxsize[0],self.statboxsize[1],0,self.statboxsize[1]*i))
			self.statbox.append(curses.newwin(self.statboxsize[0],self.statboxsize[1],YMAX-(self.statboxsize[0] + 5),self.statboxsize[1]*i))

		self._mode = MAP

		self.refresh_full()

	@property
	def mode(self):
		return self._mode
	
	@mode.setter
	def mode(self, value):
		self._mode = value
		self.clear()
		self.refresh_full()

	##################################
	##### General Draw Routines
	##################################

	def refresh_full(self):
		if self.mode == MAP:
			self.refresh_full_map()
		elif self.mode == COMBAT:
			self.refresh_full_combat()
		elif self.mode == STATS:
			self.refresh_full_stats()

	def clear(self):
		self.mapbox.clear()
		self.mapbox.refresh()
		for box in self.nmebox:
			box.clear()
			box.refresh()
		for box in self.mybox:
			box.clear()
			box.refresh()
		for box in self.statbox:
			box.clear()
			box.refresh()
		self.msgbox.clear()
		self.msgbox.refresh()
		self.screen.refresh()
		
	def show_messages(self):
	    for out in sys.stdout.readlines():
		    if out.strip() != '':
			    self.msgbox.addstr(1, 1, out)
			    self.msgbox.addstr(4, 1, sayings.press_to_continue)
			    self.msgbox.box()
			    self.msgbox.refresh()
			    waiting = True
			    while waiting:
				    key = self.msgbox.getch()
				    if key in keys.SELECT + keys.BACK:
					    waiting = False
		    self.msgbox.clear()
		    self.msgbox.box()
		    self.msgbox.refresh()


	##################################
	##### Combat Draw Routines
	##################################

	def end_battle(self):
		self.user = None
		self.enemy = None
		self.mode = MAP
		self.clear()
		self.refresh_full
	def start_battle(self, user, enemy):
		self.user = user
		self.enemy = enemy
		self.mode = COMBAT
		self.clear()
		self.refresh_full

	def refresh_full_combat(self):
		self.screen.clear()
		self.screen.refresh()
		for i in range(MAX_COMBATANTS):
			if i < len(self.user.combatants):
				self.mybox[i].box()
				self.mybox[i].refresh()
				self.mybox[i].overlay(self.screen)
			if i < len(self.enemy.combatants):
				self.nmebox[i].box()
				self.nmebox[i].refresh()
				self.nmebox[i].overlay(self.screen)
		self.refresh_combatant()
		self.msgbox.box()
		self.msgbox.refresh()
		self.msgbox.overlay(self.screen)
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

	def refresh_combatant(self):
		for i in range(MAX_COMBATANTS):
			if i < len(self.user.combatants):
				self.show_combatant(self.user.combatants[i], self.mybox[i])
			if i < len(self.enemy.combatants):
				self.show_combatant(self.enemy.combatants[i], self.nmebox[i])
		self.show_messages()

	##################################
	##### Map Draw Routines
	##################################
	def recenter(self, x = None, y = None):
		if x is None:
			x = self.zone.Player.x
		if y is None:
			y = self.zone.Player.y

		self.x = max(1, x - self.mapbox.getmaxyx()[1]/2)
		self.y = max(1, y - self.mapbox.getmaxyx()[0]/2)

	def update_pad(self):
		i = 0
		for line in self.zone.map:
			self.mappad.addstr(i, 0, line)
			i += 1
		self.mappad.addch(self.zone.Player.y, self.zone.Player.x, '@')

	def set_position(self, x, y):
		self.zone.Player.x = x
		self.zone.Player.y = y
		self.recenter()
		self.update_pad()
		self.refresh_full()


	def refresh_full_map(self):
		#self.screen.clear()
		self.screen.refresh()
		self.mapbox.box()
		self.mapbox.refresh()
		self.mapbox.overlay(self.screen)
		y0, x0 = self.mapbox.getbegyx()
		ya, xa = self.mapbox.getmaxyx()
		self.mappad.move(self.zone.Player.y, self.zone.Player.x)
		self.mappad.refresh(self.y, self.x, y0 + 1, x0 + 1, y0+ya - 2, x0+xa - 2)

		self.msgbox.box()
		self.msgbox.refresh()
		self.msgbox.overlay(self.screen)

	
	##################################
	##### Stat Draw Routines
	##################################


	def refresh_full_stats(self):
		#self.screen.clear()
		self.screen.refresh()
		for i in range(MAX_COMBATANTS):
			if i < len(self.user.combatants):
				#self.statbox[i].box()
				self.show_combatant_stats(self.user.combatants[i],self.statbox[i])
				#self.statbox[i].refresh()
				self.statbox[i].overlay(self.screen)
		self.msgbox.box()
		self.msgbox.refresh()
		self.msgbox.overlay(self.screen)
		self.screen.refresh()


	def show_combatant_stats(self, combatant, box):
		box.clear()
		box.box()
		
		#Name
		box.addstr(0, 1, combatant.name)

		#HP
		box.addstr(1, 1, progress_bar(combatant.hp, combatant.max_hp, self.combatantboxsize[1] - 2), curses.color_pair(1))
		box.addstr(2, 1, str(int(math.ceil(combatant.hp))) + ' / ' + str(int(math.ceil(combatant.max_hp))), curses.color_pair(11))
		
		#Experience
		box.addstr(3, 1, progress_bar(combatant.exp - combatant.exp_at_level(combatant.level), combatant.exp_at_level(combatant.level + 1) - combatant.exp_at_level(combatant.level), self.combatantboxsize[1] - 2), curses.color_pair(4))

		#Level
		box.addstr(4, 1, "Level: {}".format(combatant.level), curses.color_pair(1))

		#physical
		box.addstr(5, 1, "Phys. Atk./Def.: {}/{}".format(combatant.physical_strength,combatant.physical_defense), curses.color_pair(1))

		#special
		box.addstr(6, 1, "Spcl. Atk./Def: {}/{}".format(combatant.special_strength,combatant.special_defense), curses.color_pair(1))

		#speed
		box.addstr(7, 1, "Speed: {}".format(combatant.speed), curses.color_pair(1))

		#elements
		element_list = ' '.join([str(element) for element in combatant.elements])
		box.addstr(8, 1, "Elements: {}".format(element_list), curses.color_pair(1))

		box.refresh()




#TODO: work this into the object
def shutdown():
	curses.endwin()
	sys.stdout = original_stdout
