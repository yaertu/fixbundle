from __future__ import annotations

import json
import tempfile
from datetime import datetime
from pathlib import Path

from fixbundle.compare import compare_bundles, render_text
from fixbundle.otlp import build_otlp_bundle

BASELINE_TRACE = "11111111111111111111111111111111"
INCIDENT_TRACE = "22222222222222222222222222222222"
SPAN_ID = "0123456789abcdef"


def ns(text: str) -> str:
    dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    return str(int(dt.timestamp() * 1_000_000_000))


def attr(key: str, value: str) -> dict:
    return {"key": key, "value": {"stringValue": value}}


def write_incident(
    root: Path,
    *,
    name: str,
    trace_id: str,
    version: str,
    exception_type: str | None,
) -> Path:
    logs = root / f"{name}-logs.jsonl"
    traces = root / f"{name}-traces.jsonl"
    log_attributes = [attr("http.request.method", "POST")]
    severity = "INFO"
    message = "charge completed"
    status = {"code": 1}
    events: list[dict] = []
    if exception_type:
        severity = "ERROR"
        message = "charge rejected"
        status = {"code": 2, "message": "gateway timeout"}
        log_attributes.extend(
            [
                attr("exception.type", exception_type),
                attr("exception.message", "gateway timeout"),
                attr("exception.stacktrace", f"{exception_type}: timeout\n  at charge.py:42"),
            ]
        )
        events.append(
            {
                "name": "exception",
                "timeUnixNano": ns("2026-09-02T01:02:03Z"),
                "attributes": [
                    attr("exception.type", exception_type),
                    attr("exception.message", "gateway timeout"),
                ],
            }
        )

    resource = [
        attr("service.name", "payments-api"),
        attr("service.version", version),
        attr("deployment.environment.name", "production"),
        attr("deployment.id", f"deploy-{version}"),
    ]
    log_payload = {
        "resourceLogs": [
            {
                "resource": {"attributes": resource},
                "scopeLogs": [
                    {
                        "scope": {"name": "payments.logger"},
                        "logRecords": [
                            {
                                "timeUnixNano": ns("2026-09-02T01:02:03Z"),
                                "severityText": severity,
                                "traceId": trace_id,
                                "spanId": SPAN_ID,
                                "body": {"stringValue": message},
                                "attributes": log_attributes,
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
                "resource": {"attributes": resource},
                "scopeSpans": [
                    {
                        "scope": {"name": "payments.tracer"},
                        "spans": [
                            {
                                "traceId": trace_id,
                                "spanId": SPAN_ID,
                                "name": "POST /charge",
                                "startTimeUnixNano": ns("2026-09-02T01:02:02Z"),
                                "endTimeUnixNano": ns("2026-09-02T01:02:04Z"),
                                "status": status,
                                "attributes": [],
                                "events": events,
                            }
                        ],
                    }
                ],
            }
        ]
    }
    logs.write_text(json.dumps(log_payload) + "\n", encoding="utf-8")
    traces.write_text(json.dumps(trace_payload) + "\n", encoding="utf-8")
    zip_path, _ = build_otlp_bundle(
        logs_path=logs,
        traces_path=traces,
        output_dir=root / f"{name}-out",
        trace_id=trace_id,
    )
    return zip_path


def change(report: dict, field: str) -> dict:
    return next(item for item in report["changes"] if item["field"] == field)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="fixbundle-compare-demo-") as tmp:
        root = Path(tmp)
        baseline = write_incident(
            root,
            name="baseline",
            trace_id=BASELINE_TRACE,
            version="2.4.1",
            exception_type=None,
        )
        incident = write_incident(
            root,
            name="incident",
            trace_id=INCIDENT_TRACE,
            version="2.4.2",
            exception_type="PaymentGatewayError",
        )

        report = compare_bundles(baseline, incident)
        services = change(report, "production.services")
        exceptions = change(report, "failure.exceptions")
        traces = change(report, "production.trace_ids")

        assert services["status"] == "changed"
        assert services["baseline"][0]["service.version"] == "2.4.1"
        assert services["incident"][0]["service.version"] == "2.4.2"
        assert exceptions["status"] == "changed"
        assert exceptions["baseline"] == []
        assert {item["type"] for item in exceptions["incident"]} == {"PaymentGatewayError"}
        assert traces["baseline"] == [BASELINE_TRACE]
        assert traces["incident"] == [INCIDENT_TRACE]

        print(render_text(report), end="")
        print("PASS input_integrity=validated")
        print("PASS service_version=2.4.1->2.4.2")
        print("PASS exception=none->PaymentGatewayError")
        print(f"PASS trace_id={BASELINE_TRACE}->{INCIDENT_TRACE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
