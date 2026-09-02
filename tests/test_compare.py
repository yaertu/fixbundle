from __future__ import annotations

import hashlib
import json
import stat
import zipfile
from pathlib import Path

import pytest

from fixbundle.compare import CompareError, compare_bundles, render_json, render_text


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def _bundle(path: Path, files: dict[str, str | bytes]) -> Path:
    payload: dict[str, bytes] = {}
    for name, value in files.items():
        payload[name] = value if isinstance(value, bytes) else value.encode("utf-8")
    checksums = [
        f"{hashlib.sha256(payload[name]).hexdigest()}  {name}"
        for name in sorted(payload)
    ]
    payload["SHA256SUMS.txt"] = ("\n".join(checksums) + "\n").encode("utf-8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, value in payload.items():
            zf.writestr(name, value)
    return path


def _local_bundle(path: Path, *, commit: str, exit_code: int, changed: str) -> Path:
    return _bundle(
        path,
        {
            "manifest.json": _json(
                {
                    "schema": "fixbundle/0.3",
                    "project": "shop-api",
                    "stacks": [{"stack": "Python"}],
                    "commands": [
                        {
                            "command": "pytest -q",
                            "exit_code": exit_code,
                            "duration_ms": 10,
                            "timed_out": False,
                            "output_file": "commands/01.log",
                        }
                    ],
                    "redactions": 0,
                    "privacy": {},
                }
            ),
            "system.json": _json({"python": "3.12.1", "platform": "test-os"}),
            "stack.json": _json([{"stack": "Python"}]),
            "git/head.txt": commit + "\n",
            "git/diff.patch": f"diff --git a/{changed} b/{changed}\n",
            "commands/01.log": "captured output\n",
            "AI_HANDOFF.md": "evidence\n",
        },
    )


def _github_bundle(path: Path, *, sha: str, run_id: int, step: str) -> Path:
    return _bundle(
        path,
        {
            "manifest.json": _json(
                {
                    "schema": "fixbundle/0.4",
                    "capture_mode": "github-actions-failure",
                    "repository": "acme/payments",
                    "workflow": "CI",
                    "run_id": run_id,
                    "head_sha": sha,
                    "failed_jobs": [10],
                    "log_files": ["github/jobs/10.log"],
                    "privacy": {},
                }
            ),
            "github/jobs.json": _json(
                [
                    {
                        "id": 10,
                        "name": "windows / py3.12",
                        "conclusion": "failure",
                        "steps": [
                            {
                                "number": 5,
                                "name": step,
                                "conclusion": "failure",
                            }
                        ],
                    }
                ]
            ),
            "github/commit.json": _json(
                {"sha": sha, "files": [{"filename": "src/payments.py"}]}
            ),
            "github/jobs/10.log": "real failure\n",
            "AI_HANDOFF.md": "evidence\n",
        },
    )


def _otlp_bundle(path: Path) -> Path:
    trace_id = "0123456789abcdef0123456789abcdef"
    return _bundle(
        path,
        {
            "manifest.json": _json(
                {
                    "schema": "fixbundle/0.5",
                    "capture_mode": "otlp-file",
                    "selected": {
                        "logs": 1,
                        "spans": 1,
                        "exceptions": 1,
                        "trace_ids": [trace_id],
                    },
                    "privacy": {"network_required": False},
                }
            ),
            "production/exceptions.json": _json(
                [
                    {
                        "source": "span-event:exception",
                        "trace_id": trace_id,
                        "span_id": "0123456789abcdef",
                        "type": "PaymentGatewayError",
                        "message": "charge rejected",
                        "stacktrace": "omitted from compare normalization",
                    }
                ]
            ),
            "production/services.json": _json(
                [
                    {
                        "service.name": "payments-api",
                        "service.version": "2.4.2",
                        "deployment.environment.name": "production",
                        "deployment.id": "deploy-42",
                    }
                ]
            ),
            "production/traces.json": _json(
                [
                    {
                        "trace_id": trace_id,
                        "span_id": "0123456789abcdef",
                        "name": "POST /charge",
                    }
                ]
            ),
            "production/logs.json": "[]",
            "production/incident.json": _json({"trace_ids": [trace_id]}),
            "AI_HANDOFF.md": "evidence\n",
        },
    )


def _change(report: dict, field: str) -> dict:
    return next(item for item in report["changes"] if item["field"] == field)


def test_compare_local_to_local_is_deterministic(tmp_path: Path):
    baseline = _local_bundle(tmp_path / "baseline.zip", commit="aaa", exit_code=0, changed="a.py")
    incident = _local_bundle(tmp_path / "incident.zip", commit="bbb", exit_code=1, changed="b.py")

    report = compare_bundles(baseline, incident)

    assert _change(report, "git.commit")["status"] == "changed"
    assert _change(report, "git.changed_files")["incident"] == ["b.py"]
    assert _change(report, "failure.commands")["status"] == "changed"
    assert render_json(report) == render_json(compare_bundles(baseline, incident))
    text = render_text(report)
    assert "CHANGED" in text
    assert "git.commit" in text


def test_compare_github_to_github_tracks_failed_step_and_commit(tmp_path: Path):
    baseline = _github_bundle(tmp_path / "baseline.zip", sha="aaa", run_id=41, step="Tests")
    incident = _github_bundle(tmp_path / "incident.zip", sha="bbb", run_id=42, step="Build")

    report = compare_bundles(baseline, incident)

    assert _change(report, "git.commit")["status"] == "changed"
    assert _change(report, "identity.run_id")["status"] == "changed"
    step = _change(report, "failure.failed_steps")
    assert step["status"] == "changed"
    assert step["incident"][0]["name"] == "Build"


def test_compare_github_to_otlp_reports_cross_source_availability(tmp_path: Path):
    baseline = _github_bundle(tmp_path / "ci.zip", sha="aaa", run_id=41, step="Tests")
    incident = _otlp_bundle(tmp_path / "production.zip")

    report = compare_bundles(baseline, incident)

    assert _change(report, "bundle.schema")["status"] == "changed"
    assert _change(report, "identity.repository")["status"] == "removed"
    assert _change(report, "failure.failed_steps")["status"] == "removed"
    assert _change(report, "failure.exceptions")["status"] == "added"
    assert _change(report, "production.services")["status"] == "added"
    assert _change(report, "production.trace_ids")["status"] == "added"


def test_compare_rejects_checksum_tampering(tmp_path: Path):
    good = _github_bundle(tmp_path / "good.zip", sha="aaa", run_id=41, step="Tests")
    tampered = tmp_path / "tampered.zip"
    with zipfile.ZipFile(good) as source, zipfile.ZipFile(tampered, "w") as target:
        for info in source.infolist():
            data = source.read(info.filename)
            if info.filename == "manifest.json":
                data = data.replace(b'"run_id": 41', b'"run_id": 99')
            target.writestr(info, data)

    with pytest.raises(CompareError, match="checksum mismatch: manifest.json"):
        compare_bundles(tampered, good)


def test_compare_rejects_path_traversal_and_duplicate_members(tmp_path: Path):
    good = _otlp_bundle(tmp_path / "good.zip")
    traversal = tmp_path / "traversal.zip"
    with zipfile.ZipFile(traversal, "w") as zf:
        zf.writestr("../outside.txt", "nope")
        zf.writestr("SHA256SUMS.txt", "")
    with pytest.raises(CompareError, match="unsafe ZIP member path"):
        compare_bundles(traversal, good)

    duplicate = tmp_path / "duplicate.zip"
    manifest = _json({"schema": "fixbundle/0.5", "capture_mode": "otlp-file"}).encode()
    digest = hashlib.sha256(manifest).hexdigest()
    with zipfile.ZipFile(duplicate, "w") as zf:
        zf.writestr("manifest.json", manifest)
        zf.writestr("manifest.json", manifest)
        zf.writestr("SHA256SUMS.txt", f"{digest}  manifest.json\n")
    with pytest.raises(CompareError, match="duplicate ZIP member"):
        compare_bundles(duplicate, good)


def test_compare_rejects_symlink_and_unsupported_schema(tmp_path: Path):
    good = _otlp_bundle(tmp_path / "good.zip")
    symlink = tmp_path / "symlink.zip"
    link = zipfile.ZipInfo("manifest.json")
    link.create_system = 3
    link.external_attr = (stat.S_IFLNK | 0o777) << 16
    with zipfile.ZipFile(symlink, "w") as zf:
        zf.writestr(link, "target")
        digest = hashlib.sha256(b"target").hexdigest()
        zf.writestr("SHA256SUMS.txt", f"{digest}  manifest.json\n")
    with pytest.raises(CompareError, match="symlink ZIP member"):
        compare_bundles(symlink, good)

    unsupported = _bundle(
        tmp_path / "unsupported.zip",
        {"manifest.json": _json({"schema": "fixbundle/9.9"})},
    )
    with pytest.raises(CompareError, match="unsupported FixBundle schema"):
        compare_bundles(unsupported, good)
