import unittest
import typy

class TestTypy(unittest.TestCase):

    def test_argtype_match(self):
        @typy.argtype(i=int)
        def foo(i):
            return i*i
        self.assertEqual(foo(2), 4)
    
    def test_argtype_mismatch(self):
        @typy.argtype(i=int)
        def foo(i):
            return i*i
        with self.assertRaises(typy.ArgTypeError) as context:
            foo("string")

    def test_argtype_without_custom_exception(self):
        @typy.argtype(i=int, customException=False)
        def foo(i):
            return i*i
        try:
            foo("string")
        except typy.ArgTypeError:
            self.fail("@argtype raised ArgTypeError instead of TypeError")
        except TypeError:
            pass

    def test_argtype_multi_args_match(self):
        @typy.argtype(i=int, j=int)
        def foo(i, j):
            return i*j
        self.assertEqual(foo(2, 3), 6)

    def test_argtype_multi_args_mismatch(self):
        @typy.argtype(i=int, j=float)
        def foo(i, j):
            return i*j
        with self.assertRaises(typy.ArgTypeError) as context:
            foo(2, 3)

    def test_returntype_match(self):
        @typy.returntype(float)
        def foo(i, j):
            return i / j
        self.assertEqual(foo(4, 2), 2)

    def test_returntype_mismatch(self):
        @typy.returntype(int)
        def foo(i, j):
            return i / j
        with self.assertRaises(typy.ReturnTypeError) as context:
            foo(4, 2)

    def test_returntype_without_custom_exception(self):
        @typy.returntype(int, customException=False)
        def foo(i, j):
            return i / j
        try:
            foo(6, 3)
        except typy.ReturnTypeError:
            self.fail("@argtype raised ArgTypeError instead of TypeError")
        except TypeError:
            pass

    def test_argtype_returntype_together(self):
        @typy.argtype(i=int, j=int)
        @typy.returntype(float)
        def foo(i, j):
            return i / j
        self.assertEqual(foo(6, 3), 2)

    def test_custom_class(self):
        class Bar():
            pass

        @typy.argtype(Bar)
        @typy.returntype(Bar)
        def foo(bar):
            return bar
        bar = Bar()
        try:
            foo(bar)
        except:
            self.fail("Custom class caused an unexpected Exception")


if __name__ == '__main__':
    unittest.main()
