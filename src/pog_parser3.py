from json import loads, dumps

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

class ConditionalStatementNode:
	def __init__(self, condition: Node, if_body: dict, else_body: dict):
		self.condition = condition
		self.if_body = dumps(if_body, indent=1)
		self.else_body = dumps(else_body, indent=1)

	def __repr__(self):
		return f'{{"Conditional Statement" : {{ "condition" : {self.condition}, "if" : {self.if_body}, "else" : {self.else_body} }} }}'

class UnimplementedNode:
	def __init__(self):
		pass

	def __repr__(self):
		return '{ "Unimplemented Node" : null }'

class FunctionDefinitionNode:
	def __init__(self, name: str, params: list[dict[str, str]], body: dict):
		self.name = name
		self.params = params
		self.formatted_params = '['+', '.join(dumps(x) for x in params)+']'
		self.body = dumps(body)
	
	def __repr__(self):
		return f'{{"Function Definition" : {{"name" : "{self.name}", "parameters" : {self.formatted_params}, "body" : {self.body}  }} }}'

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
	def __init__(self, tokens, code):
		self.tokens = tokens
		self.code = code
		self.idx = -1
		self.advance()

	#Gets all the expressions in the code 
	#(which must be split by a <newline>)
	#and formats it into JSON to be read
	#by the compiler class
	def parse(self):
		ast = {}

		while 1:
			expr = str(self.expr())

			if self.current.type not in ("NEWLINE", "EOF"):
				code = get_code(self.code, self.current.idx)

				throw(f"POGCC 030: Missing end-of-statement token <newline>", code)

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

	#gets blocks of code in between curly braces
	def get_body(self):
		body = {}
		while self.current.value != "}":
			expr = str(self.expr())

			expr = "{}" if expr == "None" else expr

			body[f"Expression @Idx[{self.idx}]"] = loads(expr)

			if self.current.type not in ("NEWLINE", "}"):
				code = get_code(self.code, self.current.idx)

				throw(f"POGCC 030: Missing end-of-statement token <newline>", code)

			elif self.current.type == "EOF":
				code = get_code(self.code, self.current.idx)

				throw("POGCC 018: Unexpected EOF, Expected '}'", code)
				break

			self.advance()

		self.advance()

		return body

	# skip newlines
	def skip_newlines(self):
		while self.current.type == "NEWLINE": self.advance()

	# Power (**) operator
	def power(self):
		return self.bin_op(self.atom, ("**", ), self.factor)

	#Grammar Factor
	def factor(self):
		current = self.current

		if current.value == "-":
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
				
				self.advance()
				return UnimplementedNode()
		elif current.value == "if":
			self.advance()
			return self.conditional_expr()
		

		code = get_code(self.code, self.current.idx)
		
		
		throw("POGCC 018: Expected int, float, identifier, '+', '-', or '('", code)
		self.advance()
		return UnimplementedNode()

	#Grammar Expressions
	def conditional_expr(self):
		condition = self.expr()

		if condition is None:
			code = get_code(self.code, self.current.idx)

			throw("POGCC 018: Expected expression", code)

			self.advance()
			return UnimplementedNode()

		self.skip_newlines()

		if self.current.value == "{":
			self.advance()
			if_body = self.get_body()
		else:
			if_nodes = self.expr()
			if_body = {f"Expression @Idx[{self.idx}]" : loads(str(if_nodes))}
			if if_nodes is None:
				code = get_code(self.code, self.current.idx)

				throw("POGCC 018: Expected expression", code)

				self.advance()
				return UnimplementedNode()

		self.skip_newlines()
			
		if self.current.value == "else":
			self.advance()

			self.skip_newlines()

			if self.current.value == "{":
				self.advance()
				else_body = self.get_body()
			else:
				else_nodes = self.expr()
				else_body = {f"Expression @Idx[{self.idx}]" : loads(str(else_nodes))}
				if else_nodes is None:
					code = get_code(self.code, self.current.idx)

					throw("POGCC 018: Expected expression", code)
		else:
			else_body = {}
		
		return ConditionalStatementNode(condition, if_body, else_body)
			
	def func_expr(self, ret_type: str, name: str):
		if self.current.value != '(':
			code = get_code(self.code, self.current.idx),
			throw("POGCC 018: Expected opening parenthesis", code)

			self.advance()
			return UnimplementedNode()

		self.advance()

		current_vartype = ""
		parameters = []

		while 1:
			if self.current.type not in ("INT", "FLOAT", "CHAR"):
				print(self.current)
				code = get_code(self.code, self.current.idx)
				throw("POGCC 018: Expected datatype", code)

				self.advance()
				return UnimplementedNode()

			current_vartype+=self.current.value
			self.advance()

			if self.current.type not in ("VAR", "CONST", "PTR", "FUNC"):
				code = get_code(self.code, self.current.idx)
				throw("POGCC 018: Expected symbol type", code)

				self.advance()
				return UnimplementedNode()

			current_vartype+=' '+self.current.value
			self.advance()

			if self.current.type != "IDENTIFIER":
				code = get_code(self.code, self.current.idx)
				throw("POGCC 018: Expected identifier name")

				self.advance()
				return UnimplementedNode()

			parameters.append(
				{
					"vartype": current_vartype, 
					"name": self.current.value
				}
			)

			current_vartype = ""

			self.advance()

			if self.current.value not in (',', ')'):
				code = get_code(self.code, self.current.idx)
				throw("POGCC 018: Expected ',' or ')'")

				self.advance()

				return UnimplementedNode()

			if self.current.value == ')': break

			self.advance()

		self.advance()

		self.skip_newlines()

		if self.current.value != '{':
			code = get_code(self.code, self.current.idx)
			throw("POGCC 018: Expected opening curly brace", code)

			self.advance()
			return UnimplementedNode()
		
		self.advance()

		body: dict = self.get_body()

		return FunctionDefinitionNode(
			name,
			parameters,
			body
		)

	def comp_expr(self):
		if self.current.value == "not":
			op = self.current
			self.advance()

			node = self.comp_expr()
			return UnaryOpNode(op, node)

		return self.bin_op(self.num_expr, ("==", "!=", "<", ">", "<=", ">=", "and", "or"))
		

	def num_expr(self):
		return self.bin_op(self.term, ("+", "-"))

	def expr(self):
		if self.current.type in ("INT", "FLOAT", "CHAR"):
			vartype: str = self.current.value
			self.advance()
			if self.current.type in ("VAR", "PTR", "CONST", "FUNC"):
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

				if vartype.endswith("func"):
					return self.func_expr(vartype, name)

				if self.current.type == "NEWLINE":
					return VariableDeclarationNode(f"{vartype}", name)

				elif self.current.value == "=":
					self.advance()
					expr = self.expr()
					if expr is None:
						self.decrement()

						code = get_code(self.code, self.current.idx)
						
						throw("POGCC 018: Expected expression after assignment operator '='", code)
						
						self.advance()
						return UnimplementedNode()
					else:
						return VariableDefinitionNode(f"{vartype}", name, expr, self.current.idx)
				else:
					code = get_code(self.code, self.current.idx)
					
					throw(f"POGCC 018: Expected '=' or <newline>", code)
					
					self.advance()
					return UnimplementedNode()
			else:
				code = get_code(self.code, self.current.idx)
				
				throw("POGCC 018: Expected 'var', 'ptr', 'const', or 'function'", code)
				
				self.advance()
				return UnimplementedNode()

		elif self.current.type == "IDENTIFIER":
			name = self.current.value
			self.advance()
			if self.current.value == "=":
				self.advance()
				expr = self.expr()
				if expr is None:
					self.decrement()

					code = get_code(self.code, self.current.idx)
					
					throw("POGCC 018: Expected expression after assignment operator '='", code)
					
					self.advance()
					return UnimplementedNode()
				else:
					return VariableAssignmentNode(name, expr, self.current.idx)
			else:
				self.decrement() #move index pointer back to the identifier

		elif self.current.type == "NEWLINE":
			return None

		return self.bin_op(self.comp_expr, ('and', 'or'))
	#

#
