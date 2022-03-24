# PogScript

A new language written in Python

**You are free to make contributions or suggestions -- just submit a pull request!**

To use the compiler, download the source from ```src/``` (or the latest tested release from ```bin_release/```)

To view command line options, type ```pogc2 -h```

A sample program (for the *latest binary*) can look like this:

>file.pog
```cs
int foo = 838*38
int bar = 234*foo
```
A sample program (for the *untested source*) can look like this:

>file.pog
```cs
int var foo = 838*38
int var bar = 234*foo
```

Compile it with:
>pogc2 file.pog -o {outfile} --dump {tokens|ast}

where ```outfile``` can be a file ending with .lst or .json, and where the argument for --dump (-d) can be the tokens or ast
