import os, sys, re, tokenize, keyword, io
from method import Method
from collections import Counter
import nltk

#overall_documentation
messages = []
import_statements = []
code_length = 0
num_methods = 0

def start(filename):
	raw_source_input = open(filename).read().split("\n")
	source = parse_input(raw_source_input)
	basic_documentation(source)

def parse_input(raw_source_input):
	source = []
	for next in raw_source_input:
		num_enters = countEnters(next)
		if(num_enters > 0):
			append_me = next[num_enters*2-1:] #return the enters \t
		else:
			append_me = next
		if(len(append_me) > 0): #get rid of blank enters
			source.append((append_me, num_enters))
	return source

def basic_documentation(source):
	global import_statements, code_length, num_methods
	for next in source:
		if("import" in next[0]):
			import_statements.append(next[0][7:]) #get everything but 'import'
		if("def" in next[0]):
			num_methods = num_methods + 1
	code_length = len(source)

######	MESSAGES	######
def get_quick_summary(method_name, phrase=False): #pull verb/DO from method name
	verb = ""
	direct_object = ""
	if(phrase == False):
		return "This method " + verb + " " + direct_object + ". "
	else:
		return verb + " " + direct_object

def get_return_message(return_type):
	connecter = "a " #or an
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

def get_call_message(method_list, call_graph, phrase=False):
	

######	MISC	######
def countEnters(string):
    return string.count("\t")

start("foo2.txt")