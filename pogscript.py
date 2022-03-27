from sys import argv, exit
from os import (
    chdir, 
    mkdir, 
    getcwd
)
from os.path import dirname
from json import dump

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


def newproj():
    try:
        projname = argv[2]
    except IndexError:
        projname = "pogproj"

    reset_dir = getcwd()
    mkdir(projname)
    chdir(projname)

    with open("main.pog", "w") as f:
        f.write("#your code here...")

    with open("main.pogfig.json", "w") as f:
        dump(DEFAULT_CONFIG, f)

    mkdir("modifiers")
    mkdir("imports")

    chdir(reset_dir)

try:
    if argv[1] == "new":
        newproj()
except IndexError:
    print("No option specified.")
    exit(1)
