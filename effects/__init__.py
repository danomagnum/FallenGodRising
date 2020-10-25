from constants import *
import utility
import random
import os
import importlib

#from items.items import Item

#from mobs.characters import Character 
from effects.effects import Status, StatMod
from .tags import taglist

__all__ = []

for tag in taglist:
	#__dict__[tag] = []
	exec('{} = []'.format(tag))


for name in os.listdir('effects'):
	if name.endswith('.py') and not name.startswith('__'):
		module_name = 'effects.' + name[:-3]
		#module = importlib.__import__(module_name)
		module = importlib.import_module(module_name)
		__all__.append(name[:-3])
		for tag in taglist:
			if tag in module.__dict__:
				exec('{} += module.__dict__[tag]'.format(tag))

