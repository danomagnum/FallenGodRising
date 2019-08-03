import entities
import characters
import main
import moves
import elements

def party(game, battle_AI, world_AI, level, combatants, name, item_list = None):
	class Generated_Entity(world_AI,battle_AI):
		# example basic enemy
		def config(self):
			self.name = name
			for c in combatants:
				self.combatants.append(c(game, level=level))
			self.char = name[0]

	return Generated_Entity

class Rat(characters.Character):
	def config(self):
		self.moves = [moves.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 50
		self.base_physical_defense = 50
		self.base_special_strength = 50
		self.base_special_defense = 50
		self.base_speed = 50
		self.base_hp = 50
		self.base_luck = 100

class Spider(characters.Character):
	def config(self):
		self.moves = [moves.Strike(self.game), moves.Poison(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 50
		self.base_physical_defense = 50
		self.base_special_strength = 50
		self.base_special_defense = 50
		self.base_speed = 50
		self.base_hp = 20
		self.base_luck = 100

class Imp(characters.Character):
	def config(self):
		self.moves = [moves.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 50
		self.base_physical_defense = 50
		self.base_special_strength = 70
		self.base_special_defense = 70
		self.base_speed = 100
		self.base_hp = 60
		self.base_luck = 100

class Goblin(characters.Character):
	def config(self):
		self.moves = [moves.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 70
		self.base_physical_defense = 70
		self.base_special_strength = 50
		self.base_special_defense = 50
		self.base_speed = 100
		self.base_hp = 60
		self.base_luck = 100

class Hobgoblin(characters.Character):
	def config(self):
		self.moves = [moves.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 100
		self.base_physical_defense = 100
		self.base_special_strength = 80
		self.base_special_defense = 80
		self.base_speed = 100
		self.base_hp = 100
		self.base_luck = 100

class Ogre(characters.Character):
	def config(self):
		self.moves = [moves.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 120
		self.base_physical_defense = 120
		self.base_special_strength = 80
		self.base_special_defense = 80
		self.base_speed = 90
		self.base_hp = 130
		self.base_luck = 90

class Highwayman(characters.Character):
	def config(self):
		self.moves = [moves.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 90
		self.base_physical_defense = 90
		self.base_special_strength = 90
		self.base_special_defense = 90
		self.base_speed = 90
		self.base_hp = 90
		self.base_luck = 120

class Skeleton(characters.Character):
	def config(self):
		self.moves = [moves.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 90
		self.base_physical_defense = 90
		self.base_special_strength = 10
		self.base_special_defense = 50
		self.base_speed = 90
		self.base_hp = 90
		self.base_luck = 90

class Zombie(characters.Character):
	def config(self):
		self.moves = [moves.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 90
		self.base_physical_defense = 90
		self.base_special_strength = 10
		self.base_special_defense = 50
		self.base_speed = 10
		self.base_hp = 90
		self.base_luck = 90

class Mimic(characters.Character):
	def config(self):
		self.moves = [moves.Strike(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 90
		self.base_physical_defense = 90
		self.base_special_strength = 90
		self.base_special_defense = 90
		self.base_speed = 130
		self.base_hp = 90
		self.base_luck = 90


class Centaur(characters.Character):
	def config(self):
		self.moves = [moves.Blast(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 80
		self.base_physical_defense = 80
		self.base_special_strength = 100
		self.base_special_defense = 100
		self.base_speed = 110
		self.base_hp = 110
		self.base_luck = 90


class Demon(characters.Character):
	def config(self):
		self.moves = [moves.Blast(self.game)]
		self.elements = [elements.Normal]
		self.base_physical_strength = 80
		self.base_physical_defense = 80
		self.base_special_strength = 120
		self.base_special_defense = 120
		self.base_speed = 90
		self.base_hp = 130
		self.base_luck = 90


#mods: giant, lesser, greater, captain, elements
