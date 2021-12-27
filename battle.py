import math
import random
import time
import main
import sayings
import settings
import sys
import utility
from constants import *

DEBUG = True
SLOWDOWN = 0.5

class AI(object):
	def attack(self, enemy_ai):
		move = random.choice(self.combatant.moves)
		enemy = random.choice(enemy_ai.get_available())
		t = move.default_target
		if t == SELF:
			target = [self.combatant]
		elif t == ENEMY:
			target = [enemy]
		elif t == ANY:
			target = [random.choice([self.combatant, enemy])]
		elif t == ALLY:
			target = [random.choice(self.combatants)]
		elif t == MULTI_ALLY:
			target = self.combatants
		elif t == MULTI_ENEMY:
			target = enemy_ai.get_available()
		elif t == MULTI_ALL:
			target = self.get_available() + enemy_ai.get_available()
		elif t == ACTIVE:
			target = [enemy_ai.combatant]
		elif t == INACTIVE:
			target = [random.choice(enemy_ai.get_standby())]
		elif t == RAND_ENEMY:
			target = [enemy]
		elif t == RAND_ALLY:
			target = [random.choice(self.combatants)]
		#target = [self.combatant, enemy][move.default_target]
		return [move, target]

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
			action = ATTACK
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
			target = [self.combatant]
		elif t == ENEMY:
			target = [enemy]
		elif t == ANY:
			target = [random.choice([self.combatant, enemy])]
		elif t == ALLY:
			target = [random.choice(self.combatants)]
		elif t == MULTI_ALLY:
			target = self.combatants
		elif t == MULTI_ENEMY:
			target = enemy_ai.get_available()
		elif t == MULTI_ALL:
			target = self.get_available() + enemy_ai.get_available()
		elif t == ACTIVE:
			target = [enemy_ai.combatant]
		elif t == INACTIVE:
			target = [random.choice(enemy_ai.get_standby())]
		elif t == RAND_ENEMY:
			target = [enemy]
		elif t == RAND_ALLY:
			target = [random.choice(self.combatants)]
		#target = [self.combatant, enemy][move.default_target]
		return [move, target]


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
			action = random.choice([ATTACK, SWITCH, ATTACK, ATTACK, ATTACK, ATTACK])
			return action
		else:
			action = random.choice([ATTACK, ATTACK, ATTACK, ATTACK, ATTACK])
			return action


class Skiddish_AI(AI):
	def attack(self, enemy_ai):
		move = random.choice(self.combatant.moves)
		enemy = random.choice(enemy_ai.get_available())
		t = move.default_target
		if t == SELF:
			target = [self.combatant]
		elif t == ENEMY:
			target = [enemy]
		elif t == ANY:
			target = [random.choice([self.combatant, enemy])]
		elif t == ALLY:
			target = [random.choice(self.combatants)]
		elif t == MULTI_ALLY:
			target = self.combatants
		elif t == MULTI_ENEMY:
			target = enemy_ai.get_available()
		elif t == MULTI_ALL:
			target = self.get_available() + enemy_ai.get_available()
		elif t == ACTIVE:
			target = [enemy_ai.combatant]
		elif t == INACTIVE:
			target = [random.choice(enemy_ai.get_standby())]
		elif t == RAND_ENEMY:
			target = [enemy]
		elif t == RAND_ALLY:
			target = [random.choice(self.combatants)]
		#target = [self.combatant, enemy][move.default_target]
		return [move, target]


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
		if random.random() > run_chance * 10:
			self.battle_run()
			#return RUN
			return ATTACK
		if self.get_standby():
			return random.choice([ATTACK, SWITCH])
		else:
			return random.choice([ATTACK, ATTACK])

###########################################
##  Battle Actions
###########################################

class Action(object):
	@property
	def Priority(self):
		return 100

	def Execute(self, battle):
		pass

class NoAction(Action):
	pass

class UserAttack(Action):
	def __init__(self, user, move, target):
		self.user = user
		self.move = move
		self.target = target

	@property
	def Priority(self):
		return self.user.speed

	def Execute(self, battle):
		self.move.attack(self.user, self.target)

class UserItem(Action):
	def __init__(self, item, target):
		self.item = item
		self.target = target
	def Execute(self, battle):
		if len(self.target) > 0:
			item_used = self.item.take()
			selection_needed = False
			for t in self.target:
				item_used.use(t)

	@property
	def Priority(self):
		return 100 + self.item.value

class EnemyChange(Action):
	def __init__(self, enemy_ai, user):
		self.enemy_ai = enemy_ai
		self.user = user

	def Execute(self, battle):
		self.enemy_ai.change(self.user)

	@property
	def Priority(self):
		return 300


class UserChange(Action):
	def __init__(self, user):
		self.user = user

	def Execute(self, battle):
		if self.user.get_standby():
			change_choice = battle.game.display.battlemenu(self.user.get_standby())
			if change_choice is not None:
				self.user.combatant = change_choice

	@property
	def Priority(self):
		return 300

class ActionRun(Action):
	@property
	def Priority(self):
		return 25

	def Execute(self, battle):
		battle.running = False


class UserPosses(Action):
	@property
	def Priority(self):
		return 301

	def Execute(self, battle):
		battle.possess_tries += 1
		selection_needed = False

		possess_candidate = battle.valid_enemies[0]
		hp_ratio = 1.0 - (
				possess_candidate.hp / possess_candidate.max_hp) ** 0.5  # square root to make weakening further get more and more advantageous
		attempt_ratio = 1.0 - utility.clamp(battle.possess_tries / 100.0, 1.0,
											0.3)  # the more your try, the harder it gets

		chance = hp_ratio * attempt_ratio
		if random.random() < chance:
			possess = possess_candidate
			winner = USER
			battle_continue = False
			print('Possessed {}'.format(possess.name))
			battle.player.combatants.append(possess)
			battle.enemy_ai.cobatants.remove(possess)
		else:
			print('Possession Attempt {} Was Unsuccessful.'.format(battle.possess_tries))



###########################################
##  Battle Logic
###########################################

class Battle(object):
	def __init__(self, game, user, enemy_ai):
		self.game = game
		self.user = user
		self.enemy_ai = enemy_ai

		game.player.target_map = None # cancel any auto-moves if we got in a battle

		self.old_music = game.music

		self.refresh_combatants()

		self.possess_tries = 0

		self.first_choice = None
		self.user_move = None
		self.user_item = None

		self.running = True

		self.game.display.enemy = self.enemy_ai

		if settings.battle_mode == 2:
			self.prebattle()
			self.realtime()
		else:
			self.prebattle()
			self.start_battle()
			while self.running:
				self.run_turn()

		if not self.running:
			self.end_battle()


	def realtime(self):
		self.game.display.enemy = self.enemy_ai
		self.run_turn()
		self.user.purge_dead()
		if not self.running:
			self.end_battle()

	def end_battle(self):
		pass
		self.game.display.show_btl_messages()

		self.game.display.end_battle()

		self.user.purge_dead()

		self.game.set_music(self.old_music)


	def start_battle(self):
		self.game.set_music(self.enemy_ai.music)
		if settings.battle_anim:
			self.game.display.flash_screen()
		self.prebattle()

		if settings.battle_speed > 1:
			self.game.display.show_btl_messages()
			time.sleep(SLOWDOWN)
			if settings.battle_speed > 3:
				self.game.display.mapbox.getch()


	def prebattle(self):
		# make sure all pre-battle status take effect
		for combatant in self.all_combatants:
			for status in combatant.status:
				status.pre_battle(combatant)
		self.game.display.refresh_combatant()

	def preturn(self):
		# make sure all pre-turn status take effect
		for combatant in self.all_combatants:
			for status in combatant.status:
				status.pre_turn(combatant)
		self.game.display.refresh_combatant()

	def posturn(self):
		# make sure all post-turn status take place
		for combatant in self.all_combatants:
			for status in combatant.status:
				status.post_turn(combatant)
		self.game.display.refresh_combatant()

	def postbattle(self):
		# make sure all post-battle status take place
		for combatant in self.user.combatants:
			for status in combatant.status:
				status.post_battle(combatant)

	def refresh_combatants(self):
		self.valid_users = self.user.get_available()
		self.valid_enemies = self.enemy_ai.get_available()
		self.all_combatants = self.valid_users + self.valid_enemies

	def get_enemy_action(self):

		attempts = 0
		while attempts < 5:
			attempts += 1
			# have the enemy select a move and target
			enemy_decision = self.enemy_ai.action(self.user)

			if enemy_decision == ATTACK:
				enemy_move, enemy_target = self.enemy_ai.attack(self.user)
				return UserAttack(user=self.enemy_ai.combatant,
								  move=enemy_move,
								  target=enemy_target)
			elif enemy_decision == SWITCH:
				if settings.battle_mode == 0:
					self.enemy_ai.change(self.user)
				else:
					return EnemyChange(self.enemy_ai, self.user)

			elif enemy_decision == RUN:
				self.enemy_ai.running = True
				print('Enemy Is Running')

		return NoAction()


	def get_user_action_realtime(self):
		pass

	def get_user_action_turnbased(self):
		# have the user select an action
		selected_action = None

		# if we have three users, we can't posses.  If we have one we can't change.  Here we decide what menu
		# to show accordingly
		if len(self.valid_users) < 3 and len(self.valid_enemies) == 1:
			if len(self.valid_users) > 1:
				choices = ['Attack', 'Change', 'Items', 'Run', 'Possess']
			else:
				choices = ['Attack', 'Items', 'Run', 'Possess']
		else:
			if len(self.valid_users) > 1:
				choices = ['Attack', 'Change', 'Items', 'Run']
			else:
				choices = ['Attack', 'Items', 'Run']

		while not selected_action:
			# if the enemy died outside of active combat (from poison or something) this check will
			# end the battle by "running" and the final checks will take care of the rest, dosing out
			# exp and items like you won
			if len(self.enemy_ai.get_available()) == 0:
				return ActionRun()

			self.first_choice = self.game.display.battlemenu(choices, cols=2, selected=self.first_choice)

			if self.first_choice == 'Attack':
				self.user_move = self.game.display.battlemenu(self.user.combatant.moves, cols=2, selected=self.user_move)
				if self.user_move is not None:
					target = self.user_move.default_target
					if target == main.ALLY:
						selected_target = self.game.display.battlemenu(self.user.get_available(), selected=self.user.combatant)
						if selected_target is not None:
							return UserAttack(user=self.user.combatant,
											 move=self.user_move,
											 target=[selected_target])
					if target == main.SELF:

						return UserAttack(user=self.user.combatant,
										 move=self.user_move,
										 target=[self.user.combatant])

					elif target == main.ANY:
						selected_target = self.game.display.battlemenu(self.user.get_available() + self.enemy_ai.get_available(),
																  selected=self.user.combatant)
						if selected_target is not None:
							return UserAttack(user=self.user.combatant,
											 move=self.user_move,
											 target=[selected_target])

					elif target == main.ENEMY:
						if len(self.enemy_ai.get_available()) > 1:
							selected_target = self.game.display.battlemenu(self.enemy_ai.get_available(),
																	  selected=selected_target)
							if selected_target is not None:
								return UserAttack(user=self.user.combatant,
												 move=self.user_move,
												 target=[selected_target])
						else:
							return UserAttack(user=self.user.combatant,
											 move=self.user_move,
											 target=self.enemy_ai.get_available())
					elif target == main.ACTIVE:
						return UserAttack(user=self.user.combatant,
										 move=self.user_move,
										 target=[self.enemy_ai.combatant])
					elif target == main.MULTI_ENEMY:
						return UserAttack(user=self.user.combatant,
										 move=self.user_move,
										 target=self.enemy_ai.get_available())
					elif target == main.MULTI_ALLY:
						return UserAttack(user=self.user.combatant,
										 move=self.user_move,
										 target=self.user.get_available())
					elif target == main.MULTI_ALL:
						return UserAttack(user=self.user.combatant,
										 move=self.user_move,
										 target=self.user.get_available() + self.enemy_ai.get_available())
					elif target == main.INACTIVE:
						standby = self.enemy_ai.get_standby()
						return UserAttack(user=self.user.combatant,
										 move=self.user_move,
										 target=[random.choice(standby)])
					elif target == main.RAND_ENEMY:
						return UserAttack(user=self.user.combatant,
										 move=self.user_move,
										 target=[random.choice(self.enemy_ai.get_available())])
					elif target == main.RAND_ALLY:
						return UserAttack(user=self.user.combatant,
										 move=self.user_move,
										 target=[random.choice(self.user.get_available())])

			elif self.first_choice == 'Change':
				if settings.battle_mode == 1:
					# if we are in "turn choice" mode we lose our turn
					return UserChange(self.user)
				else:
					# if we are in "free choice" mode we don't
					if self.user.get_standby():
						change_choice = self.game.display.battlemenu(self.user.get_standby())
						if change_choice is not None:
							self.user.combatant = change_choice
							self.game.display.refresh_combatant()

			elif self.first_choice == 'Items':
				item_slot_used = self.game.display.battlemenu(self.user.backpack.show(), cols=2)
				if item_slot_used is not None:
					item_target_type = item_slot_used.target_type
					if item_target_type == ALLY:
						item_target = [self.game.display.battlemenu(self.user.combatants, cols=2)]
					elif item_target_type == SELF:
						item_target = self.user.combatant
					elif item_target_type == ENEMY:
						item_target = [self.game.display.battlemenu(self.enemy_ai.combatants, cols=2)]
					elif item_target_type == MULTI_ALLY:
						item_target = self.user.combatants
					elif item_target_type == MULTI_ENEMY:
						item_target = self.enemy_ai.combatants
					elif item_target_type == ANY:
						item_target = [self.game.display.battlemenu(self.user.get_available() + self.enemy_ai.get_available(),
															   selected=self.user.combatant, cols=2)]
					else:
						item_target = None
						print("Can't use that now")
					if item_target is not None:
						return UserItem(item=item_slot_used,
										target=item_target)

			elif self.first_choice == 'Possess':
				return UserPosses(self)

			elif self.first_choice == 'Run':
				return ActionRun()

	def run_turn(self):
		self.game.display.show_btl_messages()
		self.refresh_combatants()

		self.preturn()

		if settings.battle_speed > 1:
			self.game.display.show_btl_messages()
			time.sleep(SLOWDOWN)
			if settings.battle_speed > 3:
				self.game.display.mapbox.getch()


		if settings.battle_mode == 2:
			user_action = self.get_user_action_realtime()
		else:
			user_action = self.get_user_action_turnbased()

		enemy_action = self.get_enemy_action()

		actions = [user_action, enemy_action]
		sorted_actions = sorted(actions, key=lambda x: -x.Priority)

		for action in sorted_actions:
			action.Execute(self)
			self.game.display.refresh_combatant()

			if settings.battle_speed > 0:
				self.game.display.show_btl_messages()
				time.sleep(SLOWDOWN)
				if settings.battle_speed > 3:
					self.game.display.mapbox.getch()

			if not self.running:
				break;

		self.game.display.show_btl_messages()
		self.posturn()

		if settings.battle_speed > 1:
			self.game.display.show_btl_messages()
			time.sleep(SLOWDOWN)
			if settings.battle_speed > 3:
				self.game.display.mapbox.getch()

		if len(self.enemy_ai.get_available()) == 0:
			battle_continue = False
			winner = USER

		# check for any deaths
		for e in self.valid_enemies:
			if e.hp == 0:
				print("{}: {}".format(e.name, random.choice(sayings.death)))
				exp = e.exp_value
				divied_exp = max(1, exp / (
							len(self.user.combatants) + 1))  # plus one because the active comatant gets a larger share of exp.
				for comb in self.user.get_available():
					if comb == self.user.combatant:
						# active combatant gets twice the experience of everyone else
						gained = divied_exp * 2
					else:
						gained = divied_exp
					print("{} gained {} xp".format(comb.name, int(gained)))
					comb.exp += gained

				if self.enemy_ai.change(self.user.combatant) is not None:
					# print("{} sent out {}".format(enemy_ai.name, e.name))
					self.game.display.refresh_combatant()
				else:
					battle_continue = False
					winner = USER

		if self.user.combatant.hp == 0:
			if self.user.get_standby():
				need_choice = True
				while need_choice:
					change_choice = self.game.display.battlemenu(self.user.get_standby())
					if change_choice is not None:
						self.user.combatant = change_choice
						print('changed to {}'.format(self.user.combatant))
						self.game.display.refresh_combatant()
						need_choice = False
			else:
				battle_continue = False
				print("{} {}".format(self.user.combatant.name, random.choice(sayings.death)))
				print('you lost')
				winner = ENEMY
				raise main.GameOver()

		self.game.display.refresh_combatant()

		for c in self.user.get_available():
			c.battletick()
		for c in self.enemy_ai.get_available():
			c.battletick()

		self.game.ticks += 1

