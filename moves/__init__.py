from constants import *
import utility
import random
import os
import importlib

#from items.items import Item

from moves.moves import Move


from .tags import taglist

__all__ = []

for tag in taglist:
	#__dict__[tag] = []
	exec('{} = []'.format(tag))

all_moves = []

for name in os.listdir('moves'):
	if name.endswith('.py') and not name.startswith('__'):
		module_name = 'moves.' + name[:-3]
		#module = importlib.__import__(module_name)
		module = importlib.import_module(module_name)
		__all__.append(name[:-3])
		for tag in taglist:
			if tag in module.__dict__:
				exec('{} += module.__dict__[tag]'.format(tag))
				exec('all_moves += module.__dict__[tag]'.format(tag))


