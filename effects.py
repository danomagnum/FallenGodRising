from elements import *

class Status(object):
	def __init__(self, name=None):
		if name is None:
			self.name = 'Status'
		else:
			self.name = name
		self.expired = False
	def pre_battle(self, effected):
		pass
	def pre_turn(self, effected):
		pass
	def pre_attack(self, effected):
		pass
	def allow_attack(self, effected): # something like paralyze would use this to prevent attacking.
		return True
	def post_attack(self, effected): # things like poison should happen here.
		pass
	def post_turn(self, effected):
		pass
	def post_battle(self, effected): # remove yourself at the end of a battle if needed
		effected.status.remove(self)
	def tick(self, effected): # for persistant effects
		pass
	def physical_strength(self, initial): # passive stat boosts take effect on these routines
		return initial
	def physical_defense(self, initial):
		return initial
	def special_strength(self, initial):
		return initial
	def special_defense(self, initial):
		return initial
	def speed(self, initial):
		return initial
	def hp(self, initial):
		return initial
	def max_hp(self, initial):
		return initial
	def evasion(self, initial):
		return initial
	def accuracy(self, initial):
		return initial
	def luck(self, initial):
		return initial



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


