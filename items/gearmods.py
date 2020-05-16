from constants import *
import random
import elements
import inspect
from .item import Item
from .gear import Gear

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
general_gear_mod_levels = [(Crude, -2), (Lesser, -1),(None, 0), (Greater, 1), (Exceptional, 2)]

# Start base gear mods

class Bronze(Gear):
	def config(self):
		self.prefixes.append('Bronze')
		self.level += 5
class Iron(Gear):
	def config(self):
		self.prefixes.append('Iron')
		self.level += 10
class Steel(Gear):
	def config(self):
		self.prefixes.append('Steel')
		self.level += 15
class Mithrill(Gear):
	def config(self):
		self.prefixes.append('Mithrill')
		self.level += 20
class Admantium(Gear):
	def config(self):
		self.prefixes.append('Admantium')
		self.level += 25

base_gear_mods = [Bronze, Iron, Steel, Mithrill, Admantium]
base_gear_mod_levels = [(None, 0),(Bronze, 5), (Iron, 10),(Steel, 15),(Mithrill, 20),(Admantium, 25)]
# Start Special gear mods

class OfWarrior(Gear):
	def config(self):
		self.suffixes.append('of the warrior')

	def physical_strength(self, initial):
		return initial * 1.1

class OfSquire(Gear):
	def config(self):
		self.suffixes.append('of the squire')

	def physical_strength(self, initial):
		return initial * 0.9

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
class OfApprentice(Gear):
	def config(self):
		self.suffixes.append('of the apprentice')

	def special_strength(self, initial):
		return initial * 0.9

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

class OfSloth(Gear):
	def config(self):
		self.suffixes.append('of sloth')

	def speed(self, initial):
		return initial * 0.9

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

class OfBlind(Gear):
	def config(self):
		self.suffixes.append('of the blind')

	def accuracy(self, initial):
		return initial * 0.9

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

class OfRegen(Gear):
	def config(self):
		self.suffixes.append('of survival')
	
	def tick(self, wearer):
		if random.randint(0,100) < 20:
			if wearer.hp < wearer.max_hp:
				wearer.hp += 1
				print('{} Recovered from {}'.format(wearer.name, self.name))


special_gear_mods = [OfWarrior, OfSquire, OfRock, OfWizard, OfApprentice, OfDevotion, OfVigor, OfSloth, OfRobustness, OfMystique, OfFalcon, OfBlind, OfGambler, OfSorrow, OfChaos, OfRegen]

def gen_thunder_sword(game):
	test_thunder_sword = add_item_mod(Sword(game), ElectricMod)
	return test_thunder_sword
