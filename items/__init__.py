from constants import *
import utility
import random
import os
import importlib

#from items.items import Item

from items.item import Item
from .backpack import ItemSlot, Backpack


from .tags import taglist

__all__ = []

for tag in taglist:
	#__dict__[tag] = []
	exec('{} = []'.format(tag))

gear_items = {EQUIP_HEAD:[],
              EQUIP_BODY: [],
              EQUIP_RIGHT:[],
              EQUIP_LEFT: [],
              EQUIP_HANDS:[],
              EQUIP_TOKEN:[]}


for name in os.listdir('items'):
	if name.endswith('.py') and not name.startswith('__'):
		module_name = 'items.' + name[:-3]
		#module = importlib.__import__(module_name)
		module = importlib.import_module(module_name)
		__all__.append(name[:-3])
		for tag in taglist:
			if tag in module.__dict__:
				exec('{} += module.__dict__[tag]'.format(tag))
		if 'gear_items' in module.__dict__:
			if EQUIP_HEAD in module.gear_items:
				gear_items[EQUIP_HEAD] += module.gear_items[EQUIP_HEAD]
			if EQUIP_BODY in module.gear_items:
				gear_items[EQUIP_BODY] += module.gear_items[EQUIP_BODY]
			if EQUIP_RIGHT in module.gear_items:
				gear_items[EQUIP_RIGHT] += module.gear_items[EQUIP_RIGHT]
			if EQUIP_LEFT in module.gear_items:
				gear_items[EQUIP_LEFT] += module.gear_items[EQUIP_LEFT]
			if EQUIP_HANDS in module.gear_items:
				gear_items[EQUIP_HANDS] += module.gear_items[EQUIP_HANDS]
			if EQUIP_TOKEN in module.gear_items:
				gear_items[EQUIP_TOKEN] += module.gear_items[EQUIP_TOKEN]



def gen_gear(game, level, equip_position=None, luck_ratio = 1.0):
	all_gear = []
	for sublist in gear_items.values():
		for item in sublist:
			all_gear.append(item)
	if equip_position is None:
		gear = random.choice(all_gear)
	else:
		gear = random.choice(gear_items[equip_position])

	gear = gear(game)

	rand_val = random.random()

	delta_levels = [(tup[0], abs(tup[1] - level)) for tup in base_gear_mod_levels]
	delta_levels.sort(key=lambda x:x[1])
	selected = None
	for tlevel in delta_levels:
		selected = tlevel[0]
		if random.random() / luck_ratio < 0.8:
			break

	if selected is not None:
		utility.add_class_to_instance(gear, selected)
	
	rand_val = random.random()
	level_error = level - gear.level
	delta_levels = [(tup[0], abs(level_error - tup[1])) for tup in general_gear_mod_levels]
	delta_levels.sort(key=lambda x:x[1])
	for level in delta_levels:
		selected = level[0]
		if random.random() / luck_ratio < 0.3:
			break

	if selected is not None:
		utility.add_class_to_instance(gear, selected)

	elemental_mod = random.choice(elemental_gear_mods)
	if random.random() * luck_ratio > 0.80:
		utility.add_class_to_instance(gear, elemental_mod)

	special_mod= random.choice(special_gear_mods)
	if random.random() * luck_ratio > 0.99:
		utility.add_class_to_instance(gear, special_mod)
	return gear



def gen_base_item(game):
	item = random.choice(base_items)
	return item(game)
	
