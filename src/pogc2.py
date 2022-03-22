#Local Imports
from lexer import Lexer
from pog_parser3 import Parser3
from compiler import Compiler
from utils import checkfailure, throw, warn, throwerrors, CYAN, END
#Stdlib Imports
from json import loads, dumps
from json.decoder import JSONDecodeError
from argparse import ArgumentParser
from pprint import pprint
from os import getcwd, listdir, system
from os.path import isfile, dirname
from ast import literal_eval
from sys import exit, argv, executable as sys_exe

def main(argc: int, argv: list[str]):
	argparser = ArgumentParser(description="Cooler Command Prompt (R) PogScript Compiler", prog = "pogc")
	
	argparser.add_argument('-d', '--dump', type=str, help="show AST, tokens, disassembly, or ALL")
	argparser.add_argument('-s', '--suppresswarnings', help="suppress all warnings", action="store_true")
	argparser.add_argument('filename', nargs="?", default="", type=str, help='Source file')
	outgroup = argparser.add_mutually_exclusive_group()
	outgroup.add_argument('-o', '--out', type=str, help="output file")
	outgroup.add_argument('-e', '--executable', help="run compileasm.bat and produce an executable using NASM and LINK", action="store_true")


	args = argparser.parse_args()
	
	warnings = not args.suppresswarnings
	executable = args.executable
	
	try:
		show = args.dump.lower()
	except AttributeError:
		show = None 

	file = args.filename

	if file == "":
		for filename in listdir(getcwd()):
			if isfile(filename) and filename.endswith(".pog"):
				file = filename

		if file != "":
			warn("POGCC 011: No source file specified. Assuming the below file.", f">{file}\n")	
		else:
			throw("Fatal Error POGCC 022: No valid source file found.")
			throwerrors()
			return 1

	try:
		with open(file, 'r') as f:
			code = f.read()
	except OSError:
		throw("Fatal Error POGCC 022: Either the specified source file could not be found, or permission was denied.")
	
	
	basesource = ".".join(file.split(".")[:-1])

	if args.out == None:
		out = basesource+".asm"
		warn("POGCC 006: -o option unspecified, assuming assembly", f">{out}\n")
	else:
		out = args.out

	try:
		pogfig = basesource+".pogfig"
		with open(pogfig , "r") as f:
			pogdata = f.read().splitlines()
			modifiers = loads(pogdata[0])
			modifier_path = literal_eval(pogdata[1])
			spec_imports = loads(pogdata[2])
			import_path = literal_eval(pogdata[3])

		assert (type(modifier_path) is list) and (type(import_path) is list)
	
	except IndexError:
		throw(f"Fatal Error POGCC 017: Data is missing in {pogfig} - All the data is critical for correct execution of the program")
	except FileNotFoundError:
		warn(f"POGCC 016: {pogfig} is missing, using default configuration")
		modifiers = {}
		modifier_path = [f"{sys_exe}/modifiers"]
		spec_imports = {"libc" : "LIBC_LIST"}
		import_path = [f"{sys_exe}/imports"]	
	except PermissionError:
		throw(f"Fatal Error POGCC 029: Could not open {pogfig} due to a permission error.")
	except SyntaxError or AssertionError:
		throw(f"Fatal Error POGCC 017: The modifier or import path lists in {pogfig} are not valid lists")
	except JSONDecodeError:
		throw(f"Fatal Error POGCC 017: Either the file modifier or special import data in {pogfig} is not valid JSON")
		
	throwerrors()
	checkfailure()

	lexer = Lexer(code)

	tokens, braces, mainmethods = lexer.tokenize()
	
	tokens.sort()

	if not braces:
		warn("POGCC 026: Indents have not been fully implemented and it is unsafe to not use brace delimited scopes")

	if show in ("tok", "toks", "token", "tokens", "all"):
		print("Raw:\n\n\n")
		print(tokens)
		print("\n\n")
		print("Pretty-print:\n\n\n")
		pprint(tokens.tokens)
		print(f"Length of tokens: {len(tokens.tokens)}\n\n")


	if out.endswith(".lst"):
		with open(out, "w") as f:
			pprint(tokens.tokens, f)
		with open(out, "r") as f:
			list_tokens = f.read().replace("'", '"')
		with open(out, "w") as f:
			f.write(list_tokens)



	parser = Parser3(tokens.tokens, braces, code)
	parser.parse()

	throwerrors()
	checkfailure()

	raw_ast = parser.ast
	ast = dumps(raw_ast, indent=1)

	if show in ("ast", "tree", "all"):
		ast_name_str = f"{CYAN}AST @File['{file}']{END}"
		print("Raw:\n\n\n")
		print(ast_name_str)
		print(raw_ast)
		print("\n\n")
		print("Pretty-print:\n\n\n")
		print(ast_name_str)
		print(ast)
		print("\n")

	if out.endswith(".json"):
		with open(out, "w") as f:
			f.write(ast)

	compiler = Compiler(loads(ast))
	compiler.traverse()

	throwerrors()
	checkfailure()

	if out.endswith(".asm"):
		with open(out, "w") as f:
			f.write(compiler.asm)

	if executable:
		system(f"assemble {out.removesuffix('.asm')}")


	if show in ("dis", "disassemble", "disassembly", "all"):
		warn("POGCC 001: Cannot show disassembly from -s option.")

	



	return 0

	'''
	chdir(dirname(file))

	file = spl(file)[1].split(".", 1)[0]

	with open(file+".py", "w") as f:
		f.write(pycode)

	compiled = compile(pycode, file+".pogc", "exec")

	print("Token positions:")
	for item in tokens.instructions:
		print(" ".join(item))
		sleep(0.1)

	sleep(2)

	print(f"Disassembly of {argv[1]}:")
	dis(compiled)

	sleep(2)
	
	with open(file+".pogc", "wb") as f:
		f.write(compiled.co_code)
		f.write(compiled.co_lnotab)

	with open(file+".pogc", "a") as f:
		f.write(f"\n{compiled.co_argcount}\n{compiled.co_cellvars}\n{compiled.co_consts}\n{compiled.co_filename}\n{compiled.co_firstlineno}\n{compiled.co_flags}\n{compiled.co_freevars}\n{compiled.co_kwonlyargcount}\n{compiled.co_varnames}")
	'''

if __name__ == "__main__":
	exit(main(len(argv), argv))