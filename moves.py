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

