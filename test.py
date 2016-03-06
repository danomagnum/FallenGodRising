import characters
import battle

a = characters.TestChar()
b = characters.TestChar()

damage = []

a.level = 50
a.name = 'my mon'
b.level = 52
b.name = 'enemy mon'
a.heal()
b.heal()

battle.battle(a,b)

#print a.exp, '/', (a.level+1)**3 - a.exp
