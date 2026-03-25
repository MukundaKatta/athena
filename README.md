# 🔥 Athena

> Modular skills framework for AI agents

[![CI](https://github.com/MukundaKatta/athena/actions/workflows/ci.yml/badge.svg)](https://github.com/MukundaKatta/athena/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)]()

## What is Athena?

Athena is a framework for creating, registering, and executing reusable AI agent skills. Define skills as simple Python functions with the `@skill` decorator, register them in a discovery-friendly registry, and let your agents find and invoke them dynamically.

## ✨ Features

- ✅ `@skill` decorator for turning functions into discoverable agent skills
- ✅ Skill registry with fuzzy search and category filtering
- ✅ Input/output schema validation via Pydantic
- ✅ Built-in skills: summarize, extract keywords, analyze sentiment, and more
- ✅ CLI for listing, searching, and running skills
- 🔜 Async skill execution and streaming
- 🔜 Remote skill discovery over HTTP

## 🚀 Quick Start

```bash
pip install -e .
athena list
athena run summarize --input '{"text": "Athena is a skills framework for AI agents."}'
athena info summarize
```

```python
from athena import skill, SkillRegistry

@skill(name="greet", description="Greet a user by name")
def greet(name: str) -> str:
    return f"Hello, {name}!"

registry = SkillRegistry()
registry.register(greet)
result = registry.execute("greet", {"name": "World"})
```

## 🏗️ Architecture

```mermaid
graph TD
    A[@skill decorator] --> B[Skill Object]
    B --> C[SkillRegistry]
    C --> D[Search / Discover]
    C --> E[Execute]
    E --> F[Validate Input]
    F --> G[Run Function]
    G --> H[Validate Output]
    H --> I[Return Result]
```

## 🛠️ Tech Stack

- **Pydantic** — Schema validation for skill inputs/outputs
- **Click + Rich** — CLI interface
- **httpx** — HTTP client for remote skills

## 📖 Inspired By

This project was inspired by [Semantic Kernel](https://github.com/microsoft/semantic-kernel) and [LangChain Tools](https://python.langchain.com/) but takes a different approach with a simpler, decorator-first API.

---

**Built by [Officethree Technologies](https://github.com/MukundaKatta)** | Made with ❤️ and AI
