class Method:
	"""docstring for Method"""
	names = [] #store as (name, [args], [lines inside])

	def __init__(self, arg): #arg should be the method contents
		super(Method, self).__init__()
		self.arg = arg

	def return3(self):
		return 3
		