import json
import subprocess
import zipfile
from pathlib import Path

from fixbundle.history import build_historical_bundle


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def test_historical_capture_uses_old_commit_without_touching_dirty_workspace(tmp_path: Path):
    project = tmp_path / "demo-history"
    project.mkdir()
    subprocess.check_call(["git", "init"], cwd=project, stdout=subprocess.DEVNULL)
    subprocess.check_call(["git", "config", "user.email", "fixbundle@example.invalid"], cwd=project)
    subprocess.check_call(["git", "config", "user.name", "FixBundle Test"], cwd=project)

    app = project / "app.py"
    app.write_text("def total(a, b):\n    return a - b  # BUG\n\nassert total(2, 3) == 5\n", encoding="utf-8")
    subprocess.check_call(["git", "add", "app.py"], cwd=project)
    subprocess.check_call(["git", "commit", "-m", "buggy"], cwd=project, stdout=subprocess.DEVNULL)
    buggy = git(project, "rev-parse", "HEAD")

    app.write_text("def total(a, b):\n    return a + b\n\nassert total(2, 3) == 5\n", encoding="utf-8")
    subprocess.check_call(["git", "add", "app.py"], cwd=project)
    subprocess.check_call(["git", "commit", "-m", "fixed"], cwd=project, stdout=subprocess.DEVNULL)

    (project / "notes.txt").write_text("uncommitted user work\n", encoding="utf-8")
    before = git(project, "status", "--porcelain=v1", "-uall")
    current = git(project, "rev-parse", "HEAD")

    zip_path, manifest = build_historical_bundle(
        project, buggy, project / ".fixbundle", ["python app.py"], timeout=10
    )

    after_lines = [line for line in git(project, "status", "--porcelain=v1", "-uall").splitlines() if ".fixbundle/" not in line]
    assert before.splitlines() == after_lines
    assert git(project, "rev-parse", "HEAD") == current
    assert manifest["incident"]["incident_commit"] == buggy
    assert manifest["incident"]["current_head"] == current
    assert manifest["schema"] == "fixbundle/0.3"

    with zipfile.ZipFile(zip_path) as zf:
        old_source = zf.read("project/app.py").decode()
        command_log = zf.read("commands/01.log").decode()
        incident = json.loads(zf.read("incident.json"))
        assert "return a - b" in old_source
        assert "AssertionError" in command_log
        assert incident["capture_mode"] == "historical-worktree"
