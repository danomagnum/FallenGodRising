import curses
import sys
import os
import time

import characters
import battle

a = characters.TestChar()
b = characters.TestChar()

damage = []

a.name = 'my mon'
a.level = 50
b.name = 'enemy mon'
b.level = 52
a.heal()
b.heal()
a.moves[0].mp = 1


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



screen.keypad(1)
YMAX, XMAX = screen.getmaxyx()
curses.noecho()

#newwin is numlines, numcols, line0, col0
monboxsize = [5, 20]
msgboxsize = [5, XMAX]
nmebox = curses.newwin(monboxsize[0],monboxsize[1],0,0)
mybox = curses.newwin(monboxsize[0],monboxsize[1],YMAX-(monboxsize[0] + 5),XMAX-monboxsize[1])

msgbox   = curses.newwin(msgboxsize[0],msgboxsize[1],YMAX-msgboxsize[0],0)

nmebox.box()
mybox.box()
msgbox.box()
nmebox.overlay(screen)
mybox.overlay(screen)
msgbox.overlay(screen)
screen.refresh()

loop = True

screen.clear()
nmebox.overlay(screen)
mybox.overlay(screen)
msgbox.overlay(screen)
screen.refresh()

def progress_bar(actual, maxvalue, length):
	percent = float(actual) / float(maxvalue)
	filled = int(percent * length)
	unfilled = length - filled
	filled_char = '_'
	unfilled_char = ' '
	return filled_char * filled + unfilled_char * unfilled


while loop:
	screen.clear()
	mybox.clear()
	mybox.box()

	nmebox.clear()
	nmebox.box()

	msgbox.clear()
	msgbox.box()


	#display my pokemon's info
	mybox.addstr(0, 1, a.name)
	mybox.addstr(1, 1, progress_bar(a.hp, a.max_hp, monboxsize[1] - 2), curses.color_pair(1))
	mybox.addstr(2, 1, str(a.hp) + ' / ' + str(a.max_hp), curses.color_pair(11))
	mybox.addstr(3, 1, progress_bar(a.exp, a.exp_to_next_level(), monboxsize[1] - 2), curses.color_pair(4))

	nmebox.addstr(0, 1, 'nmemonname')

	screen.clear()
	nmebox.overlay(screen)
	mybox.overlay(screen)
	msgbox.overlay(screen)
	screen.refresh()
	time.sleep(10)

curses.endwin()

sys.exit(0)
