from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

import pytest

from ._utils import TEST_URL, decode_qr_png


@pytest.mark.smoke
def test_docker_cli_generates_decodable_qr(tmp_path: Path) -> None:
    if shutil.which("docker") is None:
        pytest.skip("docker is not available in PATH")

    if sys.platform.startswith("win"):
        pytest.skip("docker smoke test uses a Linux-style bind mount path")

    image_tag = f"qrcodr-smoke:{uuid4().hex[:12]}"
    stem = "docker_smoke"

    build_cmd = ["docker", "build", "-t", image_tag, "."]
    run_cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{tmp_path}:/output",
        image_tag,
        "--payload",
        TEST_URL,
        "--output-dir",
        "/output",
        "--stem",
        stem,
    ]

    try:
        subprocess.run(build_cmd, check=True)
        subprocess.run(run_cmd, check=True)
    finally:
        subprocess.run(["docker", "image", "rm", "-f", image_tag], check=False)

    png_path = tmp_path / f"{stem}.png"
    assert png_path.exists()
    assert decode_qr_png(png_path) == TEST_URL
