# generator.py

- What: AST + docstring parsing to generate pytest skeletons.
- Touches: `cli.py` (calls `generate_tests`).
- Parses `>>> ` doctest examples via regex.
- Falls back to placeholder assertions when no examples are present.
