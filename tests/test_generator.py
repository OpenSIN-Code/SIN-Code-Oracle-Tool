"""Test suite for Oracle generator and checker.

Docs: test_generator.doc.md
"""
from pathlib import Path

import pytest

from oracle.generator import generate_tests, _extract_examples, _parse_function
from oracle.checker import check_coverage, _extract_tested_functions, _extract_source_functions

FIXTURES = Path(__file__).parent / "fixtures"


class TestExtractExamples:
    """Doctest example extraction."""

    def test_extract_add_example(self):
        """Extract >>> example from add docstring."""
        doc = """Add two integers.

        >>> add(2, 3)
        5
        """
        cases = _extract_examples(doc)
        assert len(cases) == 1
        assert cases[0].call == "add(2, 3)"
        assert cases[0].expected == "5"

    def test_extract_multiple_examples(self):
        """Multiple >>> blocks are all extracted."""
        doc = """Do something.

        >>> foo(1)
        10
        >>> foo(2)
        20
        """
        cases = _extract_examples(doc)
        assert len(cases) == 2


class TestGenerateFromSignature:
    """Test generation from function signatures without docstring examples."""

    def test_generate_no_args_function(self):
        """A function with no args generates a basic test."""
        code = "def foo():\n    return 1\n"
        import ast
        tree = ast.parse(code)
        spec = _parse_function(tree.body[0])
        assert spec.name == "foo"
        assert spec.args == []
        assert spec.test_cases == []

    def test_generate_with_args(self):
        """A function with typed args is parsed correctly."""
        code = "def add(a: int, b: int) -> int:\n    return a + b\n"
        import ast
        tree = ast.parse(code)
        spec = _parse_function(tree.body[0])
        assert spec.name == "add"
        assert spec.args == ["a", "b"]
        assert spec.return_type == "int"


class TestGenerateOutput:
    """Full generate_tests output assertions."""

    def test_generates_test_add(self):
        """Generated file should contain test_add with assert."""
        out = generate_tests(FIXTURES / "calculator.py")
        assert "def test_add():" in out
        assert "assert add(2, 3) == 5" in out

    def test_generates_test_subtract(self):
        """Generated file should contain test_subtract."""
        out = generate_tests(FIXTURES / "calculator.py")
        assert "def test_subtract():" in out

    def test_generates_class_method_tests(self):
        """Methods inside classes should be tested too."""
        out = generate_tests(FIXTURES / "calculator.py")
        assert "def test_multiply():" in out
        assert "def test_divide():" in out


class TestCheckCoverage:
    """Coverage checker tests."""

    def test_calculator_coverage(self):
        """Manually written tests cover add, subtract, greet but not divide/multiply."""
        result = check_coverage(FIXTURES / "calculator.py", FIXTURES / "calculator_test.py")
        assert result.total_functions == 5  # add, subtract, multiply, divide, greet
        assert result.covered_functions == 3  # add, subtract, greet
        assert result.coverage_percent == 60.0
        assert "multiply" in result.missing_functions
        assert "divide" in result.missing_functions

    def test_extract_tested_functions(self):
        """_extract_tested_functions finds test_add etc."""
        tested = _extract_tested_functions(FIXTURES / "calculator_test.py")
        assert "add" in tested
        assert "subtract" in tested
        assert "greet" in tested

    def test_extract_source_functions(self):
        """_extract_source_functions lists all public functions."""
        funcs = _extract_source_functions(FIXTURES / "calculator.py")
        assert "add" in funcs
        assert "subtract" in funcs
        assert "multiply" in funcs
        assert "divide" in funcs
        assert "greet" in funcs
