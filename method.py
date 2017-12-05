class Method:
	"""docstring for Method"""
	# names = [] #store as (name, [args], [lines inside])
	name = ""
	args = []
	lines = []
	docs = "Documentation not available" #string; summarizes what the method does

	# def __init__(self, arg): #arg should be the method contents
	# 	super(Method, self).__init__()
	# 	self.arg = arg

	def __init__(self, name, args, lines):
		super(Method, self).__init__()
		self.name = name
		self.args = args
		self.lines = lines

	def return3(self):
		return 3

	def getName(self):
		return self.name

	def getArgs(self):
		return self.args

	def getLines(self):
		return self.lines

	def getDocs(self):
		return self.docs

	def setName(self, newname):
		self.name = newname

	def setArgs(sef, newargs):
		self.args = newargs

	def setLines(self, newlines):
		self.lines = newlines

	def setDocs(self, newdocs):
		self.docs = newdocs

	def toString(self):
		print("My name is ", name, " and I take ", args, " and here is my code ", lines, " and documentation: ", docs)
		