class ioCatcher(object):
	#replace sys.stdout with this class and you can just use print wherever you want.
	def __init__(self):
		self.messages = []
	def readlines(self):
		messages = ''.join(self.messages)
		self.messages = []
		return messages.split('\n')
	def writeline(self, line):
		self.messages.append(line)
	def write(self, line):
		self.messages.append(line)
