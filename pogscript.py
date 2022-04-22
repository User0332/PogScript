from json import dump


from sys import argv, exit
from os import (
	chdir, 
	mkdir,
	remove,
)
from os.path import (
	dirname, 
	exists
)
from shutil import move, rmtree
from subprocess import run as sub_run

exe_dir = dirname(argv[0]).replace("\\", "/")

DEFAULT_CONFIG = {
	"$schema" : f"{exe_dir}/pogfig_schema/pogfig_schema.json",

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

	if exists(projname):
		rmtree(projname)

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

def build():
	rmtree(f"{exe_dir}/tests")
	rmtree(f"{exe_dir}/docs")
	rmtree(f"{exe_dir}/deprecated")
	rmtree(f"{exe_dir}/syntax_highlighting")
	remove(f"{exe_dir}/package.json")
	remove(f"{exe_dir}/README.md")
	remove(f"{exe_dir}/LICENSE")
	remove(f"{exe_dir}/.gitignore")
	remove(f"{exe_dir}/.gitattributes")
	chdir(f"{exe_dir}/src")
	sub_run(["python", "-m", "nuitka", "--onefile", "pogc2.py"])
	move(f"pogc2.exe", f"{exe_dir}/pogc2.exe")
	move(f"cleanup.bat", f"{exe_dir}/cleanup.bat")
	move(f"assemble.bat", f"{exe_dir}/assemble.bat")
	chdir("..")
	rmtree(f"{exe_dir}/src")


if len(argv) < 2:
	print("No option specified.")
	exit(1)

if argv[1] == "new":
	newproj()
elif argv[1] == "compile":
	try: sub_run(["pogc2.py"]+argv[2:])
	except OSError:
		try: sub_run(["pogc2"]+argv[2:])
		except OSError: print("Please add pogc2 to your PATH.")
elif argv[1] == "build":
	build()
