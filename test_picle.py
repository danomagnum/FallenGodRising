import dill
import pickle

class B(object):
	pass

class A(object):
	pass

class C(object):
	pass



def party(a, b):
	class Gen(a, b):
		def __reduce__(self):
			return (party, (a, b))
			
		def config(self):
			pass

	Gen.test = 1

	return Gen
	#Generated_Entity = type('Picleable', (a, b), {'config': config, '__reduce__':reduce})
	#return Generated_Entity


p = party(A, B)()
print p.__reduce__()

pickle.dumps(p)

