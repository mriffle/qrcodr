"""Tkinter GUI application for qrcodr."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk

from .core import save_all_formats, validate_payload, render_qr_pil_image
from .version import get_version

WINDOW_TITLE = "QR Code Generator"
WINDOW_GEOMETRY = "520x620"
PREVIEW_SIZE = 400
STATUS_LIMIT = 60


class QRGeneratorApp:
    """Main desktop UI for generating and exporting QR codes."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(f"{WINDOW_TITLE} {get_version()}")
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.resizable(False, False)

        self.qr_image: Image.Image | None = None
        self.photo_image: ImageTk.PhotoImage | None = None

        self.url_var = tk.StringVar(value="https://")
        self.status_var = tk.StringVar(value=f"{get_version()} - Enter a URL and click Generate.")
        self.canvas: tk.Canvas | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        input_frame = ttk.LabelFrame(self.root, text="Enter URL", padding=12)
        input_frame.pack(fill="x", padx=16, pady=(16, 8))

        entry = ttk.Entry(input_frame, textvariable=self.url_var, font=("Arial", 13))
        entry.pack(fill="x", pady=(0, 8))
        entry.bind("<Return>", lambda _: self.generate())

        buttons = ttk.Frame(input_frame)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Generate QR Code", command=self.generate).pack(
            side="left", expand=True, fill="x", padx=(0, 4)
        )
        ttk.Button(buttons, text="Save All Formats", command=self.save_all).pack(
            side="left", expand=True, fill="x", padx=(4, 0)
        )

        preview_frame = ttk.LabelFrame(self.root, text="Preview", padding=8)
        preview_frame.pack(fill="both", expand=True, padx=16, pady=(8, 8))
        self.canvas = tk.Canvas(preview_frame, width=PREVIEW_SIZE, height=PREVIEW_SIZE, bg="white")
        self.canvas.pack(expand=True)

        ttk.Label(self.root, textvariable=self.status_var, foreground="gray").pack(pady=(0, 12))

    def generate(self) -> None:
        raw_url = self.url_var.get()
        try:
            url = validate_payload(raw_url)
        except ValueError:
            messagebox.showwarning("Input needed", "Please enter a URL.")
            return

        self.qr_image = render_qr_pil_image(url)

        preview = self.qr_image.copy().resize((PREVIEW_SIZE, PREVIEW_SIZE), Image.NEAREST)
        self.photo_image = ImageTk.PhotoImage(preview)
        assert self.canvas is not None
        self.canvas.delete("all")
        self.canvas.create_image(PREVIEW_SIZE // 2, PREVIEW_SIZE // 2, image=self.photo_image)

        suffix = "..." if len(url) > STATUS_LIMIT else ""
        self.status_var.set(f"QR code generated for: {url[:STATUS_LIMIT]}{suffix}")

    def save_all(self) -> None:
        if self.qr_image is None:
            messagebox.showinfo("Nothing to save", "Generate a QR code first.")
            return

        folder = filedialog.askdirectory(title="Choose save folder")
        if not folder:
            return

        url = self.url_var.get()
        try:
            outputs = save_all_formats(url, Path(folder))
        except ValueError as exc:
            messagebox.showwarning("Input needed", str(exc))
            return

        self.status_var.set(f"Saved PNG, SVG, and PDF to {folder}")
        messagebox.showinfo(
            "Saved",
            "Files saved to:\n\n"
            f"• {outputs['png']}\n"
            f"• {outputs['svg']}\n"
            f"• {outputs['pdf']}",
        )


def main() -> None:
    """Start the qrcodr desktop app."""
    root = tk.Tk()
    QRGeneratorApp(root)
    root.mainloop()
