from sys import stderr, exit


errors=""
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
	global thrown
	errors+=f"{FAIL}ERROR: {message+END}\n{code}"
	if not thrown:
		thrown = not thrown


def warn(string, code=""):
	global errors
	errors += f"{YELLOW}WARNING: {string}{END}\n{code}"

def throwerrors():
	global errors
	stderr.write(errors)
	errors = ""

def checkfailure():
	global thrown
	if thrown: exit(1)

class Token:
	def __init__(self, token=None, num=0):
		if token is None:
			self.type = None
			self.value = None
			self.idx = None
		else:
			self.type = token[0]
			self.value = token[1]
			self.idx = token[2]
			self.is_even = num % 2 == 0
			self.is_odd = not self.is_even

	def __repr__(self):
		return str(self.type)+" -> "+str(self.value)

	def __str__(self):
		return str([self.type, self.value])


class AttrTable:
	def __init__(self):
		self.attrs = {}
		self.parent = False

	def get(self, name):
		attr = self.attrs.get(name, None)
		if attr is None:
			if self.parent:
				return self.parent.get(name)
			else:
				#get arrows pointing to error
				throw(f"POGCC 027: Name Error: Name '{name}' not defined.")
		
		return attr

	def getaddr(self, name):
		return self.get(name)[1]

	def declare(self, name, dtype, address):
		self.attrs[name] = [dtype, address]

	def assign(self, name, value):
		if name not in self.attrs.keys():
			throw(f"POGCC 027: Name Error: Attemped to assign to undeclared variable {name}")
		self.attrs[name][2] = value

	def delete(self, name):
		del self.attrs[name]