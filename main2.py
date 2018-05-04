import os, sys, re, tokenize, keyword, io
from method import Method
from collections import Counter
import nltk

def start(filename):
	raw_source_input = open(filename).read().split("\n")
	source = parse_input(raw_source_input)
	print(source)

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

def countEnters(string):
    return string.count("\t")

start("foo2.txt")