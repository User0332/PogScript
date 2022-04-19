# Pogfig Configuration Guide

A configuration file should be named like this: `.<filename>_pogfig.json`

Ex. `.main_pogfig.json`

<br/>

And should look something like this:

>.main_pogfig.json

```json
{
	"$schema": "path-to-pogfig-schema/pogfig_schema.json",
	"imports.paths": [
		"%FILE%/imports",
		"%COMPILER%/imports"
	],
	"imports.names": {
        "projlib" : [
            "mylib.pog",
            "myotherlibpog"
        ]
    },

	"compiler.optimizations": 0
}
```

NOTE: The information needed in the pogfig file can be found in `pogfig_schema/pogfig_schema.json`

<br/>
<br/>

List of properties and their uses:

<br/>


`imports.paths` - A list of paths in which to search for imported files.

`imports.names` - A dictionary of **valid identifiers** that correspond to imports in the program. Using the example above, if you import the name `projlib`, both `mylib.pog` and `myotherlib.pog` will be imported instead.

`compiler.optimizations` - An integer representing the level of compiler optimization. Level 0 means no optimizations, level 1 means invoking `ast_preprocessor.py` to simplify the syntax tree, and level 2 means invoking `optimizer.py` which optimizes the assembly code.

<br/>
<br/>

Special path aliases:

<br/>

`%FILE%` - This will be replaced with the path to the file being compiled

`%COMPILER%` - This will be replaced with the path to the compiler
