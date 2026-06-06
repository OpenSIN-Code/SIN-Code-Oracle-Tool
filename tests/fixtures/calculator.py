"""Simple calculator fixture for Oracle tests.

Docs: calculator.doc.md
"""


def add(a: int, b: int) -> int:
    """Add two integers.

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    """
    return a + b


def subtract(a: int, b: int) -> int:
    """Subtract b from a.

    >>> subtract(5, 3)
    2
    """
    return a - b


class Calculator:
    """A calculator class."""

    def multiply(self, a: int, b: int) -> int:
        """Multiply two numbers.

        >>> calc = Calculator()
        >>> calc.multiply(2, 3)
        6
        """
        return a * b

    def divide(self, a: int, b: int) -> float:
        """Divide a by b.

        >>> calc = Calculator()
        >>> calc.divide(10, 2)
        5.0
        """
        return a / b


def greet(name: str = "world") -> str:
    """Greet someone."""
    return f"Hello, {name}!"
