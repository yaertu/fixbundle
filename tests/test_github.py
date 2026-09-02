import json
import zipfile
from pathlib import Path

import pytest

from fixbundle.github import GitHubAPIError, build_github_bundle


class FakeGitHubAPI:
    def __init__(self, *, conclusion: str = "failure"):
        self.conclusion = conclusion
        self.resources_read = ["fixture://run", "fixture://jobs"]

    def run(self, repo: str, run_id: int) -> dict:
        return {
            "id": run_id,
            "run_number": 42,
            "name": "CI",
            "display_title": "break build",
            "event": "push",
            "status": "completed",
            "conclusion": self.conclusion,
            "head_branch": "main",
            "head_sha": "a" * 40,
            "path": ".github/workflows/ci.yml",
            "html_url": f"https://github.com/{repo}/actions/runs/{run_id}",
            "created_at": "2026-09-02T00:00:00Z",
            "updated_at": "2026-09-02T00:01:00Z",
        }

    def jobs(self, repo: str, run_id: int) -> list[dict]:
        return [
            {
                "id": 7001,
                "name": "ubuntu / Python 3.12",
                "status": "completed",
                "conclusion": "failure",
                "runner_name": "GitHub Actions 1",
                "started_at": "2026-09-02T00:00:05Z",
                "completed_at": "2026-09-02T00:00:50Z",
                "html_url": "https://example.invalid/job/7001",
                "steps": [
                    {"number": 1, "name": "Checkout", "status": "completed", "conclusion": "success"},
                    {"number": 2, "name": "Tests", "status": "completed", "conclusion": "failure"},
                ],
            }
        ]

    def job_log(self, repo: str, job_id: int) -> str:
        return "Tests failed\npassword=hunter2\nghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\nAssertionError: 2 != 3\n"

    def commit(self, repo: str, sha: str) -> dict:
        return {
            "sha": sha,
            "html_url": "https://example.invalid/commit",
            "commit": {
                "message": "break build",
                "author": {"date": "2026-09-02T00:00:00Z"},
                "committer": {"date": "2026-09-02T00:00:00Z"},
            },
            "files": [
                {
                    "filename": "src/app.py",
                    "status": "modified",
                    "additions": 1,
                    "deletions": 1,
                    "changes": 2,
                    "patch": "@@ -1 +1 @@\n-return 2\n+return 3",
                }
            ],
        }

    def content(self, repo: str, path: str, ref: str) -> str:
        return "name: CI\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n"


def test_github_failure_bundle_is_portable_redacted_and_exact(tmp_path: Path):
    zip_path, manifest = build_github_bundle(
        "octo/demo",
        123456,
        tmp_path / "out",
        api=FakeGitHubAPI(),
        max_log_chars=50_000,
    )

    assert zip_path.exists()
    assert manifest["schema"] == "fixbundle/0.4"
    assert manifest["capture_mode"] == "github-actions-failure"
    assert manifest["repository"] == "octo/demo"
    assert manifest["run_id"] == 123456
    assert manifest["head_sha"] == "a" * 40
    assert manifest["failed_jobs"] == [7001]
    assert manifest["privacy"]["github_token_serialized"] is False
    assert manifest["privacy"]["remote_capture_requires_local_checkout"] is False
    assert manifest["redactions"] >= 2

    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        assert "AI_HANDOFF.md" in names
        assert "SHA256SUMS.txt" in names
        assert "github/run.json" in names
        assert "github/jobs.json" in names
        assert "github/jobs/7001.log" in names
        assert "github/commit.json" in names
        assert "github/workflow.yml" in names

        log = zf.read("github/jobs/7001.log").decode()
        assert "AssertionError" in log
        assert "hunter2" not in log
        assert "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890" not in log
        assert "<REDACTED>" in log

        run = json.loads(zf.read("github/run.json"))
        assert run["run_id"] == 123456
        assert run["head_sha"] == "a" * 40


def test_github_capture_rejects_non_failed_run(tmp_path: Path):
    with pytest.raises(GitHubAPIError, match="not a completed failure"):
        build_github_bundle("octo/demo", 5, tmp_path / "out", api=FakeGitHubAPI(conclusion="success"))


def test_github_capture_rejects_invalid_repo(tmp_path: Path):
    with pytest.raises(ValueError, match="owner/repo"):
        build_github_bundle("not a repo", 5, tmp_path / "out", api=FakeGitHubAPI())
