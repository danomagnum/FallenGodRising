USE_BIOME = True

class Biome(object):
	def __init__(self, name):
		self.name = name
		self.modifiers = {}
	def __str__(self):
		return str(self.name)
	
class Element(object):
	def __init__(self, name, nominal = 1.0):
		self.name = name
		self.nominal_modifier = nominal
		self.modifiers = {}
		self.bonus = 2.0

	def effectiveness(self, defending_element, biome = None):
		biome_mod = 1.0
		if USE_BIOME:
			if biome is not None:
				biome_mod = biome.modifiers.get(self, 1.0)
		return biome_mod * self.modifiers.get(defending_element, self.nominal_modifier)

	def __str__(self):
		return self.name


#base element definitions
Normal = Element('Normal')

Fire = Element('Fire')
Water = Element('Water')
Earth = Element('Earth')
Electric = Element('Electric')
Wind = Element('Wind')

Light = Element('Light')
Dark = Element('Dark')

# base biome definitions
Sea = Biome('Sea')
Desert = Biome('Desert')
Marsh = Biome('Marsh')
Forest = Biome('Forest')
Plains = Biome('Plains')
Mountains = Biome('Mountains')

Sky = Biome('Sky')
Underground = Biome('Underground')

#element bonus
Normal.bonus = 1.05

#element interactions
Fire.modifiers[Water] = 0.5
Fire.modifiers[Wind] = 1.5
Fire.modifiers[Fire] = 0.75

Water.modifiers[Fire] = 2.0
Water.modifiers[Earth] = 1.5
Water.modifiers[Electric] = 0.5
Water.modifiers[Water] = 0.75

Earth.modifiers[Water] = 1.5
Earth.modifiers[Electric] = 2
Earth.modifiers[Earth] = 0.75

Electric.modifiers[Water] = 2.0
Electric.modifiers[Earth] = 0.5
Electric.modifiers[Electric] = 0.75

Wind.modifiers[Fire] = 1.5
Wind.modifiers[Earth] = 1.5
Wind.modifiers[Wind] = 0.75

Light.modifiers[Dark] = 2.0
Light.modifiers[Light] = 0.5
Light.modifiers[Normal] = 1.5
Light.modifiers[Fire] = 0.8
Light.modifiers[Water] = 0.8
Light.modifiers[Earth] = 0.8
Light.modifiers[Electric] = 0.8
Light.modifiers[Wind] = 0.8

Dark.modifiers[Light] = 2.0
Dark.modifiers[Dark] = 0.5
Dark.modifiers[Normal] = 1.5
Dark.modifiers[Fire] = 0.8
Dark.modifiers[Water] = 0.8
Dark.modifiers[Earth] = 0.8
Dark.modifiers[Electric] = 0.8
Dark.modifiers[Wind] = 0.8



# base biome interactions.
# each element has one "strong" biome.
# Light and Dark are slightly nerfed in all "normal" biomes.
# and majorly nerfed in opposing biomes

Desert.modifiers[Fire] = 1.5
Marsh.modifiers[Water] = 1.5
Forest.modifiers[Earth] = 1.5
Plains.modifiers[Electric] = 1.5
Mountains.modifiers[Wind] = 1.5

Sky.modifiers[Light] = 1.5
Desert.modifiers[Light] = 0.8
Marsh.modifiers[Light] = 0.8
Forest.modifiers[Light] = 0.8
Plains.modifiers[Light] = 0.8
Mountains.modifiers[Light] = 0.8
Underground.modifiers[Light] = 0.4

Underground.modifiers[Dark] = 1.5
Desert.modifiers[Dark] = 0.8
Marsh.modifiers[Dark] = 0.8
Forest.modifiers[Dark] = 0.8
Plains.modifiers[Dark] = 0.8
Mountains.modifiers[Dark] = 0.8
Sky.modifiers[Dark] = 0.4


elements = [Normal, Fire, Water, Earth, Electric, Wind, Light, Dark]
biomes = [Sea, Marsh, Plains, Desert, Forest, Mountains, Sky, Underground]
