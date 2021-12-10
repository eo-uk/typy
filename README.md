# typy
Static Typing in Python without the Type Annotation Syntax  
*Version: 1.1*

## Description
This light-weight library provides decorators and functions that can be used to implement statically-typed behaviour in Python projects without needing the type annotation syntax. Works with built-in as well as custom classes. Decorators can be used together or stand alone.

## Example Usage
```
from typy import *

class Bar():
	@argtype(s=str)
	def __init__(self, s):
		self.s = s

@argtype(a=int, b=int, c=Bar)
@returntype(float)
def foo(a, b, c):
	return a / b

bar = Bar('test')
print(foo(6, 3, bar))

x = vartype(int, 5)
y = vartype(Bar, Bar('test'))
```