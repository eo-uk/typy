#--------------------------------------------------------------------------------------------
# TyPy
# Strong Typing in Python with Decorators
#--------------------------------------------------------------------------------------------
# Author: eo-uk
# Version: 1.0
# License: MIT License
# GitHub: github.com/eo-uk/typy
#
# Description:
# This light-weight library provides decorators that can be used
# to implement strongly-typed behaviour in Python projects.
# Works with built-in as well as custom classes.
# Decorators can be used together or stand alone.
#
#--------------------------------------------------------------------------------------------
# Example Usage:
#--------------------------------------------------------------------------------------------
#   class Bar():
#        pass
#
#    @argtype(int, int, Bar)
#    @returntype(float)
#    def foo(a, b, c):
#        return a / b
#
#    bar = Bar()
#    print(foo(6, 3, bar))
#
#    x = vartype(int, 5)
#    y = vartype(Bar, Bar())
#--------------------------------------------------------------------------------------------


class StrongTypeError(TypeError):
    """Base exception for TyPy errors"""
    pass

class ArgTypeError(StrongTypeError):
    """Raised when argtype fails to match expected type"""
    pass

class ReturnTypeError(StrongTypeError):
    """Raised when returntype fails to match expected type"""
    pass

class VarTypeError(StrongTypeError):
    """Raised when vartype fails to match expected type"""
    pass

def _formatError(msg, expected, actual):
    '''
    Formats error message in exception
    
    Params:
        msg (str): Error message
        expected (class): Expected type
        actual (any): Actual value detected
    '''
    return (
        msg
        + "\n - Expected  : " + str(expected)
        + "\n - Actual    : " + str(type(actual)) + " " + str(actual)
    )

def argtype(*types, customException=True):
    '''
    @argtype(*types, customException=True)

    Decorator that checks if argument types of a function match the expected argument types.
    Raises ArgTypeError (or TypeError with customException=False) in case of mismatch.

    Params:
        *types (class): Expected types. Order of types must match order of parameters
        customException (bool): Raises ArgTypeError if true, else raises TypeError
    '''
    ERROR_MSG = "Argument type does not match expected argument type"
    def inner(func):
        def wrapper(*args, **kwargs):
            for arg, expectedType in zip(args, types):
                if type(arg) != expectedType:
                    error = _formatError(ERROR_MSG, expectedType, arg)
                    if customException:
                        raise ArgTypeError(error)
                    raise TypeError(error)
            return func(*args, **kwargs)
        return wrapper
    return inner


def returntype(expectedType, customException=True):
    '''
    @returntype(expectedType, customException=True)

    Decorator that checks if return type of a function match the expected return type.
    Raises ReturnTypeError (or TypeError with customException=False) in case of mismatch.

    Params:
        expectedType (class): Expected return type
        customException (bool): Raises ReturnTypeError if true, else raises TypeError
    '''
    ERROR_MSG = "Return type does not match expected return type"
    def inner(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if type(result) != expectedType:
                error = _formatError(ERROR_MSG, expectedType, result)
                if customException:
                    raise ReturnTypeError(error)
                raise TypeError(error)
            return func(*args, **kwargs)
        return wrapper
    return inner

def vartype(expectedType, value, customException=True):
    '''
    vartype(expectedType, customException=True)

    Function that checks if the type of a variable's value matches the expected type.
    Raises ReturnTypeError (or TypeError with customException=False) in case of mismatch.

    Params:
        expectedType (class): Expected type of the variable's value
        customException (bool): Raises VarTypeError if true, else raises TypeError
    '''
    ERROR_MSG = "Variable type does not match expected variable type"
    if type(value) != expectedType:
        error = _formatError(ERROR_MSG, expectedType, value)
        if customException:
            raise VarTypeError(error)
        raise TypeError(error)
    return value
