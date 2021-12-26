#!/usr/bin/python
#coding: utf-8 
import sys
import traceback
import settings


sys.dont_write_bytecode = True

#import characters
import mobs
import battle
import main
import random
import utility

#import dill as pickle
import pickle

import os
from os import listdir
from os.path import isfile, join
from version import *

#import curses_interface as graphics_interface
#import keys
import bearlib_interface as graphics_interface
import bearlibkeys as keys

import time
#from items import items
import items
import entities
import elements
from constants import *
import player


import maps.overworld
import maps.fortress
import maps.goblincave
import maps.wizardtower
import maps.pyramid
import maps.maptools
import maps.buildings
import maps.lair
import maps.sewers
import maps.town
import maps.home
import maps.lighthouse
import maps.final

import music

from multiprocessing import Process, Queue

WRITEMAP = False



music_queue = Queue()
music_process = Process(target=music.thread, args=(music_queue,))
music_volume = 1
music_process.start()

if not settings.music:
	music_queue.put(['volume', 0])

def shutdown():
	graphics_interface.shutdown()
	music.shutdown(music_process, music_queue)

try:
	if __name__ == '__main__':
		graphics_interface.initialize()
		display = graphics_interface.Display()
		while True:
			music_queue.put(['play', 'mainmenu'])
			#music_queue.put(['play', 'data/music/mainmenu.mid'])
			#pygame.mixer.music.load('data/music/mainmenu.mid')
			#pygame.mixer.music.play(loops = -1, start=0.0, fade_ms=1000)
			display.mode = MAP
			mainmenu = True
			while mainmenu:
				display.splash_screen()
				print(versionstring)
				display.show_messages()

				player_choice = graphics_interface.menu(display.menubox, ['New Game', 'Resume', 'Backstory', 'Instructions', 'Settings', 'Quit'] ,cols = 1, clear=False)
				if player_choice == 'Quit':
					shutdown()
					sys.exit(0)
				elif player_choice == 'Backstory':
					display.show_txt('data/backstory.txt')
				elif player_choice == 'Instructions':
					display.show_txt('data/instructions.txt')
				elif player_choice == 'Settings':
					display.settingsmenu(music_queue)
				elif player_choice == 'Resume':
					onlyfiles = [f for f in listdir(SAVEDIR) if (isfile(join(SAVEDIR, f)) and (f[-3:] == 'sav'))]	
					if onlyfiles:
						player_choice = graphics_interface.menu(display.menubox, onlyfiles ,cols=1, clear=False)
						if player_choice is not None:
							try:
								f = open(join(SAVEDIR, player_choice), 'rb')
								game = pickle.load(f)
								game.music_lock = False
								display.game = game
								game.display = display
								game.music_queue = music_queue
								display.change_zone(game.zone)
								game.set_music(game.music, force=True)
								f.close()
								game.filename = player_choice
								mainmenu = False
								if not settings.debug:
									os.remove(join(SAVEDIR, player_choice))
							except Exception as e:
								traceback.print_exc(file=sys.stderr)
								print("Error loading" + player_choice)
								display.show_messages()
					else:
						print('No Saves Detected')
						display.show_messages()

				elif player_choice == 'New Game':
					zone_count = 2 * 16*16 + 10 + 20 + 5*5 + 3 + 5 + 10 + 20
					print('Please Wait, Generating World. ({} tasks)'.format(zone_count))
					display.show_messages()


					game = main.Game()
					game.music_lock = True
					game.set_var('Alters', [])

					#The global level offset
					game.set_var('GLO', 0)

					display.game = game
					game.display = display
					game.music_queue = music_queue

					game.progress_reset(zone_count)
					zone, biome_map, overworld_minimap = maps.overworld.genzone(game)

					game.biome_map = biome_map
					game.overworld_minimap = overworld_minimap
					game.overworld = zone
					print('ow done')
					display.show_messages()

					#zone2 = maps.goblincave.genzone(game)
					#print('gc done')
					#display.show_messages()
					#zone6 = maps.pyramid.genzone(game)
					#print('p done')
					#display.show_messages()
					zone3 = maps.wizardtower.genzone(game)
					print('wt done')
					display.show_messages()
					zone4 = maps.sewers.genzone(game)
					print('s done')
					display.show_messages()
					zone5 = maps.fortress.genzone(game)
					print('f done')
					display.show_messages()
					zone6 = maps.lair.genzone(game)
					print('l done')
					display.show_messages()
					zone7 = maps.lighthouse.genzone(game)
					zone8 = maps.final.genzone(game)

					homezone = maps.home.genzone(game)


					maps.town.genzone(game, 'Town1')
					maps.town.genzone(game, 'Town2')
					maps.town.genzone(game, 'Town3')

					game.overworld_y = int(game.overworld.level % game.overworld.grid_width)
					game.overworld_x = int(game.overworld.level / game.overworld.grid_width)


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

					game.zone = homezone
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
						player_characters = []
						for starter in mobs.starters:
							player_characters.append(starter(game,level=settings.start_level))

						if i > 0:
							player_characters.append('None')


						def update_confirm_box(choice):
							if choice != 'None':
								display.show_combatant_stats(choice, display.start_menus[(i * 3) + 2])
							else:
								pass

						update_confirm_box(player_characters[0])
						player_choice = graphics_interface.menu(display.start_menus[i * 3], player_characters,selected=random.choice(player_characters) ,cols=1, clear=False, callback_on_change=update_confirm_box)

						if player_choice is not None:
							if player_choice == 'None':
								player_party = player_party[:i]
								user = player.PlayerEntity(game, 'playercharacter', combatants=player_party, char='@',is_player=True)
								#user.combatants = player_party
								user.x, user.y = game.zone.find_empty_position()
								user.backpack.gold = 100
								#zone.set_player(user)
								display.user = user
								game.player = user
								loop = False
								mainmenu = False
								break
							player_elements = [elements.Normal, elements.Fire, elements.Water, elements.Earth, elements.Electric, elements.Wind, elements.Light, elements.Dark]
							def update_confirm_box(choice):
								player_choice.elements = [choice]
								#player_choice.elements.append(choice)
								display.show_combatant_stats(player_choice, display.start_menus[(i * 3) + 2])

							element_choice =graphics_interface.menu(display.start_menus[(i * 3) + 1], player_elements, selected=random.choice(player_elements),cols=1, clear=False, callback_on_change=update_confirm_box)

							#confirm_choices = ['Accept', 'Cancel', 'Randomize']
							#confirm_choice = graphics_interface.menu(display.start_menus[(i * 3) + 2], confirm_choices, clear=False)
							if element_choice is not None:
								player_choice.elements = [element_choice]
								#player_choice.elements.append(element_choice)
								player_party[i] = player_choice
								i += 1
								if i == graphics_interface.MAX_COMBATANTS:
									user = player.PlayerEntity(game, 'playercharacter', combatants=player_party, char='@',is_player=True)
									#user.combatants = player_party
									user.x, user.y = game.zone.find_empty_position()
									user.backpack.gold = 100
									#zone.set_player(user)
									display.user = user
									game.player = user
									loop = False
									mainmenu = False
						else:
							if i > 0:
								i -= 1


			##########################
			# Main Game Loop
			##########################
			display.mode = graphics_interface.MAP
			display.refresh_full()
			gameloop = True
			game.music_lock = False
			game.set_music(game.zone.music)
			game.zone.update_fog()


			while gameloop:
				display.refresh_full()
				display.show_messages()
				#key = display.mapbox.getch()
				##########################
				# Player movement
				##########################

				try:
					game.tick()
				except main.GameOver as e:
					display.show_messages()
					#terminal.read()
					display.getch()
					display.game_over()
					#TODO: delete save file
					#terminal.read()
					display.getch()
					gameloop = False
				except main.GameSoftExit as e:
					game.save()
					time.sleep(1)
					break
				except main.GameHardExit as e:
					game.save()
					time.sleep(1)
					shutdown()
					sys.exit(0)
				except Exception as e:
					raise e

except Exception as e:
	shutdown()
	sys.stdout = graphics_interface.original_stdout
	raise

shutdown()



sys.exit(0)
