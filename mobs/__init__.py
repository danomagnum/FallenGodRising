from constants import *
import utility
import random
import os
import importlib

#from items.items import Item

from mobs.characters import Character 
from .tags import taglist

__all__ = []

for tag in taglist:
	#__dict__[tag] = []
	exec('{} = set()'.format(tag))


for name in os.listdir('mobs'):
	if name.endswith('.py') and not name.startswith('__'):
		module_name = 'mobs.' + name[:-3]
		#module = importlib.__import__(module_name)
		module = importlib.import_module(module_name)
		__all__.append(name[:-3])
		for tag in taglist:
			if tag in module.__dict__:
				exec('{} = {} | set(module.__dict__[tag])'.format(tag, tag))


def party(game, battle_AI, world_AI, level, combatants, name=None, item_list = None):
	#class Generated(world_AI,battle_AI, utility.Serializable):
	class Generated(battle_AI, world_AI, utility.Serializable):
		# example basic enemy
		def config(self):
			self.name = name
			for c in combatants:
				try:
					instance = c(game, level=level)
					instance.spawn_element()
					self.combatants.append(c(game, level=level))
				except:
					c.spawn_element()
					self.combatants.append(c)
			if self.name is None:
				self.name = self.combatants[0].name
			self.char = self.name[0]
	return Generated(game)


