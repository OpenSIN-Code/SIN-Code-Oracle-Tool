# Oracle Skill

## Usage

```bash
oracle generate <file.py> [-o <test_file.py>]
oracle check <file.py> --against <test_file.py>
```

## How It Works

1. Parse AST for `FunctionDef` and `ClassDef` nodes.
2. Extract `>>>` doctest examples from docstrings.
3. Generate `def test_<name>(...):` with `assert` statements.
4. If no examples, emit placeholder assertions with default args.

## Coverage Check

- Scans test file for `test_*` functions.
- Infers tested function names by stripping `test_` prefix.
- Reports missing functions and percentage.

## Integration

Pre-commit hook:

```yaml
- run: oracle check src/ --against tests/
```
