from utils import (
	get_code,
	throw,
	SymbolTable
)

class FunctionCompiler:
	def __init__(self, function: dict, code: str):
		self.prolog = ""
		self.epilog = ""
		self.asm = ""
		self.function = function
		self.allocated_bytes = 0
		self.locals = SymbolTable(code)
		self.source = code

	def instr(self, instruction: str):
		self.asm+="\n\t"+instruction

	def toplevelinstr(self, instruction: str):
		self.asm = "\t"+instruction+"\n"+self.asm

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

				memaddr =  self.locals.get(name, index)["address"]
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

		for key, node in top.items():
			if key.startswith("Expression"):
				self.traverse(node)
			elif key.startswith("Variable Declaration"):
				self.declare_variable(node)
			elif key.startswith("Variable Definition"):
				self.define_variable(node)
			elif key.startswith("Variable Assignment"):
				self.assign_variable(node)

		#make prolog and epilog
		self.prolog = f"push ebx\n\tpush esi\n\tsub esp, {self.allocated_bytes+8}"
		self.prolog = f"add esp, {self.allocated_bytes+8}\n\tpop esi\n\tpop ebx"

		return self.prolog+"\n\t"+self.asm+"\n\t"+self.epilog


#Compiler
class Compiler:
	def __init__(self, ast: dict, code: str, module_name: str):
		self.ast = ast
		self.asm = f"section .text\n\tglobal _{module_name}_init.1\n\n_{module_name}_init.1:"
		self.scope = "global"
		self.globals = SymbolTable(code)
		self.source = code
		self.module_name = module_name

	def instr(self, instruction: str):
		self.asm+="\n\t"+instruction

	def toplevelinstr(self, instruction: str):
		self.asm = "\t"+instruction+"\n"+self.asm

	def traverse_function(self, node: dict):
		self.scope = "local"
		#make prolog
		compiler = FunctionCompiler(node, self.source)
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
			self.toplevelinstr(f"{self.module_name}.{name} resb 4")
			self.globals.declare(name, dtype, 4, f"{self.module_name}.{name}")

	def define_variable(self, node: dict):
		name = node["name"]
		dtype = node["type"]
		value = node["value"]
		index = node["index"]

		assert dtype == "int var"

		if self.scope == "global":
			self.toplevelinstr(f"{self.module_name}.{name} resb 4")
			self.globals.declare(name, dtype, 4, f"{self.module_name}.{name}")
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

		if top is self.ast: # add bss section
			self.asm=f"section .bss\n"+self.asm

		return self.asm
	#
#