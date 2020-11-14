import sys
HEADER = ['import self_save as _self_save\n', 
          '_save = _self_save.gen_save_func(__file__, __name__)\n',
	  '################\n',
	  '#Only Edit Below This Line\n',
	  '################\n\n']

def gen_save_func(file, name):
	def save(headers=True):
		module = sys.modules[name]
		vars = dir(module)

		lines = []
		for var in vars:
			if var[0] != '_':
				vardef = repr(module.__dict__[var])
				lines.append('{} = {}\n'.format(var, vardef))

		write_self = open(file, 'w')
		if headers:
			write_self.writelines(HEADER)
		write_self.writelines(lines)
		write_self.close()

	return save

def bootstrap(module):
	module._save = gen_save_func(module.__file__, module.__name__)


def save_module(module):
	save_func = gen_save_func(module.__file__, module.__name__)
	save_func(headers=False)
