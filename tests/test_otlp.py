from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from fixbundle.otlp import OTLPError, build_otlp_bundle

TRACE_A = "0123456789abcdef0123456789abcdef"
TRACE_B = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
SPAN_A = "0123456789abcdef"


def ns(text: str) -> str:
    dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return str(int(dt.timestamp() * 1_000_000_000))


def attr(key: str, value: str) -> dict:
    return {"key": key, "value": {"stringValue": value}}


def write_jsonl(path: Path, *docs: dict) -> None:
    path.write_text("\n".join(json.dumps(doc) for doc in docs) + "\n", encoding="utf-8")


def log_doc(trace_id: str, *, message: str, at: str, exception: bool = False) -> dict:
    attrs = [attr("http.request.method", "GET")]
    if exception:
        attrs += [
            attr("exception.type", "DatabaseError"),
            attr("exception.message", "database password=hunter2 refused connection"),
            attr("exception.stacktrace", "DatabaseError: refused\n  at app.py:42"),
        ]
    return {
        "resourceLogs": [
            {
                "resource": {
                    "attributes": [
                        attr("service.name", "checkout-api"),
                        attr("service.version", "2026.9.2"),
                        attr("deployment.environment.name", "production"),
                    ]
                },
                "scopeLogs": [
                    {
                        "scope": {"name": "demo.logger"},
                        "logRecords": [
                            {
                                "timeUnixNano": ns(at),
                                "severityText": "ERROR" if exception else "INFO",
                                "traceId": trace_id,
                                "spanId": SPAN_A,
                                "body": {"stringValue": message},
                                "attributes": attrs,
                            }
                        ],
                    }
                ],
            }
        ]
    }


def trace_doc(trace_id: str, *, at: str, with_exception: bool) -> dict:
    events = []
    if with_exception:
        events.append(
            {
                "name": "exception",
                "timeUnixNano": ns(at),
                "attributes": [
                    attr("exception.type", "DatabaseError"),
                    attr("exception.message", "connection refused"),
                    attr("exception.stacktrace", "DatabaseError: refused\n  at db.py:9"),
                ],
            }
        )
    return {
        "resourceSpans": [
            {
                "resource": {"attributes": [attr("service.name", "checkout-api")]},
                "scopeSpans": [
                    {
                        "scope": {"name": "demo.tracer"},
                        "spans": [
                            {
                                "traceId": trace_id,
                                "spanId": SPAN_A,
                                "name": "GET /checkout",
                                "startTimeUnixNano": ns(at),
                                "endTimeUnixNano": str(int(ns(at)) + 10_000_000),
                                "attributes": [attr("server.address", "api.example.test")],
                                "events": events,
                            }
                        ],
                    }
                ],
            }
        ]
    }


def test_otlp_bundle_selects_exact_trace_correlates_exception_and_redacts(tmp_path: Path):
    logs = tmp_path / "logs.jsonl"
    traces = tmp_path / "traces.jsonl"
    write_jsonl(
        logs,
        log_doc(TRACE_A, message="checkout failed token=abc123secretvalue", at="2026-09-02T01:02:00Z", exception=True),
        log_doc(TRACE_B, message="unrelated", at="2026-09-02T01:03:00Z"),
    )
    write_jsonl(
        traces,
        trace_doc(TRACE_A, at="2026-09-02T01:02:00Z", with_exception=True),
        trace_doc(TRACE_B, at="2026-09-02T01:03:00Z", with_exception=False),
    )

    zip_path, manifest = build_otlp_bundle(
        logs_path=logs,
        traces_path=traces,
        output_dir=tmp_path / "out",
        trace_id=TRACE_A,
        since="2026-09-02T01:01:00Z",
        until="2026-09-02T01:02:30Z",
    )

    assert manifest["schema"] == "fixbundle/0.5"
    assert manifest["capture_mode"] == "otlp-file"
    assert manifest["selected"]["trace_ids"] == [TRACE_A]
    assert manifest["selected"]["logs"] == 1
    assert manifest["selected"]["spans"] == 1
    assert manifest["selected"]["exceptions"] == 2
    assert manifest["omitted"] == {"logs": 1, "spans": 1}
    assert manifest["privacy"]["network_required"] is False

    with zipfile.ZipFile(zip_path) as zf:
        names = set(zf.namelist())
        assert {
            "manifest.json",
            "AI_HANDOFF.md",
            "SHA256SUMS.txt",
            "production/incident.json",
            "production/logs.json",
            "production/traces.json",
            "production/exceptions.json",
            "production/services.json",
        } <= names
        logs_text = zf.read("production/logs.json").decode()
        exceptions_text = zf.read("production/exceptions.json").decode()
        assert TRACE_A in logs_text
        assert TRACE_B not in logs_text
        assert "abc123secretvalue" not in logs_text
        assert "hunter2" not in exceptions_text
        assert "<REDACTED>" in logs_text
        assert "<REDACTED>" in exceptions_text

        for line in zf.read("SHA256SUMS.txt").decode().splitlines():
            digest, member = line.split("  ", 1)
            assert hashlib.sha256(zf.read(member)).hexdigest() == digest


def test_otlp_rejects_malformed_jsonl(tmp_path: Path):
    logs = tmp_path / "bad.jsonl"
    logs.write_text('{"resourceLogs": []}\nnot-json\n', encoding="utf-8")
    with pytest.raises(OTLPError, match="malformed OTLP JSONL"):
        build_otlp_bundle(logs_path=logs, traces_path=None, output_dir=tmp_path / "out")


def test_otlp_rejects_invalid_time_range_and_record_overflow(tmp_path: Path):
    logs = tmp_path / "logs.jsonl"
    write_jsonl(logs, log_doc(TRACE_A, message="x", at="2026-09-02T01:02:00Z"))

    with pytest.raises(OTLPError, match="--since"):
        build_otlp_bundle(
            logs_path=logs,
            traces_path=None,
            output_dir=tmp_path / "out-a",
            since="2026-09-02T02:00:00Z",
            until="2026-09-02T01:00:00Z",
        )

    with pytest.raises(OTLPError, match="record count exceeds"):
        build_otlp_bundle(
            logs_path=logs,
            traces_path=None,
            output_dir=tmp_path / "out-b",
            max_records=0,
        )
