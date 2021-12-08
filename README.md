# typy
Static Typing in Python with Decorators

## Description
This light-weight library provides decorators and functions that can be used to implement statically-typed behaviour in Python projects. Works with built-in as well as custom classes. Decorators can be used together or stand alone.

## Example Usage
```
from typy import *

class Bar():
	pass

@argtype(a=int, b=int, c=Bar)
@returntype(float)
def foo(a, b, c):
	return a / b

bar = Bar()
print(foo(6, 3, bar))

x = vartype(int, 5)
y = vartype(Bar, Bar())
```