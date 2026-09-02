from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from .collect import build_bundle


def _git(root: Path, *args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(root),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and proc.returncode != 0:
        raise RuntimeError(proc.stdout.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def build_historical_bundle(
    root: Path,
    commit_ref: str,
    output_dir: Path,
    commands: list[str],
    timeout: int = 180,
    max_files: int = 250,
) -> tuple[Path, dict]:
    root = root.resolve()
    if shutil.which("git") is None or not (root / ".git").exists():
        raise RuntimeError("--commit requires a Git repository and the git executable")

    current_head = _git(root, "rev-parse", "HEAD")
    resolved = _git(root, "rev-parse", f"{commit_ref}^{{commit}}")
    output_dir = output_dir if output_dir.is_absolute() else root / output_dir

    try:
        output_rel = output_dir.resolve().relative_to(root).as_posix().rstrip("/")
    except ValueError:
        output_rel = None

    def workspace_status() -> str:
        raw = _git(root, "status", "--porcelain=v1", "-uall", check=False)
        if not output_rel:
            return raw
        kept: list[str] = []
        for line in raw.splitlines():
            path_text = line[3:] if len(line) > 3 else line
            if path_text == output_rel or path_text.startswith(output_rel + "/"):
                continue
            kept.append(line)
        return "\n".join(kept)

    status_before = workspace_status()

    with tempfile.TemporaryDirectory(prefix="fixbundle-worktree-") as tmp:
        worktree = Path(tmp) / "snapshot"
        added = False
        try:
            _git(root, "worktree", "add", "--detach", str(worktree), resolved)
            added = True
            incident = {
                "capture_mode": "historical-worktree",
                "requested_ref": commit_ref,
                "incident_commit": resolved,
                "current_head": current_head,
                "workspace_status_before": status_before,
            }
            zip_path, manifest = build_bundle(
                root=worktree,
                output_dir=output_dir,
                commands=commands,
                timeout=timeout,
                max_files=max_files,
                project_name=root.name,
                incident=incident,
            )
        finally:
            if added:
                _git(root, "worktree", "remove", "--force", str(worktree), check=False)
                _git(root, "worktree", "prune", check=False)

    status_after = workspace_status()
    if status_after != status_before:
        raise RuntimeError("historical capture changed the current working tree; refusing to continue")
    return zip_path, manifest
