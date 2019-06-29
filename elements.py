class Element(object):
	def __init__(self, name, nominal = 1.0, bonus=1.5):
		self.name = name
		self.nominal_modifier = nominal
		self.special_modifiers = {}
		self.bonus = bonus

	def effectiveness(self, defending_element):
		return self.special_modifiers[defending_element] if (defending_element in self.special_modifiers) else self.nominal_modifier


#base definitions
Normal = Element('Normal')
Fire = Element('Fire')
Water = Element('Water')
Earth = Element('Earth')
Electric = Element('Electric')
Wind = Element('Wind')

Light = Element('Light')
Dark = Element('Dark')

#interactions
Fire.special_modifiers[Water] = 0.5
Fire.special_modifiers[Wind] = 1.5
Fire.special_modifiers[Fire] = 0.75

Water.special_modifiers[Fire] = 2.0
Water.special_modifiers[Earth] = 1.5
Water.special_modifiers[Electric] = 0.5
Water.special_modifiers[Water] = 0.75

Earth.special_modifiers[Water] = 1.5
Earth.special_modifiers[Electric] = 2
Earth.special_modifiers[Earth] = 0.75

Electric.special_modifiers[Water] = 2.0
Electric.special_modifiers[Earth] = 0.5
Electric.special_modifiers[Electric] = 0.75

Wind.special_modifiers[Fire] = 1.5
Wind.special_modifiers[Earth] = 1.5
Wind.special_modifiers[Wind] = 0.75

Light.special_modifiers[Dark] = 1.5
Light.special_modifiers[Light] = 0.5
Light.special_modifiers[Normal] = 2.0

Dark.special_modifiers[Light] = 1.5
Dark.special_modifiers[Dark] = 0.5
Dark.special_modifiers[Normal] = 2.0


