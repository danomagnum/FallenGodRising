import sys

sys.dont_write_bytecode = True

import characters
import battle
import main
import curses_interface as graphics_interface
#import pygcurses_interface as graphics_interface
import time
import items
import overworld
import keys
import entities
import elements
from constants import *

import maps.testmap

try:
	if __name__ == '__main__':
		graphics_interface.initialize()
		zone = maps.testmap.zone

		user = characters.gen_testuser()
		user.x, user.y = zone.find_empty_position()

		display = graphics_interface.Display(zone=zone)
		zone.display = display

		zone.set_player(user)

		display.user = user
		loop = True
		display.mode = graphics_interface.STARTMENU
		i = 0
		player_party = [None, None, None]
		while loop:
			if i >= graphics_interface.MAX_COMBATANTS:
				i = 0
			player_characters = [characters.Fighter(), characters.Wizard(), characters.Cleric(), characters.Knight(), characters.Paladin(), characters.Rogue(), characters.Dragoon(), characters.Juggernaut(), characters.Battlemage(), characters.Nightblade(), characters.Spellsword(), characters.Witchhunter()]
			player_choice = graphics_interface.menu(display.start_menus[i * 3], player_characters, clear=False)

			player_elements = [elements.Normal, elements.Fire, elements.Water, elements.Earth, elements.Electric, elements.Wind, elements.Light, elements.Dark]
			element_choice =graphics_interface.menu(display.start_menus[(i * 3) + 1], player_elements, clear=False)

			confirm_choices = ['Accept', 'Cancel', 'Randomize']
			confirm_choice = graphics_interface.menu(display.start_menus[(i * 3) + 2], confirm_choices, clear=False)
			if confirm_choice == 'Accept':
				player_choice.elements.append(element_choice)
				player_party[i] = player_choice
				i += 1
				if i == graphics_interface.MAX_COMBATANTS:
					user.combatants = player_party
					loop = False


		display.mode = graphics_interface.MAP
		loop = True
		while loop:
			key = display.mapbox.getch()
			if key in keys.UP:
				user.move(zone, UP)
			elif key in keys.DOWN:
				user.move(zone, DOWN)
			elif key in keys.LEFT:
				user.move(zone, LEFT)
			elif key in keys.RIGHT:
				user.move(zone, RIGHT)
			elif key == ord('m'):
				#Menu
				choice = display.menu(['Battlers', 'Quests', 'Transport', 'Save', 'Options', 'Items'], 4)
				if choice == 'Battlers':
					display.mode=graphics_interface.STATS
					display.refresh_full()
					key = display.mapbox.getch()
					display.mode=graphics_interface.MAP
					display.refresh_full()
				elif choice == 'Quests':
					pass

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
				pass
			zone.tick()
			display.show_messages()
			display.refresh_full()

except Exception as e:
	graphics_interface.shutdown()
	raise e



time.sleep(3)

graphics_interface.shutdown()

sys.exit(0)