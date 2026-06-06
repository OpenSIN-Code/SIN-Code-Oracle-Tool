"""Typer CLI for Oracle.

Docs: cli.doc.md
"""
from pathlib import Path

import typer

from oracle.generator import generate_tests
from oracle.checker import check_coverage

app = typer.Typer(help="Verification Oracle — generate tests and check coverage")


@app.command()
def generate(
    source_file: Path = typer.Argument(..., help="Python source file to generate tests for"),
    output: Path = typer.Option(None, "--output", "-o", help="Output test file (default: stdout)"),
) -> None:
    """Generate pytest test skeletons from a Python file."""
    test_code = generate_tests(source_file)
    if output:
        output.write_text(test_code, encoding="utf-8")
        typer.echo(f"Generated tests written to {output}")
    else:
        typer.echo(test_code)


@app.command()
def check(
    source_file: Path = typer.Argument(..., help="Python source file"),
    against: Path = typer.Option(..., "--against", help="Existing test file to compare against"),
) -> None:
    """Check test coverage of *source_file* against *against*."""
    result = check_coverage(source_file, against)
    typer.echo(f"Source: {result.source_file}")
    typer.echo(f"Tests:  {result.test_file}")
    typer.echo(f"Functions: {result.covered_functions}/{result.total_functions}")
    typer.echo(f"Coverage: {result.coverage_percent:.1f}%")
    if result.missing_functions:
        typer.echo("Missing tests for:")
        for func in result.missing_functions:
            typer.echo(f"  - {func}")
    raise typer.Exit(code=0 if result.coverage_percent == 100 else 1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
