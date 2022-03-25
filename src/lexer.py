from re import (
	finditer as re_finditer,
	MULTILINE as RE_MULTILINE,
	IGNORECASE as RE_IGNORECASE
)

from utils import (
	throw, 
	get_code,
	TokenSorter
)

#Lexer
class Lexer():
	def __init__(self, source_code):
		self.source_code = source_code

	#Uses regex patterns to search for tokens
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
				code = get_code(self.source_code, customization.start())
				
				throw(f"POG 024: Syntax customization '{custom}' was not found.")
				

		if ";" in working_code and not customizable["semicolons"]:
			code = get_code(self.source_code, working_code.index(";"))
			
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
			code = get_code(self.source_code, working_code.index(unlexed[0]))
			
			throw(f"POGCC 019: Unknown token {unlexed[0]}", code)

			
		return TokenSorter(tokens), customizable["braces"], customizable["mainmethods"], customizable["semicolons"]
#
