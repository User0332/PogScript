from utils import throw, AttrTable

global_attrs = AttrTable()

offset = 0

class Compiler:
	def __init__(self, ast):
		self.ast = ast
		self.asm = ""

	def traverse(self, top=None):
		top = top if top else self.ast

		self.asm = '''section .text
	global _start

_start:
	;do something here...
	
	xor eax, eax
	
	ret'''