# PogScript

A new, C-like language which aims to provide dynamic typng, object-oriented programming, and other high-level language features while also being compiled to x86 assembly. The code in this repository is for the base implementation, **pogc2**, which is a compiler for the language written in Python.

**You are free to make contributions or suggestions -- just submit a pull request!**

To use the compiler, download the latest tested release or the pre-release from the [Releases](https://github.com/User0332/PogScript/releases) tab.

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
```console
pogc2 file.pog -o <outfile> --dump <tokens|ast>
```

where ```outfile``` can be a file ending with .lst or .json, and where the argument for --dump (-d) can be the tokens or ast
