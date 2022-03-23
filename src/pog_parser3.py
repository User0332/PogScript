from utils import Token, formatline, strgetline, throw, warn
from json import loads

class NumNode:
	def __init__(self, token):
		self.token = token

	def __repr__(self):
		return f'{{"Number Literal" : {self.token.value} }}'

class BinOpNode:
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def __repr__(self):
		return f'{{ "Binary Operation {self.op.value}" : [{self.left}, {self.right}] }}'

class UnaryOpNode:
	def __init__(self, op, node):
		self.op = op
		self.node = node

	def __repr__(self):
		return f'{{"Unary Operation {self.op.value}" : {self.node} }}'

class VariableDeclarationNode:
	def __init__(self, dtype, name, idx):
		self.dtype = dtype
		self.name = name
		self.idx = idx

	def __repr__(self):
		return f'{{"Variable Declaration @Idx[{self.idx}]" : {{ "type" : "{self.dtype}", "name" : "{self.name}" }} }}'

class VariableDefinitionNode:
	def __init__(self, dtype, name, expression, idx):
		self.dtype = dtype
		self.name = name
		self.expr = str(expression)
		self.idx = idx

	def __repr__(self):
			return f'{{"Variable Definition @Idx[{self.idx}]" : {{ "type" : "{self.dtype}", "name" : "{self.name}", "value" : {self.expr} }} }}'

class VariableAccessNode:
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return f'{{"Variable Reference" : {{ "name" : "{self.name}" }} }}'

class UnimplementedNode:
	def __init__(self):
		pass

	def __repr__(self):
		return '{ "Unimplemented Node" : null }'


class Parser3:
	def __init__(self, tokens, braces, semicolons, code):
		self.tokens = tokens
		self.braces = braces
		self.semicolons = semicolons
		self.code = code
		self.idx = -1
		self.advance()

	def parse(self):
		ast = {}

		while self.current.type != "EOF":
			expr = str(self.expr())

			if self.current.type != "NEWLINE":
				end_statement_char = "';'" if self.semicolons else "<newline>"
				throw(f"POGCC 030: Missing end-of-statement token {end_statement_char}")
			
			self.advance()

			expr = "{}" if expr is None else expr
	

			ast[f"Expression @Idx[{self.idx}]"] = loads(expr)

		return ast

	def advance(self):
		self.idx+=1
		try:
			self.current = Token(self.tokens[self.idx])
		except IndexError as e:
			self.current.type = "EOF"

	def power(self):
		return self.bin_op(self.atom, ("^", ), self.factor)

	def factor(self):
		current = self.current

		if current.value in ("+", "-"):
			self.advance()
			fac = self.factor()
			if fac is None:
				self.idx-=2
				self.advance()
				
				line, idx, linenum = strgetline(self.code, self.current.idx)
				code = formatline(line, idx, linenum)
				throw("POGCC 018: Expecting value or expression", code)
				return UnimplementedNode()
			return UnaryOpNode(current, fac)

		return self.power()

	def bin_op(self, func_a, ops, func_b=None):
		if func_b is None:
			func_b = func_a

		left = func_a()

		while self.current.value in ops:
			op = self.current
			self.advance()
			right = func_b()
			
			left = BinOpNode(left, op, right)		
		

		return left

	def term(self):
		return self.bin_op(self.factor, ('*', '/'))
		
	def atom(self):
		current = self.current

		if current.type == "IDENTIFIER":
			self.advance()
			return VariableAccessNode(current)

		elif current.type in ("INTEGER", "FLOAT"):
			self.advance()
			return NumNode(current)

		elif current.value == "(":
			self.advance()
			expression = self.expr()
			if expression is None:
				expression = {}
			if self.current.value == ")":
				self.advance()
				return expression
			else:
				line, idx, linenum = strgetline(self.code, self.current.idx)
				code = formatline(line, idx, linenum)
				throw("POGCC 018: Expected ')'", code)
				return UnimplementedNode()

		line, idx, linenum = strgetline(self.code, self.current.idx)
		code = formatline(line, idx, linenum)
		throw("POGCC 018: Expected int, float, identifier, '+', '-', or '('", code)
		self.advance()
		return UnimplementedNode()

	def comp_expr(self):
		if self.current.type == "NOT":
			op = self.current
			self.advance()

			node = self.comp_expr()
			return UnaryOpNode(op, node)

		return self.bin_op(self.num_expr, ("==", "!=", "<", ">", "<=", ">="))
		

	def num_expr(self):
		return self.bin_op(self.term, ("+", "-"))

	def expr(self):
		if self.current.type == "INT":
			self.advance()
			if self.current.type == "VAR":
				self.advance()
				if self.current.type != "IDENTIFIER":
					self.idx-=2
					self.advance()
					
					line, idx, linenum = strgetline(self.code, self.current.idx)
					code = formatline(line, idx, linenum)
					throw("POGCC 018: Expected Indentifier after 'let'", code)
					return UnimplementedNode()
			
				name = self.current.value
				self.advance()

				if self.current.type == "NEWLINE":
					self.advance()
					return VariableDeclarationNode("DWORD int", name, self.idx)

				elif self.current.value == "=":
					self.advance()
					expr = self.expr()
					if expr is None:
						self.idx-=2
						self.advance()

						line, idx, linenum = strgetline(self.code, self.current.idx)
						code = formatline(line, idx, linenum)
						throw("POGCC 018: Expected value after assignment operator '='", code)
						return UnimplementedNode()
					else:
						return VariableDefinitionNode("DWORD int", name, expr, self.idx)
				else:
					line, idx, linenum = strgetline(self.code, self.current.idx)
					code = formatline(line, idx, linenum)
					throw("POGCC 018: Expecting '=' or <newline>", code)
					return UnimplementedNode()


		return self.bin_op(self.comp_expr, ('and', 'or'))