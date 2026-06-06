# Oracle — Verification Oracle

Generate test oracles from Python docstrings and verify coverage.

## Quick Start

```bash
pip install -e .
oracle generate src/calculator.py -o tests/test_calculator.py
oracle check src/calculator.py --against tests/test_calculator.py
```

## CLI

### `generate`

Reads a Python file, parses function signatures and `>>>` doctest examples, and emits a `pytest` test skeleton.

```bash
oracle generate <file.py> [-o <test_file.py>]
```

### `check`

Compares an existing test file against a source file and reports missing coverage.

```bash
oracle check <file.py> --against <test_file.py>
```

Exit code: `0` = 100% coverage, `1` = missing tests.

## GitHub

https://github.com/OpenSIN-Code/SIN-Code-Oracle-Tool
