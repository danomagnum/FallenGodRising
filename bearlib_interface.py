#!/usr/bin/python
#coding: utf-8 


# http://foo.wyrd.name/en:bearlibterminal:design

from bearlibterminal import terminal
import sys
import os
import time
import random
import math
import sayings
import bearlibkeys as keys
from constants import *

import stdoutCatcher

import locale
locale.setlocale(locale.LC_ALL, '')

#from StringIO import StringIO

import characters

DEBUG = True

DEBUG_STDOUT = False

original_stdout = sys.stdout

current_layer = 0

TERMSIZE = [200, 50]
XRAT = 1
YRAT = 1

def font_setup():
	global XRAT
	global YRAT
	terminal.set("font: UbuntuMono-R.ttf, size=8x16")
	terminal.set("main font: UbuntuMono-R.ttf, size=8x16")
	#terminal.set("tiles font: tilesets/Bisasam_24x24.png, size=24x24, spacing=3x3")
	#terminal.set("tiles font: tilesets/Bisasam_24x24.png, size=24x24, spacing=3x3")
	#XRAT = 3
	#YRAT = 3
	terminal.set("tiles font: tilesets/Phoebus_16x16.png, size=16x16, spacing=2x1")
	XRAT = 2
	YRAT = 1

def initialize():
	terminal.open()
	terminal.set("window: size=200x50;")
	font_setup()

	original_stdout = sys.stdout
	if not DEBUG_STDOUT:
		sys.stdout = stdoutCatcher.ioCatcher()



def progress_bar(actual, maxvalue, length):
	percent = float(actual) / float(maxvalue)
	filled = int(percent * length)
	unfilled = length - filled
	filled_char = '█'
	unfilled_char = ''
	return filled_char * filled + unfilled_char * unfilled

BOXCHARS = ['┌', '─', '┐', '│', ' ', '│', '└', '─', '┘']

class Window(object):
	def __init__(self, height, width, top, left):
		global current_layer
		self.height = height
		self.width = width
		self.top = top
		self.left = left
		self.x = 0
		self.y = 0
		self.layer = current_layer + 1
		current_layer = current_layer + 1

	def getmaxyx(self):
		return(self.height, self.width)

	def getyx(self):
		return(self.height, self.width)

	def erase(self):
		terminal.clear_area(self.left, self.top, self.width, self.height)

	def box(self):
		char = '█'
		for x in range(self.width):
			terminal.printf(self.left + x, self.top, BOXCHARS[1])
			terminal.printf(self.left + x, self.top + self.height, BOXCHARS[7])
		for y in range(self.height):
			terminal.printf(self.left, self.top + y, BOXCHARS[3])
			terminal.printf(self.left + self.width, self.top + y, BOXCHARS[5])
		terminal.printf(self.left, self.top, BOXCHARS[0])
		terminal.printf(self.left + self.width, self.top, BOXCHARS[2])
		terminal.printf(self.left, self.top + self.height, BOXCHARS[6])
		terminal.printf(self.left + self.width, self.top + self.height, BOXCHARS[8])

	def addstr(self, yposition, xposition, string, color = None, font=None):
		#TODO: add color/bold/etc
		if color is not None:
			color = terminal.color_from_name(color)
			terminal.color(color)
		if font is None:
			terminal.printf(self.left + xposition, self.top + yposition,string)
		else:
			prefix = "[font=" + font + "]"
			postfix = "[/font]"
			terminal.printf(self.left + xposition, self.top + yposition,prefix + string + postfix)
		color = terminal.color_from_name("white")
		terminal.color(color)

	def addch(self, y, x, char, color = None, font=None):
		#TODO: add color/bold/etc
		if color is not None:
			color = terminal.color_from_name(color)
			terminal.color(color)
		if font is None:
			terminal.printf(self.left + x, self.top + y,char)
		else:
			prefix = "[font=" + font + "]"
			postfix = "[/font]"
			terminal.printf(self.left + x, self.top + y,prefix + char + postfix)

		#terminal.put(self.left + x, self.top + y, char)
		color = terminal.color_from_name("white")
		terminal.color(color)

	def getch(self):
		return terminal.read()



#TODO: add a "helptext" function where you can hit "?" on a menu to get more
# information on the entry you've selected before going back to the menu right
# where you left off.  Some items could even give better help info (on monsters, etc...)
def menu(window, options, cols = 1, selected = None, clear=True, callback_on_change=None):

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
					color = "green"
				else:
					color = "white"
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
		terminal.refresh()
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
		elif key == terminal.TK_BACKSPACE:
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
		terminal.refresh()

	if clear:
		window.erase()
	terminal.refresh()
	try:
		pass
	except:
		pass # xterm does not like this
	return options[selected]



MAX_COMBATANTS = 3

class Display(object):
	def __init__(self, game=None, user=None, enemy=None):

		XMAX, YMAX = TERMSIZE


		self.statboxsize = [12, int(XMAX/MAX_COMBATANTS)]
		self.charboxsize = (int(YMAX / MAX_COMBATANTS), 40)
		self.msgboxsize = [8, int(XMAX - 2*self.charboxsize[1])]
		self.splashbox = None
		self.charboxes = []
		self.nmeboxes = []
		for i in range(MAX_COMBATANTS):
			charbox = Window(self.charboxsize[0],self.charboxsize[1],self.charboxsize[0]*i,0) 
			nmebox = Window(self.charboxsize[0],self.charboxsize[1],self.charboxsize[0]*i,XMAX - self.charboxsize[1]) 
			self.nmeboxes.append(nmebox)
			self.charboxes.append(charbox)
		self.msgbox   = Window(self.msgboxsize[0],self.msgboxsize[1],YMAX-self.msgboxsize[0],self.charboxsize[1])

		self.overworldbox = Window(self.charboxsize[0],self.charboxsize[1],0,XMAX - self.charboxsize[1]) 

		MENUHEIGHT = 10
		MENUWIDTH = 20
		self.menubox = Window(MENUHEIGHT,MENUWIDTH,YMAX / 2 - MENUHEIGHT,XMAX / 2 - MENUWIDTH) 

		self.user = user
		self.enemy = enemy

		self.mapbox = Window(YMAX - self.msgboxsize[0], XMAX - 2*self.charboxsize[1], 0, self.charboxsize[1])

		self.zone = None

		self.x = 0
		self.y = 0

		self.statbox = []
		for i in range(MAX_COMBATANTS):
			self.statbox.append(Window(self.statboxsize[0],self.statboxsize[1],0,self.statboxsize[1]*i))

		self.startmenusize = (int((YMAX) / MAX_COMBATANTS), int((XMAX - 1) / MAX_COMBATANTS))
		self.start_menus = []
		for i in range(MAX_COMBATANTS):
			classbox = Window(self.startmenusize[0],self.startmenusize[1],self.startmenusize[0]*i,self.startmenusize[1]*0)
			elementbox = Window(self.startmenusize[0],self.startmenusize[1],self.startmenusize[0]*i,self.startmenusize[1]*1) 
			confirmbox = Window(self.startmenusize[0],self.startmenusize[1],self.startmenusize[0]*i,self.startmenusize[1]*2) 
			self.start_menus.append(classbox)
			self.start_menus.append(elementbox)
			self.start_menus.append(confirmbox)

		self.storemenusize = ((YMAX - 1 - self.msgboxsize[0]), int((XMAX -1) / 3))
		self.storebox = Window(self.storemenusize[0], self.storemenusize[1],0,0)
		self.storeinfobox = Window(self.storemenusize[0], self.storemenusize[1],0,self.storemenusize[1])

		self._mode = MAP

		self.refresh_full()

		#self.storebox
		#self.storeinfobox
		#self.charboxes

	def text_entry(self):
		#TODO: text entry box
		return ""

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

	def flash_screen(self, wait_time=0.25):
		pass
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

		terminal.refresh()


	def clear(self):
		self.mapbox.erase()
		for box in self.nmeboxes:
			box.erase()
		for box in self.statbox:
			box.erase()
		self.msgbox.erase()
		terminal.clear()
		
	def show_messages(self):
		msgs = sys.stdout.readlines()
		self.msgbox.erase()
		self.msgbox.box()
		for i in range(len(msgs)):
			self.msgbox.addstr(self.msgboxsize[0] - 2 - i, 1, msgs[i])
		terminal.refresh()

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
		for i in range(MAX_COMBATANTS):
			if i < len(self.user.combatants):
				self.show_combatant_stats(self.game.player.combatants[i], self.charboxes[i])
			else:
				self.charboxes[i].erase()
				self.charboxes[i].box()
			if i < len(self.enemy.combatants):
				self.nmeboxes[i].box()
		self.refresh_combatant()
		self.msgbox.box()

	def menu(self, options, cols = 1, selected = None):
		window = self.msgbox
		return menu(window, options, cols, selected)

	def refresh_combatant(self):
		for i in range(MAX_COMBATANTS):
			if i < len(self.user.combatants):
				self.show_combatant_stats(self.game.player.combatants[i], self.charboxes[i])
			else:
				self.charboxes[i].erase()
				self.charboxes[i].box()
			if i < len(self.enemy.combatants):
				self.show_combatant_stats(self.enemy.combatants[i], self.nmeboxes[i])

	##################################
	##### Map Draw Routines
	##################################
	def update_pad(self):
		self.mapbox.erase()
		if self.zone is None:
			return
		i = 1
		for line in self.zone.map:
			self.mapbox.addstr(i, 1, line, font="tiles")
			i += 1
		drawn = set()
		entity_list = sorted(self.zone.entities, key=lambda x:x.priority)
		for e in entity_list:
			if (e.x, e.y) not in drawn:
				try:
					self.mapbox.addch(YRAT * e.y + 1,XRAT * e.x + 1, e.char, None, font="tiles")
				except:
					print ('{} {} {}'.format(e.y + 1, e.x + 1, e.char))
				drawn.add((e.x + 1, e.y + 1))

		if self.game.player is not None:
			self.mapbox.addch(YRAT * self.game.player.y + 1, XRAT * self.game.player.x + 1, self.game.player.char, None, font="tiles")

	def refresh_full_map(self):
		if self.zone is None:
			return
		self.mapbox.box()
		self.update_pad()
		self.overworldbox.erase()
		self.overworldbox.box()
		self.show_overworld()

		if self.game.player is not None:
			for i in range(MAX_COMBATANTS):
				if i < len(self.game.player.combatants):
					self.show_combatant_stats(self.game.player.combatants[i], self.charboxes[i])
				else:
					self.charboxes[i].erase()
					self.charboxes[i].box()

		self.msgbox.box()
		self.show_messages()

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
		self.refresh_full()



	
	##################################
	##### Stat Draw Routines
	##################################


	def refresh_full_stats(self):
		for i in range(MAX_COMBATANTS):
			if i < len(self.game.player.combatants):
				#self.statbox[i].box()
				self.show_combatant_stats(self.user.combatants[i],self.statbox[i])

		self.msgbox.box()

	def show_combatant_stats(self, combatant, box):
		col2pos = 20
		box.erase()
		box.box()
		height, width = box.getmaxyx()
		
		#Name
		box.addstr(0, 1, '{}  (Level {})'.format(combatant.name, combatant.level))

		#HP
		box.addstr(1, 1, progress_bar(combatant.hp, combatant.max_hp, width - 2), None)
		box.addstr(2, 1, 'HP: {} / {}'.format(int(math.ceil(combatant.hp)),int(math.ceil(combatant.max_hp))), None)
		
		#Experience
		box.addstr(3, 1, 'Exp: {} / {}'.format(int(combatant.exp), int(combatant.exp_at_level(combatant.level + 1))))


		#physical
		box.addstr(4, 1, "P. Atk.: {}".format(int(combatant.physical_strength)), None)
		box.addstr(5, 1, "P. Def.: {}".format(int(combatant.physical_defense)), None)

		#special
		box.addstr(6, 1, "S. Atk: {}".format(int(combatant.special_strength)), None)
		box.addstr(7, 1, "S. Def: {}".format(int(combatant.special_defense)), None)

		#speed
		box.addstr(8, 1, "Speed: {}".format(int(combatant.speed)), None)

		#elements
		element_list = ' '.join([str(element) for element in combatant.elements])
		box.addstr(9, 1, "Elements: {}".format(element_list), None)

		box.addstr(10, 1, "Head: {}".format(combatant.equipment.Head), None)
		box.addstr(11, 1, "Body: {}".format(combatant.equipment.Body), None)
		box.addstr(12, 1, "Token: {}".format(combatant.equipment.Token), None)
		if combatant.equipment.Hands is None:
			box.addstr(13, 1, "Left: {}".format(combatant.equipment.Left), None)
			box.addstr(14, 1, "Right: {}".format(combatant.equipment.Right), None)
		else:
			box.addstr(13, 1, "Hands: {}".format(combatant.equipment.Hands), None)




	##################################
	##### Start Menu Draw Routines
	##################################
	def refresh_full_startmenu(self):
		for box in self.start_menus:
			box.box()


	##################################
	##### Start Shop Draw Routines
	##################################
	def refresh_full_shop(self):
		self.storebox.box()
		self.storeinfobox.box()
		for box in self.charboxes:
			box.box()

	def display_item_stats(self, item, backpack = None):
		self.storeinfobox.box()
		self.storeinfobox.addstr(0, 1, item.name)
		if backpack is not None:
			self.storeinfobox.addstr(1, 1, 'In Backpack: {}'.format(backpack.qty(item.name)))
		self.storeinfobox.addstr(2, 1, 'Cost: {} ({} in backpack)     '.format(item.cost(), self.game.player.backpack.gold))
		self.storeinfobox.addstr(3, 1, 'Desc: {}'.format(item.helptext()))

	def splash_screen(self):
		with open('Splash.txt') as f:
			splash_data = f.readlines()
		width, height = TERMSIZE
		#width = len(splash_data[1])
		self.splashbox = Window(height,width,0,0) 
		splashbox = self.splashbox

		for y, line in enumerate(splash_data):
			splashbox.addstr(y + 1, 1, line)

		splashbox.box()
		terminal.refresh()

	def update_generation_progress(self, percent):
		splashbox = self.splashbox
		splashbox.addstr(y+6, 1, str(percent))

	def game_over(self):
		with open('GameOver.txt') as f:
			splash_data = f.readlines()
		width, height = TERMSIZE
		splashbox = Window(height,width,0,0) 

		for y, line in enumerate(splash_data):
			splashbox.addstr(y + 1, 1, line)

		splashbox.addstr(y+5, 1, 'Press Ctrl+c to exit...')

		splashbox.box()



#TODO: work this into the object
def shutdown():
	terminal.close()
	sys.stdout = original_stdout