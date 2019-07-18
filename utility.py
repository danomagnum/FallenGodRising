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
