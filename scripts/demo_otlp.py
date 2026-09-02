from __future__ import annotations

import hashlib
import json
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

from fixbundle.otlp import build_otlp_bundle

TRACE_ID = "4bf92f3577b34da6a3ce929d0e0e4736"
SPAN_ID = "00f067aa0ba902b7"


def ns(text: str) -> str:
    dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return str(int(dt.timestamp() * 1_000_000_000))


def attr(key: str, value: str) -> dict:
    return {"key": key, "value": {"stringValue": value}}


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="fixbundle-otlp-demo-") as tmp:
        root = Path(tmp)
        logs = root / "otel-logs.jsonl"
        traces = root / "otel-traces.jsonl"

        log_payload = {
            "resourceLogs": [
                {
                    "resource": {
                        "attributes": [
                            attr("service.name", "payments-api"),
                            attr("service.version", "2026.9.2"),
                            attr("deployment.environment.name", "production"),
                        ]
                    },
                    "scopeLogs": [
                        {
                            "scope": {"name": "payments.logger"},
                            "logRecords": [
                                {
                                    "timeUnixNano": ns("2026-09-02T01:02:03Z"),
                                    "severityText": "ERROR",
                                    "traceId": TRACE_ID,
                                    "spanId": SPAN_ID,
                                    "body": {"stringValue": "charge failed api_key=demo-secret-should-disappear"},
                                    "attributes": [
                                        attr("exception.type", "PaymentGatewayError"),
                                        attr("exception.message", "gateway timeout"),
                                        attr("exception.stacktrace", "PaymentGatewayError: timeout\n  at charge.py:42"),
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ]
        }
        trace_payload = {
            "resourceSpans": [
                {
                    "resource": {"attributes": [attr("service.name", "payments-api")]},
                    "scopeSpans": [
                        {
                            "scope": {"name": "payments.tracer"},
                            "spans": [
                                {
                                    "traceId": TRACE_ID,
                                    "spanId": SPAN_ID,
                                    "name": "POST /charge",
                                    "startTimeUnixNano": ns("2026-09-02T01:02:02Z"),
                                    "endTimeUnixNano": ns("2026-09-02T01:02:04Z"),
                                    "status": {"code": 2, "message": "gateway timeout"},
                                    "attributes": [attr("server.address", "gateway.example.test")],
                                    "events": [],
                                }
                            ],
                        }
                    ],
                }
            ]
        }
        logs.write_text(json.dumps(log_payload) + "\n", encoding="utf-8")
        traces.write_text(json.dumps(trace_payload) + "\n", encoding="utf-8")

        zip_path, manifest = build_otlp_bundle(
            logs_path=logs,
            traces_path=traces,
            output_dir=root / "out",
            trace_id=TRACE_ID,
            since="2026-09-02T01:02:00Z",
            until="2026-09-02T01:02:10Z",
        )

        with zipfile.ZipFile(zip_path) as zf:
            incident = json.loads(zf.read("production/incident.json"))
            exceptions = json.loads(zf.read("production/exceptions.json"))
            services = json.loads(zf.read("production/services.json"))
            log_text = zf.read("production/logs.json").decode("utf-8")
            checksums = zf.read("SHA256SUMS.txt").decode("utf-8").splitlines()

            assert manifest["schema"] == "fixbundle/0.5"
            assert incident["trace_ids"] == [TRACE_ID]
            assert incident["log_records"] == 1
            assert incident["span_records"] == 1
            assert exceptions[0]["type"] == "PaymentGatewayError"
            assert services[0]["service.name"] == "payments-api"
            assert "demo-secret-should-disappear" not in log_text
            assert "<REDACTED>" in log_text

            for line in checksums:
                digest, member = line.split("  ", 1)
                assert hashlib.sha256(zf.read(member)).hexdigest() == digest

        print(f"PASS trace_id={TRACE_ID}")
        print("PASS correlated_logs=1")
        print("PASS correlated_spans=1")
        print("PASS exception=PaymentGatewayError")
        print("PASS service=payments-api")
        print("PASS secret_redacted")
        print(f"PASS checksums={len(checksums)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
