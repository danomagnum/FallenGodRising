import characters
import sys
import battle
import curses_interface
import time

curses_interface.initialize()

battleuser = characters.TestChar2()
battleenemy = characters.TestChar()
battleenemy2 = characters.TestChar()

battleuser.name = 'my comb'
battleuser.level = 55
battleuser.heal()

battleenemy.name = 'enemy comb'
battleenemy.level = 52
battleenemy.heal()

battleenemy2.name = 'enemy comb 2'
battleenemy2.level = 11
battleenemy2.heal()



junk = sys.stdout.readlines()

battledisplay = curses_interface.curses_display(battleuser, battleenemy)

battle.Battle([battleuser], [battleenemy,battleenemy2], battledisplay, battle.Random_AI())

time.sleep(3)

curses_interface.shutdown()

sys.exit(0)
