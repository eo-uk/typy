#--------------------------------------------------------------------------------------------
# TyPy
# Strong Typing in Python with Decorators
#--------------------------------------------------------------------------------------------
# Author: eo-uk
# Version: 1.1
# License: MIT License
# GitHub: github.com/eo-uk/typy
#
# Description:
# This light-weight library provides decorators and functions 
# that can be used to implement strongly-typed behaviour in
# Python projects. Works with built-in as well as custom classes.
# Decorators can be used together or stand alone.
#
#--------------------------------------------------------------------------------------------
# Example Usage:
#--------------------------------------------------------------------------------------------
#   from typy import *
#
#   class Bar():
#        pass
#
#    @argtype(a=int, b=int, c=Bar)
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

def _formatError(msg, expected, actual, name=None):
    '''
    Formats error message in exception
    
    Params:
        msg (str): Error message
        expected (class): Expected type
        actual (any): Actual value detected
        name=None (string): Name of the variable
    '''
    return (
        msg
        + ('\nVariable Name: ' + name if name else '')
        + "\n - Expected  : " + str(expected)
        + "\n - Actual    : " + str(type(actual)) + " " + str(actual)
    )

def argtype(customException=True, *expectedTypesArgs, **expectedTypesKwargs):
    '''
    @argtype(**expectedTypesKwargs, customException=True)

    Decorator that checks if argument types of a function match the expected argument types.
    Raises ArgTypeError (or TypeError with customException=False) in case of mismatch.
    *** Must be called with keyword arguments only. ***
    
    Exampe Usage:
        @argtype(a=str, b=int, c=bool)
        foo(a, b, c):
            pass

    Params:
        *types (class): Expected types. Order of types must match order of parameters
        customException (bool): Raises ArgTypeError if true, else raises TypeError
    '''
    ERROR_MSG = "Argument type does not match expected argument type"
    def inner(func):
        def wrapper(*args, **kwargs):

            # Turn args into kwargs and merge with remaining kwargs
            actualArgs = {name: arg for arg, name in zip(args, func.__code__.co_varnames)}
            actualArgs.update(kwargs)

            # Compare types
            for actualArgName, actualArgValue in actualArgs.items():
                for expectedArgName, expectedArgType in expectedTypesKwargs.items():
                    if actualArgName == expectedArgName and type(actualArgValue) != expectedArgType:
                        error = _formatError(ERROR_MSG, expectedArgType, actualArgValue, name=actualArgName)
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

            # Get return value of func and compare its type
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
    # Compare variable type
    if type(value) != expectedType:
        error = _formatError(ERROR_MSG, expectedType, value)
        if customException:
            raise VarTypeError(error)
        raise TypeError(error)
    return value
