import main
import random
import elements
import effects

def MoveGen(name, elementlist=None, effect_list=None, power=10.0, mp=10.0, cost=1, accuracy=0.9, target=main.ENEMY):
	if elementlist is None:
		elementlist = [elements.Normal]
	if effect_list is None:
		effect_list = [] # effects should be a list of tuples (effect, chance as 0 < real < 1)
	return lambda: main.Move(name, elementlist, accuracy, power, mp, effect_list, target)

Pound = MoveGen('Pound')
Slam = MoveGen('Slam', power=20)

Buff = MoveGen('Buff', effect_list=[(effects.Strength2x(), 1)], accuracy = 1 , power=0, target=main.SELF)

Poison = MoveGen('Poison', effect_list=[(effects.Poison_Minor(), 1)], power=0)
