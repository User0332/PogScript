from utils import throw, SymbolTable



offset = 0

class Compiler:
	def __init__(self, ast, code):
		self.ast = ast
		self.asm = ""
		self.globals = SymbolTable(code)

	def traverse(self, top=None):
		top = top if top else self.ast

		self.asm = '''section .text
	global _start

_start:
	;do something here...
	
	xor eax, eax
	
	ret'''