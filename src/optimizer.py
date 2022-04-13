#The below assembly optimizer will optimize the assembly code
#rather than the syntax tree. The optimizer will remove redundant
#code like:
#mov eax, 4
#mov [__NOACCESS.mainmem.1+0], eax
#Into:
#mov [__NOACCESS.mainmem.1+0], 4
#The optimizer will also remove inefficient expressions
#that could be optimized like assigning a value to a variable
#in a loop where the variable is never used.
#instead, ecx could just be used as the counter.

class AssemblyOptimizer:
	def __init__(self, asm: str):
		self.asm = asm


	def optimize(self):
		for i, line in enumerate(self.asm.splitlines()):
			line = line.strip()


		return self.asm
