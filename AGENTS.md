# SIN-Code-Oracle-Tool — Verification Oracle — generates pytest test skeletons from Python function signatures and >>> doctest examples; checks that a test file fully covers a source file (exit 1 if any function is untested).

<!--
  Docs: this file follows the SIN-Code AGENTS.md standard
  (see OpenSIN-Code/SIN-Code AGENTS.md section "Ecosystem map" and
  issue #40). sin-brain discovers rules via the section headers below;
  sin-context-bridge queries this file via the "## Architecture" anchor.
  Generated: 2026-06-13; standard version: v1 (chore/issue-40).
-->

## Architecture

Two pipelines: `generate` (AST scan + pytest skeleton emission from docstrings/doctests) and `check` (compares source functions vs. test functions, exits 1 on gap). pytest-coupled by design; doctest prefix `>>>` is the contract. Main entry point: `src/oracle/cli.py` (Typer, 2 subcommands).

## Services

| Service | Port | Purpose |
| ------- | ---- | ------- |
| CLI     | N/A  | `oracle <subcommand>` — generate, check |

## Quick-Start

```bash
pip install -e .
oracle --help
oracle generate tests/fixtures/calculator.py -o /tmp/test_calc.py && oracle check tests/fixtures/calculator.py --against /tmp/test_calc.py
```

## Key Endpoints / Commands

- `oracle generate` — generate pytest skeleton from source module
- `oracle check` — verify test file covers all source functions

## CoDocs

- All Python source files in `src/oracle/` MUST have a `.doc.md` companion.
- Run `sin codocs check` to validate. Output MUST be `OK: 3 files` to pass.
- CoDocs companion for THIS file: none (AGENTS.md is itself a doc).

## Testing

```bash
pytest tests/ -v
pytest tests/test_agents_md.py -v
```

Expected: 14 tests pass (13 existing + 1 from issue #40).

## Integration

- **sin-code HubTool:** `sin code oracle <action>` (e.g. `sin code oracle generate`).
- **MCP server:** `oracle` exposes MCP via the `sin-code serve` adapter; the
  tool prefix in MCP namespace is `oracle__*` (e.g. `oracle__generate`).
- **Cross-repo:** called by `sin code audit` and the verification gate pipeline.

---

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **SIN-Code-Oracle-Tool** (146 symbols, 197 relationships, 5 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/SIN-Code-Oracle-Tool/context` | Codebase overview, check index freshness |
| `gitnexus://repo/SIN-Code-Oracle-Tool/clusters` | All functional areas |
| `gitnexus://repo/SIN-Code-Oracle-Tool/processes` | All execution flows |
| `gitnexus://repo/SIN-Code-Oracle-Tool/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
