from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import cv2
import pytest

TEST_URL = "https://www.google.com/"


def decode_qr_png(path: Path) -> str:
    image = cv2.imread(str(path))
    assert image is not None, f"Failed to read image: {path}"
    detector = cv2.QRCodeDetector()
    decoded, _, _ = detector.detectAndDecode(image)
    return decoded


@pytest.mark.smoke
def test_cli_generate_outputs_decodable_qr(tmp_path: Path) -> None:
    stem = "cli_smoke"
    cmd = [
        sys.executable,
        "-m",
        "qrcodr",
        "generate",
        "--payload",
        TEST_URL,
        "--output-dir",
        str(tmp_path),
        "--stem",
        stem,
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)

    png_path = tmp_path / f"{stem}.png"
    assert png_path.exists()
    assert decode_qr_png(png_path) == TEST_URL
