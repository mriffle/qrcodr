"""Version helpers."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from ._build_version import BUILD_VERSION


def get_version() -> str:
    """Return build-injected, installed package, or local development version."""
    if BUILD_VERSION:
        return BUILD_VERSION

    try:
        return version("qrcodr")
    except PackageNotFoundError:
        return "0.0.0+local"
