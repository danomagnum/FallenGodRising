from main import Item, TARGET_COMBATANT, TARGET_COMMANDER, TARGET_NONE
import effects

class Potion(Item):
	def __init__(self):
		self.name = 'Potion 1'
		self.target = TARGET_COMBATANT
	def use(self, target):
		target.heal(20)
		print target.name, ' used ', self.name

class Booster(Item):
	def __init__(self):
		self.name = 'Roids 1'
		self.target = TARGET_COMBATANT
	def use(self, target):
		target.status.append(effects.Strength2x())
		print target.name, ' used ', self.name
