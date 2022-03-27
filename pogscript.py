from json import dump


from sys import argv, exit
from os import (
    chdir, 
    mkdir, 
    getcwd,
    rmdir
)
from os.path import dirname
from subprocess import call

DEFAULT_CONFIG = {
    "$schema" : f"{dirname(argv[0])}/pogfig_schema/pogfig_schema.json",

    "modifiers.paths" : ["%FILE%/modifiers", 
        "%COMPILER%/modifiers"],

    "modifiers.names" : {

    },

    "imports.paths" : ["%FILE%/imports", 
        "%COMPILER%/imports"],

    "imports.names" : {

    },

    "compile.optimizations" : 0
}

def compile_pog():
    try:
        call(["pogc2"]+argv[2:])
    except OSError:
        print("Please add pogc2 to your PATH")
        exit(1)

    

def newproj():
    try:
        projname = argv[2]
    except IndexError:
        projname = "pogproj"

    try:
        rmdir(projname) #clear the directory if existent
    except OSError:
        pass

    mkdir(projname)
    chdir(projname)

    with open("main.pog", "w") as f:
        f.write("#your code here...")

    with open(".main_pogfig.json", "w") as f:
        dump(DEFAULT_CONFIG, f)

    mkdir("modifiers")
    mkdir("imports")

try:
    if argv[1] == "new":
        newproj()
    elif argv[1] == "compile":
        compile_pog()
except IndexError:
    print("No option specified.")
    exit(1)
