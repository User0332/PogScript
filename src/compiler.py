from utils import (
	get_code,
	throw,
	SymbolTable
)



#Compiler
class Compiler:
	def __init__(self, ast: dict, code: str):
		self.ast = ast
		self.allocated_bytes = []
		self.globals = SymbolTable(code)
		self.source = code

	#The two methods below allocate memory for the
	#variable and place it in a symbol table
	def declare_variable(self, node: dict):
		name = node["name"]
		dtype = node["type"]

		assert dtype == "DWORD int"
		
		start = len(self.allocated_bytes)-1
		for i in range(4): self.allocated_bytes.append(i)

		self.globals.declare(name, dtype, 4, f"__NOACCESS.1.allocmem+{start}")

	def define_variable(self, node: dict):
		name = node["name"]
		dtype = node["type"]
		value = node["value"]
		index = node["index"]

		assert dtype == "DWORD int"

		start = len(self.allocated_bytes)
		for i in range(4): self.allocated_bytes.append(i)

		self.globals.declare(name, dtype, 4, f"__NOACCESS.1.allocmem+{start}")
		self.globals.assign(name, value, index)
	#

	def assign_variable(self, node: dict):
		name = node["name"]
		value = node["value"]
		index = node["index"]

		self.globals.assign(name, value, index)

	#Traverses the AST and passes off each node to a specialized function
	def traverse(self, top: dict=None):
		asm = ""

		key: str; node: dict
		
		top = top if top is not None else self.ast

		for key, node in top.items():
			if key.startswith("Expression"):
				self.traverse(node)
			elif key.startswith("Variable Declaration"):
				self.declare_variable(node)
			elif key.startswith("Variable Definition"):
				self.define_variable(node)
			elif key.startswith("Variable Assignment"):
				self.assign_variable(node)

		#Placeholder assembly for now
		asm+=f'''
section .bss
	__NOACCESS.1.allocmem resb {len(self.allocated_bytes)}


section .text
	global _start
_start:
	;do something here...
	
	xor eax, eax
	
	ret'''

		return asm
	#

#