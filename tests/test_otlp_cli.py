from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

TRACE_ID = "4bf92f3577b34da6a3ce929d0e0e4736"
SPAN_ID = "00f067aa0ba902b7"


def ns(text: str) -> str:
    return str(int(datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp() * 1_000_000_000))


def attr(key: str, value: str) -> dict:
    return {"key": key, "value": {"stringValue": value}}


def test_otlp_cli_creates_portable_bundle(tmp_path: Path):
    logs = tmp_path / "logs.jsonl"
    output = tmp_path / "out"
    payload = {
        "resourceLogs": [
            {
                "resource": {"attributes": [attr("service.name", "cli-demo")]},
                "scopeLogs": [
                    {
                        "logRecords": [
                            {
                                "timeUnixNano": ns("2026-09-02T01:00:00Z"),
                                "traceId": TRACE_ID,
                                "spanId": SPAN_ID,
                                "severityText": "ERROR",
                                "body": {"stringValue": "cli failure"},
                                "attributes": [attr("exception.type", "CliDemoError")],
                            }
                        ]
                    }
                ],
            }
        ]
    }
    logs.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "fixbundle.cli",
            "otlp",
            "--logs",
            str(logs),
            "--trace-id",
            TRACE_ID,
            "--output",
            str(output),
            "--lang",
            "tr",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )

    assert proc.returncode == 0, proc.stdout
    assert "FixBundle production kanıt paketi hazır [OK]" in proc.stdout
    assert "Log: 1" in proc.stdout
    assert "Exception: 1" in proc.stdout
    assert len(list(output.glob("*.zip"))) == 1
