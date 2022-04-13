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
	def __init__(self, source_code: str):
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

		syntax_customizations = re_finditer("(^|;| |\t)using .*['\s]", working_code, RE_MULTILINE)
		for customization in syntax_customizations:
			custom = customization.group().replace("using", "").replace("\n", "").replace(" ", "")
			custom = "".join(custom.split())
			working_code = working_code.replace(customization.group(), " "*len(customization.group()), 1)
			if custom in customizable.keys():
				customizable[custom] = True
			else:
				code = get_code(self.source_code, customization.start())
				
				throw(f"POGCC 024: Syntax customization '{custom}' was not found.")


		comments = re_finditer("^#.*$", working_code, RE_MULTILINE)
		for comment in comments:
			working_code = working_code.replace(comment.group(), " "*len(comment.group()), 1)

		regexes = [
			['".*?"', "STRING"],
			["==|>=|<=|>|<", "COMPARISON_OP"],
			["=", "ASSIGNMENT"],
			["[\d]+\.[\d]+", "FLOAT"],
			["[\.:,\[\]\(\)}{|]", "SPECIAL"],
			["\*\*|[/\*\-\+]", "OPERATOR"],
			["(^|;| |\t)return['\s]", "RETURN", RE_MULTILINE],
			["(^|;| |\t)namespace['\s]", "NAMESPACE", RE_MULTILINE],
			["(^|;| |\t)int['\s]", "INT", RE_MULTILINE],
			["(^|;| |\t)char['\s]", "CHAR", RE_MULTILINE],
			["(^|;| |\t)float['\s]", "FLOAT", RE_MULTILINE],
			["(^|;| |\t)var['\s]", "VAR", RE_MULTILINE],
			["(^|;| |\t)ptr['\s]", "PTR", RE_MULTILINE],
			["(^|;| |\t)const['\s]", "CONST", RE_MULTILINE],
			["(^|;| |\t)func['\s]", "FUNC", RE_MULTILINE],
			["(^|;| |\t)is['\s]", "IDENTITY_COMPARISON", RE_MULTILINE],
			["(^|;| |\t)(not|or|and)['\s]", "UNARY_LOGICAL_OP", RE_MULTILINE],
			["(^|;| |\t)(if|else)['\s]", "CONDITIONAL_KEYWD"],
			["[a-z_]\w*", "IDENTIFIER", RE_IGNORECASE],
			["\d+", "INTEGER"]
		]

		for regex in regexes:
			matches = re_finditer(regex[0], working_code, regex[2]) if len(regex) > 2 else re_finditer(regex[0], working_code)

			for match in matches:
				group = match.group().strip()
				tokens.append([regex[1], group, match.start()])
				working_code = working_code.replace(group, " "*len(group), 1)


		if ";" in working_code and not customizable["semicolons"]:
			code = get_code(self.source_code, working_code.index(";"))
			
			throw("POGCC 019: Unknown token ';'", code)

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

		unlexed = "".join(working_code.split())
		if unlexed != "":
			code = get_code(self.source_code, working_code.index(unlexed[0]))
			
			throw(f"POGCC 019: Unknown token {unlexed[0]}", code)

			
		return TokenSorter(tokens), customizable["braces"], customizable["mainmethods"], customizable["semicolons"]
#
