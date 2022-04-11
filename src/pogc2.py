#LOCAL MODULES
from lexer import Lexer
from pog_parser3 import Parser3
from compiler import Compiler
from ast_preprocessor import SyntaxTreePreproccesor

from utils import (
	checkfailure, 
	throw, 
	warn, 
	throwerrors, 
	printwarnings, 
	CYAN, 
	END, 
	ArgParser
)


#JSON I/O MODULES
from json.decoder import JSONDecodeError

from json import (
	loads, 
	dumps
)


#SYSTEM MODULES
from subprocess import (
	call as subprocess_call
)

from os import (
	getcwd, 
	listdir,
	chdir
)

from os.path import (
	isfile, 
	dirname,
	basename
)

from sys import (
	exit, 
	argv
)


#Indepenedent Environment Constants
COMPILER_EXE_PATH = dirname(argv[0]).replace("\\", "/")
DEFAULT_MODIFIER_PATH = f"{COMPILER_EXE_PATH}/modifiers".replace("\\", "/")
DEFAULT_IMPORT_PATH = f"{COMPILER_EXE_PATH}/imports".replace("\\", "/")
#


def main():
	argparser = ArgParser(description="PogScript Compiler", prog = "pogc2")
	
	argparser.add_argument('-d', '--dump', type=str, help="show AST, tokens, disassembly, or ALL")
	argparser.add_argument('-s', '--suppresswarnings', help="suppress all warnings", action="store_true", default=False)
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
	
	#Dependent Constants
	INPUT_FILE_PATH = dirname(file).replace("\\", "/")
	if INPUT_FILE_PATH == '':
		INPUT_FILE_PATH = './'
	#

	chdir(INPUT_FILE_PATH)

	basesource = ".".join(basename(file).split(".")[:-1])

	if args.out == None:
		out = basesource+".asm"
		warn("POGCC 006: -o option unspecified, assuming assembly", f">{out}\n")
	elif not args.out.endswith((".asm", ".lst", ".json")) and args.out != 'NULL':
		warn(f"POGCC 004: '{args.out}' is an invalid output file. Switching to assembly by default.")
		out = basesource+".asm"
	else:
		out = args.out

	

	try:
		pogfig = "."+basesource+"_pogfig.json"
		with open(pogfig , "r") as f:
			pogfig_info = f.read().replace("%FILE%", INPUT_FILE_PATH).replace("%COMPILER%", COMPILER_EXE_PATH)
			pogdata = loads(pogfig_info)

			modifiers = pogdata["modifiers.names"]
			modifier_path = pogdata["modifiers.paths"]
			spec_imports = pogdata["imports.names"]
			import_path = pogdata["imports.paths"]
			compile_optimizations = pogdata["compiler.optimizations"]

		assert (type(modifier_path) is list) and (type(import_path) is list)

		if type(compile_optimizations) is not int:
			raise ValueError

	except KeyError:
		throw(f"Fatal Error POGCC 017: Data is missing in {pogfig}")
	except FileNotFoundError:
		warn(f"POGCC 016: {pogfig} is missing, using default configuration")
		modifiers = {}
		modifier_path = []
		spec_imports = {"libc" : "LIBC_LIST"}
		import_path = []
		compile_optimizations = 0
	except PermissionError:
		throw(f"Fatal Error POGCC 029: Could not open {pogfig} due to a permission error")
	except AssertionError:
		throw(f"Fatal Error POGCC 017: The modifier or import path lists in {pogfig} are not valid lists")
	except JSONDecodeError:
		throw(f"Fatal Error POGCC 017: The data in {pogfig} is not valid JSON")
		raise	
	except ValueError:
		throw(f"Fatal Error POGCC 017: The compiler optimization level in {pogfig} must be an integer.")
		
	throwerrors()
	if warnings: printwarnings()
	checkfailure()

	modifier_path.append(DEFAULT_MODIFIER_PATH)
	import_path.append(DEFAULT_IMPORT_PATH)

	lexer = Lexer(code)

	tokens, braces, mainmethods, semicolons = lexer.tokenize()
	
	tokens.sort()

	formatted_list = ["[\n"]

	formatted_list += [str(token)+"\n" for token in tokens] + ["]"]

	if not braces:
		warn("POGCC 026: Indents have not been fully implemented and it is unsafe to not use brace delimited scopes")

	if show in ("tok", "toks", "token", "tokens", "all"):
		print("Raw:\n\n\n")
		print(tokens)
		print("\n\n")
		print("Pretty-print:\n\n\n")
		print(formatted_list)
		print(f"Length of tokens: {len(tokens)}\n\n")


	if out.endswith(".lst"):
		with open(out, "w") as f:
			f.write("".join(formatted_list))


	parser = Parser3(tokens.tokens, braces, semicolons, code)

	raw_ast = parser.parse()

	if compile_optimizations == 1:
		simplifier = SyntaxTreePreproccesor(raw_ast)
		raw_ast = simplifier.simplify()

	ast = dumps(raw_ast, indent=1)

	throwerrors()
	if warnings: printwarnings()
	checkfailure()

	


	if show in ("ast", "tree", "all"):
		ast_name_str = f"{CYAN}AST @File['{file}']{END}"
		print(f"Raw:\n\n\n\n{ast_name_str}\n{raw_ast}\n\n\n")
		print(f"Pretty-print:\n\n\n{ast_name_str}\n{ast}\n\n\n")

	if out.endswith(".json"):
		with open(out, "w") as f:
			f.write(ast)

	compiler = Compiler(raw_ast, code)
	asm = compiler.traverse()

	throwerrors()
	if warnings: printwarnings()
	checkfailure()

	if out.endswith(".asm"):
		with open(out, "w") as f:
			f.write(asm)

	if executable:
		try:
			subprocess_call(["assemble.bat", out.removesuffix(".asm")])
		except OSError:
			throw("POGCC 022: assemble.bat is missing, destroyed, or broken")
			

	if show in ("dis", "disassemble", "disassembly", "asm", "assembly", "all"):
		print("Disassembly:\n")
		print(asm)

	throwerrors()
	if warnings: printwarnings()
	checkfailure()

	return 0



if __name__ == "__main__":
	exit(main())