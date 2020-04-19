#!/usr/bin/python
#coding: utf-8 
import sys
import traceback

sys.dont_write_bytecode = True

import characters
import battle
import main
import random

#import dill as pickle
import pickle

from os import listdir
from os.path import isfile, join
from version import *

#import curses_interface as graphics_interface
#import keys
import bearlib_interface as graphics_interface
import bearlibkeys as keys

import time
import items
import entities
import elements
from constants import *

import maps.overworld
import maps.goblincave
import maps.wizardtower
import maps.maptools
import maps.buildings
import maps.sewers

WRITEMAP = False

try:
	if __name__ == '__main__':
		graphics_interface.initialize()
		display = graphics_interface.Display()
		while True:

			display.mode = MAP
			display.splash_screen()
			print('Version: ' + version)
			display.show_messages()


			player_choice = graphics_interface.menu(display.menubox, ['New Game', 'Resume', 'Quit'] ,clear=False)
			if player_choice == 'Quit':
				graphics_interface.shutdown()
				sys.exit(0)
			elif player_choice == 'Resume':
				onlyfiles = [f for f in listdir(SAVEDIR) if (isfile(join(SAVEDIR, f)) and (f[-3:] == 'sav'))]	
				if onlyfiles:
					player_choice = graphics_interface.menu(display.menubox, onlyfiles ,clear=False)
					if player_choice is not None:
						try:
							f = open(join(SAVEDIR, player_choice), 'rb')
							game = pickle.load(f)
							display.game = game
							game.display = display
							display.change_zone(game.zone)
							f.close()
							#break
						except Exception as e:
							traceback.print_exc(file=sys.stderr)
							print("Error loading" + player_choice)
							display.show_messages()
				else:
					print('No Saves Detected')
					display.show_messages()

			elif player_choice == 'New Game':
				print('Please Wait, Generating Overworld...')
				display.show_messages()
				game = main.Game()
				zone, biome_map, overworld_minimap = maps.overworld.genzone(game)

				game.biome_map = biome_map
				game.overworld_minimap = overworld_minimap
				game.overworld = zone

				zone2 = maps.goblincave.genzone(game)
				zone3 = maps.wizardtower.genzone(game)
				zone4 = maps.sewers.genzone(game)


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

				display.game = game
				game.display = display
				display.change_zone(game.zone)
				#zone.display = display

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
								item_list = []
								item_list = [items.gen_base_item(game) for x in range(4)]
								item_list += [items.gen_gear(game, level=1) for x in range(4)]
								item_list += [items.gen_movescroll(game) for x in range(4)]
								amulet = items.Amulet(game)
								amulet = items.add_item_mod(amulet, items.OfRegen)
								item_list.append(amulet)

								user = main.Entity('playercharacter', game, combatants=player_party, item_list=item_list, char='@',is_player=True)
								#user.combatants = player_party
								user.x, user.y = zone.find_empty_position()
								user.backpack.gold = 100
								#zone.set_player(user)
								display.user = user
								game.player = user
								loop = False
					else:
						if i > 0:
							i -= 1
				#break


			##########################
			# Main Game Loop
			##########################
			display.mode = graphics_interface.MAP
			display.refresh_full()
			gameloop = True
			while gameloop:
				key = display.mapbox.getch()
				##########################
				# Player movement
				##########################

				try:
					if key in keys.UP:
						game.player.move(game.zone, UP)
					elif key in keys.DOWN:
						game.player.move(game.zone, DOWN)
					elif key in keys.LEFT:
						game.player.move(game.zone, LEFT)
					elif key in keys.RIGHT:
						game.player.move(game.zone, RIGHT)

					##########################
					# Player menu
					##########################
					elif key in keys.MENUKEY:
						#Menu
						choice = display.menu(['Battlers', 'Quests', 'Fast Travel', 'Save', 'Options', 'Items', 'Quit'], 4)
						if choice == 'Battlers':
							battler = display.menu(game.player.combatants)
							if battler is not None:
								item_target = display.menu(battler.equipment.all_items())
								if item_target is not None:
									unequipped = battler.equipment.unequip_by_instance(item_target)
									if unequipped is not None:
										game.player.backpack.store(unequipped)
						elif choice == 'Quests':
							pass
						elif choice == 'Fast Travel':
							if game.zone.check_clear():
								selected_zone = display.menu(list(game.fast_travel), cols=2)
								if selected_zone != game.zone.name:
									print('Fast Traveling To {}'.format(selected_zone))
									z = game.zones[selected_zone]
									newx, newy = z.find_empty_position()
									if selected_zone is not None:
										game.change_zone(selected_zone, newx, newy)
								else:
									print('Already in zone {}'.format(selected_zone))
							else:
								print('Cannot Fast Travel Until Zone Is Clear')
						elif choice == 'Items':
							item_slot_used = display.menu(game.player.backpack.show(), cols=2)
							item_target = None
							if item_slot_used is not None:
								item_target_type = item_slot_used.target_type
								if item_target_type == ALLY:
									item_target = [display.menu(game.player.combatants, cols=2)]
								elif item_target_type == MULTI_ALLY:
									item_target = game.player.combatants
								elif item_target_type in EQUIPPABLE:
									item_target = [display.menu(game.player.combatants, cols=2)]
								else:
									print("Can't Use that now")
								if item_target[0] is not None:
									item_used = item_slot_used.take()
									selection_needed = False
									for t in item_target:
										if t is not None:
											item_used.use(t)
						elif choice == 'Quit':
							game.save()
							break

						elif choice == 'Save':
							game.save()

					elif key in keys.DEBUG_K:
						#up
						game.zone.exit(game.player, UP)
					elif key in keys.DEBUG_J:
						game.zone.exit(game.player, DOWN)
						#down
					elif key in keys.DEBUG_H:
						game.zone.exit(game.player, LEFT)
						#left
					elif key in keys.DEBUG_L:
						game.zone.exit(game.player, RIGHT)
						#right
					##########################
					# Player did nothing
					##########################
					elif key in keys.DEBUGKEY:
						#print(game.display.mapbox.getmaxyx())
						#game.player.combatants[0].level += 1
						while True:
							input_command = display.text_entry(history=game.debug_history)
							if input_command == '':
								break
							try:
								output = game.debug(input_command)
								if output is not None:
									print(output)
							except Exception as e:
								#print(e.message)
								print(sys.exc_info()[0])
							display.show_messages()
					elif key in keys.EXIT:

						game.save()
						time.sleep(1)
						break

					game.zone.tick()

				except main.GameOver as e:
					display.show_messages()
					#terminal.read()
					display.getch()
					display.game_over()
					#TODO: delete save file
					#terminal.read()
					display.getch()
					gameloop = False
				display.show_messages()
				display.refresh_full()

except Exception as e:
	graphics_interface.shutdown()
	raise

graphics_interface.shutdown()



sys.exit(0)
