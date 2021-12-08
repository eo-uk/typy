import unittest
from typy import *

class TestTypy(unittest.TestCase):

    def test_argtype_match(self):
        @argtype(i=int)
        def foo(i):
            return i*i
        self.assertEqual(foo(2), 4)
    
    def test_argtype_mismatch(self):
        @argtype(i=int)
        def foo(i):
            return i*i
        with self.assertRaises(ArgTypeError) as context:
            foo("string")

    def test_argtype_without_custom_exception(self):
        @argtype(i=int, customException=False)
        def foo(i):
            return i*i
        try:
            foo("string")
        except ArgTypeError:
            self.fail("@argtype raised ArgTypeError instead of TypeError")
        except TypeError:
            pass

    def test_argtype_multi_args_match(self):
        @argtype(i=int, j=int)
        def foo(i, j):
            return i*j
        self.assertEqual(foo(2, 3), 6)

    def test_argtype_multi_args_reverse_match(self):
        @argtype(j=int, i=int)
        def foo(i, j):
            return i*j
        self.assertEqual(foo(2, 3), 6)

    def test_argtype_with_kwargs_mismatch(self):
        @argtype(i=int, j=int, k=int)
        def foo(i, j, k):
            return i*j
        with self.assertRaises(ArgTypeError) as context:
            foo(2, 3, k=5.5)

    def test_argtype_too_many_kwargs(self):
        @argtype(i=int, j=int, k=int)
        def foo(i, j):
            return i*j
        foo(2, 3)

    def test_argtype_too_few_kwargs(self):
        @argtype(i=int)
        def foo(i, j, k):
            return i*j
        self.assertEqual(foo(2, 3.5, k='test'), 7.0)

    def test_argtype_multi_args_mismatch(self):
        @argtype(i=int, j=float)
        def foo(i, j):
            return i*j
        with self.assertRaises(ArgTypeError) as context:
            foo(2, 3)

    def test_returntype_match(self):
        @returntype(float)
        def foo(i, j):
            return i / j
        self.assertEqual(foo(4, 2), 2)

    def test_returntype_mismatch(self):
        @returntype(int)
        def foo(i, j):
            return i / j
        with self.assertRaises(ReturnTypeError) as context:
            foo(4, 2)

    def test_returntype_without_custom_exception(self):
        @returntype(int, customException=False)
        def foo(i, j):
            return i / j
        try:
            foo(6, 3)
        except ReturnTypeError:
            self.fail("@argtype raised ReturnTypeError instead of TypeError")
        except TypeError:
            pass

    def test_argtype_returntype_together(self):
        @argtype(i=int, j=int)
        @returntype(float)
        def foo(i, j):
            return i / j
        self.assertEqual(foo(6, 3), 2)

    def test_custom_class(self):
        class Bar():
            pass

        @argtype(Bar)
        @returntype(Bar)
        def foo(bar):
            return bar
        bar = Bar()
        try:
            foo(bar)
        except:
            self.fail("Custom class caused an unexpected Exception")

    def test_class_method_match(self):
        class Bar():
            @argtype(a=str, b=str)
            def foo(self, a, b):
                return a + b
        bar = Bar()
        self.assertEqual(bar.foo('test ', 'string'), 'test string')

    def test_class_method_mismatch(self):
        class Bar():
            @argtype(a=str, b=str)
            def foo(self, a, b):
                return a + b
        bar = Bar()
        with self.assertRaises(ArgTypeError) as context:
            bar.foo('test ', 42)

    def test_class_init_method_match(self):
        class Bar():
            @argtype(a=str)
            def __init__(self, a):
                self.a = a
        bar = Bar('test')
        
    def test_class_init_method_mismatch(self):
        class Bar():
            @argtype(a=str)
            def __init__(self, a):
                self.a = a
        with self.assertRaises(ArgTypeError) as context:
            bar = Bar(42)
        
    def test_vartype_match(self):
        i = vartype(int, 5)

    def test_vartype_mismatch(self):
        with self.assertRaises(VarTypeError) as context:
            i = vartype(int, '5')


if __name__ == '__main__':
    unittest.main()
