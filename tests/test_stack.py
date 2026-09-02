from pathlib import Path

from fixbundle.stack import detect_stacks


def test_detects_node_and_python(tmp_path: Path):
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    stacks = {item.stack for item in detect_stacks(tmp_path)}
    assert stacks == {"node", "python"}
