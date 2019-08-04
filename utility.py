import random
import inspect

def call_all_recursive(value, method, instance):
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
	#so the order can be reversed and they can be called from
	# the mose base to the most top-level.  So top-level takes precidence
	# if any of the same values are set
	calls.reverse()

	# finally call them all
	for call in calls:
		value = call(instance, value)
	return value

def call_all(method, instance):
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
	
