# PogScript

NOTE: THIS REPOSITORY IS NOW ARCHIVED AND THE PROJECT HAS BEEN DROPPED. A NEW PROJECT HAS BRANCHED OFF OF POGSCRIPT AT [https://github.com/User0332/UntypedScript](https://github.com/User0332/UntypedScript)

A new, C-style language which aims to provide dynamic typing, object-oriented programming, and other high-level language features while also being compiled to x86 assembly. The code in this repository is for the base implementation, **pogc2**, which is a compiler for the language written in Python.

**Feel free to make contributions or suggestions -- just submit a pull request!**

To use the compiler, download the latest tested release or pre-release from the [Releases](https://github.com/User0332/PogScript/releases) tab. You must also have a working version of Python 3.9 or higher for the compiler source to work.

<br/>

NOTE: For the source, the command `pogscript build` will build the compiler and remove unnecessary files. You must have Python and Nutika installed for the command to work.

<br/>

To view command line options, type ```pogc2 -h```

<br/>

A sample program for the latest compiler can look like this:

>main.pog

```c
int var foo = 838*38
int var bar = 234*foo
```

<br/>
<br/>

NOTE: Information for writing programs can be found at [https://User0332.github.io/PogScript/docs](https://User0332.github.io/PogScript/docs)

<br/>
<br/>

Compile it with:

```console
pogc2 main.pog -o <outfile> -d <tokens|ast|dis>
```

or

```console
pogscript compile main.pog -o <outfile> -d <tokens|ast|dis>
```

<br/>

where `outfile`, the argument for -o (--out), can be a file ending with .lst (tokens), .json (syntax tree), or .asm (assembly) and where the argument for -d (--dump) can be the `tokens`, `ast`, or `dis` (assembly output)

<br/>

For more information, you can visit the [docs](https://User0332.github.io/PogScript/docs) section of my Github Pages site.
