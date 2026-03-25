"""Athena CLI — manage and execute agent skills."""

from __future__ import annotations

import json

import click
from rich.console import Console
from rich.table import Table

from athena.core import SkillRegistry
from athena.builtin_skills import get_all_builtin_skills

console = Console()


def _build_registry() -> SkillRegistry:
    """Build a registry with all built-in skills."""
    registry = SkillRegistry()
    for s in get_all_builtin_skills():
        registry.register(s)
    return registry


@click.group()
@click.version_option(version="0.1.0", prog_name="athena")
def main() -> None:
    """Athena — Modular skills framework for AI agents."""
    pass


@main.command("list")
@click.option("--category", "-c", default=None, help="Filter by category")
def list_skills(category: str | None) -> None:
    """List all registered skills."""
    registry = _build_registry()
    skills = registry.list_skills()

    if category:
        skills = [s for s in skills if s["category"] == category]

    table = Table(title="Registered Skills")
    table.add_column("Name", style="cyan")
    table.add_column("Category", style="yellow")
    table.add_column("Description")

    for s in skills:
        table.add_row(s["name"], s["category"], s["description"])

    console.print(table)


@main.command()
@click.argument("name")
@click.option("--input", "input_json", required=True, help="JSON input for the skill")
def run(name: str, input_json: str) -> None:
    """Execute a skill by name."""
    registry = _build_registry()
    try:
        inputs = json.loads(input_json)
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON input:[/red] {e}")
        raise SystemExit(1)

    try:
        result = registry.execute(name, inputs)
        console.print(f"[green]Result:[/green] {result}")
    except KeyError:
        console.print(f"[red]Skill not found:[/red] {name}")
        raise SystemExit(1)
    except Exception as e:
        console.print(f"[red]Execution error:[/red] {e}")
        raise SystemExit(1)


@main.command()
@click.argument("name")
def info(name: str) -> None:
    """Show detailed information about a skill."""
    registry = _build_registry()
    skill_obj = registry.get(name)
    if skill_obj is None:
        console.print(f"[red]Skill not found:[/red] {name}")
        raise SystemExit(1)

    details = skill_obj.info()
    console.print(f"\n[bold cyan]{details['name']}[/bold cyan]")
    console.print(f"  Description: {details['description']}")
    console.print(f"  Category:    {details['category']}")
    console.print(f"  Parameters:  {details['parameters']}\n")


if __name__ == "__main__":
    main()
