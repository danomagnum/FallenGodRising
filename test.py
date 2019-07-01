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

def dotestbattle(user, display, level=50):

	sys.stdout.silent = True
	battleenemy = characters.Page(level=(level+2))
	battleenemy2 = characters.Cleric(level=(level-2))
	battleenemy3 = characters.Fighter(level=(level-3))

	enemy = battle.Random_AI([battleenemy,battleenemy2,battleenemy3])

	sys.stdout.silent = False
	display.flash_screen()
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
		user = characters.gen_testuser()
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
						item_target_type = item_slot_used.target_type
						if item_target_type == SELF:
							item_target = [display.menu(user.combatants, cols=2)]
						elif item_target_type == MULTI_SELF:
							item_target = user.combatants
						elif item_target_type in EQUIPPABLE:
							pass
						else:
							print("Can't Use that now")
						if item_target is not None:
							item_used = item_slot_used.take()
							selection_needed = False
							for t in item_target:
								item_used.use(t)


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
