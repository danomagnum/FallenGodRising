from constants import *
from .item import Item

class Gear(Item):
	def __init__(self, game=None, level=1, name=None, target=TARGET_NONE, uses=None):
		self.status = []
		self.owner = None
		Item.__init__(self, game, level,  name, target=TARGET_NONE, uses=None)

	def use(self, target):
		return_items = target.equipment.equip(self)
		for item in return_items:
			self.game.player.backpack.store(item)
			print('{} unequipped {}'.format(target.name,item.name))
		print('{} equipped {}'.format(target.name,self.name))
		self.owner = target

	def config(self):
		pass

	@property
	def power(self):
		return self.level + 5

	def physical_strength(self, initial): # passive stat boosts take effect on these routines
		return initial
	def evasion(self, initial):
		return initial
	def accuracy(self, initial):
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


