# qrcodr

`qrcodr` is a desktop QR code generator that takes a URL (or any text payload) and exports it as:

- PNG
- SVG
- PDF

The app is built with Python + Tkinter. It can run from source or as precompiled binaries for Windows, macOS, and Linux.
It also supports full headless generation from the command line.

## Features

- Simple desktop UI with QR preview
- Export to 3 formats in one click
- Full command-line generation workflow (`generate` subcommand)
- Runs as a standalone binary (double-click to open, no terminal required)
- Test suite with `pytest`
- GitHub Actions for CI tests and release binary builds

## Project layout

- `src/qrcodr/app.py`: GUI application
- `src/qrcodr/cli.py`: CLI entrypoint and subcommands
- `src/qrcodr/core.py`: QR generation and export logic
- `tests/test_core.py`: pytest tests for core behavior
- `tests/test_cli.py`: pytest tests for command-line generation behavior
- `.github/workflows/ci.yml`: test workflow on push/release
- `.github/workflows/release-binaries.yml`: cross-platform binary build + release upload

## Run from source

### 1. Create and activate a local virtual environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

### 3. Launch the GUI app

Any of these are supported:

```bash
python -m qrcodr
```

```bash
qrcodr
```

```bash
python qrcodr.py
```

### 4. Run from command line (no GUI)

Generate all output formats directly:

```bash
python -m qrcodr generate --payload "https://example.com" --output-dir ./output --stem my_qr
```

Equivalent via script wrapper:

```bash
python qrcodr.py generate --payload "https://example.com" --output-dir ./output --stem my_qr
```

Show version:

```bash
python -m qrcodr --version
```

If no subcommand is provided, `qrcodr` opens the GUI.

## Run tests (pytest)

With the virtual environment activated:

```bash
pytest
```

or explicitly via the venv interpreter:

```bash
.venv/bin/python -m pytest
```

(Windows: `.venv\Scripts\python.exe -m pytest`)

## Use precompiled binaries

1. Go to the project Releases page on GitHub.
2. Download the archive for your platform:
   - `qrcodr-vX.Y.Z-windows.zip`
   - `qrcodr-vX.Y.Z-macos.zip`
   - `qrcodr-vX.Y.Z-linux.zip`
3. Extract the archive.
4. Double-click the `qrcodr` executable (`qrcodr.exe` on Windows).

The desktop app opens directly, so users do not need to use the command line.
The app window title shows the release version, and `--version` reports it in command-line mode.

## CI/CD behavior

- On every push and release, GitHub Actions runs the test suite.
- On every published or prereleased GitHub release, GitHub Actions builds one-file binaries for Windows/macOS/Linux and uploads them using the release tag in the filename.
