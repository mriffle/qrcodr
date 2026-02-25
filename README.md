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
python run_qrcodr.py
```

### 4. Run from command line (no GUI)

Generate all output formats directly:

```bash
python -m qrcodr generate --payload "https://example.com" --output-dir ./output --stem my_qr
```

Equivalent via script wrapper:

```bash
python run_qrcodr.py generate --payload "https://example.com" --output-dir ./output --stem my_qr
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

Run only smoke tests (CLI + GUI end-to-end, QR decode verification):

```bash
pytest -m smoke
```

Run all non-smoke tests:

```bash
pytest -m "not smoke"
```

## Use precompiled binaries

1. Go to the project Releases page on GitHub.
2. Download your platform binary and checksum file:
   - Windows: `qrcodr-vX.Y.Z-windows.exe` and `qrcodr-vX.Y.Z-windows.exe.sha256`
   - macOS: `qrcodr-vX.Y.Z-macos` and `qrcodr-vX.Y.Z-macos.sha256`
   - Linux: `qrcodr-vX.Y.Z-linux` and `qrcodr-vX.Y.Z-linux.sha256`
3. (Recommended) verify checksum:
   - Linux/macOS: `sha256sum -c qrcodr-vX.Y.Z-linux.sha256` (or the matching macOS file)
   - Windows PowerShell: `Get-FileHash .\qrcodr-vX.Y.Z-windows.exe -Algorithm SHA256`
4. Run the binary directly (double-click on Windows/macOS desktop environments, or execute in terminal on Linux/macOS if needed).

The desktop app opens directly, so users do not need to use the command line.
The app window title shows the release version, and `--version` reports it in command-line mode.

## CI/CD behavior

- On every push and release, GitHub Actions runs the test suite.
- On every published GitHub release, GitHub Actions builds one-file binaries for Windows/macOS/Linux, uploads the binaries directly (no ZIP), and uploads a `.sha256` file for each binary.
