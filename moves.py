from main import Move
import random
import elements
import effects

class DamageMove(Move):
	def __init__(self,name, elements, accuracy, power, mp, cost):
		self.name = name
		self.mp = mp
		self.max_mp = mp
		self.mp_cost = cost
		self.accuracy = accuracy
		self.power = power
		self.elements = elements
		self.uses = 0

	def attack(self, user, target): # do whatever the attack needs to do
		print user.name, 'used move', self.name
		hit_chance = ((user.speed/target.speed)/9) + user.accuracy/target.evasion * self.accuracy
		val =  user.physical_strength/target.physical_strength

		damage = ((user.level/100.0 ) * user.physical_strength/target.physical_strength * self.power)

		for atk_element in self.elements:
			for target_element in target.elements:
				damage *= atk_element.effectiveness(target_element)
			for user_element in user.elements:
				if user_element == atk_element:
					damage *= atk_element.bonus

		self.uses += 1

		damage += ((damage + 1) * 3 * min(self.uses, 100.0) / 100.0 + 5) / 10.0
		print 'damage: ', damage

		damage = random.normalvariate(damage, damage/8.0) # normal distribution with stdev of 8% for randomness

		return max(1,damage)



def DamageMoveGen(name, elementlist=None, power=10.0, mp=10.0, cost=1, accuracy=0.9):
	if elementlist == None:
		elementlist = [elements.Normal]
	return lambda: DamageMove(name, elementlist, accuracy, power, mp, cost)

pound = DamageMoveGen('Pound')

class UserModifierMove(Move):
	def __init__(self,name, elementlist, accuracy, mp, cost, effect):
		self.name = name
		self.mp = mp
		self.max_mp = mp
		self.mp_cost = cost
		self.accuracy = accuracy
		self.elements = elementlist
		self.effect = effect
		self.uses = 0

	def attack(self, user, target):
		self.uses += 1
		user.status.append(effect())

def UserModMoveGen(name, effect, elementlist=None, mp=10, cost=1, accuracy=0.9):
	if elementlist == None:
		elementlist = [elements.Normal]
	return lambda: UserModifierMove(name, elementlist, accuracy, mp, cost, effect)

class TargetModifierMove(Move):
	def __init__(self,name, elementlist, accuracy, mp, effect):
		self.name = name
		self.mp = mp
		self.max_mp = mp
		self.mp_cost = cost
		self.accuracy = accuracy
		self.elements = elementlist
		self.effect = effect
		self.uses = 0

	def attack(self, user, target):
		self.uses += 1
		target.status.append(effect())


def TargetModMoveGen(name, effect, elementlist=None, mp=10, cost=1, accuracy=0.9):
	if elementlist == None:
		elementlist = [elements.Normal]
	return lambda: TargetModifierMove(name, elementlist, accuracy, mp, cost, effect)
