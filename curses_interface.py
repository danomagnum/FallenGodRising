import curses
import libtcod_curses
import curses.textpad
import sys
import os
import time
import random
import math
import sayings
import keys
from constants import *

import stdoutCatcher

import locale
locale.setlocale(locale.LC_ALL, '')

#curses = libtcod_curses.Curses()
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
def menu(window, options, cols = 1, selected = None, clear=True, callback_on_change=None):
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
		#window.clear()
		window.erase()
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

		if callback_on_change is not None:
			callback_on_change(options[selected])

		if DEBUG:
			#options += str(key)
			#print str(key)
			pass
		window.refresh()

	if clear:
		#window.clear()
		window.erase()
	window.refresh()
	try:
		curses.curs_set(old_cursor)
	except:
		pass # xterm does not like this
	return options[selected]



MAX_COMBATANTS = 3

class Display(object):
	def __init__(self, game=None, user=None, enemy=None):
		self.game = game
		self.screen = screen
		self.screen.keypad(1)

		YMAX, XMAX = self.screen.getmaxyx()


		self.statboxsize = [12, int(XMAX/MAX_COMBATANTS)]
		self.charboxsize = (int(YMAX / MAX_COMBATANTS), 40)
		self.msgboxsize = [8, int(XMAX - 2*self.charboxsize[1])]
		self.splashbox = None
		self.charboxes = []
		self.nmeboxes = []
		for i in range(MAX_COMBATANTS):
			charbox = curses.newwin(self.charboxsize[0],self.charboxsize[1],self.charboxsize[0]*i,0) 
			nmebox = curses.newwin(self.charboxsize[0],self.charboxsize[1],self.charboxsize[0]*i,XMAX - self.charboxsize[1]) 
			self.nmeboxes.append(nmebox)
			self.charboxes.append(charbox)
		self.msgbox   = curses.newwin(self.msgboxsize[0],self.msgboxsize[1],YMAX-self.msgboxsize[0],self.charboxsize[1])
		self.battlemenubox   = curses.newwin(self.msgboxsize[0],self.msgboxsize[1],YMAX-2*self.msgboxsize[0],self.charboxsize[1])

		self.overworldbox = curses.newwin(self.charboxsize[0],self.charboxsize[1],0,XMAX - self.charboxsize[1]) 



		MENUHEIGHT = 10
		MENUWIDTH = 20
		self.menubox = curses.newwin(MENUHEIGHT,MENUWIDTH,YMAX / 2 - MENUHEIGHT,XMAX / 2 - MENUWIDTH) 


		self.user = user
		self.enemy = enemy

		self.mapbox = curses.newwin(YMAX - self.msgboxsize[0], XMAX - 2*self.charboxsize[1], 0, self.charboxsize[1])

		#self.change_zone(self.game.zone)
		self.zone = None

		self.x = 0
		self.y = 0

		self.statbox = []
		for i in range(MAX_COMBATANTS):
			self.statbox.append(curses.newwin(self.statboxsize[0],self.statboxsize[1],0,self.statboxsize[1]*i))
			#self.statbox.append(curses.newwin(self.statboxsize[0],self.statboxsize[1],YMAX-(self.statboxsize[0] + 5),self.statboxsize[1]*i))

		self.startmenusize = (int((YMAX) / MAX_COMBATANTS), int((XMAX - 1) / MAX_COMBATANTS))
		self.start_menus = []
		for i in range(MAX_COMBATANTS):
			classbox = curses.newwin(self.startmenusize[0],self.startmenusize[1],self.startmenusize[0]*i,self.startmenusize[1]*0)
			elementbox = curses.newwin(self.startmenusize[0],self.startmenusize[1],self.startmenusize[0]*i,self.startmenusize[1]*1) 
			confirmbox = curses.newwin(self.startmenusize[0],self.startmenusize[1],self.startmenusize[0]*i,self.startmenusize[1]*2) 
			self.start_menus.append(classbox)
			self.start_menus.append(elementbox)
			self.start_menus.append(confirmbox)

		self.storemenusize = ((YMAX - 1 - self.msgboxsize[0]), int((XMAX -1) / 3))
		self.storebox = curses.newwin(self.storemenusize[0], self.storemenusize[1],0,0)
		self.storeinfobox = curses.newwin(self.storemenusize[0], self.storemenusize[1],0,self.storemenusize[1])
		#self.charboxes = []
		#for i in range(MAX_COMBATANTS):
			#charbox = curses.newwin(self.startmenusize[0],self.startmenusize[1],self.startmenusize[0]*i,self.startmenusize[1]*2) 
			#self.charboxes.append(charbox)

		self._mode = MAP

		self.refresh_full()

		#self.storebox
		#self.storeinfobox
		#self.charboxes

	def text_entry(self):
		YMAX, XMAX = self.screen.getmaxyx()
		w = curses.newwin(1,XMAX,1,1) 
		t = curses.textpad.Textbox(w)
		t.edit()
		return t.gather()

	@property
	def mode(self):
		return self._mode
	
	@mode.setter
	def mode(self, value):
		self._mode = value
		self.clear()
		#self.erase()
		self.refresh_full()

	##################################
	##### General Draw Routines
	##################################

	def flash_screen(self, wait_time=0.25):
		curses.flash()
		time.sleep(wait_time)

	def refresh_full(self):
		if self.mode == MAP:
			self.refresh_full_map()
		elif self.mode == COMBAT:
			self.refresh_full_combat()
		elif self.mode == STATS:
			self.refresh_full_stats()
		elif self.mode == STARTMENU:
			self.refresh_full_startmenu()
		elif self.mode == SHOP:
			self.refresh_full_shop()


	def clear(self):
		#self.mapbox.clear()
		self.mapbox.erase()
		self.mapbox.refresh()
		for box in self.nmeboxes:
			#box.clear()
			box.erase()
			box.refresh()
		#for box in self.mybox:
			#box.clear()
			#box.refresh()
		for box in self.statbox:
			#box.clear()
			box.erase()
			box.refresh()
		#self.msgbox.clear()
		self.msgbox.erase()
		self.msgbox.refresh()
		self.screen.refresh()
		
	def show_messages(self):
		msgs = sys.stdout.readlines()
		#self.msgbox.clear()
		self.msgbox.erase()
		self.msgbox.box()
		for i in range(len(msgs)):
			self.msgbox.addstr(self.msgboxsize[0] - 2 - i, 1, msgs[i])
		self.msgbox.refresh()

	##################################
	##### Combat Draw Routines
	##################################

	def end_battle(self):
		self.user = None
		self.enemy = None
		self.mode = MAP
		self.clear()
		#self.erase()
		self.refresh_full
	def start_battle(self, user, enemy):
		self.user = user
		self.enemy = enemy
		self.mode = COMBAT
		self.clear()
		#self.erase()
		self.refresh_full

	def refresh_full_combat(self):
		#self.screen.clear()
		self.screen.refresh()
		for i in range(MAX_COMBATANTS):
			if i < len(self.user.combatants):
				self.show_combatant_stats(self.game.player.combatants[i], self.charboxes[i])
				#self.mybox[i].box()
				#self.mybox[i].refresh()
				#self.mybox[i].overlay(self.screen)
			else:
				self.charboxes[i].erase()
				self.charboxes[i].box()
				self.charboxes[i].refresh()
			if i < len(self.enemy.combatants):
				self.nmeboxes[i].box()
				self.nmeboxes[i].refresh()
				self.nmeboxes[i].overlay(self.screen)
		self.refresh_combatant()
		self.msgbox.box()
		self.msgbox.refresh()
		self.msgbox.overlay(self.screen)
		self.screen.refresh()

	def battlemenu(self, options, cols=1, selected=None):
		window = self.battlemenubox
		return menu(window, options, cols, selected)

	def menu(self, options, cols = 1, selected = None):
		#window = curses.newwin(4, 40, 20, 10)
		YMAX, XMAX = self.screen.getmaxyx()
		#window = curses.newwin(self.msgboxsize[0],self.msgboxsize[1],YMAX-self.msgboxsize[0],0)
		window = self.msgbox
		return menu(window, options, cols, selected)

	def refresh_combatant(self):
		for i in range(MAX_COMBATANTS):
			if i < len(self.user.combatants):
				self.show_combatant_stats(self.game.player.combatants[i], self.charboxes[i])
			else:
				self.charboxes[i].erase()
				self.charboxes[i].box()
				self.charboxes[i].refresh()
			if i < len(self.enemy.combatants):
				self.show_combatant_stats(self.enemy.combatants[i], self.nmeboxes[i])
		#self.show_messages()

	##################################
	##### Map Draw Routines
	##################################
	def update_pad(self):
		if self.zone is None:
			return
		i = 0
		for line in self.zone.map:
			self.mappad.addstr(i, 0, line)
			i += 1
		drawn = set()
		entity_list = sorted(self.zone.entities, key=lambda x:x.priority)
		for e in entity_list:
			if (e.x, e.y) not in drawn:
				#print e.y, e.x, e.char
				#self.mappad.addch(e.y, e.x, e.char)
				try:
					self.mappad.addch(e.y, e.x, e.char, curses.A_BOLD)
				except:
					print ('{} {} {}'.format(e.y, e.x, e.char))
				drawn.add((e.x, e.y))

		if self.game.player is not None:
			self.mappad.addch(self.game.player.y, self.game.player.x, self.game.player.char, curses.A_STANDOUT)

	def refresh_full_map(self):
		#self.screen.clear()
		if self.zone is None:
			return
		self.update_pad()
		#self.screen.refresh()
		self.mapbox.box()
		self.mapbox.refresh()
		self.mapbox.overlay(self.screen)
		self.overworldbox.erase()
		self.overworldbox.box()
		self.show_overworld()
		self.overworldbox.refresh()
		self.overworldbox.overlay(self.screen)
		y0, x0 = self.mapbox.getbegyx()
		ya, xa = self.mapbox.getmaxyx()
		self.mappad.refresh(self.y, self.x, y0 + 1, x0 + 1, y0+ya - 2, x0+xa - 2)

		if self.game.player is not None:
			for i in range(MAX_COMBATANTS):
				if i < len(self.game.player.combatants):
					self.show_combatant_stats(self.game.player.combatants[i], self.charboxes[i])
				else:
					self.charboxes[i].erase()
					self.charboxes[i].box()
					self.charboxes[i].refresh()

		self.msgbox.box()
		self.msgbox.refresh()
		self.msgbox.overlay(self.screen)

	def show_overworld(self):
		y = 1
		for line in self.game.overworld_minimap:
			x = 1
			for cell in line:
				self.overworldbox.addstr(17 - y, x, str(cell))
				x += 1
			y += 1
		x0 = 16 - self.game.overworld_x
		y0 = self.game.overworld_y + 1
		self.overworldbox.addch(x0, y0, '@')
		try:
			self.overworldbox.addstr(1, 17, str(self.game.biome()))
		except:
			pass

	def change_zone(self, zone):
		self.zone = zone
		if zone is not None:
			self.mappad = curses.newpad(zone.height + 1, zone.width + 1)



	
	##################################
	##### Stat Draw Routines
	##################################


	def refresh_full_stats(self):
		#self.screen.clear()
		self.screen.refresh()
		for i in range(MAX_COMBATANTS):
			if i < len(self.game.player.combatants):
				#self.statbox[i].box()
				self.show_combatant_stats(self.user.combatants[i],self.statbox[i])
				#self.statbox[i].refresh()
				self.statbox[i].overlay(self.screen)

		self.msgbox.box()
		self.msgbox.refresh()
		self.msgbox.overlay(self.screen)
		self.screen.refresh()


	def show_combatant_stats(self, combatant, box):
		col2pos = 20
		#box.clear()
		box.erase()
		box.box()
		height, width = box.getmaxyx()
		
		#Name
		box.addstr(0, 1, '{}  (Level {})'.format(combatant.name, combatant.level))

		#HP
		box.addstr(1, 1, progress_bar(combatant.hp, combatant.max_hp, width - 2), curses.color_pair(1))
		box.addstr(2, 1, 'HP: {} / {}'.format(int(math.ceil(combatant.hp)),int(math.ceil(combatant.max_hp))), curses.color_pair(11))
		
		#Experience
		box.addstr(3, 1, 'Exp: {} / {}'.format(int(combatant.exp), int(combatant.exp_at_level(combatant.level + 1))))


		#physical
		box.addstr(4, 1, "P. Atk.: {}".format(int(combatant.physical_strength)), curses.color_pair(11))
		box.addstr(5, 1, "P. Def.: {}".format(int(combatant.physical_defense)), curses.color_pair(11))

		#Arcane
		box.addstr(6, 1, "A. Atk: {}".format(int(combatant.arcane_strength)), curses.color_pair(11))
		box.addstr(7, 1, "A. Def: {}".format(int(combatant.arcane_defense)), curses.color_pair(11))

		#speed
		box.addstr(8, 1, "Speed: {}".format(int(combatant.speed)), curses.color_pair(11))

		#elements
		element_list = ' '.join([str(element) for element in combatant.elements])
		box.addstr(9, 1, "Elements: {}".format(element_list), curses.color_pair(11))

		box.addstr(10, 1, "Head: {}".format(combatant.equipment.Head), curses.color_pair(11))
		box.addstr(11, 1, "Body: {}".format(combatant.equipment.Body), curses.color_pair(11))
		box.addstr(12, 1, "Token: {}".format(combatant.equipment.Token), curses.color_pair(11))
		if combatant.equipment.Hands is None:
			box.addstr(13, 1, "Left: {}".format(combatant.equipment.Left), curses.color_pair(11))
			box.addstr(14, 1, "Right: {}".format(combatant.equipment.Right), curses.color_pair(11))
		else:
			box.addstr(13, 1, "Hands: {}".format(combatant.equipment.Hands), curses.color_pair(11))



		#box.addstr(4, col2pos, "Head: {}".format(combatant.equipment.Head), curses.color_pair(11))
		#box.addstr(5, col2pos, "Body: {}".format(combatant.equipment.Body), curses.color_pair(11))
		#box.addstr(6, col2pos, "Legs: {}".format(combatant.equipment.Legs), curses.color_pair(11))
		#if combatant.equipment.Hands is None:
			#box.addstr(7, col2pos, "Left: {}".format(combatant.equipment.Left), curses.color_pair(11))
			#box.addstr(8, col2pos, "Right: {}".format(combatant.equipment.Right), curses.color_pair(11))
		#else:
			#box.addstr(7, col2pos, "Hands: {}".format(combatant.equipment.Hands), curses.color_pair(11))
#
		#box.addstr(9, col2pos, "Token: {}".format(combatant.equipment.Token), curses.color_pair(11))

		box.refresh()

	##################################
	##### Start Menu Draw Routines
	##################################
	def refresh_full_startmenu(self):
		#self.screen.clear()
		self.screen.refresh()
		for box in self.start_menus:
			box.overlay(self.screen)
			box.box()
			box.refresh()


		#self.msgbox.box()
		#self.msgbox.refresh()
		#self.msgbox.overlay(self.screen)
		self.screen.refresh()

	##################################
	##### Start Shop Draw Routines
	##################################
	def refresh_full_shop(self):
		self.storebox.box()
		self.storebox.refresh()
		self.storeinfobox.box()
		self.storeinfobox.refresh()
		for box in self.charboxes:
			box.box()
			box.refresh()

	def display_item_stats(self, item, backpack = None):
		self.storeinfobox.box()
		self.storeinfobox.addstr(0, 1, item.name)
		if backpack is not None:
			self.storeinfobox.addstr(1, 1, 'In Backpack: {}'.format(backpack.qty(item.name)))
		self.storeinfobox.addstr(2, 1, 'Cost: {} ({} in backpack)     '.format(item.cost(), self.game.player.backpack.gold))
		self.storeinfobox.addstr(3, 1, 'Desc: {}'.format(item.helptext()))
		self.storeinfobox.refresh()

	def splash_screen(self):
		with open('Splash.txt') as f:
			splash_data = f.readlines()
		height, width = self.screen.getmaxyx()
		#width = len(splash_data[1])
		self.splashbox = curses.newwin(height,width,0,0) 
		splashbox = self.splashbox

		for y, line in enumerate(splash_data):
			splashbox.addstr(y + 1, 1, line)

		splashbox.box()
		splashbox.refresh()
		splashbox.overlay(self.screen)
		screen.refresh()

	def update_generation_progress(self, percent):
		splashbox = self.splashbox
		splashbox.addstr(y+6, 1, str(percent))

	def game_over(self):
		with open('GameOver.txt') as f:
			splash_data = f.readlines()
		height, width = self.screen.getmaxyx()
		#width = len(splash_data[1])
		splashbox = curses.newwin(height,width,0,0) 

		for y, line in enumerate(splash_data):
			splashbox.addstr(y + 1, 1, line)

		splashbox.addstr(y+5, 1, 'Press Ctrl+c to exit...')

		splashbox.box()
		splashbox.refresh()
		splashbox.overlay(self.screen)
		screen.refresh()



#TODO: work this into the object
def shutdown():
	curses.endwin()
	sys.stdout = original_stdout
