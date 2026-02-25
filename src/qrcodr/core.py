"""Core QR generation and export helpers."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import qrcode
import qrcode.image.svg
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

DEFAULT_STEM = "qrcode"


def validate_payload(payload: str) -> str:
    """Return a normalized QR payload or raise ValueError."""
    value = payload.strip()
    if not value:
        raise ValueError("Payload cannot be empty.")
    return value


def render_qr_pil_image(
    payload: str,
    *,
    box_size: int = 10,
    border: int = 4,
) -> Image.Image:
    """Render a QR code as a PIL image."""
    value = validate_payload(payload)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(value)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")


def render_qr_svg(payload: str, *, box_size: int = 10, border: int = 4) -> bytes:
    """Render a QR code as SVG bytes."""
    value = validate_payload(payload)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(value)
    qr.make(fit=True)
    svg_image = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    buffer = BytesIO()
    svg_image.save(buffer)
    return buffer.getvalue()


def save_pdf_from_image(image: Image.Image, payload: str, output_path: Path) -> None:
    """Save a single-page PDF containing the QR code image and payload text."""
    value = validate_payload(payload)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    page_w, page_h = letter
    pdf = canvas.Canvas(str(destination), pagesize=letter)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawCentredString(page_w / 2, page_h - 60, "QR Code")

    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(page_w / 2, page_h - 80, value[:100])

    qr_size = 4 * inch
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    x_pos = (page_w - qr_size) / 2
    y_pos = (page_h - qr_size) / 2 - 20
    pdf.drawImage(ImageReader(buffer), x_pos, y_pos, width=qr_size, height=qr_size)
    pdf.save()


def save_all_formats(payload: str, folder: Path, *, stem: str = DEFAULT_STEM) -> dict[str, Path]:
    """Save PNG, SVG, and PDF QR assets and return their output paths."""
    value = validate_payload(payload)
    output_dir = Path(folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    image = render_qr_pil_image(value)
    png_path = output_dir / f"{stem}.png"
    svg_path = output_dir / f"{stem}.svg"
    pdf_path = output_dir / f"{stem}.pdf"

    image.save(png_path)
    svg_path.write_bytes(render_qr_svg(value))
    save_pdf_from_image(image, value, pdf_path)

    return {"png": png_path, "svg": svg_path, "pdf": pdf_path}
