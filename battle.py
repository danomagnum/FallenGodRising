import math
import random
import time
import main
import sayings
import sys
import utility
from constants import *

DEBUG = True

class AI(object):
	def attack(self, enemy_ai):
		move = random.choice(self.combatant.moves)
		enemy = random.choice(enemy_ai.get_available())
		t = move.default_target
		if t == SELF:
			target = self.combatant
		elif t == ENEMY:
			target = enemy
		elif t == ANY:
			target = random.choice([self.combatant, enemy])
		elif t == ALLY:
			target = random.choice(self.combatants)
		elif t == MULTI_ALLY:
			target = self.combatants
		elif t == MULTI_ENEMY:
			target = enemy_ai.get_available()
		elif t == multi_ALL:
			target = self.get_available() + enemy_ai.get_available()
		#target = [self.combatant, enemy][move.default_target]
		return [move, [target]]

	def change(self, enemy):
		standby = self.get_standby()
		available = self.get_available()
		if standby:
			self.combatant = random.choice(standby)
			return self.combatant
		elif available:
			self.combatant = random.choice(available)
			return self.combatant
		else:
			return None
	
	def action(self, enemy_ai):
		if self.get_standby():
			return random.choice([ATTACK, SWITCH])
		else:
			action = random.choice([ATTACK, ATTACK, ATTACK, ATTACK, ATTACK, RUN])
		return action
	
	def get_available(self):
		return [ combatant for combatant in self.combatants if combatant.hp > 0 ] 
	
	def get_standby(self):
		return [ combatant for combatant in self.combatants if (combatant.hp > 0) and combatant != self.combatant ] 


class Random_AI(AI):
	def attack(self, enemy_ai):
		move = random.choice(self.combatant.moves)
		enemy = random.choice(enemy_ai.get_available())
		t = move.default_target
		if t == SELF:
			target = self.combatant
		elif t == ENEMY:
			target = enemy
		elif t == ANY:
			target = random.choice([self.combatant, enemy])
		elif t == ALLY:
			target = random.choice(self.combatants)
		elif t == MULTI_ALLY:
			target = self.combatants
		elif t == MULTI_ENEMY:
			target = enemy_ai.get_available()
		elif t == multi_ALL:
			target = self.get_available() + enemy_ai.get_available()
		#target = [self.combatant, enemy][move.default_target]
		return [move, [target]]


		#move = random.choice(self.combatant.moves)
		#enemy = random.choice(enemy_ai.get_available())
		#target = [self.combatant, enemy][move.default_target]
		#return [move, [target]]

	def change(self, enemy):
		standby = self.get_standby()
		available = self.get_available()
		if standby:
			self.combatant = random.choice(standby)
			return self.combatant
		elif available:
			self.combatant = random.choice(available)
			return self.combatant
		else:
			return None
	
	def action(self, enemy):
		if self.get_standby():
			action = random.choice([ATTACK, SWITCH, ATTACK, ATTACK, ATTACK, ATTACK, RUN])
			return action
		else:
			action = random.choice([ATTACK, ATTACK, ATTACK, ATTACK, ATTACK, RUN])
			return action


class Skiddish_AI(AI):
	def attack(self, enemy_ai):
		move = random.choice(self.combatant.moves)
		enemy = random.choice(enemy_ai.get_available())
		t = move.default_target
		if t == SELF:
			target = self.combatant
		elif t == ENEMY:
			target = enemy
		elif t == ANY:
			target = random.choice([self.combatant, enemy])
		elif t == ALLY:
			target = random.choice(self.combatants)
		elif t == MULTI_ALLY:
			target = self.combatants
		elif t == MULTI_ENEMY:
			target = enemy_ai.get_available()
		elif t == multi_ALL:
			target = self.get_available() + enemy_ai.get_available()
		#target = [self.combatant, enemy][move.default_target]
		return [move, [target]]


		#move = random.choice(self.combatant.moves)
		#enemy = random.choice(enemy_ai.get_available())
		#target = [self.combatant, enemy][move.default_target]
		#return [move, [target]]

	def change(self, enemy):
		standby = self.get_standby()
		available = self.get_available()
		if standby:
			self.combatant = random.choice(standby)
			return self.combatant
		elif available:
			self.combatant = random.choice(available)
			return self.combatant
		else:
			return None
	
	def action(self, enemy):
		health = 1
		maxhealth = 1
		for c in self.combatants:
			health += c.hp
			maxhealth += c.max_hp
		run_chance = float(health) / float(maxhealth)
		if random.random() > run_chance:
			self.battle_run()
			return RUN
		if self.get_standby():
			return random.choice([ATTACK, SWITCH])
		else:
			return random.choice([ATTACK, ATTACK])



def Battle(game, user, enemy_ai):
	game.player.target_map = None # cancel any auto-moves if we got in a battle
	old_music = game.music
	game.set_music(enemy_ai.music)
	game.display.start_battle(enemy_ai)
	valid_users = user.get_available()
	valid_enemies = enemy_ai.get_available()
	all_combatants = valid_users + valid_enemies
	possess_tries = 0
	#display = display(user, enemy_ai)

	battle_continue = True
	user_move = None
	winner = None

	#make sure all pre-battle status take effect
	for combatant in all_combatants:
		for status in combatant.status:
			status.pre_battle(combatant)
	game.display.refresh_combatant()

	selected_target = None
	first_choice = None
	running = False

	while battle_continue:
		game.display.show_btl_messages()
		valid_users = user.get_available()
		valid_enemies = enemy_ai.get_available()
		all_combatants = valid_users + valid_enemies

		#make sure all pre-turn status take effect
		for combatant in all_combatants:
			for status in combatant.status:
				status.pre_turn(combatant)
		game.display.refresh_combatant()

		#have the user select an action
		selection_needed = True
		user_is_attacking = False
		user_target = enemy_ai.combatant
		possess = None
		#print('vu: {}, ve: {}'.format(len(valid_users), len(valid_enemies)))
		if len(valid_users) < 3 and len(valid_enemies) == 1:
			if len(valid_users) > 1 :
				choices = ['Attack', 'Change', 'Items', 'Run', 'Possess']
			else:
				choices = ['Attack', 'Items', 'Run', 'Possess']
		else:
			if len(valid_users) > 1 :
				choices = ['Attack', 'Change', 'Items', 'Run']
			else:
				choices = ['Attack', 'Items', 'Run']
		while selection_needed:
			#if the enemy died outside of active combat (from poison or something) this check will
			# end the battle by "running" and the final checks will take care of the rest, dosing out
			# exp and items like you won
			if len(enemy_ai.get_available()) == 0:
				first_choice = 'Run'
			else:
				first_choice = game.display.battlemenu(choices, cols=2, selected=first_choice)
			if first_choice == 'Attack':
				#first_choice = display.menu(['Attack', 'Change', 'Items'], cols=2)
				user_move = game.display.battlemenu(user.combatant.moves, cols=2, selected=user_move)
				if user_move is not None:
					target = user_move.default_target
					if target == main.ALLY:
						selected_target = game.display.battlemenu(user.get_available(), selected=user.combatant)
						if selected_target is not None:
							user_target = [selected_target]
							user_is_attacking = True
							selection_needed = False
					if target == main.SELF:
						selected_target = user.combatant
					elif target == main.ANY:
						selected_target = game.display.battlemenu(user.get_available() + enemy_ai.get_available(), selected=user.combatant)
						if selected_target is not None:
							user_target = [selected_target]
							user_is_attacking = True
							selection_needed = False
					elif target == main.ENEMY:
						if len(enemy_ai.get_available()) > 1:
							selected_target = game.display.battlemenu(enemy_ai.get_available(), selected=selected_target)
							if selected_target is not None:
								user_target = [selected_target]
								user_is_attacking = True
								selection_needed = False
						else:
							user_target = enemy_ai.get_available()
							user_is_attacking = True
							selection_needed = False

					elif target == main.ACTIVE:
						user_target = [enemy_ai.combatant]
						user_is_attacking = True
						selection_needed = False
					elif target == main.MULTI_ENEMY:
						user_target = enemy_ai.get_available()
						user_is_attacking = True
						selection_needed = False
					elif target == main.MULTI_ALLY:
						user_target = user.get_available()
						user_is_attacking = True
						selection_needed = False
					elif target == main.MULTI_ALL:
						user_target = user.get_available() + enemy_ai.get_available()
						user_is_attacking = True
						selection_needed = False
			elif first_choice == 'Change':
				if user.get_standby():
					change_choice = game.display.battlemenu(user.get_standby())
					if change_choice is not None:
						user.combatant = change_choice
						game.display.refresh_combatant()
			elif first_choice == 'Items':
				item_slot_used = game.display.battlemenu(user.backpack.show(), cols=2)
				if item_slot_used is not None:
					item_target_type = item_slot_used.target_type
					if item_target_type == ALLY:
						item_target = [game.display.battlemenu(user.combatants, cols=2)]
					elif item_target_type == SELF:
						item_target = user.combatant
					elif item_target_type == ENEMY:
						item_target = [game.display.battlemenu(enemy_ai.combatants, cols=2)]
					elif item_target_type == MULTI_ALLY:
						item_target = user.combatants
					elif item_target_type == MULTI_ENEMY:
						item_target = enemy_ai.combatants
					elif item_target_type == ANY:
						item_target = [game.display.battlemenu(user.get_available() + enemy_ai.get_available(), selected=user.combatant, cols=2)]
					else:
						item_target = None
						print("Can't Use that now")
					if item_target is not None:
						if len(item_target) > 0:
							item_used = item_slot_used.take()
							selection_needed = False
							for t in item_target:
								item_used.use(t)
				#game.display.show_btl_messages()
				game.display.refresh_combatant()
			elif first_choice == 'Possess':
				possess_tries += 1
				selection_needed = False

				possess_candidate = valid_enemies[0]
				hp_ratio = 1.0 - (possess_candidate.hp / possess_candidate.max_hp) ** 0.5 # square root to make weakening further get more and more advantageous
				attempt_ratio = 1.0 - utility.clamp(possess_tries / 100.0, 1.0, 0.3) # the more your try, the harder it gets

				chance = hp_ratio * attempt_ratio
				if random.random() < chance:
					possess = possess_candidate
					winner = USER
					battle_continue = False
					print('Possessed {}'.format(possess.name))
				else:
					print('Possession Attempt {} Was Unsuccessful.'.format(possess_tries))

			elif first_choice == 'Run':
				running = True
				selection_needed = False
				battle_continue = False
				

		#have the enemy select a move and target
		enemy_decision = enemy_ai.action(user)
		if enemy_decision == ATTACK:
			enemy_move, enemy_target = enemy_ai.attack(user)
			enemy_is_attacking = True
		elif enemy_decision == SWITCH:
			enemy_ai.change(user)
			enemy_move = None
			enemy_target = None
			enemy_is_attacking = False
			game.display.refresh_combatant()
			enemy_move, enemy_target = enemy_ai.attack(user)
			enemy_is_attacking = True
		elif enemy_decision == RUN:
			enemy_move = None
			enemy_target = None
			enemy_is_attacking = False
			enemy_ai.running = True
			running = True
			print('Enemy Is Running')
			battle_continue = False


		#decide who should attack first
		if user.combatant.speed >= enemy_ai.combatant.speed:
			first = user.combatant
			first_target = user_target
			first_move = user_move
			first_is_attacking = user_is_attacking
			second = enemy_ai.combatant
			second_target = enemy_target
			second_move = enemy_move
			second_is_attacking = enemy_is_attacking
		else:
			first = enemy_ai.combatant
			first_target = enemy_target
			first_move = enemy_move
			first_is_attacking = enemy_is_attacking
			second = user.combatant
			second_target = user_target
			second_move = user_move
			second_is_attacking = user_is_attacking

		if possess is None:
			#first attack
			if first_is_attacking:
				for status in first.status:
					status.pre_attack(first)
				game.display.refresh_combatant()

				first_move.attack(first, first_target)
				game.display.refresh_combatant()

				for status in first.status:
					status.post_attack(first)
				game.display.refresh_combatant()

			#second attack, assuming they did not die
			if second_is_attacking and second.hp > 0:
				for status in second.status:
					status.pre_attack(second)
				game.display.refresh_combatant()

				second_move.attack(second, second_target)
				game.display.refresh_combatant()

				for status in second.status:
					status.post_attack(second)

				game.display.refresh_combatant()
		else:
			game.player.combatants.append(possess)
			print('Possess: {}'.format(str(possess)))
		
		# make sure all post-turn status take place
		for combatant in all_combatants:
			for status in combatant.status:
				status.post_turn(combatant)
		game.display.refresh_combatant()

		
		if len(enemy_ai.get_available()) == 0:
			battle_continue = False
			winner = USER

		# check for any deaths
		for e in valid_enemies:
			if e.hp == 0:
				print("{}: {}".format(e.name, random.choice(sayings.death)))
				exp = e.exp_value
				divied_exp = max(1, exp / (len(user.combatants) + 1)) # plus one because the active comatant gets a larger share of exp.
				for comb in user.get_available():
					if comb == user.combatant:
						#active combatant gets twice the experience of everyone else
						gained = divied_exp * 2
					else:
						gained = divied_exp
					print("{} gained {} xp".format(comb.name, int(gained)))
					comb.exp += gained

				if enemy_ai.change(user.combatant) is not None:
					#print("{} sent out {}".format(enemy_ai.name, e.name))
					game.display.refresh_combatant()
				else:
					battle_continue = False
					winner = USER

				
		if user.combatant.hp == 0:
			if user.get_standby():
				need_choice = True
				while need_choice:
					change_choice = game.display.battlemenu(user.get_standby())
					if change_choice is not None:
						user.combatant = change_choice
						print('changed to {}'.format(user.combatant))
						game.display.refresh_combatant()
						need_choice = False
			else:
				battle_continue = False
				print("{} {}".format(user.combatant.name, random.choice(sayings.death)))
				print('you lost')
				winner = ENEMY
				raise main.GameOver()

		game.display.refresh_combatant()

		for c in user.get_available():
			c.battletick()
		for c in enemy_ai.get_available():
			c.battletick()

		#game.display.show_btl_messages()

		#time.sleep(1.0 / 60.0)

	for combatant in user.combatants:
		for status in combatant.status:
			status.post_battle(combatant)
	
	if winner == USER:
		print('{}: {}'.format(enemy_ai.name,enemy_ai.defeated_text))
	
	game.display.show_btl_messages()

	game.display.end_battle()

	user.purge_dead()

	game.set_music(old_music)

	return winner

