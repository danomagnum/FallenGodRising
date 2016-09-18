import math
import random
DEBUG = True

def battle(user, enemy):
	battle_continue = True
	while battle_continue:
		print user.name, ' hp: ', int(math.ceil(user.hp)), '/', user.max_hp
		print enemy.name, ' hp: ', int(math.ceil(enemy.hp)), '/', enemy.max_hp

		need_selection = True
		while need_selection:
			i = 0
			for move in user.moves:
				print i, ')', str(move)
				i += 1

			selection = int(input('Which Move?'))
			if selection <= i and selection >= 0:
				need_selection = False

		user_move = user.moves[selection]
		user_target = [user, enemy][user_move.default_target]

		enemy_move = random.choice(enemy.moves)
		enemy_target = [enemy, user][enemy_move.default_target]

		if user.speed >= enemy.speed:
			user_move.attack(user, user_target)
			if enemy.hp > 0:
				enemy_move.attack(enemy, enemy_target)
		else:
			enemy_move.attack(enemy, enemy_target)
			if user.hp > 0:
				user_move.attack(user, user_target)
			
		if enemy.hp == 0:
			battle_continue = False
			print enemy.name, 'fainted'
			exp = enemy.exp_value
			user.exp += exp
			print user.name, 'gained', int(exp), 'xp. ', ((user.level+1) ** 3) - user.exp, 'to go'
				
		if user.hp == 0:
			battle_continue = False
			print user.name, 'fainted'

