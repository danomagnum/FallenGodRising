import curses
import sys
import os
import time
import random
import math

import stdoutCatcher
from StringIO import StringIO

import characters
#import battle

user = characters.TestChar()
enemy = characters.TestChar()

damage = []

user.name = 'my mon'
user.level = 55
enemy.name = 'enemy mon'
enemy.level = 52
user.heal()
enemy.heal()
user.moves[0].mp = 1
#print '--------'
#print user.exp, user.exp_to_next_level()
#user.exp += 1900
#print user.exp
#sys.exit(0)


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

#sys.stdout = StringIO()
sys.stdout = stdoutCatcher.ioCatcher()

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
	filled_char = ' '
	unfilled_char = ''
	return filled_char * filled + unfilled_char * unfilled

def show_mon(mon, box, hideexp=False):
	box.clear()
	box.box()
	box.addstr(0, 1, mon.name)
	box.addstr(1, 1, progress_bar(mon.hp, mon.max_hp, monboxsize[1] - 2), curses.color_pair(1))
	box.addstr(2, 1, str(int(math.ceil(mon.hp))) + ' / ' + str(int(math.ceil(mon.max_hp))), curses.color_pair(11))
	if not hideexp:
		box.addstr(3, 1, progress_bar(mon.exp - mon.exp_to_current_level(), mon.exp_to_next_level() - mon.exp_to_current_level(), monboxsize[1] - 2), curses.color_pair(4))
	box.refresh()

messages = []
def message(*args):
	string = ''
	for arg in args:
		string += arg
	messages.appen(string)

def menu(options, window, cols = 1, selected = 0):
	old_cursor = curses.curs_set(0)
	loop = True
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
	while loop:
		window.clear()
		window.box()
		count = 0
		col = 0
		row = 0
		for text, action in options:
			yposition = 1 + row - offset
			xposition = 1 + col * colgap
			if (yposition <= (ymax - 2)) and (yposition >= 1):
				if count == selected:
					selected_row = row
					color = curses.color_pair(1)
				else:
					color = curses.color_pair(11)
				window.addstr(yposition, xposition, text, color)
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
	curses.curs_set(old_cursor)
	return options[selected][1]


def show_messages():
	for out in sys.stdout.readlines():
		if out.strip() != '':
			msgbox.addstr(1, 1, out)
			msgbox.refresh()
			key = msgbox.getch()
		msgbox.clear()
		msgbox.box()
		msgbox.refresh()




def refresh_mon():
	show_mon(user, mybox)
	show_mon(enemy, nmebox)


refresh_mon()

battle_continue = True

last_attack = 0

while battle_continue:

	need_selection = True
	window = curses.newwin(4, 40, 20, 10)
	attack_list = [(str(move), move) for move in user.moves]
	user_move = menu(attack_list, window, cols=2, selected=last_attack)

	for attack_number in xrange(len(attack_list)):
		if attack_list[attack_number][1] == user_move:
			last_attack = attack_number

	user_target = [user, enemy][user_move.default_target]

	enemy_move = random.choice(enemy.moves)
	enemy_target = [enemy, user][enemy_move.default_target]

	if user.speed >= enemy.speed:
		user_move.attack(user, user_target)
		refresh_mon()
		show_messages()
		if enemy.hp > 0:
			enemy_move.attack(enemy, enemy_target)
			refresh_mon()
			show_messages()
	else:
		enemy_move.attack(enemy, enemy_target)
		refresh_mon()
		show_messages()
		if user.hp > 0:
			user_move.attack(user, user_target)
			refresh_mon()
			show_messages()

	if enemy.hp == 0:
		battle_continue = False
		print enemy.name, 'fainted'
		exp = enemy.exp_value
		print user.name, 'gained', int(exp), 'xp. ', ((user.level+1) ** 3) - user.exp, 'to go'
		user.exp += exp
			
	if user.hp == 0:
		battle_continue = False
		print user.name, 'fainted'

	refresh_mon()

	show_messages()
	screen.refresh()
	time.sleep(1.0 / 60.0)


time.sleep(10)
curses.endwin()

sys.exit(0)
