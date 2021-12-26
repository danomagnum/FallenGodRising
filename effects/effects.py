from elements import *
import random
from constants import *
import utility

class Status(object):
	def __init__(self, name=None):
		if name is None:
			self.name = 'Status'
		else:
			self.name = name
		self.life = 0
		self.max_life = 0
		utility.call_all('config', self)
		self._helptext = ''

		self.config()
	def helptext(self):
		return self._helptext
	def config(self):
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
			print('{} lost status {}'.format(effected.name, self.name))
			effected.status.remove(self)

	def physical_strength(self, initial): # passive stat boosts take effect on these routines
		return initial
	def physical_defense(self, initial):
		return initial
	def arcane_strength(self, initial):
		return initial
	def arcane_defense(self, initial):
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
	def __str__(self):
		return self.name

class StatMod(Status):
	def __init__(self, multiplier, stat, name=None):
		self.multiplier = multiplier
		self.stat = stat
		self._helptext = ''
		Status.__init__(self, name=name)
	def config(self):
		typestr = ''
		if self.stat == PHYSTR:
			typestr = 'PStr'
		elif self.stat == PHYDEF:
			typestr = 'PDef'
		elif self.stat == SPCSTR:
			typestr = 'SStr'
		elif self.stat == SPCDEF:
			typestr = 'SDef'
		elif self.stat == SPEED:
			typestr = 'Spd'
		elif self.stat == HP:
			typestr = 'HP'
		elif self.stat == MAXHP:
			typestr = 'HP'
		elif self.stat == LUCK:
			typestr = 'Lck'
		elif self.stat == ACCURACY:
			typestr = 'Acc'
		elif self.stat == EVASION:
			typestr = 'Evd'
		
		multstr = ''
		if self.multiplier > 1.5:
			multstr = '++'
		elif self.multiplier > 1:
			multstr = '+'
		elif self.multiplier < 1:
			multstr = '-'
		elif self.multiplier < 0.5:
			multstr = '--'
		else:
			multstr = ''
		self._helptext += '{} {}%'.format(self.stat,int(self.multiplier * 100))
		self.name = typestr + multstr
		self.max_life = 5

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
	def arcane_strength(self, initial):
		if self.stat == SPCSTR:
			return initial * self.multiplier
		else:
			return initial
	def arcane_defense(self, initial):
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


#starters = [Debug]


