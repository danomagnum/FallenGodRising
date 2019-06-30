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

def gen_testuser():
	sys.stdout.silent = True
	battleuser = characters.TestChar2()
	battleuser2 = characters.TestChar()

	battleuser.name = 'dude'
	battleuser.level = 55
	battleuser.full_heal()

	battleuser2.name = 'bloke'
	battleuser2.level = 50
	battleuser2.full_heal()
	battleuser2.hp -= 25

	user = main.User('playercharacter', combatants=[battleuser, battleuser2], item_list=[items.Potion(), items.Potion(), items.Booster()])

	sys.stdout.silent = False
	return user


def dotestbattle(user, display, level=50):

	sys.stdout.silent = True
	battleenemy = characters.TestChar()
	battleenemy2 = characters.TestChar2()

	battleenemy.name = 'chap'
	battleenemy.level = level + 2
	battleenemy.full_heal()

	battleenemy2.name = 'brah'
	battleenemy2.level = level + 2
	battleenemy2.full_heal()

	enemy = battle.Random_AI([battleenemy,battleenemy2])


	sys.stdout.silent = False
	battle.Battle(user, enemy , display)


try:
	if __name__ == '__main__':
		curses_interface.initialize()
		#zone = overworld.readmap('maps/test0.map')
		#zone = showmap(map_gen(40, 40, 10, 8))
		zone = overworld.Zone(None, 'maps/test0.map')
		x, y = zone.find_empty_position()
		zone.Player.x = x
		zone.Player.y = y
		display = curses_interface.curses_display(zone=zone)
		zone.display = display
		display.set_position(x, y)
		user = gen_testuser()
		display.user = user
		loop = True
		while loop:
			key = display.mapbox.getch()
			if key in keys.UP:
				zone.move(1)
			elif key in keys.DOWN:
				zone.move(2)
			elif key in keys.LEFT:
				zone.move(3)
			elif key in keys.RIGHT:
				zone.move(4)
			elif key == ord('m'):
				#Menu
				choice = display.menu(['Battlers', 'Info', 'Transport', 'Save', 'Stats', 'Options', 'Items'], 4)
				if choice == 'Battlers':
					display.mode=curses_interface.STATS
					display.refresh_full()
					key = display.mapbox.getch()
					display.mode=curses_interface.MAP
					display.refresh_full()

				elif choice == 'Items':
					item_slot_used = display.menu(user.backpack.show(), cols=2)
					if item_slot_used is not None:
						item_target = display.menu(user.combatants, cols=2)
						if item_target is not None:
							item_used = item_slot_used.take()
							item_used.use(item_target)

			elif key in keys.SELECT:
				#display.mode = curses_interface.COMBAT
				try:
					dotestbattle(user, display, 30)
				except main.GameOver:
					print("GameOver")
				display.mode = curses_interface.MAP
			display.show_messages()
			display.refresh_full()
except Exception as e:
	curses_interface.shutdown()
	raise e, None, sys.exc_info()[2]



time.sleep(3)

curses_interface.shutdown()

sys.exit(0)
