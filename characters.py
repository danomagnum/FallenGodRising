from main import Character
import elements
import moves

class TestChar(Character):
	def __init__(self):
		self.setup('test')
		self.elements.append(elements.Normal)
		self.moves = [moves.Pound(), moves.Slam(), moves.Buff()]
		self.heal()
