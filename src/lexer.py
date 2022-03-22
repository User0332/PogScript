import re
from utils import throw, strgetline, formatline

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


		syntax_customizations = re.finditer("(^|;| |\t)using .*['\n \t]", working_code, re.MULTILINE)
		for customization in syntax_customizations:
			custom = customization.group().replace("using", "").replace("\n", "").replace(" ", "")
			custom = "".join(custom.split())
			working_code = working_code.replace(customization.group(), " "*len(customization.group()), 1)
			if custom in customizable.keys():
				customizable[custom] = True
			else:
				line, idx, linenum = strgetline(self.source_code, customization.start())
				code = formatline(line, idx, linenum)
				throw(f"POG024: Syntax customization '{custom}' was not found.")
				

		if ";" in working_code and not customizable["semicolons"]:
			line, idx, linenum = strgetline(self.source_code, working_code.index(";"))
			code = formatline(line, idx, linenum)
			throw("POGCC019: Unknown token ';'", code)
				
		logical_operators = re.finditer("==|>=|<=|>|<", working_code)
		for op in logical_operators:
			tokens.append(["LOGICAL_OPERATOR", op.group(), op.start()])
			working_code = working_code.replace(op.group(), " "*(len(op.group())), 1)

		logical_operator_kwds = re.finditer("(^|;| |\t)(not|or|and)['\n \t]", working_code, re.MULTILINE)
		for kewdop in logical_operator_kwds:
			tokens.append(["LOGICAL_OPERATOR", "".join(kewdop.group().split()), kewdop.start()])
			working_code = working_code.replace(kewdop.group(), " "*(len(op.group())), 1)

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
				
		returns = re.finditer("(^|;| |\t)return['\n \t]", working_code, re.MULTILINE)
		for _return in returns:
			tokens.append(["RETURN", "return", _return.start()])
			working_code = working_code.replace("return", "      ", 1)

		ifelses = re.finditer("(^|;| |\t)(if|else)['\n \t]", working_code, re.MULTILINE)
		for ifelse in ifelses:
			tokens.append([ifelse.group().upper(), ifelse.group(), ifelse.start()])
			working_code = working_code.replace(ifelse.group(), " "*len(ifelse.group()), 1)

		if not customizable["braces"]:
			indents = re.finditer("	", working_code)
			for indent in indents:
				tokens.append(["INDENT", "	", indent.start()])

		namespaces = re.finditer("(^|;| |\t)namespace['\n \t]", working_code, re.MULTILINE)
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

		intvars = re.finditer("(^|;| |\t)int['\n \t]", working_code, re.MULTILINE)
		for intvar in intvars:
			tokens.append(["INTVAR", "int", intvar.start()])
			working_code = working_code.replace("int", "   ", 1)

		
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
			
		return Token(tokens), customizable["braces"], customizable["mainmethods"]

class Token():
	def __init__(self, tokens):
		self.tokens = tokens

	def __repr__(self):
		return str(self.tokens)

	def sort(self):
		positions = {
			}
		tokens = []
	

		for token in self.tokens:
				positions[token[2]] = [token[0], token[1], token[2]]


		token_positions = sorted(positions)

		for pos in token_positions:
			tokens.append(positions[pos])

		tokens.append(["EOF", "Reached end of file", -1])

		self.tokens = tokens
		self.positions = positions