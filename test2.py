import sys

sys.dont_write_bytecode = True

import characters
import battle
import main
import curses_interface as graphics_interface
#import pygcurses_interface as graphics_interface
import time
import items
import keys
import entities
import elements
from constants import *

import random
import maps.overworld
WRITEMAP = True

try:
	if __name__ == '__main__':
		graphics_interface.initialize()
		game = main.Game()
		zone, biome_map, overworld_minimap = maps.overworld.genzone(game)
		game.biome_map = biome_map
		game.overworld_minimap = overworld_minimap
		game.overworld = zone
		if WRITEMAP:
			file = open('mapout.txt', 'w')
			for y in range(15, -1, -1):
				for mapline in range(len(zone.maps[0])):
					megaline = ''
					for x in range(16):
						mapid = y * 16 + x
						map = zone.maps[mapid]
						megaline += zone.maps[mapid][mapline]
					file.write(megaline)
					file.write('\n')

			file.close()


		#user = characters.gen_testuser()
		#user.x, user.y = zone.find_empty_position()

		display = graphics_interface.Display(game, zone=zone)
		game.display = display
		#zone.display = display

		#zone.set_player(user)

		loop = True
		display.mode = graphics_interface.STARTMENU
		i = 0
		##########################
		# Let player select their party
		##########################
		player_party = [None, None, None]
			
		while loop:
			if i >= graphics_interface.MAX_COMBATANTS:
				i = 0
			player_characters = [characters.Fighter(game), characters.Wizard(game), characters.Cleric(game), characters.Knight(game), characters.Paladin(game), characters.Rogue(game), characters.Dragoon(game), characters.Juggernaut(game), characters.Battlemage(game), characters.Nightblade(game), characters.Witchhunter(game), characters.Debug(game)]


			def update_confirm_box(choice):
				display.show_combatant_stats(choice, display.start_menus[(i * 3) + 2])

			update_confirm_box(player_characters[0])
			player_choice = graphics_interface.menu(display.start_menus[i * 3], player_characters,selected=random.choice(player_characters) ,clear=False, callback_on_change=update_confirm_box)

			if player_choice is not None:
				player_elements = [elements.Normal, elements.Fire, elements.Water, elements.Earth, elements.Electric, elements.Wind, elements.Light, elements.Dark]
				def update_confirm_box(choice):
					player_choice.elements = []
					player_choice.elements.append(choice)
					display.show_combatant_stats(player_choice, display.start_menus[(i * 3) + 2])

				element_choice =graphics_interface.menu(display.start_menus[(i * 3) + 1], player_elements, selected=random.choice(player_elements), clear=False, callback_on_change=update_confirm_box)

				#confirm_choices = ['Accept', 'Cancel', 'Randomize']
				#confirm_choice = graphics_interface.menu(display.start_menus[(i * 3) + 2], confirm_choices, clear=False)
				if element_choice is not None:
					player_choice.elements = []
					player_choice.elements.append(element_choice)
					player_party[i] = player_choice
					i += 1
					if i == graphics_interface.MAX_COMBATANTS:
						item_list = [items.gen_base_item(game) for x in range(4)]
						item_list += [items.gen_gear(game, level=1) for x in range(4)]
						item_list += [items.gen_movescroll(game) for x in range(4)]
						user = main.Entity('playercharacter', game, combatants=player_party, item_list=item_list, char='@',is_player=True)
						#user.combatants = player_party
						user.x, user.y = zone.find_empty_position()
						user.backpack.gold = 100
						zone.set_player(user)
						display.user = user
						game.player = user
						loop = False
			else:
				if i > 0:
					i -= 1


		##########################
		# Main Game Loop
		##########################
		display.mode = graphics_interface.MAP
		loop = True
		while loop:
			key = display.mapbox.getch()
			##########################
			# Player movement
			##########################
			if key in keys.UP:
				user.move(zone, UP)
			elif key in keys.DOWN:
				user.move(zone, DOWN)
			elif key in keys.LEFT:
				user.move(zone, LEFT)
			elif key in keys.RIGHT:
				user.move(zone, RIGHT)

			##########################
			# Player menu
			##########################
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
					item_target = None
					if item_slot_used is not None:
						item_target_type = item_slot_used.target_type
						if item_target_type == SELF:
							item_target = [display.menu(user.combatants, cols=2)]
						elif item_target_type == MULTI_SELF:
							item_target = user.combatants
						elif item_target_type in EQUIPPABLE:
							item_target = [display.menu(user.combatants, cols=2)]
						else:
							print("Can't Use that now")
						if item_target is not None:
							item_used = item_slot_used.take()
							selection_needed = False
							for t in item_target:
								item_used.use(t)


			elif key == ord('k'):
				#up
				zone.exit(game.player, UP)
			elif key == ord('j'):
				zone.exit(game.player, DOWN)
				#down
			elif key == ord('h'):
				zone.exit(game.player, LEFT)
				#left
			elif key == ord('l'):
				zone.exit(game.player, RIGHT)
				#right
			##########################
			# Player did nothing
			##########################
			elif key == ord('`'):
				#print(game.display.mapbox.getmaxyx())
				#game.player.combatants[0].level += 1
				console = display.text_entry()
				try:
					game.debug(console)
				except Exception as e:
					print(e.message)
			zone.tick()
			display.show_messages()
			display.refresh_full()

except Exception as e:
	graphics_interface.shutdown()
	raise



time.sleep(3)

graphics_interface.shutdown()

sys.exit(0)
