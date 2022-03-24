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

		regexes = [
			['".*?"', "STRING"],
			["==|>=|<=|>|<", "LOGICAL_OPERATOR"],
			["=", "ASSIGNMENT"],
			["[\d]+\.[\d]+", "FLOAT"],
			["[\.:,\[\]\(\)}{<>|]", "SPECIAL"],
			["\*\*|[/\*\-\+]", "OPERATOR"],
			["(^|;| |\t)return['\s]", "RETURN", re.MULTILINE],
			["(^|;| |\t)namespace['\s]", "NAMESPACE", re.MULTILINE],
			[";", "NEWLINE"],
			["(^|;| |\t)int['\s]", "INT", re.MULTILINE],
			["(^|;| |\t)var['\s]", "VAR", re.MULTILINE],
			["[a-z_]\w*", "IDENTIFIER", re.IGNORECASE],
			["\d+", "INTEGER"]
		]

		for regex in regexes:
			matches = re.finditer(regex[0], working_code, regex[2]) if len(regex) > 2 else re.finditer(regex[0], working_code)

			for match in matches:
				tokens.append([regex[1], match.group().strip(), match.start()])
				working_code = working_code.replace(match.group().strip(), " "*len(match.group()), 1)

		modifiers = re.finditer("\$.*\n", working_code, re.MULTILINE)
		for modifier in modifiers:
			self.modifier_commands.append(modifier.group().replace("$", "", 1)[:-1])
			working_code = working_code.replace(modifier.group(), " "*len(modifier.group()), 1)


		syntax_customizations = re.finditer("(^|;| |\t)using .*['\s]", working_code, re.MULTILINE)
		for customization in syntax_customizations:
			custom = customization.group().replace("using", "").replace("\n", "").replace(" ", "")
			custom = "".join(custom.split())
			working_code = working_code.replace(customization.group(), " "*len(customization.group()), 1)
			if custom in customizable.keys():
				customizable[custom] = True
			else:
				line, idx, linenum = strgetline(self.source_code, customization.start())
				code = formatline(line, idx, linenum)
				throw(f"POG 024: Syntax customization '{custom}' was not found.")
				

		if ";" in working_code and not customizable["semicolons"]:
			line, idx, linenum = strgetline(self.source_code, working_code.index(";"))
			code = formatline(line, idx, linenum)
			throw("POGCC 019: Unknown token ';'", code)

		logical_operator_kwds = re.finditer("(^|;| |\t)(not|or|and)['\s]", working_code, re.MULTILINE)
		for kewdop in logical_operator_kwds:
			tokens.append(["LOGICAL_OPERATOR", "".join(kewdop.group().split()), kewdop.start()])
			working_code = working_code.replace(kewdop.group(), " "*(len(op.group())), 1)

		ifelses = re.finditer("(^|;| |\t)(if|else)['\s]", working_code, re.MULTILINE)
		for ifelse in ifelses:
			tokens.append([ifelse.group().upper(), ifelse.group(), ifelse.start()])
			working_code = working_code.replace(ifelse.group(), " "*len(ifelse.group()), 1)

		if not customizable["braces"]:
			indents = re.finditer("	", working_code)
			for indent in indents:
				tokens.append(["INDENT", "	", indent.start()])

		semicolons = re.finditer(";", working_code)
		for semicolon in semicolons:
			tokens.append(["NEWLINE", ";", semicolon.start()])
			working_code = working_code.replace(";", " ", 1)

		if not customizable["semicolons"]:
			newlines = re.finditer("\n", working_code)
			for newline in newlines:
				tokens.append(["NEWLINE", "\n", newline.start()])
			
		return Token(tokens), customizable["braces"], customizable["mainmethods"], customizable["semicolons"]

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