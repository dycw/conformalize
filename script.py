#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "click",
#   "dycw-utilities",
#   "pytest-xdist",
#   "tomlkit",
#   "typed-settings[attrs, click]",
# ]
# ///
from __future__ import annotations

from logging import getLogger
from pathlib import Path

from click import command
from tomlkit import dumps, parse
from tomlkit.container import Container
from typed_settings import click_options, settings
from utilities.click import CONTEXT_SETTINGS_HELP_OPTION_NAMES
from utilities.logging import basic_config

_LOGGER = getLogger(__name__)


@settings()
class Settings:
    pyproject_build_system: bool = False
    dry_run: bool = False


@command(**CONTEXT_SETTINGS_HELP_OPTION_NAMES)
@click_options(Settings, "app", show_envvars_in_help=True)
def main(settings: Settings, /) -> None:
    if settings.dry_run:
        _LOGGER.info("Dry run; exiting...")
        return
    _LOGGER.info("Running...")
    if settings.pyproject_build_system:
        _add_pyproject_build_system()


def _add_pyproject_build_system() -> None:
    _add_pyproject()
    path = Path("pyproject.toml")
    existing = parse(path.read_text())
    new = existing.copy()
    new.setdefault("build-system", {})
    if not isinstance(build_system := new["build-system"], Container):
        raise TypeError(build_system)
    build_system["build-backend"] = "uv_build"
    build_system["requires"] = ["uv_build"]
    if new != existing:
        _LOGGER.info("Adding `pyproject.toml` [build-system]...")
        _ = path.write_text(dumps(new))


def _add_pyproject() -> None:
    if not (path := Path("pyproject.toml")).is_file():
        _LOGGER.info("Adding `pyproject.toml`...")
        path.touch()


if __name__ == "__main__":
    basic_config(obj=__name__)
    main()
