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
	exec('{} = set()'.format(tag))

gear_items = {EQUIP_HEAD:set(),
              EQUIP_BODY: set(),
              EQUIP_RIGHT:set(),
              EQUIP_LEFT: set(),
              EQUIP_HANDS:set(),
              EQUIP_TOKEN:set()}


for name in os.listdir('items'):
	if name.endswith('.py') and not name.startswith('__'):
		module_name = 'items.' + name[:-3]
		#module = importlib.__import__(module_name)
		module = importlib.import_module(module_name)
		__all__.append(name[:-3])
		for tag in taglist:
			if tag in module.__dict__:
				#exec('{} += module.__dict__[tag]'.format(tag))
				exec('{} = {} | set(module.__dict__[tag])'.format(tag, tag))
		if 'gear_items' in module.__dict__:
			if EQUIP_HEAD in module.gear_items:
				gear_items[EQUIP_HEAD] =  gear_items[EQUIP_HEAD] | set(module.gear_items[EQUIP_HEAD])
			if EQUIP_BODY in module.gear_items:
				gear_items[EQUIP_BODY] = gear_items[EQUIP_BODY] | set(module.gear_items[EQUIP_BODY])
			if EQUIP_RIGHT in module.gear_items:
				gear_items[EQUIP_RIGHT] = gear_items[EQUIP_RIGHT] | set(module.gear_items[EQUIP_RIGHT])
			if EQUIP_LEFT in module.gear_items:
				gear_items[EQUIP_LEFT] = gear_items[EQUIP_LEFT] | set(module.gear_items[EQUIP_LEFT])
			if EQUIP_HANDS in module.gear_items:
				gear_items[EQUIP_HANDS] = gear_items[EQUIP_HANDS]| set(module.gear_items[EQUIP_HANDS])
			if EQUIP_TOKEN in module.gear_items:
				gear_items[EQUIP_TOKEN] = gear_items[EQUIP_TOKEN] | set(module.gear_items[EQUIP_TOKEN])


def gen_gear(game, level, equip_position=None, luck_ratio = 1.0):
	all_gear = []
	for sublist in gear_items.values():
		for item in sublist:
			all_gear.append(item)
	if equip_position is None:
		gear = random.sample(all_gear,1)[0]
	else:
		gear = random.sample(gear_items[equip_position],1)[0]

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

	elemental_mod = random.sample(elemental_gear_mods,1)[0]
	if random.random() * luck_ratio > 0.80:
		utility.add_class_to_instance(gear, elemental_mod)

	special_mod = random.sample(special_gear_mods,1)[0]
	if random.random() * luck_ratio > 0.99:
		utility.add_class_to_instance(gear, special_mod)
	return gear



def gen_base_item(game):
	#item = random.choice(base_items)
	item = random.sample(base_items,1)[0]
	return item(game)
	
