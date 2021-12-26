import main
import entities
import bearlibkeys as keys
import sys
from bearlibterminal import terminal
import bearlib_interface as graphics_interface
from constants import *
import settings

class PlayerEntity(entities.ActingEntity):

	def collide(self, entity, zone):
		if entity.blocking:
			self.target_map = None

	def config(self):
		self.target_map = None
		self.target_pos = None

	def vision(self, zone):
		pass

	def tick(self, zone):
		
		while True: # we will return if they do an action.
			game = self.game
			display = game.display
			display.show_messages()
			display.refresh_full()
			if not terminal.has_input():
				#no user inputs ready
				if self.target_map is not None:
					#not trying to go somewhere
					dir = self.follow_distmap(self.target_map)
					if dir is None:
						self.target_map = None
					else:
						self.move(zone, dir)
						zone.update_fog()
						if self.x == self.target_pos[0] and self.y == self.target_pos[1]:
							self.target_map = None
						return

				display.refresh_full()
				continue

			#key = display.mapbox.getch()
			key = terminal.read()

			#this gets rid of auto-repeat characters
			#if you don't do this, the character will keep moving once you let off the button
			while terminal.peek() == key:
				terminal.read()

			if key == terminal.TK_MOUSE_LEFT:
				windowpos = self.game.display.mapbox.getmousepos()
				if windowpos is not None:
					self.target_map = self.game.zone.dist_map(windowpos[0], windowpos[1] - 1)
					self.target_pos = windowpos

			elif key in keys.UP:
				self.target_map = None
				self.move(zone, UP)
				try:
					zone.update_fog()
				except:
					pass
				return
			elif key in keys.DOWN:
				self.target_map = None
				self.move(zone, DOWN)
				try:
					zone.update_fog()
				except:
					pass
				return
			elif key in keys.LEFT:
				self.target_map = None
				self.move(zone, LEFT)
				try:
					zone.update_fog()
				except:
					pass
				return
			elif key in keys.RIGHT:
				self.target_map = None
				self.move(zone, RIGHT)
				try:
					zone.update_fog()
				except:
					pass
				return

			##########################
			# Player menu
			##########################
			elif key in keys.MENUKEY:
				self.target_map = None
				#Menu
				choice = display.menu(['Battlers', 'Quests', 'Fast Travel', 'Save', 'Options', 'Items', 'Settings', 'Quit'], cols=4)
				if choice == 'Battlers':
					battler = display.menu(self.combatants)
					if battler is not None:
						battler_choice = display.menu(['Items', 'Moves', 'Select'])
						if battler_choice == 'Items':
							item_target = display.menu(battler.equipment.all_items())
							if item_target is not None:
								unequipped = battler.equipment.unequip_by_instance(item_target)
								if unequipped is not None:
									self.backpack.store(unequipped)
									print('{} unequipped {}'.format(battler, unequipped))
									return
						elif battler_choice == 'Moves':
							def update_move_desc(move):
								display.show_move_stats(move, display.popupbox)
							move_choice = self.game.display.popup('Select a move', battler.moves, callback_on_change=update_move_desc, cols=1)
							if (move_choice is not None) and len(battler.moves) > 1:
								delete_choice = self.game.display.popup('Delete move {}'.format(move_choice.name), ['No, Keep', 'Yes, Delete'],  cols=1)
								if delete_choice == 'Yes, Delete':
									battler.moves.remove(move_choice)
						elif battler_choice == 'Select':
							self.combatant = battler
								
				elif choice == 'Quests':
					pass
				elif choice == 'Settings':
					display.settingsmenu(game.music_queue)

				elif choice == 'Fast Travel':
					if game.zone.check_clear():
						sel_ft = display.menu(list(game.fast_travel()), cols=2)
						if sel_ft is not None:
							if sel_ft.level != game.zone.level:
								print('Fast Traveling To {}'.format(sel_ft))
								game.zone.change_level(sel_ft.level)
								x, y = game.zone.find_empty_position()
								self.x = x
								self.y = y
								return

							else:
								print('Already at {}'.format(sel_ft))
					else:
						print('Cannot Fast Travel Until Zone Is Clear')
				elif choice == 'Items':
					item_slot_used = display.menu(self.backpack.show(), cols=2)
					item_target = None
					if item_slot_used is not None:
						item_target_type = item_slot_used.target_type
						if item_target_type == ALLY:
							item_target = [display.menu(self.combatants, cols=2)]
						elif item_target_type == ANY:
							item_target = [display.menu(self.combatants, cols=2)]
						elif item_target_type == MULTI_ALLY:
							item_target = self.combatants
						elif item_target_type == WORLD:
							print('here')
							item_target = [WORLD]
						elif item_target_type in EQUIPPABLE:
							item_target = [display.menu(self.combatants, cols=2)]
						else:
							item_target = [None]
							print("Can't Use that now")
						if item_target[0] is not None:
							item_used = item_slot_used.take()
							selection_needed = False
							for t in item_target:
								if t is not None:
									if t == WORLD:
										item_used.use()
									else:
										item_used.use(t)
				elif choice == 'Quit':
					raise main.GameSoftExit()

				elif choice == 'Save':
					game.save()

			elif key in keys.DEBUG_K:
				self.target_map = None
				#up
				game.zone.exit(self, UP)
				return
			elif key in keys.DEBUG_J:
				self.target_map = None
				game.zone.exit(self, DOWN)
				return
				#down
			elif key in keys.DEBUG_H:
				self.target_map = None
				game.zone.exit(self, LEFT)
				return
				#left
			elif key in keys.DEBUG_L:
				self.target_map = None
				game.zone.exit(self, RIGHT)
				return
				#right
			elif key in keys.DEBUGKEY:
				self.target_map = None
				#print(game.display.mapbox.getmaxyx())
				while True:
					input_command = display.text_entry(history=game.debug_history)
					if input_command == '' or input_command is None:
						break
					try:
						output = game.debug(input_command)
						if output is not None:
							print(output)
					except Exception as e:
						#print(e.message)
						print(sys.exc_info()[0])
						raise e
					display.show_messages()
					display.refresh_full()
				display.show_messages()
				display.refresh_full()
			elif key in keys.EXIT:
				self.target_map = None
				raise main.GameHardExit()



