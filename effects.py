from main import Status
from elements import *

class Strength2x(Status):
	def __init__(self):
		self.name = 'Strength 2x'
	def physical_strength(self, initial):
		return initial * 2

class Strength_Mult(Status):
	def __init__(self, multiplier):
		self.multiplier = multiplier
		self.name = 'Strength ' + str(self.multiplier) + '%'
	def physical_strength(self, initial):
		return initial * self.multiplier



class Poison_Minor(Status):
	def __init__(self):
		self.name = 'Minor Poison'
	def pre_turn(self, effected):
		print('{} was effected by {}'.format(effected.name,self.name))
		effected.hp -= max(1, effected.hp / 10)

class Poison_Major(Status):
	def __init__(self):
		self.name = 'Major Poison'
	def pre_turn(self, effected):
		print('{} was effected by {}'.format(effected.name,self.name))
		effected.hp -= max(1, effected.hp / 6)


