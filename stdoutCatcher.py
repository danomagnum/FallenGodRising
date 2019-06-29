class ioCatcher(object):
	#replace sys.stdout with this class and you can just use print wherever you want.
	def __init__(self):
		self.messages = []
		self.silent = False
	def readlines(self):
		messages = ''.join(self.messages)
		self.messages = []
		return messages.split('\n')
	def writeline(self, line):
		if not self.silent:
			self.messages.append(line)
	def write(self, line):
		if not self.silent:
			self.messages.append(line)
