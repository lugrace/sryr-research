class Method:
	"""docstring for Method"""
	# names = [] #store as (name, [args], [lines inside])
	name = ""
	args = []
	lines = []
	methodsCalled = []
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

	def setArgs(self, newargs):
		self.args = newargs

	def setLines(self, newlines):
		self.lines = newlines

	def setDocs(self, newdocs):
		self.docs = newdocs

	def setMethodsCalled(self, methodsCalled):
		self.methodsCalled = methodsCalled

	def toString(self):
		numMethods = len(self.methodsCalled)
		returnMe = "I don't really do anything. I'm sorry."
		if(numMethods > 0):
			if(numMethods > 1):
				returnMe = "I call " + str(numMethods) + " methods. "
				returnMe = returnMe + "They are "
			else:
				returnMe = "I call " + str(numMethods) + " method. "
				returnMe = returnMe + "It is "
			
			for next in self.methodsCalled:
				returnMe = returnMe + next + ", "
			returnMe = returnMe[0:len(returnMe)-2] + ". "

		#add getDocs (documentation to strings)
		return returnMe

	def toStringPrint(self):
		print("I call these methods: ", self.methodsCalled)
		print("My name is ", self.name, " and I take ", self.args, " and here is my code ", self.lines, " and documentation: ", self.docs)



		