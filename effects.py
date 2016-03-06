from main import Status
from elements import *

class Strength2x(Status):
	def __init__(self):
		self.name = 'Strength 2x'
	def physical_strength(self, initial):
		return initial * 2
