import random
import math
import inspect

def call_all_recursive(value, method, instance):
	#get a higherarcy list of all base classes
	mro = list(inspect.getmro(instance.__class__))

	#go through the base classes and check if they have a method.	
	#if they do, add them to the set.  The set keeps any classes that inherited
	#the method from a base class from running a method twice.
	calls = []
	call_set = set()
	for m in mro:
		try:
			call = getattr(m, method)
			if call not in call_set:
				calls.append(call)
			call_set.add(call)
		except:
			pass
	#so the order can be reversed and they can be called from
	# the mose base to the most top-level.  So top-level takes precidence
	# if any of the same values are set
	calls.reverse()

	# finally call them all
	for call in calls:
		value = call(instance, value)
	return value

def call_all(method, instance, *params):
	#get a higherarcy list of all base classes
	mro = list(inspect.getmro(instance.__class__))

	#go through the base classes and check if they have a config method.	
	#if they do, add them to the set.  The set keeps any classes that inherited
	#the config method from a base class from running a config twice.
	calls = []
	call_set = set()
	for m in mro:
		try:
			call = getattr(m, method)
			if call not in call_set:
				calls.append(call)
			call_set.add(call)
		except:
			pass
	#change the set to a list
	calls = list(calls)
	#so the order can be reversed and they can be called from
	# the mose base to the most top-level.  So top-level takes precidence
	# if any of the same values are set
	calls.reverse()
	# For some reason this is't working right

	# finally call them all
	for call in calls:
		if params:
			call(instance, *params)
		else:
			call(instance)

def list_calls(method, instance):
	#get a higherarcy list of all base classes
	mro = list(inspect.getmro(instance.__class__))

	#go through the base classes and check if they have a config method.	
	#if they do, add them to the set.  The set keeps any classes that inherited
	#the config method from a base class from running a config twice.
	calls = []
	call_set = set()
	for m in mro:
		try:
			call = getattr(m, method)
			if call not in call_set:
				calls.append(call)
			call_set.add(call)
		except:
			pass
	#change the set to a list
	return calls


def clamp(val, minimum, maximum):
	return min(maximum, max(val, minimum))

def scale(value, in_min, in_max, out_min, out_max, clamp_output = True):
	in_range = float(in_max - in_min)
	out_range = float(out_max - out_min)
	if in_range != 0:
		in_offset = float(value - in_min)
		in_percent = in_offset / in_range
		final = (out_range * in_percent) + out_min
		if clamp_output:
			final = clamp(final, out_min, out_max)
		return final
	
	else:
		raise Exception('Divide By Zero In Scale.')


def select_by_level(level, options):
	weighted = []
	weight_total = 0
	for opt in options:
		weight_denom = 1 + (opt[0] - level)**2
		if level < opt[0]:
			weight_num = 1.0
		else:
			weight_num = 1.2
		weight = weight_num / weight_denom
		w = (opt[1], weight)
		weight_total += weight
		weighted.append(w)
	weighted.sort(key=lambda x:-x[1])

	rand_val = random.uniform(0, weight_total)

	for option in weighted:
		rand_val -= option[1]
		if rand_val < 0:
			break


	return option[0]
	

def serialize_multiobj(*classes):
	def reduce(self):
		return (serialize_multiobj, self.__class__.__bases__)
	class_list = list(classes)

	if Serializable not in classes:
		class_list += [Serializable]

	obj = type('Generated', tuple(class_list), {})
	return obj.__new__(obj)

class Serializable(object):
	def __reduce__(self):
		classes = list(self.__class__.__bases__)
		if self.__class__.__name__ == 'Generated':
			pass
		else:
			classes = [self.__class__] + classes

		return (serialize_multiobj, tuple(classes), self.__dict__)

	def __setstate__(self, val):
		self.__dict__.update(val)


def add_class(original, addition):
	if original.__name__ == 'Generated':
		classes = list(original.__bases__)
		if addition not in classes:
			classes.append(addition)
		classes = tuple(classes)
		Generated = type('Generated', classes, {})
		
	else:
		class Generated(original, addition):
			pass
	return Generated


def add_class_to_instance(instance, mod):

	mro = list(inspect.getmro(instance.__class__))
	calls = set()
	for m in mro:
		try:
			call = m.config
			calls.add(call)
		except:
			pass

	if instance.__class__.__name__ == 'Generated':
		classes = list(instance.__class__.__bases__)
		if mod not in classes:
			classes.append(mod)
		classes = tuple(classes)
		Generated = type('Generated', classes, {})
		
	else:
		class Generated(instance.__class__, mod):
			pass
	instance.__class__ = Generated

	try:
		if mod.config not in calls:
			mod.config(instance)
	except:
		pass
	return instance



def change_class_of_instance(instance, *newclasses):
	newclasses = list(newclasses)
	if Serializable not in newclasses:
		newclasses.append(Serializable)

	Generated = type('Generated', tuple(newclasses), {})

	instance.__class__ = Generated

	return instance


def dist_from_entity(entity1, entity2):
	x0 = entity1.x
	y0 = entity1.y
	x1 = entity2.x
	y1 = entity2.y
	dx = x1 - x0
	dy = y1 - y0
	sumsq = dx * dx + dy * dy
	return math.sqrt(sumsq)
