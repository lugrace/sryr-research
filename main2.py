import os, sys, re, tokenize, keyword, io
from method import Method
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
# nltk.download()

#overall_documentation
source = []
messages = []
import_statements = []
code_length = 0
num_methods = 0
list_of_methods = []
simplified_method_names = []

def start(filename):
	global source
	raw_source_input = open(filename).read().split("\n")
	source = parse_input(raw_source_input)
	print("Source: ", source)
	print()
	basic_documentation(source)

def parse_input(raw_source_input):
	source = []
	for next in raw_source_input:
		num_enters = countEnters(next)
		if(num_enters > 0):
			append_me = next[num_enters:] #return the enters \t
		else:
			append_me = next
		if(len(append_me) > 0): #get rid of blank enters
			source.append((append_me, num_enters))
	return source

def basic_documentation(source):
	global import_statements, code_length, num_methods, list_of_methods, simplified_method_names
	for next in source:
		if("import" in next[0]):
			import_statements.append(next[0][7:]) #get everything but 'import'
		if("def" in next[0]):
			num_methods = num_methods + 1
			list_of_methods.append(next[0])
	code_length = len(source)
	simplified_method_names = simplify_method_names(source)

######	MESSAGES	######
def get_quick_summary(method_name, phrase=False): #pull verb/DO from method name
	result = parse_method_name(method_name)
	verb = result[0]
	direct_object = result[1]
	if(phrase == False):
		return "This method " + verb + " " + direct_object + ". "
	else:
		return verb + " " + direct_object

def get_return_message(return_type):
	connecter = "a " #or an
	real_return_type = ""
	#I actually dont really know how to do this BRB; rn = arg in return statement
	return "It returns " + connecter + return_type 

def get_output_message(return_type, method_list): #returns a list of output messages
	#so if we have two, we can do aggregation
	verb = " is "
	output_messages = []
	for next in method_list:
		quick_sum = get_quick_summary(next, True)
		output_message = "The " + return_type + " returned by this method " + verb \
							+ "used to " + quick_sum + "."
		output_messages.append(output_message)
	return output_messages

def get_call_message(method_list, phrase=False):
	call_messages = []
	for next in method_list:
		quick_sum = get_quick_summary(next, True)
		if(phrase == False):
			call_message = "This method calls a method that " + quick_sum + "." 
		else:	
			call_message = "Calls a method that " + quick_sum
		call_messages.append(call_message)
	return call_messages

def get_use_message(usage_example):
	assignment_statement = find_assignment_statement(usage_example)
	subject = "This method "
	verb = " can be used "
	prep = " as a "
	return subject + verb + prep + assignment_statement + " statement" + ". For example: " \
			+ usage_example

######	MISC	######
def countEnters(string):
    return string.count("\t")

def find_assignment_statement(example):
	statement = ""
	if("if" in example):
		statement = "conditional"
	elif("for" in example or "while" in example):
		statement = "iteration"
	elif("=" in example):
		statement = "assignment"
	else:
		statement = "procedural"
	return statement

def parse_method_name(method_name): #def getTime():
	pos_first_paran = method_name.find("(")
	parsed = method_name[4:pos_first_paran].split("_")
	remake_phrase = ""
	verb = ""
	direct_object = ""
	for next in parsed:
		remake_phrase = remake_phrase + next + " "
	text = word_tokenize(remake_phrase) #call NLTK on remake_phrase to tag
	tagged = nltk.pos_tag(text)
	for next in tagged:
		if(next[1] == "VB"):
			verb = next[0]
		elif(next[1] == "NN"):
			direct_object = next[0]
	return (verb, direct_object)

def get_method(method_name, source): #def method_name
	method = []
	pos_method_start = 0
	for i in range (0, len(source)):
		if(source[i][0] == method_name):
			pos_method_start = i
	method.append(source[pos_method_start]) #get method name
	pos_method_start = pos_method_start + 1
	while(pos_method_start < len(source) and source[pos_method_start][1] != 0):
		method.append(source[pos_method_start])
		pos_method_start = pos_method_start + 1
	return method

def simplify_method_names(source):
	global list_of_methods, simplified_method_names
	simplified = []
	for next in list_of_methods:
		pos_first_paran = next.find("(")
		parsed = next[4:pos_first_paran]
		simplified.append(parsed)
	return simplified

def make_call_graph(source, simplified_method_names):
	graph = {}
	#everything that this method calls
	for i in range(0, len(simplified_method_names)):
		next = simplified_method_names[i]
		methods = []
		this_method = get_method(list_of_methods[i], source) #coordinates
		for next_line in this_method:
			next_line = next_line[0]
			for every_method in simplified_method_names:
				if(next != every_method and every_method in next_line):
					methods.append(every_method)
					#find a way to add an example
		graph[next] = set(methods)
	return graph

def build_index(links): #adjacency matrix
	method_list = links.keys()
	return {method: index for index, method in enumerate(method_list)}

######	RUN ######
start("foo2.txt")

######	TEST	######
# print(get_quick_summary("def get_the_time():"))
# print(get_method("def return_the_variable_x(x):", source))
# print(simplify_method_names(source))
print(build_index(make_call_graph(source, simplified_method_names)))



