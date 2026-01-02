from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML

BUMPVERSION_TOML = Path(".bumpversion.toml")
COVERAGERC_TOML = Path(".coveragerc.toml")
PYPROJECT_TOML = Path("pyproject.toml")
PRE_COMMIT_CONFIG_YAML = Path(".pre-commit-config.yaml")
YAML_INSTANCE = YAML()


__all__ = [
    "BUMPVERSION_TOML",
    "COVERAGERC_TOML",
    "PRE_COMMIT_CONFIG_YAML",
    "PYPROJECT_TOML",
    "YAML_INSTANCE",
]
