from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def run(*args: str, cwd: Path, check: bool = True) -> str:
    proc = subprocess.run(
        list(args), cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, encoding="utf-8", errors="replace"
    )
    if check and proc.returncode != 0:
        raise RuntimeError(proc.stdout)
    return proc.stdout.strip()


def main() -> int:
    if shutil.which("git") is None:
        print("demo requires git", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    env = dict(__import__("os").environ)
    env["PYTHONPATH"] = str(repo_root / "src") + (__import__("os").pathsep + env.get("PYTHONPATH", "") if env.get("PYTHONPATH") else "")

    with tempfile.TemporaryDirectory(prefix="fixbundle-demo-") as tmp:
        project = Path(tmp) / "sample-project"
        project.mkdir()
        run("git", "init", cwd=project)
        run("git", "config", "user.email", "demo@example.invalid", cwd=project)
        run("git", "config", "user.name", "FixBundle Demo", cwd=project)

        app = project / "app.py"
        app.write_text("def total(a, b):\n    return a - b  # BUG\n\nassert total(2, 3) == 5\n", encoding="utf-8")
        run("git", "add", "app.py", cwd=project)
        run("git", "commit", "-m", "buggy production state", cwd=project)
        buggy = run("git", "rev-parse", "HEAD", cwd=project)

        app.write_text("def total(a, b):\n    return a + b\n\nassert total(2, 3) == 5\n", encoding="utf-8")
        run("git", "add", "app.py", cwd=project)
        run("git", "commit", "-m", "current main is fixed", cwd=project)
        current = run("git", "rev-parse", "HEAD", cwd=project)
        (project / "notes.txt").write_text("uncommitted work must survive\n", encoding="utf-8")
        before = run("git", "status", "--porcelain=v1", "-uall", cwd=project)

        proc = subprocess.run(
            [sys.executable, "-m", "fixbundle.cli", ".", "--commit", buggy,
             "--run", f'"{sys.executable}" app.py', "--lang", "en"],
            cwd=project, env=env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, encoding="utf-8", errors="replace"
        )
        if proc.returncode != 0:
            print(proc.stdout)
            return proc.returncode

        zips = sorted((project / ".fixbundle").glob("*.zip"))
        if len(zips) != 1:
            raise RuntimeError(f"expected one bundle zip, got {len(zips)}")
        zip_path = zips[0]
        after = "\n".join(
            line for line in run("git", "status", "--porcelain=v1", "-uall", cwd=project).splitlines()
            if ".fixbundle/" not in line
        )

        with zipfile.ZipFile(zip_path) as zf:
            incident = json.loads(zf.read("incident.json"))
            command_log = zf.read("commands/01.log").decode("utf-8", "replace")
            old_source = zf.read("project/app.py").decode("utf-8", "replace")

        checks = {
            "incident_commit_matches": incident["incident_commit"] == buggy,
            "current_head_preserved": run("git", "rev-parse", "HEAD", cwd=project) == current,
            "dirty_workspace_preserved": before == after,
            "old_buggy_source_captured": "return a - b" in old_source,
            "real_failure_captured": "AssertionError" in command_log,
        }

        print("FixBundle historical demo")
        print(f"incident: {buggy[:8]}")
        print(f"current : {current[:8]}")
        for name, ok in checks.items():
            print(f"{'PASS' if ok else 'FAIL'}  {name}")
        print(f"bundle  : {zip_path.name}")
        return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
