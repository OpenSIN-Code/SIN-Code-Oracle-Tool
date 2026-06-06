"""Generate pytest skeletons from Python source and docstring examples.

Docs: generator.doc.md
"""
import ast
import re
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional


class TestCase(NamedTuple):
    """A single test case extracted from a docstring example."""
    call: str
    expected: str


class FuncSpec(NamedTuple):
    """Metadata about a function to be tested."""
    name: str
    args: List[str]
    return_type: Optional[str]
    is_method: bool
    test_cases: List[TestCase]


# ── Docstring parsing ─────────────────────────────────


def _extract_examples(docstring: str) -> List[TestCase]:
    """Extract `>>> ` doctest examples from a docstring.

    Returns a list of (call_str, expected_str) pairs.
    """
    lines = docstring.splitlines()
    cases: List[TestCase] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith(">>>"):
            # Extract the call (strip `>>>` prefix)
            call = line.strip()[3:].strip()
            i += 1
            # Continue with `...` continuation lines
            while i < len(lines) and lines[i].strip().startswith("..."):
                call += "\n" + lines[i].strip()[3:].strip()
                i += 1
            # Collect expected output lines until next `>>>`/`...` or blank line
            expected_lines: List[str] = []
            while i < len(lines):
                stripped = lines[i].strip()
                if stripped.startswith(">>>") or stripped.startswith("..."):
                    break
                if stripped == "":
                    # Stop at blank line unless we already have expected output
                    if expected_lines:
                        break
                    i += 1
                    continue
                expected_lines.append(stripped)
                i += 1
            if expected_lines:
                expected = "\n".join(expected_lines)
                cases.append(TestCase(call=call, expected=expected))
        else:
            i += 1
    return cases


# ── AST parsing ───────────────────────────────────────

def _type_str(node: ast.AST | None) -> Optional[str]:
    """Convert an AST annotation node back to a string (best-effort)."""
    if node is None:
        return None
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant):
        return str(node.value)
    if isinstance(node, ast.Subscript):
        value = _type_str(node.value)
        slice_ = _type_str(node.slice)
        return f"{value}[{slice_}]"
    if isinstance(node, ast.Attribute):
        return f"{_type_str(node.value)}.{node.attr}"
    if isinstance(node, ast.List):
        return "list"
    if isinstance(node, ast.Tuple):
        return "tuple"
    return None


def _parse_function(node: ast.FunctionDef | ast.AsyncFunctionDef, is_method: bool = False) -> FuncSpec:
    """Build a FuncSpec from a function AST node."""
    args = []
    for arg in node.args.args:
        if arg.arg == "self" and is_method:
            continue
        args.append(arg.arg)
    for arg in node.args.kwonlyargs:
        args.append(arg.arg)

    return_type = _type_str(node.returns)
    docstring = ast.get_docstring(node) or ""
    test_cases = _extract_examples(docstring)
    return FuncSpec(
        name=node.name,
        args=args,
        return_type=return_type,
        is_method=is_method,
        test_cases=test_cases,
    )


def _build_assertion(spec: FuncSpec, case: TestCase) -> str:
    """Generate a single assert statement from a test case."""
    call = case.call
    expected = case.expected

    # Try to parse expected as a literal for clean assert
    try:
        ast.literal_eval(expected)
        is_literal = True
    except Exception:
        is_literal = False

    if is_literal:
        return f"    assert {call} == {expected}"
    else:
        return f"    result = {call}\n    assert result == {expected}"


def _build_test_function(spec: FuncSpec) -> str:
    """Generate a pytest test function for a FuncSpec."""
    lines = [f"def test_{spec.name}():"]

    if spec.test_cases:
        for case in spec.test_cases:
            lines.append(_build_assertion(spec, case))
    else:
        # No examples — generate a placeholder based on signature
        if spec.args:
            # Build default args (int → 0, str → "", float → 0.0, etc.)
            arg_values = []
            for arg in spec.args:
                arg_values.append("0")  # default fallback
            call = f"{spec.name}({', '.join(arg_values)})"
            lines.append(f"    result = {call}")
            if spec.return_type:
                lines.append(f"    assert result is not None  # TODO: assert type {spec.return_type}")
            else:
                lines.append("    assert result is not None  # TODO: verify return value")
        else:
            lines.append(f"    result = {spec.name}()")
            lines.append("    assert result is not None  # TODO: verify return value")

    return "\n".join(lines)


# ── Public API ──────────────────────────────────────

def generate_tests(source_path: Path) -> str:
    """Generate a pytest test file from *source_path*."""
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    specs: List[FuncSpec] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            specs.append(_parse_function(node, is_method=False))
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    specs.append(_parse_function(item, is_method=True))

    lines = [
        f'"""Auto-generated tests for {source_path.name}."""',
        "import pytest",
        f"from {source_path.stem} import *",
        "",
    ]

    for spec in specs:
        lines.append(_build_test_function(spec))
        lines.append("")

    return "\n".join(lines)
