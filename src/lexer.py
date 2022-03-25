from re import (
	finditer as re_finditer,
	MULTILINE as RE_MULTILINE,
	IGNORECASE as RE_IGNORECASE
)

from utils import (
	throw, 
	strgetline, 
	formatline
)

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
			["(^|;| |\t)return['\s]", "RETURN", RE_MULTILINE],
			["(^|;| |\t)namespace['\s]", "NAMESPACE", RE_MULTILINE],
			[";", "NEWLINE"],
			["(^|;| |\t)int['\s]", "INT", RE_MULTILINE],
			["(^|;| |\t)var['\s]", "VAR", RE_MULTILINE],
			["[a-z_]\w*", "IDENTIFIER", RE_IGNORECASE],
			["\d+", "INTEGER"]
		]

		for regex in regexes:
			matches = re_finditer(regex[0], working_code, regex[2]) if len(regex) > 2 else re_finditer(regex[0], working_code)

			for match in matches:
				tokens.append([regex[1], "".join(match.group().split()), match.start()])
				working_code = working_code.replace(match.group(), " "*len(match.group()), 1)

		modifiers = re_finditer("\$.*\n", working_code, RE_MULTILINE)
		for modifier in modifiers:
			self.modifier_commands.append(modifier.group().replace("$", "", 1)[:-1])
			working_code = working_code.replace(modifier.group(), " "*len(modifier.group()), 1)


		syntax_customizations = re_finditer("(^|;| |\t)using .*['\s]", working_code, RE_MULTILINE)
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

		logical_operator_kwds = re_finditer("(^|;| |\t)(not|or|and)['\s]", working_code, RE_MULTILINE)
		for kewdop in logical_operator_kwds:
			tokens.append(["LOGICAL_OPERATOR", "".join(kewdop.group().split()), kewdop.start()])
			working_code = working_code.replace(kewdop.group(), " "*(len(op.group())), 1)

		ifelses = re_finditer("(^|;| |\t)(if|else)['\s]", working_code, RE_MULTILINE)
		for ifelse in ifelses:
			tokens.append([ifelse.group().upper(), ifelse.group(), ifelse.start()])
			working_code = working_code.replace(ifelse.group(), " "*len(ifelse.group()), 1)

		if not customizable["braces"]:
			indents = re_finditer("	", working_code)
			for indent in indents:
				tokens.append(["INDENT", "	", indent.start()])

		semicolons = re_finditer(";", working_code)
		for semicolon in semicolons:
			tokens.append(["NEWLINE", ";", semicolon.start()])
			working_code = working_code.replace(";", " ", 1)

		if not customizable["semicolons"]:
			newlines = re_finditer("\n", working_code)
			for newline in newlines:
				tokens.append(["NEWLINE", "\n", newline.start()])

		comments = re_finditer("#.*$", working_code, RE_MULTILINE)
		for comment in comments:
			working_code = working_code.replace(comment.group(), " "*len(comment.group()), 1)

		unlexed = "".join(working_code.split())
		if unlexed != "":
			line, idx, linenum = strgetline(self.source_code, working_code.index(unlexed[0]))
			code = formatline(line, idx, linenum)
			throw(f"POGCC 019: Unknown token {unlexed[0]}", code)

			
		return Token(tokens), customizable["braces"], customizable["mainmethods"], customizable["semicolons"]

class Token():
	def __init__(self, tokens):
		self.tokens = tokens
		self.idx = 0

	def __repr__(self):
		return str(self.tokens)

	def __len__(self):
		return len(self.tokens)

	def __iter__(self):
		self.idx = 0
		return self

	def __next__(self):
		if self.idx < len(self.tokens)-1:
			val = self.tokens[self.idx]
			self.idx+=1
			return val
		else:
			raise StopIteration

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
