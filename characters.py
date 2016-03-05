from main import Character
from elements import *
from moves import *

class TestChar(Character):
	def __init__(self):
		self.setup('test')
		self.elements.append(Normal)
		self.moves = [pound()]
		self.heal()
