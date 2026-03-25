"""Configuration management for Athena."""

from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field


class AthenaConfig(BaseSettings):
    """Athena application configuration."""

    model_config = {"env_prefix": "ATHENA_", "env_file": ".env"}

    default_model: str = Field(default="gpt-4", alias="DEFAULT_MODEL")
    skill_registry_path: Path = Field(default=Path("./skills"), alias="SKILL_REGISTRY_PATH")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")


def load_config() -> AthenaConfig:
    """Load configuration from environment."""
    return AthenaConfig()
