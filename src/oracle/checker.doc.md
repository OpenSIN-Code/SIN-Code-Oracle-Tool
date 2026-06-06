# checker.py

- What: Coverage comparison between source and test files.
- Touches: `cli.py` (calls `check_coverage`).
- Heuristic: strips `test_` prefix from test function names to infer coverage.
- Also scans `Call` nodes inside test bodies to find tested functions.
