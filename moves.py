import main
import random
import elements
import effects
from utility import clamp, scale
from constants import *


class Strike(main.Move):
	def config(self):
		self.name = 'Strike'
		self.max_mp = 20.0
		self.accuracy = 0.9
		self.physical = (True, True)

class FireStrike(Strike):
	def config(self):
		self.name = 'Fire Strike'
		self.elements = [elements.Fire]


class WaterStrike(Strike):
	def config(self):
		self.name = 'Water Strike'
		self.elements = [elements.Water]

class EarthStrike(Strike):
	def config(self):
		self.name = 'Earth Strike'
		self.elements = [elements.Earth]

class ElectricStrike(Strike):
	def config(self):
		self.name = 'Electric Strike'
		self.elements = [elements.Electric]

class WindStrike(Strike):
	def config(self):
		self.name = 'Wind Strike'
		self.elements = [elements.Wind]

class LightStrike(Strike):
	def config(self):
		self.name = 'Light Strike'
		self.elements = [elements.Light]

class DarkStrike(Strike):
	def config(self):
		self.name = 'Dark Strike'
		self.elements = [elements.Dark]

typed_strikes = [FireStrike, WaterStrike, EarthStrike, WindStrike, LightStrike, DarkStrike]

class Buff(main.Move):
	def config(self):
		self.name = 'Buff'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, PHYSTR))

class Taunt(main.Move):
	def config(self):
		self.name = 'Taunt'
		self.accuracy = 1
		self.power = 0
		self.default_target = ENEMY

	def effect(self, target):
		target.status.append(effects.StatMod(0.85, PHYSTR))


class Focus(main.Move):
	def config(self):
		self.name = 'Focus'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, SPCSTR))

class Guard(main.Move):
	def config(self):
		self.name = 'Guard'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, PHYDEF))
		
class Protect(main.Move):
	def config(self):
		self.name = 'Protect'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, SPCDEF))

class Smoke(main.Move):
	def config(self):
		self.name = 'Smoke'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, EVASION))

class Haste(main.Move):
	def config(self):
		self.name = 'Haste'
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF

	def effect(self, target):
		target.status.append(effects.StatMod(1.15, SPEED))


class Heal(main.Move):
	def config(self):
		self.name = 'Heal'
		self.accuracy = 0.9
		self.power = -10
		self.default_target = SELF
		self.physical = (False, False)

class Poison(main.Move):
	def config(self):
		self.name = 'Poison'
		self.power = 2.0
		self.elements = [elements.Normal]
		self.physical = (True, True)

	def effect(self, target):
		randval = random.random()
		# for starters, poison minorly 20% of the time.  Once the move is more used, poison minorly 95%
		minor_range = scale(self.uses, 0, 1000, 0.2, 0.95)
		# for starters, poison majorly 5% of the time.  Once the move is more used, poison major 50%
		major_range = scale(self.uses, 0, 1000, 0.05, 0.5)
		if randval < major_range:
			print('{} has major poisoning'.format(target.name))
			target.status.append(effects.Poison_Major())
		elif randval < minor_range:
			print('{} has minor poisoning'.format(target.name))
			target.status.append(effects.Poison_Minor())


class Cure(main.Move):
	def config(self):
		self.name = 'Cure'
		self.max_mp = 2.0
		self.accuracy = 1
		self.power = 0
		self.default_target = SELF
		self.physical = (False, False)

	def effect(self, target):
		if len(target.status) > 0:
			to_remove = random.choice(target.status)
			target.status.remove(to_remove)


class Blast(main.Move):
	def config(self):
		self.name = 'Blast'
		self.max_mp = 20.0
		self.accuracy = 0.9
		self.physical = (False, False)

class FireBlast(Blast):
	def config(self):
		self.name = 'Fire Blast'
		self.elements = [elements.Fire]


class WaterBlast(Blast):
	def config(self):
		self.name = 'Water Blast'
		self.elements = [elements.Water]

class EarthBlast(Blast):
	def config(self):
		self.name = 'Earth Blast'
		self.elements = [elements.Earth]

class ElectricBlast(Blast):
	def config(self):
		self.name = 'Electric Blast'
		self.elements = [elements.Electric]

class WindBlast(Blast):
	def config(self):
		self.name = 'Wind Blast'
		self.elements = [elements.Wind]

class LightBlast(Blast):
	def config(self):
		self.name = 'Light Blast'
		self.elements = [elements.Light]

class DarkBlast(Blast):
	def config(self):
		self.name = 'Dark Blast'
		self.elements = [elements.Dark]


typed_blasts = [FireBlast, WaterBlast, EarthBlast, ElectricBlast, WindBlast, LightBlast, DarkBlast]
