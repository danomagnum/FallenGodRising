import main
from items import items
import elements
import moves
import random
import utility
import traceback

class Character(object):
	def __init__(self, game,  name=None, level=1):
		self.game = game
		self.initialized = False
		if name is None:
			#self.name = 'MissingNo'
			self.name = self.__class__.__name__
		else:
			self.name = name
		self._hp = 1
		self._exp = 0
		self._elements = [elements.Normal]
		self.status = []
		self.equipment = main.Equipment(game)
		# stat growth rate for p.str, p.def, s.str, s.def, speed, maxhp
		self.coefficients = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)
		self.helptext = ''
		self.moves = []
		self._level = 1
		self.stat_randomizer()
		utility.call_all('config', self)
		#utility.call_all_configs(self)

		self.level = level
		self.full_heal()
		self._exp = self.exp_at_level(self.level)
		self.initialized = True

	@property
	def elements(self):
		#return self._elements
		try:
			e_list = self._elements[:]
			for item in self.equipment.all_items():
				e_list = item.elements(e_list)
			return e_list
		except Exception as e:
			with open('traceback.log', 'a') as f:
				f.write(str(e))
				f.write(traceback.format_exc())

	@elements.setter
	def elements(self, value):
		self._elements = value

	def stat_randomizer(self):
		# when the entity is created, give it some variety in power
		# nominally 1.0 +- 5%
		BASE = 1.0
		DEV = 0.05
		self.mod_physical_strength = random.normalvariate(BASE, DEV)
		self.mod_physical_defense = random.normalvariate(BASE, DEV)
		self.mod_arcane_strength = random.normalvariate(BASE, DEV)
		self.mod_arcane_defense = random.normalvariate(BASE, DEV)
		self.mod_speed = random.normalvariate(BASE, DEV)
		self.mod_hp = random.normalvariate(BASE, DEV)
		self.mod_luck = random.normalvariate(BASE, DEV)


	def config(self):
		self.moves = []
		self.base_stats()

	def base_stats(self):
		self.base_physical_strength = 10
		self.base_physical_defense = 10
		self.base_arcane_strength = 10
		self.base_arcane_defense = 10
		self.base_speed = 10
		self.base_hp = 10
		self.base_luck = 100
		self.physical = True
	
	def tick(self):
		for stat in self.status:
			utility.call_all('pre_turn', stat, self)
			utility.call_all('post_turn', stat, self)

	def battletick(self):
		for item in self.equipment.all_items():
			item.subtick(self)
			item.tick(self)
		for move in self.moves:
			move.tick(self)

	def subtick(self):
		for item in self.equipment.all_items():
			utility.call_all('tick', item, self)
			utility.call_all('subtick', item, self)
		for move in self.moves:
			utility.call_all('tick', move, self)
			#move.tick(self)
		for stat in self.status:
			utility.call_all('tick', stat, self)
			#stat.tick(self)

	def __str__(self):
		return self.name

	@property
	def level(self):
		return self._level

	@level.setter
	def level(self, value):
		if self.initialized:
			print('{} leveled up from {} to {}'.format(self.name, self._level, value))
		if value > self._level:
			for lvl in range(self._level + 1, value + 1):
				self._level = lvl
				if self.exp_at_level(self.level) > self._exp:
					self._exp = self.exp_at_level(self.level)
				self.levelup()
				level_method = 'level_{:02}'.format(lvl)
				try:
					method = getattr(self, level_method)
				except:
					method = None
				if method is not None:
					method()
		self.levelup()
		self.partial_heal()

	def levelup(self):
		#check if the character leveled up.  Template code below
		#if self.level > xx:
		#	res = self.game.prompt('Advance {} to {}'.format(self.name, 'NewCharName'))
		#	if res:
		#		utilities.change_class_of_instance(self, NewCharacter)
		pass
	
	def add_move(self, move):
		m = move(self.game)
		if self.initialized:
			print('{} Gained The Skill {}'.format(self.name, m.name))
		self.moves.append(m)

	@property
	def exp(self):
		return self._exp

	@exp.setter
	def exp(self, value):
		self._exp = value
		check_level = True
		while check_level:
			if self._exp >= self.exp_at_level(self.level + 1):
				self.level += 1
			else:
				check_level = False

	@property
	def exp_value(self):
		val = self.physical_strength + self.physical_defense
		val += self.arcane_strength + self.arcane_defense
		val += self.speed + self.max_hp
		val *= self.level / 6
		return int(val)

	def exp_at_level(self, level):
		return (level ) ** 3

	def exp_progress(self):
		return (float(self.exp) - float(self.exp_at_level(self.level)) ) / float(self.exp_at_level(self.level + 1))
	@property
	def physical_strength(self):
		stat = (self.base_physical_strength + self.coefficients[0]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.physical_strength(stat)
		stat = self.equipment.physical_strength(stat)
		stat = stat * self.mod_physical_strength
		return utility.clamp(stat, 1, 3* self.base_physical_strength)
	@property
	def physical_defense(self):
		stat = (self.base_physical_defense + self.coefficients[1]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.physical_defense(stat)
		stat = self.equipment.physical_defense(stat)
		stat = stat * self.mod_physical_defense
		return utility.clamp(stat, 1, 3* self.base_physical_defense)
	@property
	def arcane_strength(self):
		stat = (self.base_arcane_strength + self.coefficients[2]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.arcane_strength(stat)
		stat = self.equipment.arcane_strength(stat)
		stat = stat * self.mod_arcane_strength
		return utility.clamp(stat, 1, 3* self.base_arcane_strength)
	@property
	def arcane_defense(self):
		stat = (self.base_arcane_defense + self.coefficients[3]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.arcane_defense(stat)
		stat = self.equipment.arcane_defense(stat)
		stat = stat * self.mod_arcane_defense
		return utility.clamp(stat, 1, 3* self.base_arcane_defense)

	@property
	def speed(self):
		stat = (self.base_speed + self.coefficients[4]) * 3 * self.level / 100.0 + 5
		for status in self.status:
			stat = status.speed(stat)
		stat = self.equipment.speed(stat)
		stat = stat * self.mod_speed
		return utility.clamp(stat, 1, 3* self.base_speed)

	def raw_hp(self):
		return self._hp

	@property
	def hp(self):
		if self._hp > self.max_hp:
			self._hp = self.max_hp
		stat = self._hp
		for status in self.status:
			stat = status.hp(stat)
		stat = self.equipment.hp(stat)
		return  min(max(0,stat), self.max_hp)
	
	@property
	def luck(self):
		stat = float(self.base_luck) / 100.0 # One point of luck is a 2% change. Will need balanced.
		for status in self.status:
			stat = status.luck(stat)
		stat = self.equipment.luck(stat)
		stat = stat * self.mod_luck
		return utility.clamp(stat, 0.1, 3* self.base_luck)

	@hp.setter
	def hp(self, value):
		self._hp = utility.clamp(value, 0, self.max_hp)

	def heal(self, amount):
		if self.hp > 0:
			self._hp = min(max(0,self._hp + amount), self.max_hp)

	@property
	def max_hp(self):
		stat = int((self.base_hp + self.coefficients[5]) * 10 * self.level / 100.0 + 5)
		for status in self.status:
			stat = status.max_hp(stat)
		stat = self.equipment.max_hp(stat)
		stat = stat * self.mod_hp
		return stat

	@property
	def virtual_hp(self):
		stat = int((100 + self.coefficients[5]) * 10 * self.level / 100.0 + 5)
		return stat


	@property
	def evasion(self):
		stat = 1.0
		for status in self.status:
			stat = status.evasion(stat)
		stat = self.equipment.evasion(stat)
		return stat

	@property
	def accuracy(self):
		stat = 1.0
		for status in self.status:
			stat = status.accuracy(stat)
		stat = self.equipment.accuracy(stat)
		return stat

	def full_heal(self):
		for move in self.moves:
			move.mp = move.max_mp
		if self.hp > 0:
			self.hp = self.max_hp

	def partial_heal(self):
		for move in self.moves:
			move.mp += int(move.max_mp / 8)
		if self.hp > 0:
			self.hp += int(self.max_hp / 10)

	def levelup(self): # override this with sub classes to do fancy things
		pass

	def revive(self):
		if self.hp <= 0:
			self.hp = 1

class Dragoon(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Smoke(self.game)]
		self.base_physical_strength = 120
		self.base_physical_defense = 80
		self.base_arcane_strength = 100
		self.base_arcane_defense = 80
		self.base_speed = 120
		self.base_hp = 120
		self.base_luck = 100

class Battlemage(Character):
	def config(self):
		self.moves = [moves.arc.Blast(self.game), moves.stat.Protect(self.game)]
		self.base_physical_strength = 80
		self.base_physical_defense = 120
		self.base_arcane_strength = 100
		self.base_arcane_defense = 100
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100

class Nightblade(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.arc.Blast(self.game)]
		self.base_physical_strength = 120
		self.base_physical_defense = 80
		self.base_arcane_strength = 120
		self.base_arcane_defense = 80
		self.base_speed = 100
		self.base_hp = 80
		self.base_luck = 100

class Witchhunter(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game), moves.stat.Haste(self.game)]
		self.base_physical_strength = 100
		self.base_physical_defense = 100
		self.base_arcane_strength = 60
		self.base_arcane_defense = 140
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100


class Debug(Character):
	def config(self):
		self.moves = [moves.phy.Strike(self.game),
		              moves.stat.Haste(self.game),
		              moves.arc.Wave(self.game),
		              moves.moves.SelfDestruct(self.game),
		              moves.heal.Transfuse(self.game),
		              moves.stat.Drain(self.game),
			      moves.mods.mod_move(moves.phy.Strike, moves.mods.Piercing)(self.game),
			      moves.mods.mod_move(moves.mods.mod_move(moves.phy.Strike, moves.mods.Piercing), moves.mods.Multi)(self.game),
			      moves.mods.mod_move(moves.phy.Strike, moves.mods.Poison)(self.game),
			      moves.mods.mod_move(moves.mods.mod_move(moves.phy.Strike, moves.mods.Poison), moves.mods.Piercing)(self.game)]
		self.base_physical_strength = 100
		self.base_physical_defense = 100
		self.base_arcane_strength = 60
		self.base_arcane_defense = 140
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100

def promote(instance, newclass):
	# need to figure out if we've had any base stat modifiers. So save the current base stat values
	base_hp = instance.base_hp
	base_physical_strength = instance.base_physical_strength 
	base_physical_defense = instance.base_physical_defense
	base_arcane_strength = instance.base_arcane_strength
	base_arcane_defense = instance.base_arcane_defense
	base_speed = instance.base_speed
	base_luck = instance.base_luck

	#then reset them to default for the current instance
	instance.base_stats()

	#then subtract the current (base) values from the original
	base_hp -= instance.base_hp
	base_physical_strength -= instance.base_physical_strength 
	base_physical_defense -= instance.base_physical_defense
	base_arcane_strength -= instance.base_arcane_strength
	base_arcane_defense -= instance.base_arcane_defense
	base_speed -= instance.base_speed
	base_luck -= instance.base_luck

	name = instance.name
	utility.change_class_of_instance(instance, newclass)
	print('{} was promoted to {}'.format(name, newclass.__name__))
	instance.name = newclass.__name__

	#update the base stats to the new class
	instance.base_stats()

	#add the modifiers back
	instance.base_hp += base_hp
	instance.base_physical_strength += base_physical_strength 
	instance.base_physical_defense += base_physical_defense
	instance.base_arcane_strength += base_arcane_strength
	instance.base_arcane_defense += base_arcane_defense
	instance.base_speed += base_speed
	instance.base_luck += base_luck


starters = [Debug]


