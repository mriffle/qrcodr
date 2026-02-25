"""Command-line entrypoint for qrcodr."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .app import main as run_gui
from .core import DEFAULT_STEM, save_all_formats
from .version import get_version


def build_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="qrcodr",
        description="Generate QR codes with a GUI or from the command line.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"qrcodr {get_version()}",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("gui", help="Launch the desktop GUI.")

    generate = subparsers.add_parser(
        "generate",
        help="Generate QR assets (PNG, SVG, PDF) from the command line.",
    )
    generate.add_argument(
        "-p",
        "--payload",
        required=True,
        help="Text payload to encode in the QR code (URL or any string).",
    )
    generate.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Directory where files will be written (default: current directory).",
    )
    generate.add_argument(
        "--stem",
        default=DEFAULT_STEM,
        help=f"Base filename for outputs (default: {DEFAULT_STEM}).",
    )
    return parser


def run_generate(payload: str, output_dir: str, stem: str) -> int:
    """Run headless QR generation and print output paths."""
    outputs = save_all_formats(payload, Path(output_dir), stem=stem)
    print(f"qrcodr {get_version()} generated:")
    print(outputs["png"])
    print(outputs["svg"])
    print(outputs["pdf"])
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """CLI main. Defaults to launching GUI when no subcommand is provided."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in (None, "gui"):
        run_gui()
        return 0

    if args.command == "generate":
        return run_generate(args.payload, args.output_dir, args.stem)

    parser.error(f"Unknown command: {args.command}")
    return 2
