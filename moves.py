import main
import random
import elements
import effects
from utility import clamp, scale


class Pound(main.Move):
	def __init__(self):
		self.name = 'Pound'
		self.mp = 10.0
		self.max_mp = 10.0
		self.accuracy = 0.9
		self.power = 10.0
		self.elements = [elements.Normal]
		self.uses = 0
		self.default_target = main.ENEMY


class Slam(main.Move):
	def __init__(self):
		self.name = 'Slam'
		self.mp = 10.0
		self.max_mp = 10.0
		self.accuracy = 0.9
		self.power = 20.0
		self.elements = [elements.Normal]
		self.uses = 0
		self.default_target = main.ENEMY



class Spray(main.Move):
	def __init__(self):
		self.name = 'Spray'
		self.mp = 10.0
		self.max_mp = 10.0
		self.accuracy = 0.9
		self.power = 20.0
		self.elements = [elements.Water]
		self.uses = 0
		self.default_target = main.ENEMY



class Buff(main.Move):
	def __init__(self):
		self.name = 'Buff'
		self.mp = 10.0
		self.max_mp = 10.0
		self.accuracy = 1
		self.power = 0
		self.elements = [elements.Normal]
		self.uses = 0
		self.default_target = main.SELF

	def effect(self, target):
		target.status.append(effects.Strength_Mult(1.15))


class Heal(main.Move):
	def __init__(self):
		self.name = 'Heal'
		self.mp = 10.0
		self.max_mp = 10.0
		self.accuracy = 1
		self.power = 20
		self.elements = [elements.Normal]
		self.uses = 0
		self.default_target = main.SELF

	def attack(self, user, targets): # do whatever the attack needs to do
		if (self.mp > 0):
			print user.name, 'used move', self.name
			self.mp -= 1
		else:
			print user.name, 'is out of mp to use move', self.name
			self.mp = 0
			if 0.2 > random.random():
				print user.name, 'used move', self.name
			else:
				return
		target_coefficient = 1.1 / len(targets)

		for target in targets:
			hit_chance = ((user.speed/target.speed)/9) + user.accuracy/target.evasion * self.accuracy

			if hit_chance > random.random():
				target.hp += self.power

				self.effect(target)


class Debuff(main.Move):
	def __init__(self):
		self.name = 'Debuff'
		self.mp = 10.0
		self.max_mp = 10.0
		self.accuracy = 1
		self.power = 0
		self.elements = [elements.Normal]
		self.uses = 0
		self.default_target = main.ENEMY

	def effect(self, target):
		target.status.append(effects.Strength_Mult(0.85))

class Poison(main.Move):
	def __init__(self):
		self.name = 'Poison'
		self.mp = 10.0
		self.max_mp = 10.0
		self.accuracy = 0.9
		self.power = 2.0
		self.elements = [elements.Normal]
		self.uses = 0
		self.default_target = main.ENEMY


	def effect(self, target):
		randval = random.random()
		# for starters, poison minorly 20% of the time.  Once the move is more used, poison minorly 95%
		minor_range = scale(self.uses, 0, 1000, 0.2, 0.95)
		# for starters, poison majorly 5% of the time.  Once the move is more used, poison major 50%
		major_range = scale(self.uses, 0, 1000, 0.05, 0.5)
		if randval < major_range:
			target.status.append(effects.Poison_Major())
		elif randval < minor_range:
			target.status.append(effects.Poison_Minor())

