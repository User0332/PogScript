from sys import stderr, exit
from argparser import ArgumentParser


errors = ""
warnings = ""
thrown = False

FAIL = "\033[31m"
END = "\033[0m"
BLUE = "\033[34m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"

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


def throw(message, code=""):
	global errors

	errors+=f"{FAIL}ERROR: {message+END}\n{code}"
	if not thrown:
		thrown = not thrown


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
	return exit(1) if errors != "" else 0

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

	def getaddr(self, name):
		return self.get(name)[1]

	def declare(self, name, dtype, address):
		self.attrs[name] = [dtype, address, None]

	def assign(self, name, value, index):
		if name not in self.symbols.keys():

			line, idx, linenum = strgetline(self.code, index)
			code = formatline(line, idx, linenum)
			throw(f"POGCC 027: Name Error: Attemped to assign to undeclared variable '{name}'", code)
		
		self.symbols[name][2] = value

	def delete(self, name):
		del self.symbols[name]