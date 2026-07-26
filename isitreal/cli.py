import sys
from typing import Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from isitreal import verify
from isitreal.models import PackageResult

console = Console()


def _format_risk_badge(risk: Optional[str], exists: bool) -> str:
    if not exists:
        if risk == "high":
            return "[bold red]HIGH (MISSING)[/bold red]"
        return "[bold red]MISSING[/bold red]"
    if risk == "high":
        return "[bold red]HIGH[/bold red]"
    elif risk == "unknown":
        return "[bold yellow]UNKNOWN[/bold yellow]"
    elif risk == "low":
        return "[bold green]LOW[/bold green]"
    return "[dim]NONE[/dim]"


@click.group()
def cli():
    """isitreal: dependency reality-checker for AI coding agents."""
    pass


@cli.command()
@click.argument("name")
@click.option("--fail-on", default=None, help="Exit nonzero if risk matches or exceeds threshold (e.g. 'high')")
def check(name: str, fail_on: Optional[str]):
    """Check a single package name for existence and risk."""
    res: PackageResult = verify.package(name)

    title = f"Dependency Check: [bold cyan]{res.name}[/bold cyan]"
    lines = []
    if res.exists:
        lines.append(f"Status: [green]Exists on PyPI[/green] (Canonical name: {res.canonical_name or res.name})")
        lines.append(f"Latest Version: [bold]{res.latest_version or 'N/A'}[/bold]")
        lines.append(f"Age: [bold]{res.age_days if res.age_days is not None else 'N/A'}[/bold] days (Total releases: {res.total_releases})")
        lines.append(f"Risk Level: {_format_risk_badge(res.risk, res.exists)}")
        if res.reasons:
            lines.append("Reasons:")
            for reason in res.reasons:
                lines.append(f"  • {reason}")
    else:
        lines.append("[bold red]Status: Does not exist on PyPI![/bold red]")
        lines.append(f"Risk Level: {_format_risk_badge(res.risk, res.exists)}")
        if res.suggestions:
            lines.append(f"Did you mean one of these? [bold yellow]{', '.join(res.suggestions)}[/bold yellow]")
        if res.reasons:
            for reason in res.reasons:
                lines.append(f"  • {reason}")

    console.print(Panel("\n".join(lines), title=title, expand=False))

    if fail_on:
        fail_on_lower = fail_on.lower()
        if fail_on_lower == "high" and (res.risk == "high" or not res.exists):
            sys.exit(1)
        elif fail_on_lower == "unknown" and (res.risk in ("high", "unknown") or not res.exists):
            sys.exit(1)


@cli.command()
@click.argument("target")
@click.option("--fail-on", default=None, help="Exit nonzero if any package matches threshold (e.g. 'high')")
def scan(target: str, fail_on: Optional[str]):
    """Scan dependencies from a file (requirements.txt/pyproject.toml) or text."""
    results = verify.scan(target)
    if not results:
        console.print("[yellow]No dependencies found to scan.[/yellow]")
        return

    table = Table(title=f"Dependency Scan Results ({len(results)} packages)")
    table.add_column("Package", style="cyan", no_wrap=True)
    table.add_column("Exists", justify="center")
    table.add_column("Risk", justify="center")
    table.add_column("Version", justify="right")
    table.add_column("Age (Days)", justify="right")
    table.add_column("Notes / Suggestions", style="white")

    has_high_risk = False
    has_unknown_risk = False

    for res in results:
        exists_str = "[green]Yes[/green]" if res.exists else "[bold red]No[/bold red]"
        risk_str = _format_risk_badge(res.risk, res.exists)
        version_str = res.latest_version or "-"
        age_str = str(res.age_days) if res.age_days is not None else "-"
        notes_list = []
        if not res.exists and res.suggestions:
            notes_list.append(f"Suggestions: {', '.join(res.suggestions)}")
        if res.reasons:
            notes_list.extend(res.reasons)
        notes_str = "; ".join(notes_list)

        table.add_row(res.name, exists_str, risk_str, version_str, age_str, notes_str)

        if res.risk == "high" or not res.exists:
            has_high_risk = True
        elif res.risk == "unknown":
            has_unknown_risk = True

    console.print(table)

    if fail_on:
        fail_on_lower = fail_on.lower()
        if fail_on_lower == "high" and has_high_risk:
            sys.exit(1)
        elif fail_on_lower == "unknown" and (has_high_risk or has_unknown_risk):
            sys.exit(1)


@cli.command()
def mcp():
    """Run the isitreal MCP server."""
    from isitreal.mcp_server import main as run_mcp
    run_mcp()


def main():
    cli()


if __name__ == "__main__":
    main()
