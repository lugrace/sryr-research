class Method:
	"""docstring for Method"""
	# names = [] #store as (name, [args], [lines inside])
	name = ""
	args = []
	lines = []

	def __init__(self, arg): #arg should be the method contents
		super(Method, self).__init__()
		self.arg = arg

	def return3(self):
		return 3

	def getName(self):
		return name

	def getArgs(self):
		return args

	def getLines(self):
		return lines
		