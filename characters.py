from main import Character
import elements
import moves

class TestChar(Character):
	def __init__(self):
		self.setup('test')
		self.elements.append(elements.Normal)
		self.elements.append(elements.Water)
		self.moves = [moves.Pound(), moves.Slam(), moves.Buff(), moves.Heal()]
		self.full_heal()

class TestChar2(Character):
	def __init__(self):
		self.setup('test')
		self.elements.append(elements.Normal)
		self.elements.append(elements.Fire)
		self.moves = [moves.Pound(), moves.Slam(), moves.Buff(), moves.Poison(), moves.Spray()]
		self.full_heal()
