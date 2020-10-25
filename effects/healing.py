from .effects import Status, StatMod
from elements import *
import random
from constants import *
import utility

class Recovery(Status):
	def config(self):
		self.name = 'Recovery'
		self.max_life = 5
	def post_turn(self, effected):
		effected.hp = effected.hp * 1.15

basic = [Recovery]
#advanced = [Poison_Major]
