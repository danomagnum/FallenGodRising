import characters

a = characters.TestChar()
b = characters.TestChar()

damage = []

a.level = 100
b.level = 100
a.heal()
b.heal()
for x in xrange(100):
	damage.append(a.moves[0].attack(a,b))

print damage[0], damage[-1]
print a.hp, b.hp
