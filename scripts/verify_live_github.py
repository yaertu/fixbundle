from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

EXPECTED_RUN = 33587184675
EXPECTED_REPO = "yaertu/fixbundle"
EXPECTED_LOG_MARKERS = ("UnicodeEncodeError", "cp1252")
EXPECTED_FAILED_STEP = "Historical demo"


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".fixbundle-live")
    zips = sorted(root.glob("*.zip"))
    if len(zips) != 1:
        raise SystemExit(f"expected exactly one FixBundle ZIP in {root}, found {len(zips)}")

    zip_path = zips[0]
    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        required = {
            "manifest.json",
            "AI_HANDOFF.md",
            "SHA256SUMS.txt",
            "github/run.json",
            "github/jobs.json",
            "github/commit.json",
            "github/workflow.yml",
        }
        missing = sorted(required - names)
        if missing:
            raise SystemExit(f"missing evidence members: {missing}")

        manifest = json.loads(zf.read("manifest.json"))
        assert manifest["schema"] == "fixbundle/0.4"
        assert manifest["capture_mode"] == "github-actions-failure"
        assert manifest["repository"] == EXPECTED_REPO
        assert manifest["run_id"] == EXPECTED_RUN
        assert manifest["privacy"]["github_token_serialized"] is False
        assert manifest["privacy"]["remote_capture_requires_local_checkout"] is False
        assert manifest["failed_jobs"], "expected at least one failed job"
        assert manifest["log_files"], "expected failed job logs"

        jobs = json.loads(zf.read("github/jobs.json"))
        failed_steps = {
            step.get("name")
            for job in jobs
            if job.get("conclusion") == "failure"
            for step in job.get("steps", [])
            if step.get("conclusion") == "failure"
        }
        assert EXPECTED_FAILED_STEP in failed_steps, f"missing failed step identity: {EXPECTED_FAILED_STEP}"

        combined_logs = "\n".join(zf.read(name).decode("utf-8", "replace") for name in manifest["log_files"])
        for marker in EXPECTED_LOG_MARKERS:
            assert marker in combined_logs, f"missing real failure marker: {marker}"
        assert "AUTHORIZATION: basic ***" in combined_logs

        checksums = zf.read("SHA256SUMS.txt").decode("utf-8").splitlines()
        checked = 0
        for line in checksums:
            digest, member = line.split("  ", 1)
            actual = hashlib.sha256(zf.read(member)).hexdigest()
            assert actual == digest, f"checksum mismatch: {member}"
            checked += 1
        assert checked >= 6

    print(f"PASS live_run={EXPECTED_RUN}")
    print(f"PASS failed_jobs={len(manifest['failed_jobs'])}")
    print(f"PASS log_files={len(manifest['log_files'])}")
    print(f"PASS failed_step={EXPECTED_FAILED_STEP}")
    print("PASS real_failure=UnicodeEncodeError/cp1252")
    print(f"PASS checksums={checked}")
    print("PASS token_not_serialized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
