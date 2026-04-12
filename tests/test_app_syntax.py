import py_compile
import unittest


class TestAppSyntax(unittest.TestCase):
    def test_app_py_compiles(self):
        py_compile.compile("app.py", doraise=True)


if __name__ == "__main__":
    unittest.main()
