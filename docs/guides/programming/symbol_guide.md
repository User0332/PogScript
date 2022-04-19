# Variable and function guide

Symbols can be created using a datatype followed by a symbol type and identifier.

Ex.

```c

int         var           foo          =            0
^           ^             ^            ^            ^
datatype    symbol type   identifier   assignment   value
```

<br/>

Below are tables for datatypes and symbol types

<br/>

| Data Type     | Description 
| -----------   | ----------- 
| `int`         | standard int32
| `char`        | single character stored as an `int` (not implemented)
| `float`       | floating-point number (not implemented)

<br/>
<br/>

| Symbol Type   | Description 
| -----------   | ----------- 
| `var`         | standard variable
| `ptr`         | variable pointer (this can be stacked like `char ptr ptr`) (not implemented)
| `const`       | constant variable (not implemented)
| `func`        | used to define a function (not implemented)

<br/>

---------------------------------

<br/>

Functions can look a little like this:

```cpp
using braces

int func myfunction(int var arg)
{
    
}

```
