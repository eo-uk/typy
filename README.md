# typy
Strong Typing in Python with Decorators

## Description
This light-weight library provides decorators that can be used to implement strongly-typed behaviour in Python projects. Works with built-in as well as custom classes. Decorators can be used together or stand alone.

## Example Usage
```
class Bar():
	pass

@argtype(int, int, Bar)
@returntype(float)
def foo(a, b, c):
	return a / b

bar = Bar()
print(foo(6, 3, bar))
```