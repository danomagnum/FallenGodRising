MAX_MESSAGES = 100

class ioCatcher(object):
	#replace sys.stdout with this class and you can just use print wherever you want.
	def __init__(self):
		self.messages = []
		self.new = 0
		self.newest_read = True
		self.silent = False
	def readlines(self, lines=10):
		#messages = ''.join(self.messages)
		if len(self.messages) > MAX_MESSAGES:
			self.messages = self.messages[-MAX_MESSAGES:]
		toshow = self.messages[-lines:]
		for x in range(1,self.new + 1):
			#toshow[-x] = '> ' + toshow[-x]
			toshow[-x] = '[color=lightest yellow]> ' + toshow[-x] + '[/color]'
		self.newest_read = True
		return toshow
		msgstring = ''
		for line in toshow:
			msgstring += str(line) + '\n'
		return msgstring
	
	def writeline(self, line):
		if not self.silent:
			if len(line) > 1:
				if self.newest_read:
					self.newest_read = False
					self.new = 0
				self.messages.append(line)
				self.new += 1
	def write(self, line):
		if not self.silent:
			if len(line) > 1:
				if self.newest_read:
					self.newest_read = False
					self.new = 0
				self.messages.append(line)
				self.new += 1

	def flush(self):
		pass

