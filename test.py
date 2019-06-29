import sys

sys.dont_write_bytecode = True

import characters
import battle
import main
import curses_interface
import time
import items
import overworld
import keys



def dotestbattle(display):
	battleuser = characters.TestChar2()
	battleuser2 = characters.TestChar()

	battleenemy = characters.TestChar()
	battleenemy2 = characters.TestChar2()

	battleuser.name = 'dude'
	battleuser.level = 55
	battleuser.full_heal()

	battleuser2.name = 'bloke'
	battleuser2.level = 50
	battleuser2.full_heal()
	battleuser2.hp -= 25

	battleenemy.name = 'chap'
	battleenemy.level = 52
	battleenemy.full_heal()

	battleenemy2.name = 'brah'
	battleenemy2.level = 48
	battleenemy2.full_heal()

	user = main.User('playercharacter', combatants=[battleuser, battleuser2], item_list=[items.Potion(), items.Potion(), items.Booster()])
	enemy = battle.Random_AI([battleenemy,battleenemy2])


	battle.Battle(user, enemy , display)


try:
	if __name__ == '__main__':
		curses_interface.initialize()
		zone = overworld.readmap('maps/test0.map')
		#zone = showmap(map_gen(40, 40, 10, 8))
		x, y = overworld.find_valid_position(zone)
		display = curses_interface.curses_display(area_map=zone)
		display.set_position(x, y)
		loop = True
		while loop:
			key = display.mapbox.getch()
			if key in keys.UP:
				display.move(1)
			elif key in keys.DOWN:
				display.move(2)
			elif key in keys.LEFT:
				display.move(3)
			elif key in keys.RIGHT:
				display.move(4)
			elif key in keys.SELECT:
				display.mode = curses_interface.COMBAT
				testbtl.dotestbattle(display)
				display.mode = curses_interface.MAP

			display.refresh_full()
except Exception as e:
	curses_interface.shutdown()
	raise e, None, sys.exc_info()[2]



time.sleep(3)

curses_interface.shutdown()

sys.exit(0)
