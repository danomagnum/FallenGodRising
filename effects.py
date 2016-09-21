from main import Status
from elements import *

class Strength2x(Status):
	def __init__(self):
		self.name = 'Strength 2x'
	def physical_strength(self, initial):
		return initial * 2

class Poison_Minor(Status):
	def __init__(self):
		self.name = 'Minor Poison'
	def pre_turn(self, effected):
		print effected.name, 'was effected by', self.name
		effected.hp -= max(1, effected.hp / 10)
