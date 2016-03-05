from main import Element

#base definitions
Normal = Element('Normal')
Fire = Element('Fire')
Water = Element('Water')
Grass = Element('Grass')

#interactions
Fire.special_modifiers[Water] = 0.5
Fire.special_modifiers[Grass] = 2.0

Water.special_modifiers[Fire] = 2.0
Water.special_modifiers[Grass] = 0.5

Grass.special_modifiers[Fire] = 0.5
Grass.special_modifiers[Water] = 2.0
