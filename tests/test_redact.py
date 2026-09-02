from pathlib import Path

from fixbundle.redact import redact_text


def test_redacts_common_secrets_and_paths(tmp_path: Path):
    root = tmp_path / "project"
    root.mkdir()
    text = (
        "API_KEY=super-secret-value\n"
        "Authorization: Bearer abc.def.ghi\n"
        "sk-abcdefghijklmnopqrstuvwx\n"
        f"failure at {root / 'src' / 'app.py'}\n"
        "https://user:password@example.com/repo.git\n"
    )
    out, hits = redact_text(text, project_root=root, home=Path.home())
    assert "super-secret-value" not in out
    assert "abc.def.ghi" not in out
    assert "sk-abcdefghijklmnopqrstuvwx" not in out
    assert str(root) not in out
    assert "password@example.com" not in out
    assert "<PROJECT>" in out
    assert hits >= 5
