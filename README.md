# PogScript

A new, C-style language which aims to provide dynamic typing, object-oriented programming, and other high-level language features while also being compiled to x86 assembly. The code in this repository is for the base implementation, **pogc2**, which is a compiler for the language written in Python.

**Feel free to make contributions or suggestions -- just submit a pull request!**

To use the compiler, download the latest tested release or pre-release from the [Releases](https://github.com/User0332/PogScript/releases) tab.

To view command line options, type ```pogc2 -h```

<br/>

A sample program (for the *latest binary*) can look like this:

>main.pog

```c
int foo = 838*38
int bar = 234*foo
```

<br/>

A sample program (for the *untested source*) can look like this:
(to create a new project for the current source, you can type ```pogscript new <project_name>``` which will automatically set up a directory and configurations)

>main.pog

```c
int var foo = 838*38
int var bar = 234*foo
```

<br/>

NOTE: Information for writing programs can be found in [docs/guides/progamming/](https://github.com/User0332/PogScript/tree/master/docs/guides/programming)

<br/>
<br/>

Compile it with:

```console
pogc2 main.pog -o <outfile> -d <tokens|ast|dis>
```

<br/>

NOTE: If you are using the source you can also use:

```console
pogscript compile main.pog -o <outfile> -d <tokens|ast|dis>
```

<br/>

where ```outfile```, the argument for -o (--out), can be a file ending with .lst (tokens), .json (syntax tree), or .asm (assembly) and where the argument for -d (--dump) can be the tokens, ast, or dis (assembly output)

<br/>

For more information, you can visit the [guides](https://github.com/User0332/PogScript/tree/master/docs/guides/) section of this repository.
