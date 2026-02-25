# qrcodr

`qrcodr` is a desktop QR code generator that takes a URL (or any text payload) and exports it as:

- PNG
- SVG
- PDF

The app is built with Python + Tkinter. The primary way to run it is via precompiled release binaries for Windows, macOS, and Linux.
It can also run from source and supports full headless generation from the command line.

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

## Run from release binaries (recommended)

Get binaries from the latest release:

- Latest release page: `https://github.com/mriffle/qrcodr/releases/latest`
- Asset pattern:
  - Windows: `qrcodr-vX.Y.Z-windows.exe`
  - macOS: `qrcodr-vX.Y.Z-macos`
  - Linux: `qrcodr-vX.Y.Z-linux`
- Note: Each binary also has a matching checksum file: `.sha256`. This can be used to verify the file you downloaded is precisely the same as the file on GitHub.

### Download examples (latest release)

Linux/macOS (replace `vX.Y.Z` with the version shown in the latest release):

```bash
curl -LO https://github.com/mriffle/qrcodr/releases/download/vX.Y.Z/qrcodr-vX.Y.Z-linux
curl -LO https://github.com/mriffle/qrcodr/releases/download/vX.Y.Z/qrcodr-vX.Y.Z-linux.sha256
sha256sum -c qrcodr-vX.Y.Z-linux.sha256
chmod +x qrcodr-vX.Y.Z-linux
./qrcodr-vX.Y.Z-linux
```

Windows PowerShell:

```powershell
Invoke-WebRequest https://github.com/mriffle/qrcodr/releases/download/vX.Y.Z/qrcodr-vX.Y.Z-windows.exe -OutFile qrcodr-vX.Y.Z-windows.exe
Invoke-WebRequest https://github.com/mriffle/qrcodr/releases/download/vX.Y.Z/qrcodr-vX.Y.Z-windows.exe.sha256 -OutFile qrcodr-vX.Y.Z-windows.exe.sha256
Get-FileHash .\qrcodr-vX.Y.Z-windows.exe -Algorithm SHA256
.\qrcodr-vX.Y.Z-windows.exe
```

Double-click is supported on Windows and common desktop environments.

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

The desktop app opens directly, so users do not need to use the command line.
The app window title shows the release version, and `--version` reports it in command-line mode.

## CI/CD behavior

- On every push and release, GitHub Actions runs the test suite.
- On every published GitHub release, GitHub Actions builds one-file binaries for Windows/macOS/Linux, uploads the binaries directly (no ZIP), and uploads a `.sha256` file for each binary.
