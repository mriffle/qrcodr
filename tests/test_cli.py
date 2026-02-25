from pathlib import Path

from qrcodr.cli import main


def test_cli_generate_writes_all_formats(tmp_path: Path) -> None:
    payload = "https://example.com/cli"
    output_dir = tmp_path / "out"

    code = main([
        "generate",
        "--payload",
        payload,
        "--output-dir",
        str(output_dir),
        "--stem",
        "from_cli",
    ])

    assert code == 0
    assert (output_dir / "from_cli.png").exists()
    assert (output_dir / "from_cli.svg").exists()
    assert (output_dir / "from_cli.pdf").exists()
