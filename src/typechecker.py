from utils import throw, get_code

class TypeChecker:
	def __init__(self, ast: dict, code: str):
		self.ast = ast
		self.source = code

	def get_types_from_expr(self, expr: dict, types: set=None):
		key: str; node: dict

		types = types if types is not None else set()

		for key, node in expr.items():
			if key.startswith("Numerical Constant"):
				types.add("int var")
			elif key.startswith("Variable Reference"):
				name = node['name'] #get datatype
			elif key.startswith("String Constant"):
				types.add("char ptr")
			elif key.startswith("Character Constant"):
				types.add("char var")

		return types



	def check_var_definition(self, node: dict):
		dtype = node["type"]
		value = node["value"]
		index = node["index"]
		types = self.get_types_from_expr(value)
		types.discard(dtype)

		if types:
			code = get_code(self.source, index)

			throw(f"POGCC 032: Value for variable '{node['name']}' does not match variable type.", code)
		
			

	def traverse(self, top: dict=None):
		key: str; node: dict
		top = top if top is not None else self.ast

		for key, node in top.items():
			if key.startswith("Expression"):
				self.traverse(node)
			elif key.startswith("Variable Definition"):
				self.check_var_definition(node)
			elif key.startswith("Untypechecked Block"):
				continue