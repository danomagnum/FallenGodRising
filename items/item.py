from constants import *
import utility


class Item(utility.Serializable):
	def __init__(self, game=None, level=1, name=None, target=TARGET_NONE, uses=None, char='?'):
		self.game = game
		self.prefixes = []
		self.suffixes = []
		self._name = name
		self.target_type = target
		self.weight = 0
		self.value = 0
		self.rarity = 0.5
		self.helptext = ''
		self.char = char
		if uses is not None:
			self.uses = uses
	
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
		if self.suffixes != []:
			namestr += ' '
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


