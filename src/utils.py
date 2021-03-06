from argparse import ArgumentParser

from sys import (
	stderr, 
	exit
)

#Error buffers
errors = ""
warnings = ""
thrown = False
#


#Color Constants
FAIL = "\033[31m"
END = "\033[0m"
BLUE = "\033[34m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
#


#Getting code for error throwing
def get_code(string, index):
	return formatline(*strgetline(string, index))

def formatline(line, idx, linenum):
	lineno = "ln "+str(linenum)
	code = BLUE+lineno+END+" "+line+"\n"
	for i, char in enumerate(line):
		if char == "\t":
			code+="\t"
		else:
			code+=" "

		if i == idx:
			break

	linenolen = len(lineno)+1
	code+=(" "*linenolen)+"^^^\n"
	return code

def strgetline(string, index):
	current_idx = 0
	for i, line in enumerate(string.splitlines()):
		current_idx+=1
		for j in range(1, len(line)):
			current_idx+=1
			if current_idx == index:
				return [line, j, i+1]

		if current_idx == index:
			return [line, j+1, i+1]

	return ["", 0, 0]
#


#Error throwing functions
def throw(message, code=""):
	global errors
	global thrown

	errors+=f"{FAIL}ERROR: {message+END}\n{code}"
	thrown = True


def warn(string, code=""):
	global warnings

	warnings+=f"{YELLOW}WARNING: {string}{END}\n{code}"

def throwerrors():
	global errors

	stderr.write(errors)
	errors = ""

def printwarnings():
	global warnings

	stderr.write(warnings)
	warnings = ""

def checkfailure():
	exit(1) if thrown else None
#

#Dictionary of compatible types
compatible_types = \
{
	"int var": (
		"int var", 
		"ushort var", 
		"ishort var", 
		"char var",

	),

	"ishort var": (
		"ishort var"
	),

	"ilong var": (
		"ilong var",
		"uint var",
		"ushort var",
		"int var",
		"char var",
		"ishort var"
	),

	"uint var": (
		"uint var",
		"ushort var"
	),

	"ushort var": (
		"ushort var"
	),

	"ulong var": (
		"ulong var",
		"uint var",
		"ushort var"
	),

	"float var": (
		"float var",
		"float64 var"
	),

	"float64 var": (
		"float64 var"
	),

	"char var" : (
		"char var",
		"int var"
	)
}
#

#Custom Exception used in the ast preprocessor
class NonConstantNumericalExpressionException(Exception):
	pass
#

#Utility Classes
class Token:
	def __init__(self, token=None):
		token = token if token else [None, None, None]
		self.type = token[0]
		self.value = token[1]
		self.idx = token[2]

	def __repr__(self):
		return str(self.type)+" -> "+str(self.value)

	def __str__(self):
		return str([self.type, self.value])

class TokenSorter:
	def __init__(self, tokens: list):
		self.tokens = tokens

	def __repr__(self):
		return str(self.tokens)

	def __len__(self):
		return len(self.tokens)

	def __iter__(self):
		return self.tokens.__iter__()

	def __next__(self):
		return self.tokens.__next__()

	def sort(self):
		positions = {}
		tokens = []
	
		for token in self.tokens:
				positions[token[2]] = [token[0], token[1], token[2]]

		token_positions = sorted(positions)

		for pos in token_positions:
			tokens.append(positions[pos])

		tokens.append(["EOF", "Reached end of file", tokens[-1][2]+1])

		self.tokens = tokens
		self.positions = positions

class ArgParser(ArgumentParser):
	def error(self, message):
		throw(f"Fatal Error POGCC 031: {message.capitalize()}")
		throwerrors()
		exit(1)

class SymbolTable:
	def __init__(self, code):
		self.symbols = {}
		self.parent = False
		self.code = code

	def get(self, name, index):
		attr = self.symbols.get(name, None)
		if attr is None:
			if self.parent:
				return self.parent.get(name)
			else:
				
				line, idx, linenum = strgetline(self.code, index)
				code = formatline(line, idx, linenum)
				throw(f"POGCC 027: Name Error: Name '{name}' not defined.", code)
		
		return attr

	def declare(self, name, dtype, size, address):
		self.symbols[name] = {
			"type" : dtype, 
			"size" : size, 
			"address" : address, 
			"value" : None
			}

	def assign(self, name, value, index):
		if name not in self.symbols.keys():
			
			line, idx, linenum = strgetline(self.code, index)
			code = formatline(line, idx, linenum)
			throw(f"POGCC 027: Name Error: Attemped to assign to undeclared variable '{name}'", code)
		#check if value is too large to be held (size > self.symbols[name]['size'])


		self.symbols[name]['value'] = value
		return self.symbols[name]['address']

	def delete(self, name):
		del self.symbols[name]

class TypeTable:
	def __init__(self):
		self.symbols: dict = {}

	def add(self, name, dtype):
		self.symbols[name] = dtype

	def get(self, name):
		return self.symbols.get(name, None)

	def remove(self, name):
		self.symbols.pop(name, None)
#