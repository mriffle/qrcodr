# qrcodr

**Generate QR codes and export them as PNG, SVG, or PDF — in seconds.**

qrcodr is a simple desktop app for creating QR codes. Type in a URL (or any text), preview the QR code, and export it in the format you need. No accounts, no internet connection required, no command line necessary — just download, open, and go.

## Getting started

The easiest way to use qrcodr is to download the precompiled binary for your operating system from the [latest release page](https://github.com/mriffle/qrcodr/releases/latest).

| Platform | File to download |
|----------|-----------------|
| Windows  | `qrcodr-vX.Y.Z-windows.exe` |
| macOS    | `qrcodr-vX.Y.Z-macos` |
| Linux    | `qrcodr-vX.Y.Z-linux` |

Replace `vX.Y.Z` with the version number shown on the release page.

On Windows, just double-click the `.exe` to open. On macOS and Linux, you may need to mark the file as executable first (see below).

### Verifying your download

Each binary on the release page has a matching `.sha256` checksum file. You can use this to verify that the file you downloaded is identical to the one published on GitHub — this guards against corrupted downloads or tampered files.

**Linux / macOS:**

```bash
# Download the binary and its checksum file
curl -LO https://github.com/mriffle/qrcodr/releases/download/vX.Y.Z/qrcodr-vX.Y.Z-linux
curl -LO https://github.com/mriffle/qrcodr/releases/download/vX.Y.Z/qrcodr-vX.Y.Z-linux.sha256

# Verify the checksum — you should see "OK" if the file matches
sha256sum -c qrcodr-vX.Y.Z-linux.sha256

# Make it executable and run
chmod +x qrcodr-vX.Y.Z-linux
./qrcodr-vX.Y.Z-linux
```

**Windows (PowerShell):**

```powershell
# Download the binary and its checksum file
Invoke-WebRequest https://github.com/mriffle/qrcodr/releases/download/vX.Y.Z/qrcodr-vX.Y.Z-windows.exe -OutFile qrcodr-vX.Y.Z-windows.exe
Invoke-WebRequest https://github.com/mriffle/qrcodr/releases/download/vX.Y.Z/qrcodr-vX.Y.Z-windows.exe.sha256 -OutFile qrcodr-vX.Y.Z-windows.exe.sha256

# Verify the checksum — compare the output hash to the contents of the .sha256 file
Get-FileHash .\qrcodr-vX.Y.Z-windows.exe -Algorithm SHA256

# If the hashes match, you're good — double-click the .exe or run it from PowerShell
.\qrcodr-vX.Y.Z-windows.exe
```

On Windows, compare the hash printed by `Get-FileHash` to the value inside the `.sha256` file (open it in a text editor). If they match, your download is verified.

---

## Features

- **Desktop GUI** — a clean window with a live QR code preview and one-click export to PNG, SVG, and PDF
- **Command-line mode** — generate QR codes without opening the GUI (great for scripting and automation)
- **Docker CLI image** — run headless QR generation via `ghcr.io` without local Python setup
- **Cross-platform** — precompiled binaries for Windows, macOS, and Linux
- **No install required** — download a single file and run it

---

## Docker (CLI)

For command-line automation, you can run qrcodr from the GHCR package image:

- `ghcr.io/mriffle/qrcodr:latest` (latest published release)
- `ghcr.io/mriffle/qrcodr:vX.Y.Z` (exact release tag)
- `ghcr.io/mriffle/qrcodr:X.Y.Z`, `X.Y`, `X` (semantic aliases from releases)
- `ghcr.io/mriffle/qrcodr:sha-<commit>` (immutable commit build)

The image entrypoint is `qrcodr generate`, so you pass generate arguments directly:

```bash
docker run --rm -v "$PWD/output:/output" ghcr.io/mriffle/qrcodr:latest \
  --payload "https://www.google.com/" \
  --output-dir /output \
  --stem google_qr
```

Use a specific release:

```bash
docker run --rm -v "$PWD/output:/output" ghcr.io/mriffle/qrcodr:v1.2.9 \
  --payload "https://www.google.com/" \
  --output-dir /output \
  --stem google_qr
```

---

## Running from source

If you'd prefer to run from source (for development or because a binary isn't available for your platform), follow these steps.

### 1. Create and activate a virtual environment

**Linux / macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

### 3. Launch the app

Any of these will open the GUI:

```bash
python -m qrcodr
qrcodr
python run_qrcodr.py
```

### 4. Command-line generation (no GUI)

You can generate QR codes directly from the terminal:

```bash
python -m qrcodr generate --payload "https://example.com" --output-dir ./output --stem my_qr
```

This creates `my_qr.png`, `my_qr.svg`, and `my_qr.pdf` in the `./output` directory.

To check the version:

```bash
python -m qrcodr --version
```

If you run `qrcodr` without a subcommand, it opens the GUI.

---

## Running tests

With the virtual environment activated:

```bash
pytest                       # run all tests
pytest -m smoke              # run only smoke tests (end-to-end CLI + GUI, QR decode verification)
pytest -m "not smoke"        # run everything except smoke tests
```

---

## Project layout

| Path | Description |
|------|-------------|
| `src/qrcodr/app.py` | GUI application |
| `src/qrcodr/cli.py` | CLI entrypoint and subcommands |
| `src/qrcodr/core.py` | QR generation and export logic |
| `tests/test_core.py` | Tests for core behavior |
| `tests/test_cli.py` | Tests for command-line generation |
| `Dockerfile` | CLI-focused runtime image definition |
| `.github/workflows/ci.yml` | CI test workflow |
| `.github/workflows/release-binaries.yml` | Cross-platform binary build + release upload |
| `.github/workflows/docker-image.yml` | Build/push Docker package to GHCR |

## CI/CD

On every push and release, GitHub Actions runs the test suite. On every published release, it builds standalone binaries for Windows, macOS, and Linux, uploads them to the release page, generates a `.sha256` checksum file for each binary, and publishes a Docker image to `ghcr.io`.
