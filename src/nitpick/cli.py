from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from click import command
from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from nitpick import __version__
from nitpick.logging import LOGGER
from nitpick.settings import LOADER, Settings

if TYPE_CHECKING:
    from pathlib import Path


_MODIFICATIONS: set[Path] = set()


MODIFICATIONS: set[Path] = set()


@command(**CONTEXT_SETTINGS)
@click_options(Settings, [LOADER], show_envvars_in_help=True)
def _main(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running 'pre-commit-hook-nitpick' (version %s) with settings:
            %s
        """),
        __version__,
        pretty_repr(settings),
    )
    _add_bumpversion_toml(
        pyproject=settings.pyproject,
        python_package_name_use=settings.python_package_name_use,
    )
    _check_versions()
    _run_pre_commit_update()
    _run_ripgrep_and_replace(version=settings.python_version)
    _update_action_file_extensions()
    _update_action_versions()
    _add_pre_commit(
        dockerfmt=settings.pre_commit__dockerfmt,
        prettier=settings.pre_commit__prettier,
        ruff=settings.pre_commit__ruff,
        shell=settings.pre_commit__shell,
        taplo=settings.pre_commit__taplo,
        uv=settings.pre_commit__uv,
        script=settings.script,
    )
    if settings.coverage:
        _add_coveragerc_toml()
    if (
        settings.github__pull_request__pre_commit
        or settings.github__pull_request__pyright
        or settings.github__pull_request__pytest__os__windows
        or settings.github__pull_request__pytest__os__macos
        or settings.github__pull_request__pytest__os__ubuntu
        or settings.github__pull_request__pytest__python_version__default
        or settings.github__pull_request__pytest__python_version__3_12
        or settings.github__pull_request__pytest__python_version__3_13
        or settings.github__pull_request__pytest__python_version__3_14
        or settings.github__pull_request__pytest__resolution__highest
        or settings.github__pull_request__pytest__resolution__lowest_direct
        or settings.github__pull_request__ruff
    ):
        _add_github_pull_request_yaml(
            pre_commit=settings.github__pull_request__pre_commit,
            pyright=settings.github__pull_request__pyright,
            pytest__os__windows=settings.github__pull_request__pytest__os__windows,
            pytest__os__macos=settings.github__pull_request__pytest__os__macos,
            pytest__os__ubuntu=settings.github__pull_request__pytest__os__ubuntu,
            pytest__python_version__default=settings.github__pull_request__pytest__python_version__default,
            pytest__python_version__3_12=settings.github__pull_request__pytest__python_version__3_12,
            pytest__python_version__3_13=settings.github__pull_request__pytest__python_version__3_13,
            pytest__python_version__3_14=settings.github__pull_request__pytest__python_version__3_14,
            pytest__resolution__highest=settings.github__pull_request__pytest__resolution__highest,
            pytest__resolution__lowest_direct=settings.github__pull_request__pytest__resolution__lowest_direct,
            pytest__timeout=settings.pytest__timeout,
            python_version=settings.python_version,
            ruff=settings.ruff,
            script=settings.script,
        )
    if (
        settings.github__push__publish
        or settings.github__push__publish__trusted_publishing
        or settings.github__push__tag
        or settings.github__push__tag__major_minor
        or settings.github__push__tag__major
        or settings.github__push__tag__latest
    ):
        _add_github_push_yaml(
            publish=settings.github__push__publish,
            publish__trusted_publishing=settings.github__push__publish__trusted_publishing,
            tag=settings.github__push__tag,
            tag__major_minor=settings.github__push__tag__major_minor,
            tag__major=settings.github__push__tag__major,
            tag__latest=settings.github__push__tag__latest,
        )
    if (
        settings.pyproject
        or settings.pyproject__project__optional_dependencies__scripts
        or (len(settings.pyproject__tool__uv__indexes) >= 1)
    ):
        _add_pyproject_toml(
            version=settings.python_version,
            description=settings.description,
            package_name=settings.package_name,
            readme=settings.readme,
            optional_dependencies__scripts=settings.pyproject__project__optional_dependencies__scripts,
            python_package_name=settings.python_package_name,
            python_package_name_use=settings.python_package_name_use,
            tool__uv__indexes=settings.pyproject__tool__uv__indexes,
        )
    if settings.pyright:
        _add_pyrightconfig_json(version=settings.python_version, script=settings.script)
    if (
        settings.pytest
        or settings.pytest__asyncio
        or settings.pytest__ignore_warnings
        or (settings.pytest__timeout is not None)
    ):
        _add_pytest_toml(
            asyncio=settings.pytest__asyncio,
            ignore_warnings=settings.pytest__ignore_warnings,
            timeout=settings.pytest__timeout,
            coverage=settings.coverage,
            python_package_name=settings.python_package_name_use,
            script=settings.script,
        )
    if settings.readme:
        _add_readme_md(name=settings.repo_name, description=settings.description)
    if settings.ruff:
        _add_ruff_toml(version=settings.python_version)
    if not settings.skip_version_bump:
        _run_bump_my_version()
    if len(_MODIFICATIONS) >= 1:
        LOGGER.info(
            "Exiting due to modifications: %s",
            ", ".join(map(repr, map(str, sorted(_MODIFICATIONS)))),
        )
        sys.exit(1)


if __name__ == "__main__":
    _main()
