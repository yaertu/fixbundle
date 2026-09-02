import os
import subprocess
import sys
from pathlib import Path


def test_turkish_cli_survives_legacy_stdout_encoding(tmp_path: Path):
    project = tmp_path / "demo"
    project.mkdir()
    (project / "app.py").write_text("print('ok')\n", encoding="utf-8")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "cp1252:strict"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "fixbundle.cli",
            str(project),
            "--lang",
            "tr",
            "--output",
            str(tmp_path / "out"),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=30,
    )

    assert proc.returncode == 0, proc.stdout
    assert "FixBundle hazır [OK]" in proc.stdout
