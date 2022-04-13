from json import loads

from utils import (
	Token, 
	get_code,
	throw, 
	warn
)


#Node Utility Classes
class Node:
	pass

class NumNode(Node):
	def __init__(self, token: Token):
		self.token = token

	def __repr__(self):
		return f'{{"Numerical Constant" : {self.token.value} }}'

class BinOpNode(Node):
	def __init__(self, left: Node, op: Token, right: Node):
		self.left = left
		self.op = op
		self.right = right

	def __repr__(self):
		return f'{{ "Binary Operation {self.op.value}" : [{self.left}, {self.right}] }}'

class UnaryOpNode(Node):
	def __init__(self, op: Token, node: Node):
		self.op = op
		self.node = node

	def __repr__(self):
		return f'{{"Unary Operation {self.op.value}" : {self.node} }}'

class VariableDeclarationNode:
	def __init__(self, dtype: str, name: str):
		self.dtype = dtype
		self.name = name

	def __repr__(self):
		return f'{{"Variable Declaration" : {{ "type" : "{self.dtype}", "name" : "{self.name}" }} }}'

class VariableDefinitionNode:
	def __init__(self, dtype: str, name: str, expression: Node, idx: int):
		self.dtype = dtype
		self.name = name
		self.expr = str(expression)
		self.idx = idx

	def __repr__(self):
		return f'{{"Variable Definition" : {{ "type" : "{self.dtype}", "name" : "{self.name}", "value" : {self.expr}, "index" : {self.idx} }} }}'

class VariableAssignmentNode:
	def __init__(self, name: str, expression: Node, idx: int):
		self.name = name
		self.expr = str(expression)
		self.idx = idx

	def __repr__(self):
			return f'{{"Variable Assignment" : {{ "name" : "{self.name}", "value" : {self.expr}, "index" : {self.idx} }} }}'

class VariableAccessNode:
	def __init__(self, var_tok: Token):
		self.name = var_tok.value
		self.idx = var_tok.idx

	def __repr__(self):
		return f'{{"Variable Reference" : {{ "name" : "{self.name}", "index" : {self.idx} }} }}'

class UnimplementedNode:
	def __init__(self):
		pass

	def __repr__(self):
		return '{ "Unimplemented Node" : null }'

class FunctionDefinitionNode:
	def __init__(self, name: str, args: list[str], body: Node):
		self.name = name
		self.args = args
		self.body = body
	
	def __repr__(self):
		return f'{{"Function Definition" : {{"name" : "{self.name}", "arguments" : {self.args}, "body" : {self.body}  }} }}'

class FunctionCallNode:
	def __init__(self, name: str, args: list[str], idx: int):
		self.name = name
		self.args = args
		self.idx = idx

	def __repr__(self):
		return f'{{"Function Call" : {{"name" : "{self.name}", "arguments" : {self.args}, "index" : {self.idx} }} }}'
#

#Parser
class Parser3:
	def __init__(self, tokens, braces, semicolons, code):
		self.tokens = tokens
		self.braces = braces
		self.end_statement = "';'" if semicolons else '<newline>'
		self.code = code
		self.idx = -1
		self.advance()

	#Gets all the expressions in the code 
	#(which must be split by a <newline> or ';')
	#and formats it into JSON to be read
	#by the compiler class
	def parse(self):
		ast = {}

		while True:
			expr = str(self.expr())

			if self.current.type not in ("NEWLINE", "EOF"):
				code = get_code(self.code, self.current.idx)
				throw(f"POGCC 030: Missing end-of-statement token {self.end_statement}", code)

			expr = "{}" if expr == "None" else expr
	

			ast[f"Expression @Idx[{self.idx}]"] = loads(expr)

			if self.current.type == "EOF":
				break

			self.advance()

		return ast

	def advance(self):
		self.idx+=1
		self.current = Token(self.tokens[self.idx])

	def decrement(self):
		self.idx-=2
		self.advance()

	# Power (**) operator
	def power(self):
		return self.bin_op(self.atom, ("**", ), self.factor)

	#Grammar Factor
	def factor(self):
		current = self.current

		if current.value in ("-"):
			self.advance()
			fac = self.factor()
			if fac is None:
				self.decrement()
				
				code = get_code(self.code, self.current.idx)
				
				throw("POGCC 018: Expecting value or expression", code)
				
				self.advance()
				return UnimplementedNode()

			return UnaryOpNode(current, fac)

		return self.power()

	#Grammar Binary Operation
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

	#Grammar Term
	def term(self):
		return self.bin_op(self.factor, ('*', '/'))
		
	#Grammar Atom
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
				code = get_code(self.code, self.current.idx)
				
				throw("POGCC 018: Expected ')'", code)
				return UnimplementedNode()

		code = get_code(self.code, self.current.idx)
		
		throw("POGCC 018: Expected int, float, identifier, '+', '-', or '('", code)
		self.advance()
		return UnimplementedNode()

	#Grammar Expressions
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
		if self.current.type == ("INT", "FLOAT", "CHAR"):
			vartype = self.current.value
			self.advance()
			if self.current.type in ("VAR", "PTR"):
				vartype+=' '+self.current.value
				self.advance()
				if self.current.type != "IDENTIFIER":
					self.decrement()
					
					code = get_code(self.code, self.current.idx)
					
					throw(f"POGCC 018: Expected Indentifier after '{vartype}'", code)
					
					self.advance()
					return UnimplementedNode()
			
				name = self.current.value
				self.advance()

				if self.current.type == "NEWLINE":
					self.advance()
					return VariableDeclarationNode(f"{vartype}", name)

				elif self.current.value == "=":
					self.advance()
					expr = self.expr()
					if expr is None:
						self.decrement()

						code = get_code(self.code, self.current.idx)
						
						throw("POGCC 018: Expected value after assignment operator '='", code)
						
						self.advance()
						return UnimplementedNode()
					else:
						return VariableDefinitionNode(f"{vartype}", name, expr, self.current.idx)
				else:
					code = get_code(self.code, self.current.idx)
					
					throw(f"POGCC 018: Expecting '=' or {self.end_statement}", code)
					return UnimplementedNode()

		elif self.current.type == "IDENTIFIER":
			name = self.current.value
			self.advance()
			if self.current.type == "=":
				self.advance()
				expr = self.expr()
				if expr is None:
					self.decrement()

					code = get_code(self.code, self.current.idx)
					
					throw("POGCC 018: Expected value after assignment operator '='", code)
					
					self.advance()
					return UnimplementedNode()
				else:
					return VariableAssignmentNode(name, expr, self.current.idx)
			else:
				self.decrement() #move index pointer back to the identifier

		return self.bin_op(self.comp_expr, ('and', 'or'))
	#

#
