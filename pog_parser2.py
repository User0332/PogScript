from utils import Token, format_error as format
from keyword import iskeyword
from traceback import print_stack
import imports.pogscript_builtins
from sys import exit

class Parser:
	def __init__(self, tokens, braces):
		self.tokens = tokens
		self.braces = braces
		self.index = 0
		self.scopes = 0
		self.indent = ""
		self.exec_string = ""
		self.identities = [i for i in dir(imports.pogscript_builtins)] 



	def parse(self, waiting_for_close_scope=False):
		while self.index < len(self.tokens):
			current = Token(self.tokens[self.index])
			try:
				prev = Token(self.tokens[self.index-1])
			except IndexError:
				prev = Token()
			try:
				next = Token(self.tokens[self.index+1])
			except IndexError:
				next = Token()

			if current.type in ("CHAR", "VAR", "STRING_VAR"):
				self.parse_var(self.tokens[self.index:])
			elif current.type == "NEWLINE":
				self.exec_string += "\n" + self.indent
			elif current.type == "FUNCTION":
				self.get_function(self.tokens[self.index:])
			elif current.type == "IDENTIFIER":
				self.get_identity(current, prev)
			elif current.value == "}" and waiting_for_close_scope and self.braces:
				return
			elif current.type in ("SPECIAL", "STRING", "INTEGER"):
				self.exec_string+=current.value
			

			self.index+=1
			
		return self.exec_string

	def parse_var(self, stream):
		var_type = Token(stream[0])
		name = Token(stream[1])
		assignment = Token(stream[2])
		value = Token(stream[3])
		values = ""
		checked = 3

		print(f"getting variable {name.value}")
		self.identities.append(name.value)

		if name.type == "NEWLINE":
			print(format(f"Invalid Syntax: keyword '{var_type.value}' cannot be left by itself. Perhaps you meant to say '{var_type.value} variable = value'?"))
			exit(1)

		if name.type != "IDENTIFIER":
			print(format(f"Invalid Syntax: Bad variable name - {name.value} is an invalid variable name."))
			exit(1)

		if assignment.type != "ASSIGNMENT":
			print(format(f"Invalid Syntax: '{var_type.value} {name.value} {assignment.value}'\nMust include an assignment operator."))
			exit(1)

		if iskeyword(name.value):
			print(format(f"Invalid Syntax: '{name.value}' is a python keyword and is currently an unavaliable variable name."))
			exit(1)

		if var_type.type == "VAR":
			for i, token in enumerate(stream[3:]):
				token = Token(token, i)
				if token.is_odd and token.type == "NEWLINE":
					checked-=1
					break
				if token.is_even and token.type not in ("STRING", "INTEGER", "IDENTIFIER"):
					print(format(f"Invalid Syntax: cannot assign '{name.value}' to '{token.value}'"))
					exit(1)
				if token.is_odd and token.type != "OPERATOR":
					print(format("Invalid Syntax: Must have an operator between variable values in a variable declaration."))
					exit(1)

				values += token.value
				checked+=1
		
		elif var_type.type == "CHAR":
			self.exec_string += name.value + " " + assignment.value + f" Char({value.value})"
		else:
			self.exec_string += name.value + " " + assignment.value + f" String({value.value})"

			self.index+=checked
			return

		self.exec_string += name.value + " " + assignment.value + " " + values


		self.index+=checked

	def parse_array(self, stream):
		pass

	def get_function(self, stream):
		name = Token(stream[1])
		open_p = Token(stream[2])
		checked = 2
		params = []

		print(f"getting function {name.value}")
		self.identities.append(name.value)

		if name.type != "IDENTIFIER":
			print(format(f"Invalid Syntax: Bad function name. '{name.value}' is an invalid function name."))
			exit(1)
		if open_p.value != "(":
			print(format("Invalid Syntax: Must have opening parenthesis next to function name."))
			exit(1)

		for i, token in enumerate(stream[3:]):
			token = Token(token, i)
			checked+=1

			if token.value == ")":
				checked+=1
				break
			if token.is_even:
				if token.type != "IDENTIFIER":
					print(format("Invalid Syntax: parameters must be identifiers."))
					exit(1)
				else:
					params.append(token.value)
			if token.is_odd and token.value != ",":
				print(format("Invalid Syntax: Must have a comma between parenthesis in a function declaration."))
				exit(1)


		stream = stream[checked:]
		open_scope = Token(stream[0])

		if self.braces:
			if open_scope.value != "{":
				print(format("Invalid Syntax: Function must open a new scope"))
				exit(1)
		else:
			if open_scope.value != ":":
				print(format("Invalid Syntax: Function must open a new scope"))
				exit(1)

		self.exec_string += "def " + name.value + "(" + ",".join(params) + ") " + ":\n"
		if open_scope.value == "{":
			self.indent+="    "
			self.exec_string += self.indent

		self.index+= checked + 1

		self.parse(True)

		if self.braces:
			self.indent = self.indent.replace("    ", "", 1)

		self.exec_string+="\n"+self.indent


	def get_identity(self, identity, prev):
		if prev.value == ".":
			self.exe_string+=identity.value
		if identity.value in self.identities:
			self.exec_string+=identity.value
		else:
			print(format(f"Name Error: Unknown reference to '{identity.value}'"))
			exit(1)