import inspect

def call_all_configs(instance):
	mro = list(inspect.getmro(instance.__class__))
	calls = set()
	for m in mro:
		try:
			call = m.config
			calls.add(call)
		except:
			pass
	for call in calls:
		call(instance)

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
