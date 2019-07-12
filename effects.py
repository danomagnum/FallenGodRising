from elements import *
import random
from constants import *

class Status(object):
	def __init__(self, name=None):
		if name is None:
			self.name = 'Status'
		else:
			self.name = name
		self.life = 0
		self.max_life = 0
		for base in self.__class__.__bases__:
			try:
				base.config(self)
			except:
				pass

		self.config()
	def config(self, effected):
		pass
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
		pass
	def termination_check(self, effected):
		termination_roll = random.random() * self.life
		if self.max_life > 0:
			if termination_roll > self.max_life:
				return True
		return False

	# todo: actually call this
	def tick(self, effected): # for persistant effects
		self.life += 1
		if self.termination_check(effected):
			print('{} is no longer {}'.format(effected.name, self.name))
			effected.status.remove(self)

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

class StatMod(Status):
	def config(self, multiplier, stat):
		self.multiplier = multiplier
		self.stat = stat
		self.name = '{} {}%'.format(stat,self.multiplier)

	def physical_strength(self, initial):
		if self.stat == PHYSTR:
			return initial * self.multiplier
		else:
			return initial
	def physical_defense(self, initial):
		if self.stat == PHYDEF:
			return initial * self.multiplier
		else:
			return initial
	def special_strength(self, initial):
		if self.stat == SPCSTR:
			return initial * self.multiplier
		else:
			return initial
	def special_defense(self, initial):
		if self.stat == SPCDEF:
			return initial * self.multiplier
		else:
			return initial
	def speed(self, initial):
		if self.stat == SPEED:
			return initial * self.multiplier
		else:
			return initial
	def hp(self, initial):
		if self.stat == HP:
			return initial * self.multiplier
		else:
			return initial
	def max_hp(self, initial):
		if self.stat == MAXHP:
			return initial * self.multiplier
		else:
			return initial
	def evasion(self, initial):
		if self.stat == EVASION:
			return initial * self.multiplier
		else:
			return initial
	def accuracy(self, initial):
		if self.stat == ACCURACY:
			return initial * self.multiplier
		else:
			return initial
	def luck(self, initial):
		if self.stat == LUCK:
			return initial * self.multiplier
		else:
			return initial

class Poison_Minor(Status):
	def config(self):
		self.name = 'Minor Poison'
	def pre_turn(self, effected):
		damage = max(1, effected.hp / 6)
		print('{} was effected by {} for {}'.format(effected.name,self.name, damage))
		effected.hp -= damage

class Poison_Major(Status):
	def config(self):
		self.name = 'Major Poison'
	def pre_turn(self, effected):
		damage = max(1, effected.hp / 3)
		print('{} was effected by {} by {}'.format(effected.name,self.name, damage))
		effected.hp -= damage

