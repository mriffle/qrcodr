from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox

import pytest

from qrcodr.app import QRGeneratorApp

from ._utils import TEST_URL, decode_qr_png


@pytest.mark.smoke
def test_gui_generate_and_save_outputs_decodable_qr(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    tkinter = pytest.importorskip("tkinter")
    root = tkinter.Tk()
    root.withdraw()

    app = QRGeneratorApp(root)
    app.url_var.set(TEST_URL)

    monkeypatch.setattr(filedialog, "askdirectory", lambda title=None: str(tmp_path))
    monkeypatch.setattr(messagebox, "showinfo", lambda *args, **kwargs: None)
    monkeypatch.setattr(messagebox, "showwarning", lambda *args, **kwargs: None)

    app.generate()
    app.save_all()

    root.destroy()

    png_path = tmp_path / "qrcode.png"
    assert png_path.exists()
    assert decode_qr_png(png_path) == TEST_URL
