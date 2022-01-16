from utils import Token, throw
from sys import exit
from anytree import Node, RenderTree

class Int:
	def __init__(self, name):
		self.name = "Int "+name

class Parser3:
	def __init__(self, tokens):
		self.tokens = tokens
		self.top = Node("top")
		self.idx = -1
		self.advance()

	def parse(self):
		ast = ""
		self.expr()

		for pre, fill, node in RenderTree(self.top):
			ast+=pre+node.name+"\n"

		return ast


	def advance(self):
		self.idx+=1
		try:
			self.current = Token(self.tokens[self.idx])
		except IndexError:
			return
			
	def factor(self):
		if self.current.type == "INTEGER":
			current = self.current
			self.advance()
			return Int(current.value)

	def bin_op(self, func, ops):
		left = func()

		while self.current.value in ops:
			op = self.current
			self.advance()
			right = func()
			
			new_left = Node("BinOp "+op.value, self.top)
			Node(left.name, new_left)
			Node(right.name, new_left)


			left = new_left
			
			

		return left


	def term(self):
		return self.bin_op(self.factor, ('*', '/'))
		

	def expr(self):
		return self.bin_op(self.term, ('+', '-'))