from constants import *
import random
from .item import Item

class ExpBoost(Item):
	def config(self):
		self.name = 'Knowledge Shard'
		self.weigth = 1
		self.target_type = ANY
		self.value = 100
		self.rarity = 0.01
		self._helptext = 'Gain Some EXP.'
		self.char = '\x0E'

	def use(self, target):
		exp0 = target.exp_at_level(target.level)
		exp1 = target.exp_at_level(target.level + 1)
		exp_delta = exp1 - exp0 + 1
		target.exp += exp_delta
		print('{} used {} and gained {} exp.'.format(target.name,self.name, exp_delta))


class StrBoost(Item):
	def config(self):
		self.name = 'Steel Shard'
		self.weigth = 1
		self.target_type = ANY
		self.value = 100
		self.rarity = 0.01
		self._helptext = 'Permanently Boost Strength'
		self.char = '\x0E'

	def use(self, target):
		gain = random.randint(1, 5)
		target.base_physical_strength += gain
		print('{} used {} and gained {} physical str.'.format(target.name,self.name, gain))
		
class DefBoost(Item):
	def config(self):
		self.name = 'Stone Shard'
		self.weigth = 1
		self.target_type = ANY
		self.value = 100
		self.rarity = 0.01
		self._helptext = 'Permanently Boost Defense'
		self.char = '\x0E'

	def use(self, target):
		gain = random.randint(1, 5)
		target.base_physical_defense += gain
		print('{} used {} and gained {} physical def.'.format(target.name,self.name, gain))
	
class ArcStrBoost(Item):
	def config(self):
		self.name = 'Light Shard'
		self.weigth = 1
		self.target_type = ANY
		self.value = 100
		self.rarity = 0.01
		self._helptext = 'Permanently Boost Arcane Strength'
		self.char = '\x0E'

	def use(self, target):
		gain = random.randint(1, 5)
		target.base_arcane_strength += gain
		print('{} used {} and gained {} arcane str.'.format(target.name,self.name, gain))
	
class ArcDefBoost(Item):
	def config(self):
		self.name = 'Shade Shard'
		self.weigth = 1
		self.target_type = ANY
		self.value = 100
		self.rarity = 0.01
		self._helptext = 'Permanently Boost Arcane Defense'
		self.char = '\x0E'

	def use(self, target):
		gain = random.randint(1, 5)
		target.base_arcane_defense += gain
		print('{} used {} and gained {} arcane def.'.format(target.name,self.name, gain))

class SpdBoost(Item):
	def config(self):
		self.name = 'Time Shard'
		self.weigth = 1
		self.target_type = ANY
		self.value = 100
		self.rarity = 0.01
		self._helptext = 'Permanently Boost Speed'
		self.char = '\x0E'

	def use(self, target):
		gain = random.randint(1, 5)
		target.base_speed += gain
		print('{} used {} and gained {} speed'.format(target.name,self.name, gain))

class LuckBoost(Item):
	def config(self):
		self.name = 'Chance Shard'
		self.weigth = 1
		self.target_type = ANY
		self.value = 100
		self.rarity = 0.01
		self._helptext = 'Permanently Boost Luck'
		self.char = '\x0E'

	def use(self, target):
		gain = random.randint(1, 5)
		target.base_luck += gain
		print('{} used {} and gained {} luck'.format(target.name,self.name, gain))


class MoveBoost(Item):
	def config(self):
		self.name = 'Action Shard'
		self.weigth = 1
		self.target_type = ANY
		self.value = 100
		self.rarity = 0.01
		self._helptext = 'Permanently Boost Moves'
		self.char = '\x0E'

	def use(self, target):
		for move in target.moves:
			gain = random.randint(1, 2)
			move.max_mp += gain
			print("{}'s move {} gained {} max mp.".format(target.name,move.name, gain))
	


base_items = [ExpBoost, StrBoost, DefBoost, ArcStrBoost, ArcDefBoost, SpdBoost, LuckBoost]
