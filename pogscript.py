from json import dump


from sys import argv, exit
from os import (
	chdir, 
	mkdir,
	system
)
from os.path import dirname, join
from shutil import rmtree

exe_dir = dirname(argv[0]).replace("\\", "/")

DEFAULT_CONFIG = {
	"$schema" : f"{exe_dir}/pogfig_schema/pogfig_schema.json",

	"modifiers.paths" : ["%FILE%/modifiers", 
		"%COMPILER%/modifiers"],

	"modifiers.names" : {

	},

	"imports.paths" : ["%FILE%/imports", 
		"%COMPILER%/imports"],

	"imports.names" : {
		"projlib" : ".projlib"
	},

	"compiler.optimizations" : 0
}
	

def newproj():
	try:
		projname = argv[2]
	except IndexError:
		print("Project name not specified.")
		exit(1)

	try:
		rmtree(projname) #remove directory if it exists
	except FileNotFoundError:
		pass

	mkdir(projname)
	chdir(projname)

	with open("main.pog", "w") as f:
		f.write("#your code here...")

	with open(".main_pogfig.json", "w") as f:
		dump(DEFAULT_CONFIG, f, indent="\t")

	mkdir("modifiers")
	mkdir("imports")

	with open("imports/.projlib", "w") as f:
		f.write("mylib.lib || mylib.pog")

	with open("imports/mylib.pog", "w") as f:
		f.write("#write your library here...")

try:
	if argv[1] == "new":
		newproj()
	elif argv[1] == "compile":
		system["pogc2"+" ".join(argv[2:])
except IndexError:
	print("No option specified.")
	exit(1)
