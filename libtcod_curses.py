import libtcodpy as libtcod
SCREEN_WIDTH = 211
SCREEN_HEIGHT = 54
LIMIT_FPS = 20



class curses_window(object):
	def __init__(self, height, width, y0, x0):
		self.con = libtcod.console_new(width, height)
		self.width = width
		self.height = height
		self.y = y0
		self.x = x0

	def box(self):
		libtcod.console_print_frame(self.con,0, 0, self.width, self.height, clear=True, flag=BKGND_DEFAULT, fmt=0)
	def refresh(self):
		#update the window on screen
		libtcod.console_blit(self.con, 0, 0, self.width, self.height, 0, self.x0, self.y0)
		libtcod.console_flush()

	def addstr(self, y, x, text):
		# print a string starting at location y,x
		libtcod.console_print(self.con, x, y, text)

	def overlay(self, screen):
		libtcod.console_blit(self.con, 0, 0, self.width, self.height, 0, self.x0, self.y0)
		#pass
	def keypad(self, index):
		pass
	def getmaxyx(self):
		return (self.height, self.width)
	def getbegyx(self):
		return (self.y, self.x)
	def clear(self):
		libtcod.console_clear(self.con)
	def getch(self):

		#libtcod.sys_wait_for_event(eventMask,key,mouse,flush)
		pass # returns a character
	def addch(self, y, x, char):
		libtcod.console_put_char(self.con, x, y, char, libtcod.BKGND_NONE)


class curses_pad(curses_window):
	pass

class Curses(object):
	COLOR_BLACK = (0, 0, 0);
	COLOR_WHITE = (255, 255, 255);
	COLOR_YELLOW = (0, 255, 255);
	COLOR_RED = (255, 0, 0);
	COLOR_BLUE = (0, 0, 255);
	def initscr(self):
		#gets screen ready to go

		libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD, 0, 0)
		libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False, None)
		libtcod.sys_set_fps(LIMIT_FPS)
		libtcod.console_set_default_foreground(0, libtcod.white)


		#returns the main screen object
		return self
	def start_color(self):
		pass # allows use of color?
	def init_pair(self, index, color0, color1):
		pass
	def noecho(self):
		#turns of printing to the screen
		pass # returns nothing
	def color_pair(self, index):
		#select a color index
		pass # returns a color
	def curs_set(self, old_cursor):
		#sets the cursor position
		pass#returns nothing.
	def newwin(self, height, width, y0, x0):
		return curses_window(height, width, y0, x0)
	def newpad(self, height, width):
		return curses_window(height, width, 0, 0)
	def flash(self):
		#supposed to invert all colors on the screen
		#then turn them back
		pass # returns nothing
	def endwin(self):
		#closes curses and goes back to a regular term
		pass # returns nothing

	def keypad(self, index):
		pass
	def getmaxyx(self):
		return (self.height, self.width)
