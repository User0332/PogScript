import re
from utils import throw, Token as _Token
from sys import exit
from pprint import pprint

class Lexer():
	def __init__(self, source_code):
		self.source_code = source_code

	def tokenize(self):
		self.modifier_commands = []
		tokens = []
		customizable = {
			"namespaces" : False, 
			"semicolons" : False,
			"braces" : False,
			"contextmanagers" : False,
			"oop" : False,
			"mainmethods" : False
		}

		

		working_code = self.source_code
		
		strings = re.finditer('".*?"', working_code)
		for string in strings:
			tokens.append(["STRING", string.group(), string.start()])
			working_code = working_code.replace(string.group(), " "*len(string.group()), 1)


		modifiers = re.finditer("\$.*\n", working_code, re.MULTILINE)
		for modifier in modifiers:
			self.modifier_commands.append(modifier.group().replace("$", "", 1)[:-1])
			working_code = working_code.replace(modifier.group(), " "*len(modifier.group()), 1)


		syntax_customizations = re.finditer("^using .*\n", working_code, re.MULTILINE)
		for customization in syntax_customizations:
			custom = customization.group().replace("using", "").replace("\n", "").replace(" ", "")
			working_code = working_code.replace(customization.group(), " "*len(customization.group()), 1)
			if custom in customizable.keys():
				customizable[custom] = True
			else:
				throw(f"Name Error: Syntax customization '{custom}' was not found.")
				exit(1)

		error_semicolons = re.finditer(";", working_code)
		for semi in error_semicolons:
			if not customizable["semicolons"]:
				throw("Invalid Syntax: Unknown token ';'")
				exit(1)

		assignments = re.finditer("=", working_code)
		for assignment in assignments:
			tokens.append(["ASSIGNMENT", "=", assignment.start()])
			working_code = working_code.replace("=", " ", 1)

		specials = re.finditer("[\.:,\[\]\(\)}{<>|]", working_code)
		for special in specials:
			tokens.append(["SPECIAL", special.group(), special.start()])
			working_code = working_code.replace(special.group(), " ", 1)

		operators = re.finditer("[/\*\-\+]", working_code)
		for operator in operators:
			tokens.append(["OPERATOR", operator.group(), operator.start()])
			working_code = working_code.replace(operator.group(), " ", 1)

		if not customizable["braces"]:
			indents = re.finditer(r"\t", working_code)
			for indent in indents:
				tokens.append(["INDENT", r"\t", indent.start()])
				working_code = working_code.replace(indent.group(), "    ", 1)

		funcs = re.finditer("(^|;| )def[\n ]", working_code, re.MULTILINE)
		for func in funcs:
			tokens.append(["FUNCTION", "def", func.start()])
			working_code = working_code.replace("def", "   ", 1)
				
		returns = re.finditer("(^|;| )return[\n ]", working_code, re.MULTILINE)
		for _return in returns:
			tokens.append(["RETURN", "return", _return.start()])
			working_code = working_code.replace("return", "      ")

		if customizable["namespaces"]:
			namespaces = re.finditer("(^|;| )namespace[\n ]", working_code, re.MULTILINE)
			for namespace in namespaces:
				tokens.append(["NAMESPACE", "namespace", namespace.start()])
				working_code = working_code.replace("namespace", "         ", 1)

		semicolons = re.finditer(";", working_code)
		for semicolon in semicolons:
			tokens.append(["NEWLINE", ";", semicolon.start()])
			working_code = working_code.replace(";", " ", 1)

		if not customizable["semicolons"]:
			newlines = re.finditer("\n", working_code)
			for newline in newlines:
				tokens.append(["NEWLINE", "\n", newline.start()])

		if customizable["contextmanagers"]:
			withs = re.finditer("(^|;| )with[\n ]", working_code, re.MULTILINE)
			for _with in withs:
				tokens.append(["WITH", "with", _with.start()])
				working_code = working_code.replace("with", "    ")

		if customizable["oop"]:
			classes = re.finditer("(^|;| )class[\n ]", working_code, re.MULTILINE)
			for _class in classes:
				tokens.append(["CLASS", "class", _class.start()])
				working_code = working_code.replace("class", "    ")

		vars = re.finditer("(^|;| )let[\n ]", working_code, re.MULTILINE)
		for var in vars:
			tokens.append(["VAR", "let", var.start()])
			working_code = working_code.replace("let", "   ", 1)

		
		identifiers = re.finditer("[a-zA-Z_0-9]+", working_code)
		for identifier in identifiers:
			try:
				int(identifier.group())
				continue
			except ValueError:
				pass
			tokens.append(["IDENTIFIER", identifier.group(), identifier.start()])
			working_code = working_code.replace(identifier.group(), " "*len(identifier.group()), 1)

		integers = re.finditer("[0-9]+", working_code)
		for integer in integers:
			tokens.append(["INTEGER", integer.group(), integer.start()])
			working_code = working_code.replace(integer.group(), " "*len(integer.group()), 1)
			

		tokens.append(["EOF", "reached end of file", float("inf")])

		return Token(tokens), customizable["braces"], customizable["mainmethods"]



class Token():
	def __init__(self, tokens):
		self.tokens = tokens

	def __repr__(self):
		return repr(self.tokens)

	def sort(self):
		positions = {
			}
		tokens = []

		for token in self.tokens:
			positions[token[2]] = [token[0], token[1]]

		token_positions = sorted(positions)

		for pos in token_positions:
			tokens.append(positions[pos])

		self.tokens = tokens
		self.positions = positions

		prev = _Token()
		idx = 0
		indent_count = 0
		current_indent_count = 0

		
		while idx < len(self.tokens):
			current = _Token(self.tokens[idx])

			if prev.type == "NEWLINE" and current.type == "INDENT":
				current_indent_count = 1
				for tok in self.tokens[idx:]:
					if tok[0] == "INDENT":
						current_indent_count+=1
					else:
						idx+=current_indent_count-1
						break

			for i in range(indent_count-current_indent_count):
				self.tokens.insert(idx, ["DEDENT", "-\\t"])

			indent_count = current_indent_count
			prev = current
			idx+=1

		