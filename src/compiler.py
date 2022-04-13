from utils import (
	get_code,
	throw,
	SymbolTable
)



#Compiler
class Compiler:
	def __init__(self, ast: dict, code: str):
		self.ast = ast
		self.asm = "section .text\n\tglobal _start\n\n_start:"
		self.allocated_bytes = []
		self.globals = SymbolTable(code)
		self.source = code

	def instr(self, instruction: str):
		self.asm+="\n\t"+instruction

	def generate_expression(self, expr: dict):
		key: str; node: dict

		for key, node in expr.items():
			if key.startswith("Binary Operation"):
				op = key.removeprefix("Binary Operation ")

				self.generate_expression(node[0])
				self.instr("mov ebx, eax") #save result
				self.generate_expression(node[1])

				if op == "/": #integer division
					self.instr("push eax")
					self.instr("mov eax, ebx")
					self.instr("pop ebx")
					self.instr("idiv ebx")
				elif op == "%": #modulo
					self.instr("push eax")
					self.instr("mov eax, ebx")
					self.instr("pop ebx")
					self.instr("idiv ebx")
					self.instr("mov eax, edx")
				else:
					if op == "+": #addition
						self.instr("add ebx, eax")
					elif op == "-": #subtraction
						self.instr("sub ebx, eax")
					elif op == "*": #integer multiplication
						self.instr("imul ebx, eax")

					self.instr("mov eax, ebx")
			elif key.startswith("Unary Operation"):
				op = key.removeprefix("Unary Operation ")
				if op == "-":
					self.generate_expression(node)
					self.instr("neg eax")
			elif key.startswith("Numerical Constant"):
				self.instr(f"mov eax, {node}")
			elif key.startswith("Variable Reference"):
				name = node["name"]
				index  = node["index"]

				memaddr =  self.globals.get(name, index)["address"]
				self.instr(f"mov eax, [{memaddr}]")

	#The two methods below allocate memory for the
	#variable and place it in a symbol table
	def declare_variable(self, node: dict):
		name = node["name"]
		dtype = node["type"]

		assert dtype == "int"
		
		start = len(self.allocated_bytes)-1
		self.allocated_bytes+=[i for i in range(4)]

		self.globals.declare(name, dtype, 4, f"__NOACCESS.mainmem.1+{start}")

	def define_variable(self, node: dict):
		name = node["name"]
		dtype = node["type"]
		value = node["value"]
		index = node["index"]

		assert dtype == "int"

		start = len(self.allocated_bytes)
		self.allocated_bytes+=[i for i in range(4)]

		self.globals.declare(name, dtype, 4, f"__NOACCESS.mainmem.1+{start}")
		memaddr = self.globals.assign(name, value, index)

		self.generate_expression(value)

		self.instr(f"mov [{memaddr}], eax")
	#

	def assign_variable(self, node: dict):
		name = node["name"]
		value = node["value"]
		index = node["index"]

		memaddr = self.globals.assign(name, value, index)

		self.generate_expression(value)

		self.instr(f"mov [{memaddr}], eax")

	#Traverses the AST and passes off each node to a specialized function
	def traverse(self, top: dict=None):
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

		if top is self.ast: #add the number of bytes needed to allocate
			self.asm=f"section .bss\n\t__NOACCESS.mainmem.1 resb {len(self.allocated_bytes)}\n\n"+self.asm

		return self.asm



	#

#