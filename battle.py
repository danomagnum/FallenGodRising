import math
import random
import time
DEBUG = True

class Random_AI(object):
	def __init__(self, name='AI'):
		self.name = name
		pass
	def attack(self, user, enemy):
		move = random.choice(user.moves)
		target = [user, enemy][move.default_target]
		return [move, target]
	def change(self, valid_list, enemy):
		return random.choice(valid_list)
	
def Battle(users, enemies, display, AI):
	user = users[0]
	enemy = enemies[0]
	all_combatants = users + enemies
	battle_continue = True
	last_attack = 0

	#make sure all pre-battle status take effect
	for combatant in all_combatants:
		for status in combatant.status:
			status.pre_battle(combatant)

	while battle_continue:
		#make sure all pre-turn status take effect
		for combatant in all_combatants:
			for status in combatant.status:
				status.pre_turn(combatant)

		user_move = display.menu(user.moves, cols=2, selected=last_attack)
		for move_id in xrange(len(user.moves)):
			if user.moves[move_id] == user_move:
				last_attack = move_id

		user_target = [user, enemy][user_move.default_target]

		enemy_move, enemy_target = AI.attack(enemy, user)

		if user.speed >= enemy.speed:
			for status in user.status:
				status.pre_attack(user)

			user_move.attack(user, user_target)

			for status in user.status:
				status.post_attack(user)

			display.refresh_mon()
			display.show_messages()
			if enemy.hp > 0:

				for status in enemy.status:
					status.pre_attack(enemy)

				enemy_move.attack(enemy, enemy_target)

				for status in enemy.status:
					status.post_attack(enemy)

				display.refresh_mon()
				display.show_messages()
		else:
			for status in enemy.status:
				status.pre_attack(enemy)
			enemy_move.attack(enemy, enemy_target)
			for status in enemy.status:
				status.post_attack(enemy)
			display.refresh_mon()
			display.show_messages()
			if user.hp > 0:
				for status in user.status:
					status.pre_attack(user)
				user_move.attack(user, user_target)
				for status in user.status:
					status.post_attack(user)
				display.refresh_mon()
				display.show_messages()

		# check for any deaths
		if enemy.hp == 0:
			print enemy.name, 'fainted'
			exp = enemy.exp_value
			print user.name, 'gained', int(exp), 'xp. ', ((user.level+1) ** 3) - user.exp, 'to go'
			user.exp += exp

			valid_combatants = [ combatant for combatant in enemies if combatant.hp > 0 ]
			if valid_combatants:
				enemy = AI.change(valid_combatants, user)
				print AI.name, 'sent out', enemy.name
				display.enemy = enemy
				display.refresh_mon()
			else:
				battle_continue = False

				
		if user.hp == 0:
			battle_continue = False
			print user.name, 'fainted'

		display.refresh_mon()

		# make sure all post-turn status take place
		for combatant in all_combatants:
			for status in combatant.status:
				status.post_turn(combatant)

		display.show_messages()
		display.screen.refresh()
		time.sleep(1.0 / 60.0)
	for status in user.status:
		status.post_battle(user)


