from __future__ import annotations

from pathlib import Path

import cv2

TEST_URL = "https://www.google.com/"


def decode_qr_png(path: Path) -> str:
    image = cv2.imread(str(path))
    assert image is not None, f"Failed to read image: {path}"
    detector = cv2.QRCodeDetector()
    decoded, _, _ = detector.detectAndDecode(image)
    return decoded
