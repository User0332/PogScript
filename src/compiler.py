from utils import (
	throw, 
	SymbolTable
)



#Compiler
class Compiler:
	def __init__(self, ast: dict, code: str):
		self.ast = ast
		self.allocated_bytes = []
		self.asm = ""
		self.globals = SymbolTable(code)
		self.source = code

	#The two methods below allocate memory for the
	#variable and place it in a symbol table
	def declare_variable(self, node: dict):
		name = node["name"]
		dtype = node["type"]
		value = node["value"]

		assert dtype == "DWORD int"
		
		start = len(self.allocated_bytes)-1
		for i in range(4): self.allocated_bytes.append(i)

		self.globals.declare(name, dtype, 4, f"__NOACCESS.1.allocmem+{start}")

	def define_varaible(self, node: dict):
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
		top = top if top else self.ast

		for key, node in top.items():
			if node.startswith("Expression"):
				return self.traverse(node)
			elif node.startswith("Variable Declaration"):
				self.declare_variable(node)
			elif node.startswith("Variable Definition"):
				self.define_variable(node)
			elif node.startswith("Variable Assignment"):
				self.assign_variable(node)

		#Placeholder assembly for now
		self.asm = f'''
section .bss
	__NOACCESS.1.allocmem resb {len(self.allocated_bytes)}


section .text
	global _start
_start:
	;do something here...
	
	xor eax, eax
	
	ret'''
	#

#