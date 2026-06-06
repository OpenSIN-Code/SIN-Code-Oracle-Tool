"""Manually written tests for calculator (used by coverage check).

Docs: calculator_test.doc.md
"""
from calculator import add, subtract, Calculator, greet


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_greet():
    assert greet("Alice") == "Hello, Alice!"
