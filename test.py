import sys

sys.dont_write_bytecode = True

import characters
import battle
import main
import curses_interface
import time
import curses

curses_interface.initialize()

battleuser = characters.TestChar2()
battleuser2 = characters.TestChar()

battleenemy = characters.TestChar()
battleenemy2 = characters.TestChar()

battleuser.name = 'dude'
battleuser.level = 55
battleuser.heal()

battleuser2.name = 'bloke'
battleuser2.level = 50
battleuser2.heal()

battleenemy.name = 'chap'
battleenemy.level = 52
battleenemy.heal()

battleenemy2.name = 'brah'
battleenemy2.level = 48
battleenemy2.heal()

user = main.User('playercharacter', [battleuser, battleuser2])
enemy = battle.Random_AI([battleenemy,battleenemy2])


junk = sys.stdout.readlines()

#window = curses.newwin(30,5,10,0)
#curses_interface.menu(window, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
#sys.exit()

battle.Battle(user, enemy , curses_interface.curses_display)

time.sleep(3)

curses_interface.shutdown()

sys.exit(0)
