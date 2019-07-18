from constants import *
import effects
import elements
import utility
import inspect

class Item(object):
	def __init__(self, game, level=1, name=None, target=TARGET_NONE, use=None):
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
		self.level = level

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

	def __init__(self, game, level=1, name=None, target=TARGET_NONE, use=None):
		self.status = []
		Item.__init__(self, game, level,  name, target=TARGET_NONE, use=None)

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

#Start elemental gear mods

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

elemental_gear_mods = [FireMod, WaterMod, EarthMod, ElectricMod, WindMod, LightMod, DarkMod]

#Start general gear mods

class Crude(Gear):
	def config(self):
		self.prefixes.append('Crude')
		self.level -= 2
class Lesser(Gear):
	def config(self):
		self.prefixes.append('Lesser')
		self.level -= 1
class Greater(Gear):
	def config(self):
		self.prefixes.append('Greater')
		self.level += 1
class Exceptional(Gear):
	def config(self):
		self.prefixes.append('Exceptional')
		self.level += 2

general_gear_mods = [Crude, Lesser, Greater, Exceptional]

# Start base gear mods

class Bronze(Gear):
	def config(self):
		self.previxes.append('Bronze')
		self.level += 5
class Iron(Gear):
	def config(self):
		self.previxes.append('Iron')
		self.level += 10
class Steel(Gear):
	def config(self):
		self.previxes.append('Steel')
		self.level += 15
class Mithrill(Gear):
	def config(self):
		self.previxes.append('Mithrill')
		self.level += 20
class Admantium(Gear):
	def config(self):
		self.previxes.append('Admantium')
		self.level += 25

base_gear_mods = [Bronze, Iron, Steel, Mithrill, Admantium]
# Start Special gear mods

class OfWarrior(Gear):
	def config(self):
		self.suffixes.append('of the warrior')

	def physical_strength(self, initial):
		return initial * 1.1

class OfRock(Gear):
	def config(self):
		self.suffixes.append('of the rock')

	def physical_defense(self, initial):
		return initial * 1.1

class OfWizard(Gear):
	def config(self):
		self.suffixes.append('of the wizard')

	def special_strength(self, initial):
		return initial * 1.1

class OfDevotion(Gear):
	def config(self):
		self.suffixes.append('of devotion')

	def special_strength(self, initial):
		return initial * 1.1

class OfVigor(Gear):
	def config(self):
		self.suffixes.append('of vigor')

	def speed(self, initial):
		return initial * 1.1

class OfRobustness(Gear):
	def config(self):
		self.suffixes.append('of robustness')

	def max_hp(self, initial):
		return initial * 1.1

class OfMystique(Gear):
	def config(self):
		self.suffixes.append('of mystique')

	def evasion(self, initial):
		return initial * 1.1

class OfFalcon(Gear):
	def config(self):
		self.suffixes.append('of the falcon')

	def accuracy(self, initial):
		return initial * 1.1

class OfGambler(Gear):
	def config(self):
		self.suffixes.append('of the gambler')

	def luck(self, initial):
		return initial * 1.1

class OfSorrow(Gear):
	def config(self):
		self.suffixes.append('of sorrow')
	def physical_strength(self, initial): # passive stat boosts take effect on these routines
		return initial * 0.9
	def physical_defense(self, initial):
		return initial * 0.9
	def special_strength(self, initial):
		return initial * 0.9
	def special_defense(self, initial):
		return initial * 0.9
	def speed(self, initial):
		return initial * 0.9
	def hp(self, initial):
		return initial * 0.9
	def max_hp(self, initial):
		return initial * 0.9
	def evasion(self, initial):
		return initial * 0.9
	def accuracy(self, initial):
		return initial * 0.9
	def luck(self, initial):
		return initial * 0.9

class OfChaos(Gear):# this returns a "random" stat by actually returning the last stat info was pulled for
	def config(self):
		self.suffixes.append('of chaos')
		self.last_initial = 1
	def physical_strength(self, initial): # passive stat boosts take effect on these routines
		initial, self.last_initial = self.last_initial, initial
		return initial
	def physical_defense(self, initial):
		initial, self.last_initial = self.last_initial, initial
		return initial
	def special_strength(self, initial):
		initial, self.last_initial = self.last_initial, initial
		return initial
	def special_defense(self, initial):
		initial, self.last_initial = self.last_initial, initial
		return initial
	def speed(self, initial):
		initial, self.last_initial = self.last_initial, initial
		return initial
	def hp(self, initial):
		initial, self.last_initial = self.last_initial, initial
		return initial
	def max_hp(self, initial):
		initial, self.last_initial = self.last_initial, initial
		return initial
	def evasion(self, initial):
		initial, self.last_initial = self.last_initial, initial
		return initial
	def accuracy(self, initial):
		initial, self.last_initial = self.last_initial, initial
		return initial
	def luck(self, initial):
		initial, self.last_initial = self.last_initial, initial
		return initial


special_gear_mods = [OfWarrior, OfRock, OfWizard, OfDevotion, OfVigor, OfRobustness, OfMystique, OfFalcon, OfGambler, OfSorrow, OfChaos]

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

class Sword(Gear):
	def config(self):
		self.name = 'Sword'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_LEFT
	def physical_strength(self, initial):
		return initial + self.level

class Helm(Gear):
	def config(self):
		self.name = 'Helm'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_HEAD
	def physical_defense(self, initial):
		return initial + (self.level / 5.0)

class Mail(Gear):
	def config(self):
		self.name = 'Mail'
		self.weight = 1
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_BODY
	def physical_defense(self, initial):
		return initial + (sel.level / 4.0)

class Plate(Gear):
	def config(self):
		self.name = 'Plate'
		self.weight = 2
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_BODY
	def physical_defense(self, initial):
		return initial + (sel.level / 3.0)

class Shield(Gear):
	def config(self):
		self.name = 'Shield'
		self.weight = 2
		self.value = 300
		self.rarity = 0.2
		self.target_type = EQUIP_RIGHT
	def physical_defense(self, initial):
		return initial + (sel.level / 5.0)

