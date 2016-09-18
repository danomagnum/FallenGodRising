import characters
import battle

a = characters.TestChar()
b = characters.TestChar()

damage = []

a.name = 'my mon'
a.level = 50
b.name = 'enemy mon'
b.level = 52
a.heal()
b.heal()
a.moves[0].mp = 1

battle.battle(a,b)

#print a.exp, '/', (a.level+1)**3 - a.exp
