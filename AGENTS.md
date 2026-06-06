# SIN-Code-Oracle-Tool — Agent-Engineering Hints

## What it does (1 sentence)
Verification Oracle — generates `pytest` test skeletons from Python function signatures and `>>>` doctest examples, then verifies that an existing test file fully covers a source file (exit 1 if any function is untested).

## Stack
- Language: Python
- Version: 0.1.0
- Test count: 13 tests
- CLI: `oracle` with 2 subcommands (`generate`, `check`)

## When to use
- Bootstrapping a test file from scratch when a module already has docstrings + doctests (`oracle generate`).
- CI gate to enforce that every public function in a module has a corresponding test (`oracle check --against`).
- Verifying that a refactor did not drop test coverage by accident.

## Boundaries
- Do NOT couple `generator.py` to a specific test framework other than `pytest` — the emitted skeleton must stay pytest-compatible.
- Do NOT change the doctest parsing format (`>>>` prefix) — it is the standard contract.
- Always keep the `check` exit-code contract: `0` = 100% coverage, `1` = missing tests.
- Always run via `oracle.cli:main` — internal APIs (`generator.generate_*`, `checker.check_coverage`) may change between minor versions.

## Key files
- `src/oracle/generator.py` — AST-based scanner + pytest skeleton emitter.
- `src/oracle/checker.py` — coverage comparator (source functions vs. test functions).
- `src/oracle/cli.py` — Typer CLI (`generate`, `check`).
- `tests/test_generator.py` — 13 tests covering generation, doctest extraction, and `TestCheckCoverage` integration.
- `tests/fixtures/` — sample `calculator.py` + matching test files.

## Verification
- `pytest tests/ -v` — all 13 tests pass.
- `oracle --help` — prints help with `generate` and `check`.
- `oracle generate tests/fixtures/calculator.py -o /tmp/test_calc.py && oracle check tests/fixtures/calculator.py --against /tmp/test_calc.py` — end-to-end smoke test.
