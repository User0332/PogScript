from lexer import Lexer
from pog_parser4 import Parser4
from utils import throw, GREEN, BLUE, CYAN, END
from json import loads, dumps
from json.decoder import JSONDecodeError
from os import chdir, getcwd
from os.path import dirname, split as spl
from sys import argv, exit
from dis import dis
from argparse import ArgumentParser
from pprint import pprint


def main(argc: int, argv: list[str]):
	argparser = ArgumentParser(description="Cooler Command Prompt (R) PogScript Compiler", prog = "pogc")

	argparser.add_argument('-s', '--show', metavar='', type=str, help='show AST, tokens, disassembly, or ALL')
	argparser.add_argument('filename', type=str, help='Source file')

	args = argparser.parse_args()
	
	try:
		show = args.show.lower()
	except AttributeError:
		show = None
	file = args.filename
	try:
		with open(file, 'r') as f:
			code = f.read()
	except OSError:
		throw("Either the specified file could not be found, or permission was denied.")
	try:
		with open(f"E:\\Users\\carlf\\PogScript\\.pogfig", "r") as f:
			data = f.read().splitlines()
			modifiers = loads(data[0])
			modifier_path = data[1]
			import_path = data[2]
	except IndexError:
		throw("Data is missing in .pogfig - All the data is critical for correct execution of the program")
	except FileNotFoundError or PermissionError:
		throw(".pogfig is missing or destroyed")
	except JSONDecodeError:
		throw("The file modifiers data in .pogfig is not valid JSON")

	lexer = Lexer(code)

	tokens, braces, mainmethods = lexer.tokenize()
	
	tokens.sort()

	if show in ("tok", "toks", "token", "tokens", "all"):
		print("Raw:\n\n\n")
		print(tokens)
		print("\n\n")
		print("Pretty-print:\n\n\n")
		pprint(tokens.tokens)

	parser = Parser4(tokens.tokens)

	raw_ast = parser.parse()

	if show in ("ast", "tree", "all"):
		ast = dumps(raw_ast, indent=1).replace("\\u001b[32m", GREEN).replace("\\u001b[0m", END).replace("\\u001b[34m", BLUE)
		
		ast_name_str = f"{CYAN}AST @File['{file}']{END}"
		print("Raw:\n\n\n")
		print(ast_name_str)
		print(str(raw_ast).replace("\{GREEN}", "").replace("\\u001b[32m", "").replace("\\u001b[0m", "").replace("\\u001b[34m", ""))
		print("\n\n")
		print("Pretty-print:\n\n\n")
		print(ast_name_str)
		print(ast)
	
	if show in ("dis", "disassemble", "disassembly", "all"):
		print("Cannot show disassembly at this time.")

	return 0
	
if __name__ == "__main__":
	exit(main(len(argv), argv))