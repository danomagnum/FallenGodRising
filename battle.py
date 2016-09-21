import math
import random
import time
DEBUG = True

ATTACK = 0
SWITCH = 1
ITEM = 2

class Random_AI(object):
	def __init__(self, combatants, money=0, name='AI', items=None, defeated_text='Oh Snap! I lost!'):
		self.name = name
		self.combatants = combatants
		self.combatant = combatants[0]
		self.defeated_text = defeated_text

		if money == 0:
			self.money = int(sum([c.exp_value for c in combatants]) / 10)
		else:
			self.money = money

		if items is not None:
			self.items = items
		else:
			self.items = []

	def attack(self, enemy):
		move = random.choice(self.combatant.moves)
		target = [self.combatant, enemy][move.default_target]
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
			return random.choice([ATTACK, SWITCH])
		else:
			return ATTACK
	
	def get_available(self):
		return [ combatant for combatant in self.combatants if combatant.hp > 0 ] 
	
	def get_standby(self):
		return [ combatant for combatant in self.combatants if (combatant.hp > 0) and combatant != self.combatant ] 
	
def Battle(user_combatants, enemy_ai, display):
	user = user_combatants[0]
	valid_users = [ combatant for combatant in user_combatants if combatant.hp > 0 ]
	valid_enemies = enemy_ai.get_available()
	all_combatants = valid_users + valid_enemies

	battle_continue = True
	last_attack = 0

	#make sure all pre-battle status take effect
	for combatant in all_combatants:
		for status in combatant.status:
			status.pre_battle(combatant)
	display.refresh_combatant()

	while battle_continue:
		valid_users = [ combatant for combatant in user_combatants if combatant.hp > 0 ]
		valid_enemies = enemy_ai.get_available()
		all_combatants = valid_users + valid_enemies

		#make sure all pre-turn status take effect
		for combatant in all_combatants:
			for status in combatant.status:
				status.pre_turn(combatant)
		display.refresh_combatant()

		#have the user select a move
		user_move = display.menu(user.moves, cols=2, selected=last_attack)
		for move_id in xrange(len(user.moves)):
			if user.moves[move_id] == user_move:
				last_attack = move_id
		user_is_attacking = True

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
			display.enemy = enemy_ai.combatant
			print enemy_ai.name, 'switched to', enemy_ai.combatant.name
			display.refresh_combatant()

		#select the target of the user's move. Have to do this after the enemy has
		#gone so that you target their new combatant if they switch or something
		if user_is_attacking:
			user_target = [user, enemy_ai.combatant][user_move.default_target]

		#decide who should attack first
		if user.speed >= enemy_ai.combatant.speed:
			first = user
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
			second = user
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
		if enemy_ai.combatant.hp == 0:
			print enemy_ai.combatant.name, 'fainted'
			exp = enemy_ai.combatant.exp_value
			print user.name, 'gained', int(exp), 'xp. ', ((user.level+1) ** 3) - user.exp, 'to go'
			user.exp += exp

			if enemy_ai.change(user) is not None:
				print enemy_ai.name, 'sent out', enemy_ai.combatant.name
				display.enemy = enemy_ai.combatant
				display.refresh_combatant()
			else:
				battle_continue = False

				
		if user.hp == 0:
			battle_continue = False
			print user.name, 'fainted'

		display.refresh_combatant()

		time.sleep(1.0 / 60.0)
	for status in user.status:
		status.post_battle(user)
	
	print 'Got', enemy_ai.money, 'for winning'
	print enemy_ai.name, ':', enemy_ai.defeated_text

	display.show_messages()

