def main():
	from lexer import Lexer
	from pog_parser2 import Parser
	from imports import pogscript_builtins
	from utils import format_error as format
	from json import loads
	from json.decoder import JSONDecodeError
	from time import sleep
	from os import chdir
	from os.path import dirname, split as spl
	from sys import argv, exit
	from dis import dis


	if len(argv) == 1:
		print("Cooler Command Prompt (R) PogScript Compiler")
		print("Copyright (C) 2022 CCP Inc.")
		print("\nusage: pogc [filename]")
		exit(0)
	else:
		file = argv[1]

	try:
		with open(file, 'r') as f:
			code = f.read()
	except (FileNotFoundError, PermissionError):
		print(format("Either the specified file could not be found, or permission was denied."))
		exit(1)
	try:
		with open("E:\\Users\\carlf\\PogScript\\.pogfig", "r") as f:
			data = f.read().splitlines()
			modifiers = loads(data[0])
			modifier_path = data[1]
			import_path = data[2]
	except IndexError:
		print(format("Data is missing in .pogfig - All the data is critical for correct execution of the program"))
		exit(1)
	except FileNotFoundError or PermissionError:
		print(format(".pogfig is missing or destroyed"))
		exit(1)
	except JSONDecodeError:
		print(format("The file modifiers data in .pogfig is not valid JSON"))

	lexer = Lexer(code)

	tokens, braces, mainmethods = lexer.tokenize()
	
	tokens.sort()

	parser = Parser(tokens.tokens, braces)

	pycode = parser.parse()

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

if __name__ == "__main__":
	main()


