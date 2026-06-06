"""Coverage checker — compare generated tests against existing test files.

Docs: checker.doc.md
"""
import ast
from pathlib import Path
from typing import Dict, List, NamedTuple, Set


class CoverageResult(NamedTuple):
    """Coverage analysis result."""
    source_file: str
    test_file: str
    total_functions: int
    covered_functions: int
    missing_functions: List[str]
    coverage_percent: float


def _extract_tested_functions(test_path: Path) -> Set[str]:
    """Extract function names tested from a test file.

    Heuristic: every test function name `test_<something>` implies
    the tested function is `<something>` (stripping `test_` prefix).
    """
    source = test_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    tested: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            name = node.name
            if name.startswith("test_"):
                # strip test_ prefix to infer the tested function name
                tested.add(name[5:])
            # Also look for direct calls inside test bodies
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                    tested.add(child.func.id)
    return tested


def _extract_source_functions(source_path: Path) -> Set[str]:
    """Extract public function names from a source file."""
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    functions: Set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                functions.add(node.name)
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not item.name.startswith("_"):
                        functions.add(item.name)
    return functions


def check_coverage(source_path: Path, test_path: Path) -> CoverageResult:
    """Compare *source_path* against *test_path* and report coverage."""
    source_funcs = _extract_source_functions(source_path)
    tested_funcs = _extract_tested_functions(test_path)

    covered = source_funcs & tested_funcs
    missing = sorted(source_funcs - tested_funcs)
    total = len(source_funcs)
    percent = (len(covered) / total * 100) if total else 100.0

    return CoverageResult(
        source_file=str(source_path),
        test_file=str(test_path),
        total_functions=total,
        covered_functions=len(covered),
        missing_functions=missing,
        coverage_percent=percent,
    )
