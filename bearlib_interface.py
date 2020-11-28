#/usr/bin/python
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

import maps.maptools as maptools

import vision

import stdoutCatcher
import settings

import locale
locale.setlocale(locale.LC_ALL, '')

#from StringIO import StringIO


DEBUG = True

DEBUG_STDOUT = False

original_stdout = sys.stdout

current_layer = 0

TERMSIZE = [200, 50]
XRAT = 1
YRAT = 1

ANIMATION_RATE = 0.1 
ANIMATION_LAST = 0
ANIMATION_FRAME = 1
ANIMATION_FRAMES = 4
ANIMATION_DIR = 1


def update_animation_frame():
	global ANIMATION_FRAME
	global ANIMATION_DIR
	global ANIMATION_LAST
	global ANIMATION_RATE
	global ANIMATION_FRAMES

	now = time.time()
	delta = now - ANIMATION_LAST
	
	if delta > ANIMATION_RATE:
		ANIMATION_LAST = now
		ANIMATION_FRAME += ANIMATION_DIR
		if ANIMATION_FRAME == ANIMATION_FRAMES:
			ANIMATION_DIR = -1
		elif ANIMATION_FRAME == 1:
			ANIMATION_DIR = 1

def font_setup():
	global XRAT
	global YRAT
	terminal.set("font: data/UbuntuMono-R.ttf, size=8x16")
	terminal.set("main font: data/UbuntuMono-R.ttf, size=8x16")
	#terminal.set("tiles font: tilesets/Bisasam_24x24.png, size=24x24, spacing=3x3")
	#terminal.set("tiles font: tilesets/Bisasam_24x24.png, size=24x24, spacing=3x3")
	#XRAT = 3
	#YRAT = 3
	terminal.set("tiles font: data/tileset.png, size=16x16, spacing=2x1")
	terminal.set("tiles1 font: data/tileset1.png, size=16x16, spacing=2x1")
	terminal.set("tiles2 font: data/tileset2.png, size=16x16, spacing=2x1")
	terminal.set("tiles3 font: data/tileset3.png, size=16x16, spacing=2x1")
	XRAT = 2
	YRAT = 1

def initialize():
	terminal.open()
	terminal.set("window: size=200x50, title='Fallen God Rising';")
	terminal.set("window: size=200x50;")
	terminal.set("input: filter=[keyboard, mouse]")
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
	def __init__(self, height, width, top, left, layer=0):
		global current_layer
		self.height = height
		self.width = width
		self.top = top
		self.left = left
		self.x = 0
		self.y = 0
		self.layer = current_layer + 1
		current_layer = current_layer + 1
		self.spacing = [1, 1]
		self.layer = layer

	def getmaxyx(self):
		return(self.height, self.width)

	def getyx(self):
		return(self.height, self.width)

	def erase(self):
		for layer in range(0,4):
			terminal.layer(layer)
			terminal.clear_area(int(self.left), int(self.top), int(self.width), int(self.height))
		#terminal.clear_area(self.left, self.top, self.width, self.height)

	def box(self, opaque=False):
		if opaque:
			for layer in range(self.layer + 1):
				terminal.layer(layer)
				terminal.clear_area(int(self.left), int(self.top), int(self.width), int(self.height))

		terminal.layer(self.layer)

		for x in range(self.width):
			terminal.printf(int(self.left + x),int(self.top), BOXCHARS[1])
			terminal.printf(int(self.left + x), int(self.top + self.height), BOXCHARS[7])
		for y in range(self.height):
			terminal.printf(int(self.left), int(self.top + y), BOXCHARS[3])
			terminal.printf(int(self.left + self.width), int(self.top + y), BOXCHARS[5])

		terminal.printf(int(self.left), int(self.top), BOXCHARS[0])
		terminal.printf(int(self.left + self.width), int(self.top), BOXCHARS[2])
		terminal.printf(int(self.left), int(self.top + self.height), BOXCHARS[6])
		terminal.printf(int(self.left + self.width), int(self.top + self.height), BOXCHARS[8])

	def addstr(self, yposition, xposition, string, color = None, font=None, dx=0, dy=0, layer=None):
		if layer is None:
			terminal.layer(self.layer)
		else:
			terminal.layer(layer)

		#TODO: add color/bold/etc
		if color is not None:
			color = terminal.color_from_name(color)
			terminal.color(color)
		if font is None:
			terminal.printf(int(self.left + xposition), int(self.top + yposition),string)
		else:
			prefix = '[font={}][offset={},{}]'.format(font, dx, dy)
			postfix = '[/offset][/font]'
			terminal.printf(int(self.left + xposition), int(self.top + yposition),prefix + string + postfix)
			#terminal.put_ext(int(self.left + xposition), int(self.top + yposition), dx, dy, prefix + string + postfix)
		color = terminal.color_from_name("white")
		terminal.color(color)

	def addch(self, y, x, char, color = None, font=None, dx = 0, dy = 0):
		terminal.layer(self.layer)
		#TODO: add color/bold/etc
		if color is not None:
			color = terminal.color_from_name(color)
			terminal.color(color)
		if font is None:
			terminal.printf(int(self.left + x), int(self.top + y),char)
		else:
			prefix = '[font={}][offset={},{}]'.format(font, dx, dy)
			postfix = '[/offset][/font]'
			terminal.printf(int(self.left + x), int(self.top + y),prefix + char + postfix)

		#terminal.put(self.left + x, self.top + y, char)
		color = terminal.color_from_name("white")
		terminal.color(color)

	def getch(self):
		terminal.layer(self.layer)
		return terminal.read()

	def getmousepos(self):
		mx = terminal.state(terminal.TK_MOUSE_X)
		my = terminal.state(terminal.TK_MOUSE_Y)
		
		top = self.top
		left = self.left
		width = self.width
		height = self.height

		spacing = self.spacing

		mx1 = mx - left
		my1 = my - top

		mx2 = mx1 // spacing[0]
		my2 = my1 // spacing[1]

		if mx1 >= 0 and mx1 < width and my1 >= 0 and my1 < height: # height/width are in absolute units
			return (mx2, my2)



#TODO: add a "helptext" function where you can hit "?" on a menu to get more
# information on the entry you've selected before going back to the menu right
# where you left off.  Some items could even give better help info (on monsters, etc...)
def menu(window, options, cols = 2, selected = None, clear=True, callback_on_change=None, opaque=False):

	for opt_id in range(len(options)):
		if selected == options[opt_id]:
			selected = opt_id
			break
	else:
		selected = 0

	# offset is how far into the list the top-left
	# item is as we scroll through it.
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
		window.box(opaque)
		count = 0
		col = 0
		row = 0
		for option in options:
			yposition = 1 + row - offset
			xposition = 1 + col * colgap
			if (yposition <= (ymax - 2)) and (yposition >= 1):
				if count == selected:
					selected_row = row
					color = SELECTEDCOLOR
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
		elif key in keys.SELECT or key == terminal.TK_MOUSE_LEFT:
			loop = False
			#sys.exit(key)
		elif key == terminal.TK_BACKSPACE or key == terminal.TK_MOUSE_RIGHT:
			#sys.exit(key)
			if clear:
				window.erase()
			return None #escape key
		elif key == terminal.TK_MOUSE_MOVE:
			mousepos = window.getmousepos()
			if mousepos is not None:
				mx, my = mousepos
				#we may have to do something here with scrolling
				if mx > 0 and my > 0:
					#because we're counting wide rows here, we need to add 1
					#since the leftmost border is part of the first row. and is 0
					mcolumn = int(mx / colgap) + 1
					#we don't have to do that here since the first row is 0 but
					#is a border so it doesn't matter.
					mrow = my
					item_no = int(cols * (mrow - 1) + mcolumn - 1)
					if item_no < len(options):
						selected = item_no

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
	if selected < len(options):
		if clear:
			window.erase()
		return options[selected]
	else:
		if clear:
			window.erase()
		return None

	if clear:
		window.erase()


MAX_COMBATANTS = 3

class Display(object):
	def __init__(self, game=None, enemy=None):

		XMAX, YMAX = TERMSIZE


		self.statboxsize = [12, int(XMAX/MAX_COMBATANTS)]
		self.charboxsize = (int(YMAX / MAX_COMBATANTS), 40)
		self.msgboxsize = [12, int(XMAX - 2*self.charboxsize[1])]
		self.btl_msgboxsize = [24, int(XMAX - 2*self.charboxsize[1])]
		self.splashbox = None
		self.charboxes = []
		self.nmeboxes = []
		for i in range(MAX_COMBATANTS):
			charbox = Window(self.charboxsize[0],self.charboxsize[1],self.charboxsize[0]*i,0, 1) 
			nmebox = Window(self.charboxsize[0],self.charboxsize[1],self.charboxsize[0]*i,XMAX - self.charboxsize[1], 1) 
			self.nmeboxes.append(nmebox)
			self.charboxes.append(charbox)
		self.msgbox   = Window(self.msgboxsize[0],self.msgboxsize[1],YMAX-self.msgboxsize[0],self.charboxsize[1], 1)
		self.btl_msgbox   = Window(self.btl_msgboxsize[0],self.btl_msgboxsize[1],YMAX-self.btl_msgboxsize[0],self.charboxsize[1], 1)
		self.battlemenubox   = Window(self.msgboxsize[0],self.msgboxsize[1],YMAX-self.msgboxsize[0] - self.btl_msgboxsize[0],self.charboxsize[1], 1)

		self.overworldbox = Window(self.charboxsize[0] + 1,self.charboxsize[1],0,XMAX - self.charboxsize[1], 1) 

		MENUHEIGHT = 10
		MENUWIDTH = 20
		self.menubox = Window(MENUHEIGHT,MENUWIDTH,YMAX / 2 - MENUHEIGHT,XMAX / 2 - MENUWIDTH, 1) 

		self.enemy = enemy

		self.mapbox = Window(YMAX - self.msgboxsize[0], XMAX - 2*self.charboxsize[1], 0, self.charboxsize[1], 0)
		self.mapbox.spacing = [2,1]

		self.popupbox = Window(self.charboxsize[0] - 5, self.charboxsize[1], YMAX / 2 - self.charboxsize[0] / 2, XMAX / 2 - self.charboxsize[1] / 2, 2)
		self.popupbox_menu = Window(5, self.charboxsize[1], (YMAX / 2 - self.charboxsize[0] / 2) + self.charboxsize[0] - 5, XMAX / 2 - self.charboxsize[1] / 2, 2)

		self.zone = None

		self.x = 0
		self.y = 0

		self.statbox = []
		for i in range(MAX_COMBATANTS):
			self.statbox.append(Window(self.statboxsize[0],self.statboxsize[1],0,self.statboxsize[1]*i, 1))

		self.startmenusize = (int((YMAX) / MAX_COMBATANTS), int((XMAX - 1) / MAX_COMBATANTS))
		self.start_menus = []
		for i in range(MAX_COMBATANTS):
			classbox = Window(self.startmenusize[0],self.startmenusize[1],self.startmenusize[0]*i,self.startmenusize[1]*0, 1)
			elementbox = Window(self.startmenusize[0],self.startmenusize[1],self.startmenusize[0]*i,self.startmenusize[1]*1, 1) 
			confirmbox = Window(self.startmenusize[0],self.startmenusize[1],self.startmenusize[0]*i,self.startmenusize[1]*2, 1) 
			self.start_menus.append(classbox)
			self.start_menus.append(elementbox)
			self.start_menus.append(confirmbox)

		self.storemenusize = ((YMAX - 1 - self.msgboxsize[0]), int((XMAX -1) / 3))
		self.storebox = Window(self.storemenusize[0], self.storemenusize[1],0,0, 1)
		self.storeinfobox = Window(self.storemenusize[0], self.storemenusize[1],0,self.storemenusize[1], 1)

		self._mode = MAP

		self.refresh_full()

		#self.storebox
		#self.storeinfobox
		#self.charboxes

	def getch(self):
		return terminal.read()

	def text_entry(self, win=None, string=None, history=None):
		#TODO: text entry box
		if win is None:
			win = Window(2, TERMSIZE[0], 1, 1, 2)
		if string is None:
			string = ''
		history_position = 0

		while True:
			win.erase()
			win.box()
			printstring = string.replace('[', '[[')
			printstring = printstring.replace(']', ']]')
			printstring = printstring.replace('{', '{{')
			printstring = printstring.replace('}', '}}')
			terminal.printf(int(2),int(2), printstring)
			terminal.refresh()
			key = terminal.read()
			if key in [terminal.TK_RETURN]:
				return string
			elif key in [terminal.TK_ESCAPE, terminal.TK_CLOSE]:
				return None
			elif key in [terminal.TK_BACKSPACE]:
				if len(string) > 0:
					string = string[:-1]
			elif terminal.check(terminal.TK_CHAR):
				newchar = chr(terminal.state(terminal.TK_CHAR))
				if newchar == '`' and len(string) == 0:
					return None
				string += newchar
			elif history is not None:
				if terminal.check(terminal.TK_UP):
					if history_position < len(history):
						history_position += 1
						string = history[-history_position]
				elif terminal.check(terminal.TK_DOWN):
					if history_position > 1:
						history_position -= 1
						string = history[-history_position]
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

	def menu(self, options, window=None, cols = 1, selected = None, clear=True, callback_on_change=None):
		
		if window is None:
			window = self.msgbox
		return menu(window, options, cols, selected, clear, callback_on_change)

	def flash_screen(self):
		font = 'tiles{}'.format(ANIMATION_FRAME)
		dx = -4
		dy = 6
		y = 0
		x = 0
		allcoords = []
		for line in self.zone.map:
			for column in line:
				allcoords.append((x, y))
				x += 1
			y += 1
			x = 0
		random.shuffle(allcoords)
		popped = 0
		for x, y in allcoords:
			self.mapbox.addch(y, 2*x, '\x15', None, font=font, dx=dx, dy=dy)
			popped += 1
			if popped > 40:
				popped = 0
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
		#self.msgbox.erase()
		self.msgbox.box(opaque=True)
		for i in range(len(msgs)):
			self.msgbox.addstr(self.msgboxsize[0] - 2 - i, 1, msgs[i])
		terminal.refresh()
	
	def show_btl_messages(self):
		msgs = sys.stdout.readlines(self.btl_msgboxsize[0] - 2)
		self.btl_msgbox.erase()
		self.btl_msgbox.box()
		for i in range(len(msgs)):
			self.btl_msgbox.addstr(self.btl_msgboxsize[0] - 2 - i, 1, msgs[i])
		terminal.refresh()



	##################################
	##### Combat Draw Routines
	##################################

	def end_battle(self):
		self.enemy = None
		self.mode = MAP
		self.clear()
		self.refresh_full
	def start_battle(self, enemy):
		self.enemy = enemy
		self.mode = COMBAT
		self.clear()
		self.refresh_full

	def refresh_full_combat(self):
		for i in range(MAX_COMBATANTS):
			if i < len(self.game.player.combatants):
				self.show_combatant_stats(self.game.player.combatants[i], self.charboxes[i])
			else:
				self.charboxes[i].erase()
				self.charboxes[i].box()
			if i < len(self.enemy.combatants):
				self.nmeboxes[i].box()
		self.refresh_combatant()
		#self.msgbox.box()
	def battlemenu(self, options, cols=1, selected=None):
		window = self.battlemenubox
		return menu(window, options, cols, selected)

	#def menu(self, options, cols = 1, selected = None):
		#window = self.msgbox
		#return menu(window, options, cols, selected)

	def refresh_combatant(self):
		for i in range(MAX_COMBATANTS):
			if i < len(self.game.player.combatants):
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
		dx = -4
		dy = 6
		self.mapbox.erase()
		if self.zone is None:
			return

		font = 'tiles'
		if settings.animate:
			font = 'tiles{}'.format(ANIMATION_FRAME)
		update_animation_frame()

		i = 1
		for line in self.zone.map:
			self.mapbox.addstr(i, 1, line, font=font, dx = dx, dy = dy)
			i += 1


		if settings.fog:
			i = 1
			fog = maptools.flatten(self.zone.fog)
			for line in fog:
				self.mapbox.addstr(i, 1, line, font=font, dx = dx, dy = dy, layer = self.mapbox.layer + 1)
				i += 1

		drawn = set()
		entity_list = sorted(self.zone.entities, key=lambda x:x.priority)
		terminal.composition(True)
		for e in entity_list:
			if (e.x, e.y) not in drawn:
				if e.x is not None:
					try:
						self.mapbox.addch(YRAT * e.y + 1,XRAT * e.x + 1, e.char, None, font=font, dx=dx, dy=dy)
					except:
						print ('{} {} {}'.format(e.y + 1, e.x + 1, e.char))
					drawn.add((e.x + 1, e.y + 1))


		if self.game.player is not None:
			self.mapbox.addch(YRAT * self.game.player.y + 1, XRAT * self.game.player.x + 1, self.game.player.char, None, font=font, dx=dx, dy=dy)
		terminal.composition(False)

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

		#self.msgbox.box()
		#self.show_messages()

	def show_overworld(self):
		#show the overworld minimap
		biome_colors = ['#08B3E5', '#14C9CB', '#2AF598', '#d2b48c', '#006400', '#654321', 'white', 'white', 'white']
		y = 1
		for line in self.game.overworld_minimap:
			x = 1
			for cell in line:
				#biome_index = self.game.biome_map[16 - x][16 - y]
				biome_index = self.game.biome_map[y - 1][x - 1]
				try:
					biome_color = biome_colors[biome_index]
				except:
					print('index error: {}'.format(biome_index))
					biome_color = 'yellow'
				self.overworldbox.addstr(17 - y, x, str(cell), biome_color)
				x += 1
			y += 1
		x0 = 16 - self.game.overworld_x
		y0 = self.game.overworld_y + 1
		self.overworldbox.addch(x0, y0, '@')

		#show game stats
		try:
			self.overworldbox.addstr(1, 18, 'Biome: {}'.format(str(self.game.biome())))
			self.overworldbox.addstr(2, 18, 'Gold: {}'.format(str(self.game.player.backpack.gold)))
			self.overworldbox.addstr(3, 18, 'Alters: {}'.format(str(len(self.game.get_var('Alters')))))
			self.overworldbox.addstr(4, 18, 'Turn: {:,}'.format(self.game.ticks))
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
				self.show_combatant_stats(self.game.player.combatants[i],self.statbox[i])

		#self.msgbox.box()

	def show_combatant_stats(self, combatant, box):
		col2pos = 20
		box.erase()
		box.box(opaque=True)
		height, width = box.getmaxyx()
		
		#Name
		color = "white"
		if self.game.player is not None:
			if combatant == self.game.player.combatant:
				color = SELECTEDCOLOR

		box.addstr(0, 1, '{}  (Level {})'.format(combatant.name, combatant.level), color)
		#HP
		box.addstr(1, 1, progress_bar(combatant.hp, combatant.max_hp, width - 2), None)
		box.addstr(2, 1, 'HP: {} / {}'.format(int(math.ceil(combatant.hp)),int(math.ceil(combatant.max_hp))), None)
		
		#Experience
		box.addstr(3, 1, 'Exp: {} / {}'.format(int(combatant.exp), int(combatant.exp_at_level(combatant.level + 1))))


		#physical
		box.addstr(4, 1, "Physical Atk.: {:3}   Def.: {:3}".format(int(combatant.physical_strength), int(combatant.physical_defense)), None)
		#box.addstr(4, 1, "P. Atk.: {}".format(int(combatant.physical_strength)), None)
		#box.addstr(5, 1, "P. Def.: {}".format(int(combatant.physical_defense)), None)

		#arcane
		box.addstr(5, 1, "Arcane   Atk.: {:3}   Def.: {:3}".format(int(combatant.arcane_strength), int(combatant.arcane_defense)), None)
		#box.addstr(6, 1, "S. Atk: {}".format(int(combatant.arcane_strength)), None)
		#box.addstr(7, 1, "S. Def: {}".format(int(combatant.arcane_defense)), None)

		#speed
		box.addstr(6, 1, "Speed: {}           Luck: {}".format(int(combatant.speed), int(combatant.luck)), None)
		#box.addstr(6, 1, "Speed: {}".format(int(combatant.speed)), None)

		#elements
		element_list = ' '.join([str(element) for element in combatant.elements])
		box.addstr(7, 1, "Elements: {}".format(element_list), None)
		#box.addstr(9, 1, "Elements: {}".format(element_list), None)

		box.addstr( 8, 1, "Head : {}".format(combatant.equipment.Head), None)
		box.addstr( 9, 1, "Body : {}".format(combatant.equipment.Body), None)
		box.addstr(10, 1, "Token: {}".format(combatant.equipment.Token), None)

		#box.addstr(10, 1, "Head: {}".format(combatant.equipment.Head), None)
		#box.addstr(11, 1, "Body: {}".format(combatant.equipment.Body), None)
		#box.addstr(12, 1, "Token: {}".format(combatant.equipment.Token), None)
		if combatant.equipment.Hands is None:
			box.addstr(11, 1, "Left : {}".format(combatant.equipment.Left), None)
			box.addstr(12, 1, "Right: {}".format(combatant.equipment.Right), None)
			#box.addstr(13, 1, "Left: {}".format(combatant.equipment.Left), None)
			#box.addstr(14, 1, "Right: {}".format(combatant.equipment.Right), None)
		else:
			box.addstr(11, 1, "Hands: {}".format(combatant.equipment.Hands), None)
			#box.addstr(13, 1, "Hands: {}".format(combatant.equipment.Hands), None)

		if len(combatant.status) == 0:
			stat_list = 'None'
		else:
			stat_list = ' '.join([str(stat) for stat in combatant.status])
		box.addstr(13, 1, "Status: {}".format(stat_list), None)
		#box.addstr(15, 1, "Status: {}".format(stat_list), None)




	##################################
	##### Start Menu Draw Routines
	##################################
	def refresh_full_startmenu(self):
		for box in self.start_menus:
			box.box()


	##################################
	##### Start Popup Draw Routines
	##################################
	
	def popup(self, message, choices = None, selected=None, cols=2):
		if choices is None:
			choices = [True, False]

		self.popupbox.erase()
		self.popupbox.box(True)
		self.popupbox.addstr(1, 1, message)
		#self.popupbox_menu.erase()
		self.popupbox_menu.box(True)
		return menu(self.popupbox_menu, choices, cols, selected, opaque=True)



	##################################
	##### Start Shop Draw Routines
	##################################
	def refresh_full_shop(self):
		self.storebox.box()
		self.storeinfobox.box()
		for box in self.charboxes:
			box.box()

	def display_item_stats(self, item, backpack = None, cost_mult = 1.0):
		self.storeinfobox.box(opaque=True)
		self.storeinfobox.addstr(0, 1, item.name)
		if backpack is not None:
			self.storeinfobox.addstr(1, 1, 'In Backpack: {}'.format(backpack.qty(item.name)))
		self.storeinfobox.addstr(2, 1, 'Cost: {} ({} in backpack)     '.format(item.cost() * cost_mult, self.game.player.backpack.gold))
		self.storeinfobox.addstr(3, 1, 'Desc: {}'.format(item.helptext()))

	def splash_screen(self):
		terminal.clear()
		with open('data/splash3.txt') as f:
		#with open('data/Splash.txt') as f:
			splash_data = f.readlines()
		width, height = TERMSIZE
		#width = len(splash_data[1])
		self.splashbox = Window(height,width,0,0,0) 
		splashbox = self.splashbox
		splashbox.box()

		for y, line in enumerate(splash_data):
			splashbox.addstr(y + 1, 1, line)

		terminal.refresh()

	def update_generation_progress(self, percent):
		splashbox = self.splashbox
		splashbox.addstr(y+6, 1, str(percent))


	def show_txt(self, filename):
		terminal.clear()
		with open(filename) as f:
			txt_data = f.readlines()
		width, height = TERMSIZE
		txtbox = Window(height,width,0,0, 0) 

		for y, line in enumerate(txt_data):
			txtbox.addstr(y + 1, 1, line)

		txtbox.addstr(y+5, 1, 'Press any key to exit...')
		txtbox.box()
		terminal.refresh()
		terminal.read()


	def game_over(self):
		terminal.clear()
		with open('data/GameOver.txt') as f:
			splash_data = f.readlines()
		width, height = TERMSIZE
		splashbox = Window(height,width,0,0, 0) 

		for y, line in enumerate(splash_data):
			splashbox.addstr(y + 1, 1, line)

		splashbox.addstr(y+5, 1, 'Press any key to exit...')
		splashbox.box()
		terminal.refresh()
	
	def loading_progress(self, current, max):
		bar = progress_bar(current, max, TERMSIZE[0] - 2)
		terminal.printf(int(1),int(TERMSIZE[1] - 1), bar)
		terminal.refresh()


	def settingsmenu(self, music_queue):
		settingmenu = True
		while settingmenu:
			if settings.fog:
				if settings.fog_old:
					fogoption = 'Fog (on - current)'
				else:
					fogoption = 'Fog (on - unseen)'
			else:
				fogoption = 'Fog (off)'

			if settings.music:
				musicoption = 'Music (on)'
			else:
				musicoption = 'Music (off)'

			if settings.battle_anim:
				batan_opt = 'Battle Anim.(on)'
			else:
				batan_opt = 'Battle Anim.(off)'



			setting = menu(self.menubox, [musicoption, fogoption, batan_opt, 'Exit'] , cols=1, clear=False)
			if setting == musicoption:
				if settings.music == 1:
					music_queue.put(['volume', 0])
					settings.music = False
					print('Music is now off')
				else:
					music_queue.put(['volume', 1])
					settings.music = True
					print('Music is now on')
				self.show_messages()

			elif setting == fogoption:
				if settings.fog:
					if settings.fog_old:
						settings.fog_old = False
					else:
						settings.fog = False
				else:
					settings.fog = True
					settings.fog_old = True
			elif setting == batan_opt:
				settings.battle_anim = not settings.battle_anim
			else:
				settingmenu = False
		settings._save()


#TODO: work this into the object
def shutdown():
	terminal.close()
	sys.stdout = original_stdout



