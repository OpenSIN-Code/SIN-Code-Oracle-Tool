# Oracle — Verification Oracle

Generate test oracles from Python docstrings and verify coverage.

## SOTA Status

- Tests: **13 passing** (`pytest tests/ -q`, ~0.2s)
- CI: ![ci](https://img.shields.io/badge/ci-pending-lightgrey) (placeholder — wire up GitHub Actions)
- Maturity tier: **1 / 3** (MVP — v0.1.0)
- Last commit: 2026-06-06

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

## Integration

This tool is exposed in the unified `sin code` hub:

```bash
sin code oracle generate src/foo.py -o tests/test_foo.py    # alias of: oracle generate ...
sin code oracle check    src/foo.py --against tests/test_foo.py
```

See `AGENTS.md` for boundaries, key files, and verification steps.

