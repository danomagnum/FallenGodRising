from targets import *
import effects

class Item(object):
	def __init__(self, name, target=TARGET_NONE, use=None):
		self.name = name
		self.target_type = target
		if use is not None:
			self.use = use

	def use(self, target = None):
		pass
	def __str__(self):
		return self.name

class Equipment(Item):
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



class ItemSlot(list):
	def __init__(self, backpack, item):
		self.name = item.name
		self.backpack = backpack
		list.__init__(self,[item])
		self.target_type = item.target_type
		#self.add_item(item)

	def add_item(self, item):
		self.append(item)
	
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
	def __init__(self):
		self.slots = {}

	def store(self, item):
		itemname = str(item)
		if itemname in self.slots:
			self.slots[itemname].add_item(item)
		else:
			self.slots[itemname] = ItemSlot(self, item)

	def remove_slot(self, slot):
		self.slots.pop(slot.name)

	def take(self, slot):
		return slot.take()

	def show(self):
		return self.slots.values()
		
		


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
	

	

class Potion(Item):
	def __init__(self):
		Item.__init__(self, 'Potion 1', SELF)
	def use(self, target):
		target.heal(20)
		print('{} used {}'.format(target.name,self.name))

class HealAll(Item):
	def __init__(self):
		Item.__init__(self, 'Heal All 1', MULTI_SELF)
	def use(self, target):
		target.heal(20)
		print('{} used {}'.format(target.name,self.name))



class Booster(Item):
	def __init__(self):
		Item.__init__(self, 'Roids 1', SELF)
	def use(self, target):
		target.status.append(effects.Strength2x())
		print('{} used {}'.format(target.name,self.name))



