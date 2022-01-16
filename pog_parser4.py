from utils import Token, throw, BLUE, GREEN, END
from sys import exit
from json import loads

class Parser4:
	def __init__(self, tokens):
		self.tokens = tokens
		self.idx = -1
		self.ast = {}
		self.advance()

	def advance(self):
		self.idx+=1
		try:
			self.current = Token(self.tokens[self.idx])
		except IndexError:
			return

	def parse(self, option=None):
		while self.idx <= len(self.tokens):
			if self.current.type in ("INTEGER", "FLOAT"):
				numparser = NumParser4(self.tokens)
				numparser.set_index(self.idx)
				num_ast = str(numparser.parse())
				self.ast[f"{GREEN}Numerical Expression @Idx[{self.idx}]{END}"] = loads(num_ast)
				self.idx = numparser.idx-1
			elif self.current.type == "VAR":
				varparser = VarParser4(self.tokens)
				varparser.set_index(self.idx)
				self.ast[f"{BLUE}Variable Declaration @Idx[{self.idx}]{END}"] = loads(varparser.parse())
				self.idx = varparser.idx-1
			elif self.current.type == "FUNCTION":
				funcparser = FuncParser4(self.tokens)
				funcparser.set_index(self.idx)
				self.ast[f"{BLUE}Function Declaration @Idx[{self.idx}]{END}"] = funcparser.parse()
				self.idx = funcparser.idx-1
			elif option == "funcend" and self.current.value == '}':
				return self.ast



			self.advance()



		return self.ast

class FuncParser4:
	def __init__(self, tokens):
		self.tokens = tokens
		self.idx = -1
		self.advance()

	def set_index(self, idx):
		self.idx = idx
		try:
			self.current = Token(self.tokens[self.idx])
		except IndexError:
			return

	def parse(self):	
		self.advance()
		funcname = self.current
		self.advance()
		#Normally would parse args, but for now just skipping parenthesis
		#Can get argparser from pog_parser2 old source code
		self.advance()
		self.advance()
		open_scope = self.current
		self.advance()
		ast = { "Keyword" : "def", "Name" : funcname.value, "Open scope" : open_scope.value, "Contents" : None}
		parser = Parser4(self.tokens)
		parser.idx = self.idx-1
		parser.advance()
		ast["Contents"] = parser.parse("funcend")
		self.set_index(parser.idx)
		ast["Close Scope"] = "}"

		return ast

	def advance(self):
		self.idx+=1
		try:
			self.current = Token(self.tokens[self.idx])
		except IndexError:
			return

class VarParser4:
	def __init__(self, tokens):
		self.tokens = tokens
		self.idx = -1
		self.advance()

	def set_index(self, idx):
		self.idx = idx
		try:
			self.current = Token(self.tokens[self.idx])
		except IndexError:
			return

	def parse(self):	
		self.advance()
		var = self.current
		self.advance()
		assign = self.current
		self.advance()
		ast = f'{{ "Keyword" : "let", "Name" : "{var.value}", "Assignment" : "{assign.value}", "Contents" : '
		if self.current.type == "INTEGER":
			numparser = NumParser4(self.tokens)
			numparser.set_index(self.idx)
			result = str(numparser.parse())
			ast+='"'+result+'"'
			self.idx = numparser.idx
		
		elif self.current.type == "STRING":
			string = self.current.value.replace('"', "'")
			ast+=f'"String Literal {string}"'
		elif elf.current.type == "IDENTIFIER":
			ast+=f'"Identifier {self.current.value}"'
		else:
			throw("Type Error: Something went wrong with variable parsing")

		self.advance()

		ast+="}"
		return ast

	def advance(self):
		self.idx+=1
		try:
			self.current = Token(self.tokens[self.idx])
		except IndexError:
			return

		if self.current.type == "NEWLINE":
			return


class NumNode:
	def __init__(self, token):
		self.token = token

	def __repr__(self):
		return "Number Literal " + self.token.value

class BinOpNode:
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def __repr__(self):
		ast = f'{{ "Binary Operation {self.op.value}" : ['

		if type(self.left) is NumNode:
			ast+=f'"{self.left}"'
		else:
			ast+=f"{self.left}"

		if type(self.right) is NumNode:
			ast+=f', "{self.right}"]'
		else:
			ast+=f", {self.right}]"

		ast += "}"

		return ast


class NumParser4:
	def __init__(self, tokens):
		self.tokens = tokens
		self.idx = -1
		self.advance()

	def parse(self):
		ast = self.expr()

		return ast


	def advance(self):
		self.idx+=1
		try:
			self.current = Token(self.tokens[self.idx])
		except IndexError:
			return

		if self.current.type == "NEWLINE":
			return
			
	def set_index(self, idx):
		self.idx = idx
		try:
			self.current = Token(self.tokens[self.idx])
		except IndexError:
			return

	def factor(self):
		if self.current.type in ("INTEGER", "FLOAT"):
			current = self.current
			self.advance()
			return NumNode(current)
		

	def bin_op(self, func, ops):
		left = func()

		while self.current.value in ops:
			op = self.current
			self.advance()
			right = func()
			
			left = BinOpNode(left, op, right)		
			

		return left


	def term(self):
		return self.bin_op(self.factor, ('*', '/'))
		

	def expr(self):
		return self.bin_op(self.term, ('+', '-'))