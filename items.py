from constants import *
import effects
import elements
import utility

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
	
		utility.call_all_configs(self)

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
			self.game.player.backpack.store(return_items)
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

class FireMod(Gear):
	def config(self):
		self.prefixes.append('Fire')

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
	def elements(self, element_list):
		if elements.Fire not in element_list:
			element_list.append(elements.Fire)
		return element_list
