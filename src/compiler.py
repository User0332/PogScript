from utils import (
	get_code,
	throw,
	SymbolTable
)

class FunctionCompiler:
	def __init__(self, function: dict, code: str):
		self.function = function
		self.allocated_bytes
		self.locals = SymbolTable(code)
		self.source = code

	def instr(self, instruction: str):
		self.asm+="\n\t"+instruction

	def toplevelinstr(self, instruction: str):
		self.asm = instruction+self.asm

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

		assert dtype == "int var"

		start = self.allocated_bytes
		self.allocated_bytes+=4

		#add instrs
		self.locals.declare(name, dtype, 4, f"esp+{start}")

	def define_variable(self, node: dict):
		name = node["name"]
		dtype = node["type"]
		value = node["value"]
		index = node["index"]

		assert dtype == "int var"

		start = self.allocated_bytes
		self.allocated_bytes+=4


		#add instrs
		self.locals.declare(name, dtype, 4, f"esp+{start}")
		memaddr = self.locals.assign(name, value, index)
		self.generate_expression(value)
		self.instr(f"mov [{memaddr}], eax")
	#

	def assign_variable(self, node: dict):
		name = node["name"]
		value = node["value"]
		index = node["index"]

		memaddr = self.locals.assign(name, value, index)

		self.generate_expression(value)

		self.instr(f"mov [{memaddr}], eax")

	#Traverses the AST and passes off each node to a specialized function
	def traverse(self, top: dict=None):
		key: str; node: dict
		
		top = top if top is not None else self.function

		#make prolog		

		for key, node in top.items():
			if key.startswith("Expression"):
				self.traverse(node)
			elif key.startswith("Variable Declaration"):
				self.declare_variable(node)
			elif key.startswith("Variable Definition"):
				self.define_variable(node)
			elif key.startswith("Variable Assignment"):
				self.assign_variable(node)

		#make epilog

		return self.asm



#Compiler
class Compiler:
	def __init__(self, ast: dict, code: str):
		self.ast = ast
		self.asm = "section .text\n\tglobal _start\n\n_start:"
		self.scope = "global"
		self.globals = SymbolTable(code)
		self.source = code

	def instr(self, instruction: str):
		self.asm+="\n\t"+instruction

	def toplevelinstr(self, instruction: str):
		self.asm = instruction+self.asm

	def traverse_function(self, node: dict):
		self.scope = "local"
		#make prolog
		self.traverse(node["body"])
		#make epilog
		self.scope = "global"

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

		assert dtype == "int var"

		if self.scope == "global":
			self.asm.toplevelinstr(f"{name} resb 4")
			self.globals.declare(name, dtype, 4, name)

	def define_variable(self, node: dict):
		name = node["name"]
		dtype = node["type"]
		value = node["value"]
		index = node["index"]

		assert dtype == "int var"

		if self.scope == "global":
			self.asm.toplevelinstr(f"{name} resb 4")
			self.globals.declare(name, dtype, 4, name)
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
			self.asm=f"section .bss"+self.asm

		return self.asm
	#
#