import math
import random
import time
import main
import sayings
import sys
import items
from targets import *

DEBUG = True

class Random_AI(object):
	def __init__(self, combatants, money=0, name='AI', item_list=None, defeated_text='Oh Snap! I lost!'):
		self.name = name
		self.combatants = combatants
		self.combatant = combatants[0]
		self.defeated_text = defeated_text

		if money == 0:
			self.money = int(sum([c.exp_value for c in combatants]) / 10)
		else:
			self.money = money

		self.backpack = items.Backpack()
		if item_list is not None:
			for item in item_list:
				self.backpack.store(item)

	def attack(self, enemy):
		move = random.choice(self.combatant.moves)
		target = [self.combatant, enemy][move.default_target]
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
	
	def action(self, enemy):
		if self.get_standby():
			return random.choice([ATTACK, SWITCH])
		else:
			return ATTACK
	
	def get_available(self):
		return [ combatant for combatant in self.combatants if combatant.hp > 0 ] 
	
	def get_standby(self):
		return [ combatant for combatant in self.combatants if (combatant.hp > 0) and combatant != self.combatant ] 

def Battle(user, enemy_ai, display):
	display.start_battle(user, enemy_ai)
	valid_users = user.get_available()
	valid_enemies = enemy_ai.get_available()
	all_combatants = valid_users + valid_enemies
	#display = display(user, enemy_ai)

	battle_continue = True
	user_move = None
	winner = None

	#make sure all pre-battle status take effect
	for combatant in all_combatants:
		for status in combatant.status:
			status.pre_battle(combatant)
	display.refresh_combatant()

	selected_target = None
	first_choice = None

	while battle_continue:
		valid_users = user.get_available()
		valid_enemies = enemy_ai.get_available()
		all_combatants = valid_users + valid_enemies

		#make sure all pre-turn status take effect
		for combatant in all_combatants:
			for status in combatant.status:
				status.pre_turn(combatant)
		display.refresh_combatant()

		#have the user select an action
		selection_needed = True
		user_is_attacking = False
		user_target = enemy_ai.combatant
		while selection_needed:
			first_choice = display.menu(['Attack', 'Change', 'Items'], cols=2, selected=first_choice)
			if first_choice == 'Attack':
				#first_choice = display.menu(['Attack', 'Change', 'Items'], cols=2)
				user_move = display.menu(user.combatant.moves, cols=2, selected=user_move)
				if user_move is not None:
					target = user_move.default_target
					if target == main.SELF:
						user_target = [user.combatant]
						user_is_attacking = True
						selection_needed = False
					elif target == main.ENEMY:
						if len(enemy_ai.get_available()) > 1:
							selected_target = display.menu(enemy_ai.get_available(), selected=selected_target)
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
					elif target == main.MULTI_SELF:
						user_target = user.get_available()
			elif first_choice == 'Change':
				if user.get_standby():
					change_choice = display.menu(user.get_standby())
					if change_choice is not None:
						user.combatant = change_choice
						display.refresh_combatant()
			elif first_choice == 'Items':
				item_slot_used = display.menu(user.backpack.show(), cols=2)
				if item_slot_used is not None:
					item_target = display.menu(user.combatants + enemy_ai.combatants, cols=2)
					if item_target is not None:
						item_used = item_slot_used.take()
						item_used.use(item_target)
						selection_needed = False
				display.refresh_combatant()

		#have the enemy select a move and target
		enemy_decision = enemy_ai.action(user.combatant)
		if enemy_decision == ATTACK:
			enemy_move, enemy_target = enemy_ai.attack(user.combatant)
			enemy_is_attacking = True
		elif enemy_decision == SWITCH:
			enemy_ai.change(user.combatant)
			enemy_move = None
			enemy_target = None
			enemy_is_attacking = False
			display.refresh_combatant()
			enemy_move, enemy_target = enemy_ai.attack(user.combatant)
			enemy_is_attacking = True


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

		#first attack
		if first_is_attacking:
			for status in first.status:
				status.pre_attack(first)
			display.refresh_combatant()

			first_move.attack(first, first_target)
			display.refresh_combatant()

			for status in first.status:
				status.post_attack(first)
			display.refresh_combatant()

		#second attack, assuming they did not die
		if second_is_attacking and second.hp > 0:
			for status in second.status:
				status.pre_attack(second)
			display.refresh_combatant()

			second_move.attack(second, second_target)
			display.refresh_combatant()

			for status in second.status:
				status.post_attack(second)

			display.refresh_combatant()
	
		# make sure all post-turn status take place
		for combatant in all_combatants:
			for status in combatant.status:
				status.post_turn(combatant)
		display.refresh_combatant()


		# check for any deaths
		for e in valid_enemies:
			if e.hp == 0:
				print("{}: {}".format(e.name, random.choice(sayings.death)))
				exp = e.exp_value
				divied_exp = exp / (len(user.combatants) + 1) # plus one because the active comatant gets a larger share of exp.
				for comb in user.get_available():
					if comb == user.combatant:
						#active combatant gets twice the experience of everyone else
						gained = divied_exp * 2
					else:
						gained = divied_exp
					print("{} gained {} xp".format(comb.name, int(gained)))
					comb.exp += gained

				if enemy_ai.change(user.combatant) is not None:
					print("{} sent out {}".format(enemy_ai.name, e.name))
					display.refresh_combatant()
				else:
					battle_continue = False
					winner = USER

				
		if user.combatant.hp == 0:
			if user.get_standby():
				need_choice = True
				while need_choice:
					change_choice = display.menu(user.get_standby())
					if change_choice is not None:
						user.combatant = change_choice
						print('changed to {}'.format(user.combatant))
						display.refresh_combatant()
						need_choice = False
			else:
				battle_continue = False
				print("{} {}".format(user.combatant.name, random.choice(sayings.death)))
				print('you lost')
				winner = ENEMY
				#TODO: Raise GameOver exception

		display.refresh_combatant()

		time.sleep(1.0 / 60.0)

	#TODO: Check that this does the post battle on each of the users combatants
	for status in user.combatant.status:
		status.post_battle(user.combatant)
	
	if winner == USER:
		print('Got {} for winning'.format(enemy_ai.money))
		print('{}: {}'.format(enemy_ai.name,enemy_ai.defeated_text))

	display.show_messages()

	display.end_battle()

