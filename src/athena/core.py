"""Core skill system — decorator, Skill class, and registry."""

from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Skill:
    """A registered agent skill with metadata and execution logic."""

    name: str
    description: str
    func: Callable[..., Any]
    category: str = "general"
    input_schema: dict[str, Any] = field(default_factory=dict)
    output_schema: dict[str, Any] = field(default_factory=dict)

    def execute(self, **kwargs: Any) -> Any:
        """Execute the skill after validating inputs."""
        self.validate_input(kwargs)
        return self.func(**kwargs)

    def validate_input(self, inputs: dict[str, Any]) -> None:
        """Validate that required parameters are provided."""
        sig = inspect.signature(self.func)
        for param_name, param in sig.parameters.items():
            if param.default is inspect.Parameter.empty and param_name not in inputs:
                raise ValueError(f"Missing required input: {param_name}")

    def info(self) -> dict[str, Any]:
        """Return skill metadata as a dictionary."""
        sig = inspect.signature(self.func)
        params = {
            name: str(p.annotation.__name__) if p.annotation != inspect.Parameter.empty else "Any"
            for name, p in sig.parameters.items()
        }
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "parameters": params,
        }


def skill(
    name: str | None = None,
    description: str = "",
    category: str = "general",
) -> Callable[[Callable[..., Any]], Skill]:
    """Decorator to register a function as an agent skill.

    Usage:
        @skill(name="greet", description="Greet a user")
        def greet(name: str) -> str:
            return f"Hello, {name}!"
    """

    def decorator(func: Callable[..., Any]) -> Skill:
        skill_name = name or func.__name__
        skill_desc = description or func.__doc__ or ""
        return Skill(
            name=skill_name,
            description=skill_desc,
            func=func,
            category=category,
        )

    return decorator


class SkillRegistry:
    """Registry for discovering and executing agent skills."""

    def __init__(self) -> None:
        self._skills: dict[str, Skill] = {}

    def register(self, skill_obj: Skill) -> None:
        """Register a skill in the registry."""
        if not isinstance(skill_obj, Skill):
            raise TypeError(f"Expected Skill, got {type(skill_obj).__name__}")
        self._skills[skill_obj.name] = skill_obj

    def get(self, name: str) -> Skill | None:
        """Get a skill by exact name."""
        return self._skills.get(name)

    def search(self, query: str) -> list[Skill]:
        """Search skills by name or description (fuzzy matching)."""
        query_lower = query.lower()
        results: list[Skill] = []
        for s in self._skills.values():
            if query_lower in s.name.lower() or query_lower in s.description.lower():
                results.append(s)
        return results

    def filter_by_category(self, category: str) -> list[Skill]:
        """Filter skills by category."""
        return [s for s in self._skills.values() if s.category == category]

    def execute(self, name: str, inputs: dict[str, Any]) -> Any:
        """Execute a skill by name with the given inputs."""
        skill_obj = self._skills.get(name)
        if skill_obj is None:
            raise KeyError(f"Skill not found: {name}")
        return skill_obj.execute(**inputs)

    def list_skills(self) -> list[dict[str, Any]]:
        """List all registered skills with their metadata."""
        return [s.info() for s in self._skills.values()]

    def remove(self, name: str) -> bool:
        """Remove a skill from the registry."""
        if name in self._skills:
            del self._skills[name]
            return True
        return False

    def export_registry(self) -> dict[str, Any]:
        """Export the registry as a serializable dictionary."""
        return {
            "skills": {name: s.info() for name, s in self._skills.items()},
            "total": len(self._skills),
        }

    @property
    def size(self) -> int:
        """Return the number of registered skills."""
        return len(self._skills)
