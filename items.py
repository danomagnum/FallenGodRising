from constants import *
import effects
import elements
import utility
import inspect

class Item(object):
	def __init__(self, game, name=None, target=TARGET_NONE, use=None):
		self.game = game
		self.prefixes = []
		self.suffixes = []
		self._name = name
		self.target_type = target
		self.weight = 0
		self.value = 0
		self.rarity = 0.5
		self.helptext = ''
		if use is not None:
			self.use = use
	
		#utility.call_all_configs(self)
		utility.call_all('config', self)

	@property
	def name(self):
		namestr = ''
		namestr = ' '.join(self.prefixes)
		if namestr != '':
			namestr += ' '
		namestr += self._name
		namestr += ' '.join(self.suffixes)
		return namestr

	@name.setter
	def name(self, value):
		self._name = value

	def config(self):
		pass

	def use(self, target = None):
		pass
	def __str__(self):
		return self.name

class Gear(Item):

	def __init__(self, game, name=None, target=TARGET_NONE, use=None):
		self.status = []
		Item.__init__(self, game, name, target=TARGET_NONE, use=None)

	def use(self, target):
		return_items = target.equipment.equip(self)
		for item in return_items:
			self.game.player.backpack.store(item)
			print('{} unequipped {}'.format(target.name,item.name))
		print('{} equipped {}'.format(target.name,self.name))

	def config(self):
		pass

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
	def defend(self, damage, wearer, attacker):
		return damage
	def attack(self, damage, wearer, defender):
		return damage

	def elements(self, element_list):
		#element_list is a list containing all elements. Return a new list of all
		#elements with this item considered
		#TODO: split this into attack_elements and defense_elements
		return element_list

	def tick(self, wearer):
		pass
	def subtick(self, wearer):
		for stat in self.status:
			stat.tick(wearer)



class ItemSlot(list):
	def __init__(self, game, backpack, item):
		self.name = item.name
		self.backpack = backpack
		list.__init__(self,[item])
		self.target_type = item.target_type

	def add_item(self, item):
		self.append(item)

	def cost(self):
		return self[0].value

	def helptext(self):
		return self[0].helptext
	
	def take(self):
		if len(self) >= 1:
			item = self.pop()
		else:
			raise Exception("Not Enough Items")

		if len(self) == 0:
			self.backpack.remove_slot(self)

		return item

	def __str__(self):
		return '{} ({})'.format(self.name, len(self))

class Backpack():
	def __init__(self, game):
		self.game = game
		self.slots = {}
		self.gold = 0

	def store(self, item):
		itemname = str(item)
		if itemname in self.slots:
			self.slots[itemname].add_item(item)
		else:
			self.slots[itemname] = ItemSlot(self.game, self, item)

	def remove_slot(self, slot):
		self.slots.pop(slot.name)

	def take(self, slot):
		return slot.take()

	def take_by_name(self, name):
		return self.slots[name].take()

	def show(self):
		return self.slots.values()
	
	def empty(self):
		self.slots = {}
		
	def absorb(self, backpack, message=False):
		for item in backpack.all_items():
			self.store(item)
			if message:
				print('Got item {}'.format(item.name))
		backpack.empty()

		self.gold += backpack.gold

		if backpack.gold > 0:
			if message:
				print('Got ${}'.format(backpack.gold))
		backpack.gold = 0

	def all_items(self):
		item_list = []
		for slot in self.slots:
			for item_entry in self.slots[slot]:
				item_list.append(item_entry)
		return item_list

	def __len__(self):
		return sum(len(slot) for slot in self.slots.values())

	def __contains__(self, item):
		return self.has(item)

	def has(self, item, qty=1):
		itemname = str(item)
		if itemname in self.slots:
			if len(self.slots[itemname]) >=qty:
				return True
		return False

	def qty(self, item):
		itemname = str(item)
		if itemname in self.slots:
			return len(self.slots[itemname])
		return 0

	

	

class Potion(Item):
	def config(self):
		self.name = 'Potion 1'
		self.target_type = SELF
		self.weight = 1
		self.value = 100
		self.rarity = 0.5
		self.helptext = 'Restores Some HP'
	
	def use(self, target):
		target.heal(20)
		print('{} used {}'.format(target.name,self.name))

class HealAll(Item):
	def config(self):
		self.name = 'Heal All'
		self.target_type = MULTI_SELF
		self.weight = 1
		self.value = 500
		self.rarity = 0.1
		self.helptext = 'Clear All Status'

	def use(self, target):
		target.heal(20)
		print('{} used {}'.format(target.name,self.name))


class Booster(Item):
	def config(self):
		self.name = 'Booster'
		self.target_type = SELF
		self.weight = 1
		self.value = 300
		self.rarity = 0.3
		self.helptext = 'Increases Physical Strength'

	def use(self, target):
		target.status.append(effects.StatMod(1.15, PHYSTR))
		print('{} used {}'.format(target.name,self.name))


class Key(Item):
	def config(self):
		self.name = 'Key'
		self.weight = 0
		self.value = 100
		self.rarity = 0.5
		self.helptext = 'Opens a generic door'


	def config(self):
		self.prefixes.append('Fire')
	def elements(self, element_list):
		if elements.Fire not in element_list:
			element_list.append(elements.Fire)
		return element_list

class FireMod(Gear):
	def config(self):
		self.prefixes.append('Fire')
	def elements(self, element_list):
		if elements.Fire not in element_list:
			element_list.append(elements.Fire)
		return element_list


class WaterMod(Gear):
	def config(self):
		self.prefixes.append('Water')
	def elements(self, element_list):
		if elements.Water not in element_list:
			element_list.append(elements.Water)
		return element_list

class EarthMod(Gear):
	def config(self):
		self.prefixes.append('Earth')
	def elements(self, element_list):
		if elements.Earth not in element_list:
			element_list.append(elements.Earth)
		return element_list

class ElectricMod(Gear):
	def config(self):
		self.prefixes.append('Electric')
	def elements(self, element_list):
		if elements.Electric not in element_list:
			element_list.append(elements.Electric)
		return element_list

class WindMod(Gear):
	def config(self):
		self.prefixes.append('Wind')
	def elements(self, element_list):
		if elements.Wind not in element_list:
			element_list.append(elements.Wind)
		return element_list


class LightMod(Gear):
	def config(self):
		self.prefixes.append('Light')
	def elements(self, element_list):
		if elements.Light not in element_list:
			element_list.append(elements.Light)
		return element_list

class DarkMod(Gear):
	def config(self):
		self.prefixes.append('Dark')
	def elements(self, element_list):
		if elements.Dark not in element_list:
			element_list.append(elements.Dark)
		return element_list



class Sword(Gear):
	def config(self):
		self.name = 'Sword'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_LEFT
	def physical_strength(self, initial):
		return initial + 10

class FireSword(FireMod, Sword):
	pass

gear_mods = [FireMod, WaterMod, EarthMod, ElectricMod, WindMod, LightMod, DarkMod]

def add_item_mod(instance, mod):

	mro = list(inspect.getmro(instance.__class__))
	calls = set()
	for m in mro:
		try:
			call = m.config
			calls.add(call)
		except:
			pass

	class NewClass(instance.__class__, mod):
		pass
	instance.__class__ = NewClass

	try:
		if mod.config not in calls:
			mod.config(instance)
	except:
		pass
	return instance

def gen_thunder_sword(game):
	test_thunder_sword = add_item_mod(Sword(game), ElectricMod)
	return test_thunder_sword
