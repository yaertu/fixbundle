from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path


def _bundle(path: Path, *, commit: str) -> Path:
    files = {
        "manifest.json": json.dumps(
            {
                "schema": "fixbundle/0.3",
                "project": "cli-compare-demo",
                "stacks": [{"stack": "Python"}],
                "commands": [],
                "privacy": {},
            }
        ).encode(),
        "git/head.txt": (commit + "\n").encode(),
        "git/diff.patch": b"",
        "system.json": json.dumps({"python": "3.12", "platform": "test"}).encode(),
        "AI_HANDOFF.md": b"evidence\n",
    }
    lines = [
        f"{hashlib.sha256(files[name]).hexdigest()}  {name}"
        for name in sorted(files)
    ]
    files["SHA256SUMS.txt"] = ("\n".join(lines) + "\n").encode()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in files.items():
            zf.writestr(name, data)
    return path


def test_compare_cli_json_output(tmp_path: Path):
    baseline = _bundle(tmp_path / "baseline.zip", commit="aaa")
    incident = _bundle(tmp_path / "incident.zip", commit="bbb")

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "fixbundle.cli",
            "compare",
            str(baseline),
            str(incident),
            "--format",
            "json",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )

    assert proc.returncode == 0, proc.stdout
    report = json.loads(proc.stdout)
    commit = next(item for item in report["changes"] if item["field"] == "git.commit")
    assert commit == {
        "baseline": "aaa",
        "field": "git.commit",
        "incident": "bbb",
        "status": "changed",
    }


def test_compare_cli_fails_closed_on_invalid_zip(tmp_path: Path):
    good = _bundle(tmp_path / "good.zip", commit="aaa")
    bad = tmp_path / "bad.zip"
    bad.write_text("not a zip", encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, "-m", "fixbundle.cli", "compare", str(good), str(bad)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )

    assert proc.returncode == 1
    assert "fixbundle compare: failed:" in proc.stdout
