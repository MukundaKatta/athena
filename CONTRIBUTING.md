# Contributing to Athena

## Setup

```bash
git clone https://github.com/MukundaKatta/athena.git
cd athena && pip install -e ".[dev]"
```

## Development

```bash
make lint && make test
```

## Adding a New Skill

```python
from athena import skill

@skill(name="my_skill", description="What it does", category="custom")
def my_skill(input: str) -> str:
    return f"Processed: {input}"
```

## Pull Requests

1. Fork → branch → code → test → PR
