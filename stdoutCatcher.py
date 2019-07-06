MAX_MESSAGES = 100
SHOW_AT_ONCE = 3

class ioCatcher(object):
	#replace sys.stdout with this class and you can just use print wherever you want.
	def __init__(self):
		self.messages = []
		self.silent = False
	def readlines(self):
		#messages = ''.join(self.messages)
		if len(self.messages) > MAX_MESSAGES:
			self.messages = self.messages[-MAX_MESSAGES:]
		toshow = self.messages[-SHOW_AT_ONCE:]
		return toshow
		msgstring = ''
		for line in toshow:
			msgstring += str(line) + '\n'
		return msgstring

	def writeline(self, line):
		if not self.silent:
			if len(line) > 1:
				self.messages.append(line)
	def write(self, line):
		if not self.silent:
			if len(line) > 1:
				self.messages.append(line)

