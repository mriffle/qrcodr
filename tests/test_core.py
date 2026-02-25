from pathlib import Path

import pytest

from qrcodr.core import (
    DEFAULT_STEM,
    render_qr_pil_image,
    render_qr_svg,
    save_all_formats,
    save_pdf_from_image,
    validate_payload,
)


def test_validate_payload_strips_input() -> None:
    assert validate_payload("  https://example.com  ") == "https://example.com"


def test_validate_payload_rejects_empty() -> None:
    with pytest.raises(ValueError):
        validate_payload("   ")


def test_render_qr_pil_image_returns_rgb_square() -> None:
    image = render_qr_pil_image("https://example.com")
    assert image.mode == "RGB"
    assert image.size[0] == image.size[1]
    assert image.size[0] > 0


def test_render_qr_svg_has_svg_marker() -> None:
    data = render_qr_svg("https://example.com")
    assert b"<svg" in data


def test_save_pdf_from_image_creates_valid_pdf(tmp_path: Path) -> None:
    image = render_qr_pil_image("https://example.com")
    output = tmp_path / "qr.pdf"
    save_pdf_from_image(image, "https://example.com", output)

    assert output.exists()
    header = output.read_bytes()[:4]
    assert header == b"%PDF"


def test_save_all_formats_writes_expected_files(tmp_path: Path) -> None:
    result = save_all_formats("https://example.com", tmp_path)

    assert set(result.keys()) == {"png", "svg", "pdf"}
    for path in result.values():
        assert path.exists()
        assert path.stat().st_size > 0

    assert result["png"].name == f"{DEFAULT_STEM}.png"
