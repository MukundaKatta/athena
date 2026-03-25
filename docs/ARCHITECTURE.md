# Athena Architecture

## Overview

Athena uses a decorator-based skill registration system with a central registry for discovery and execution.

## Components

- **`@skill` decorator** — Wraps functions into `Skill` objects with metadata
- **`SkillRegistry`** — Central store for skill discovery, search, and execution
- **Built-in skills** — Pre-packaged NLP and writing skills
- **CLI** — Command-line interface for managing skills

## Data Flow

```
@skill decorator → Skill object → Registry → Search/Execute → Result
```
