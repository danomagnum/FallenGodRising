from .effects import Status, StatMod
from elements import *
import random
from constants import *
import utility

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

class Bleeding(Status):
	def config(self):
		self.name = 'Bleeding'
		self.max_life = 5
	def post_turn(self, effected):
		damage = max(1, effected.hp / 20)
		print('{} was effected by {} for {}'.format(effected.name,self.name, damage))
		effected.hp -= damage

class Drain(Status):
	def config(self):
		self.name = 'Drain'
		self.max_life = 5
	def pre_turn(self, effected):
		move = random.choice(effected.moves)
		move.mp -= 1
		print('{} lost 1 mp on move {} from {}. {} mp remain'.format(effected.name,move.name, self.name, move.mp))


basic = [Poison_Minor, Bleeding]
advanced = [Poison_Major]
