from json import dump


from sys import argv, exit
from os import (
	chdir, 
	mkdir
)
from os.path import dirname, join
from subprocess import call
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

	"compile.optimizations" : 0
}

def compile_pog():
	if len(argv) == 2:  #if there are no arguments given, 
		call(["pogc2"]) #let pogc2 throw the error


	try:
		call(["pogc2"]+argv[2:])
	except OSError:
		print("Please add pogc2 to your PATH")
		exit(1)

	

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
		compile_pog()
except IndexError:
	print("No option specified.")
	exit(1)
