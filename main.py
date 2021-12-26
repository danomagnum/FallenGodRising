import random
import settings
import sys
import math
import utility
import items
import elements
import battle
import effects
import mobs
import moves
import bearlibkeys as keys
import pickle
import time
from constants import *
from os import listdir
from os.path import isfile, join

import namegen
#import pygame

try:
	#only used for debugging right now
	import ow2img
except:
	pass

class GameOver(Exception):
	pass

class GameHardExit(Exception):
	pass

class GameSoftExit(Exception):
	pass

class FastTravel(object):
	def __init__(self, name=None, level=None):
		self.name = name
		self.level = level
	def __str__(self):
		return self.name

class Game(object):
	def __init__(self):
		self.overworld = None
		self.biome_map = None
		self.overworld_x = 0
		self.overworld_y = 0
		self.overworld_minimap = None

		self.zone = None
		self.zones = {}
		self.display = None
		self.player = None
		self.game_vars = {}
		self.debug_history = []

		self.progress_max = 1
		self.progress_value = 0

		self.filename = 'auto.sav'

		self.music = None
		self.music_lock = False

		self.generated_names = set() 

		self.ticks = 0

	def tick(self):
		#this main tick routine will determine if any active entities are ready
		# to do something.  It will loop on actions until its the players turn 
		# at which point it wil return
		self.ticks += 1
		while True:
			#self.display.refresh_full()
			valid_entities = self.zone.entities + [self.player]

			for e in valid_entities:
				e.action_accumulate()

			valid_entities.sort(key=lambda x: -x.action_points)

			top_entity = valid_entities[0]

			top_entity.tick(zone=self.zone)
			top_entity.subtick(zone=self.zone)
			top_entity.action_points = 0
			self.zone.redraw.append([top_entity.x, top_entity.y])
			#if top_entity == self.player:
				#return

			purged = [ e for e in self.zone.entities if not e.enabled]
			for p in purged:
				self.zone.redraw.append([p.x, p.y])

			self.zone.entities = [e for e in self.zone.entities if e.enabled] 
			if top_entity == self.player:
				return

	def set_music(self, filename, fade_ms=1000, force=False):
		if filename == None:
			filename = self.music
		if self.music_lock:
			return
		if filename == self.music and not force:
			return
		if filename is not None:
			#pygame.mixer.music.fadeout(1000)
			self.music_queue.put(['fadeout'])
			#self.music_queue.put(['play', 'data/music/' + filename])
			self.music_queue.put(['play', filename])
			#pygame.mixer.music.load('data/music/' + filename)
			#pygame.mixer.music.play(loops = -1, start=0.0, fade_ms = fade_ms)
			self.music = filename


	def generate_name(self, allow_repeats=False):
		
		while True:
			name = namegen.gen_name()
			if (name not in self.generated_names) or allow_repeats:
				self.generated_names.add(name)
				return name

	def fast_travel(self):
		return self.zone.fast_travel_found

	def save(self):
		print('Saving...')
		self.display.show_messages()
		file = open(join(SAVEDIR, self.filename), 'wb')
		music_queue = self.music_queue
		self.music_queue = None
		pickle.dump(self, file)
		file.close()
		self.music_queue = music_queue
		time.sleep(1)
	
	def progress_reset(self, max):
		self.progress_max = max
		self.progress_value = 0

	def progress(self):
		self.progress_value += 1
		self.display.loading_progress(self.progress_value, self.progress_max)

	def biome(self):
		if self.zone == self.overworld:
			if self.biome_map is not None:
				#TODO: fix this
				return elements.biomes[self.biome_map[self.overworld_x][self.overworld_y]]
				#return elements.biomes[self.biome_map[self.overworld_y][self.overworld_x]]
			else:
				return ''
		else:
			return self.zone.biome()

	def add_zone(self, zone):
		if zone.name not in self.zones:
			self.zones[zone.name] = zone
		if self.zone is None:
			self.zone = zone

	def change_zone(self, zonename, newx = None, newy = None, newlevel=None):
		if self.player is not None:
			self.player.target_map = None # cancel any auto-moves if we changed zones
		if zonename in self.zones:
			self.zone = self.zones[zonename]
			if newx is not None:
				self.player.x = newx
			if newy is not None:
				self.player.y = newy
			if newlevel is not None:
				self.zone.change_level(newlevel)
			self.display.change_zone(self.zone)

			print('Entering Zone {}'.format(zonename))

			self.set_music(self.zone.get_music())

			self.zone.update_fog()

		else:
			print('Zone {} does not exist'.format(zonename))


	def get_var(self, variable):
		return self.game_vars.get(variable, 0)

	def set_var(self, variable, value):
		self.game_vars[variable] = value
	
	def get_confirm(self):
		key = self.display.msgbox.getch()
		if key in keys.SELECT:
			return True
		else:
			return False
	
	def debug(self, command):
		if len(self.debug_history) > 20:
			self.debug_history = self.debug_history[1:]
		self.debug_history.append(command)
		#special debug commands
		if command == 'GODMODE':
			for c in self.player.combatants:
				c.level = 100
			self.set_var('GLO', -90)
			return

		if '=' in command:
			exec(command)
		else:
			return eval(command)

class Equipment(object):
	def __init__(self, game):
		self.game = game
		self.Head = None
		self.Body = None
		self.Left = None
		self.Right = None
		self.Hands = None
		self.Token = None
		self._helptext = ''

	def helptext(self):
		return self._helptext
	
	def equip(self, item):
		return_items = []
		if item.target_type == EQUIP_HEAD:
			if self.Head is not None:
				return_items.append(self.Head)
			self.Head = item
		elif item.target_type == EQUIP_BODY:
			if self.Body is not None:
				return_items.append(self.Body)
			self.Body = item
		elif item.target_type == EQUIP_RIGHT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Right is not None:
				return_items.append(self.Right)
			self.Right = item
		elif item.target_type == EQUIP_LEFT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Left is not None:
				return_items.append(self.Left)
			self.Left = item
		elif item.target_type == EQUIP_HANDS:
			if self.Hands is not None:
				return_items.append(self.Hands)
			if self.Left is not None:
				return_items.append(self.Left)
				self.Left = None
			if self.Right is not None:
				return_items.append(self.Right)
				self.Right = None
			self.Hands = item
		elif item.target_type == EQUIP_TOKEN:
			if self.Token is not None:
				return_items.append(self.Token)
			self.Token = item

		return return_items

	def unequip_by_instance(self, item):
		if item == self.Head:
			self.Head = None
			return item
		elif item == self.Body:
			self.Body = None
			return item
		elif item == self.Hands:
			self.Hand = None
			return item
		elif item == self.Left:
			self.Left = None
			return item
		elif item == self.Right:
			self.Right = None
			return item
		elif item == self.Token:
			self.Token = None
			return item

	def unequip(self, target):
		return_items = []
		if target == EQUIP_HEAD:
			if self.Head is not None:
				return_items.append(self.Head)
				self.Head = None
		elif target == EQUIP_BODY:
			if self.Body is not None:
				return_items.append(self.Body)
				self.Body = None
		elif target == EQUIP_RIGHT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Right is not None:
				return_items.append(self.Right)
				self.Right = None
		elif target == EQUIP_LEFT:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Left is not None:
				return_items.append(self.Left)
				self.Left = None
		elif target == EQUIP_HANDS:
			if self.Hands is not None:
				return_items.append(self.Hands)
				self.Hands = None
			if self.Left is not None:
				return_items.append(self.Left)
				self.Left = None
			if self.Right is not None:
				return_items.append(self.Right)
				self.Right = None
		elif target == EQUIP_TOKEN:
			if self.Token is not None:
				return_items.append(self.Token)
				self.Token = None
		return return_items

	def purge(self, target):
		return_items = []
		if self.Head is not None:
			return_items.append(self.Head)
			self.Head = None
		if self.Body is not None:
			return_items.append(self.Body)
			self.Body = None
		if self.Hands is not None:
			return_items.append(self.Hands)
			self.Hands = None
		if self.Right is not None:
			return_items.append(self.Right)
			self.Right = None
		if self.Hands is not None:
			return_items.append(self.Hands)
			self.Hands = None
		if self.Left is not None:
			return_items.append(self.Left)
			self.Left = None
		if self.Hands is not None:
			return_items.append(self.Hands)
			self.Hands = None
		if self.Left is not None:
			return_items.append(self.Left)
			self.Left = None
		if self.Right is not None:
			return_items.append(self.Right)
			self.Right = None
		if self.Token is not None:
			return_items.append(self.Token)
			self.Token = None
		return return_items
	
	def all_items(self):
		items = [self.Head, self.Body, self.Hands, self.Right, self.Left, self.Token]
		return [item for item in items if item is not None]

	def physical_strength(self, initial): # passive stat boosts take effect on these routines
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'physical_strength', item)

		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)

		return initial

	def evasion(self, initial): # passive stat boosts take effect on these routines
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'evasion', item)

		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)
		return initial

	def accuracy(self, initial): # passive stat boosts take effect on these routines
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'accuracy', item)

		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)
		return initial





	def physical_defense(self, initial):
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'physical_defense', item)
		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)
		return initial

	def arcane_strength(self, initial):
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'arcane_strength', item)
		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)
		return initial

	def arcane_defense(self, initial):
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'arcane_defense', item)
		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)
		return initial
		
	def speed(self, initial):
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'speed', item)
		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)
		return initial

	def hp(self, initial):
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'hp', item)
		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)
		return initial

	def max_hp(self, initial):
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'max_hp', item)
		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)
		return initial

	def evasion(self, initial):
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'evasion', item)
		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)
		return initial

	def accuracy(self, initial):
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'accuracy', item)
		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)
		return initial

	def luck(self, initial):
		sqr = initial * initial
		for item in self.all_items():
			sqr = utility.call_all_recursive(sqr, 'luck', item)
		if sqr < 0:
			initial = 0
		else:
			initial = math.sqrt(sqr)
		return initial

