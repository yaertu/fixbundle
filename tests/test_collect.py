import json
import zipfile
from pathlib import Path

from fixbundle.collect import build_bundle


def test_build_bundle_excludes_env_and_creates_handoff(tmp_path: Path):
    project = tmp_path / "demo"
    project.mkdir()
    (project / "app.py").write_text("print('hello')\n", encoding="utf-8")
    (project / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (project / ".env").write_text("API_KEY=never-copy-me\n", encoding="utf-8")
    (project / "error.log").write_text("password=hunter2\n", encoding="utf-8")

    zip_path, manifest = build_bundle(project, tmp_path / "out", ["python app.py"], timeout=10)
    assert zip_path.exists()
    assert manifest["redactions"] >= 1
    assert manifest["schema"] == "fixbundle/0.2"
    assert manifest["stacks"][0]["stack"] == "python"
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        assert "AI_HANDOFF.md" in names
        assert "manifest.json" in names
        assert "stack.json" in names
        assert "git/head.txt" in names
        assert "project/app.py" in names
        assert "project/.env" not in names
        content = zf.read("project/error.log").decode()
        assert "hunter2" not in content
        data = json.loads(zf.read("manifest.json"))
        assert data["schema"] == "fixbundle/0.2"
