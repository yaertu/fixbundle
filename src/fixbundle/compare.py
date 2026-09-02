from __future__ import annotations

import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path
from typing import Any

SUPPORTED_SCHEMAS = {"fixbundle/0.3", "fixbundle/0.4", "fixbundle/0.5"}
MAX_ZIP_MEMBERS = 2_000
MAX_MEMBER_BYTES = 16_000_000
MAX_TOTAL_UNCOMPRESSED_BYTES = 64_000_000
_CHECKSUM_RE = re.compile(r"^([0-9a-fA-F]{64})  (.+)$")
_DIFF_FILE_RE = re.compile(r"^diff --git a/(.+?) b/(.+?)$", re.MULTILINE)
_MISSING = object()

FIELD_ORDER = (
    "bundle.schema",
    "bundle.capture_mode",
    "identity.project",
    "identity.repository",
    "identity.workflow",
    "identity.run_id",
    "git.commit",
    "git.current_head",
    "git.changed_files",
    "failure.commands",
    "failure.failed_jobs",
    "failure.failed_steps",
    "failure.exceptions",
    "production.services",
    "production.trace_ids",
    "production.span_names",
    "runtime.stacks",
    "runtime.python",
    "runtime.platform",
)
STATUS_ORDER = ("changed", "added", "removed", "unavailable")


class CompareError(RuntimeError):
    pass


def _safe_member_name(name: str) -> str:
    if not name or "\x00" in name:
        raise CompareError("unsafe ZIP member name")
    if "\\" in name:
        raise CompareError(f"unsafe ZIP member path: {name}")
    if name.startswith("/") or re.match(r"^[A-Za-z]:", name):
        raise CompareError(f"unsafe ZIP member path: {name}")
    trimmed = name[:-1] if name.endswith("/") else name
    if not trimmed:
        raise CompareError(f"unsafe ZIP member path: {name}")
    parts = trimmed.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise CompareError(f"unsafe ZIP member path: {name}")
    return name


def _is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0o170000
    return mode == stat.S_IFLNK


class _BundleReader:
    def __init__(self, path: Path):
        self.path = path
        if not path.is_file():
            raise CompareError(f"bundle not found: {path}")
        try:
            self.zf = zipfile.ZipFile(path)
        except (OSError, zipfile.BadZipFile) as exc:
            raise CompareError(f"invalid FixBundle ZIP: {path.name}") from exc

        infos = self.zf.infolist()
        if len(infos) > MAX_ZIP_MEMBERS:
            self.close()
            raise CompareError(f"ZIP member count exceeds {MAX_ZIP_MEMBERS}")

        self.files: dict[str, zipfile.ZipInfo] = {}
        seen: set[str] = set()
        total = 0
        try:
            for info in infos:
                name = _safe_member_name(info.filename)
                canonical = name[:-1] if name.endswith("/") else name
                if canonical in seen:
                    raise CompareError(f"duplicate ZIP member: {canonical}")
                seen.add(canonical)
                if _is_symlink(info):
                    raise CompareError(f"symlink ZIP member is not allowed: {canonical}")
                if info.flag_bits & 0x1:
                    raise CompareError(f"encrypted ZIP member is not supported: {canonical}")
                if info.is_dir():
                    continue
                if info.file_size > MAX_MEMBER_BYTES:
                    raise CompareError(f"ZIP member exceeds {MAX_MEMBER_BYTES} bytes: {canonical}")
                total += info.file_size
                if total > MAX_TOTAL_UNCOMPRESSED_BYTES:
                    raise CompareError(
                        f"ZIP uncompressed size exceeds {MAX_TOTAL_UNCOMPRESSED_BYTES} bytes"
                    )
                self.files[canonical] = info
            self._validate_checksums()
            self.manifest = self._json("manifest.json", required=True)
            if not isinstance(self.manifest, dict):
                raise CompareError("manifest.json must contain an object")
            schema = self.manifest.get("schema")
            if schema not in SUPPORTED_SCHEMAS:
                raise CompareError(f"unsupported FixBundle schema: {schema!r}")
        except Exception:
            self.close()
            raise

    def close(self) -> None:
        try:
            self.zf.close()
        except Exception:
            pass

    def __enter__(self) -> "_BundleReader":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _bytes(self, name: str, *, required: bool = False) -> bytes | None:
        info = self.files.get(name)
        if info is None:
            if required:
                raise CompareError(f"required bundle member missing: {name}")
            return None
        try:
            data = self.zf.read(info)
        except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
            raise CompareError(f"cannot read bundle member: {name}") from exc
        if len(data) != info.file_size:
            raise CompareError(f"ZIP member size mismatch: {name}")
        return data

    def _text(self, name: str, *, required: bool = False) -> str | None:
        data = self._bytes(name, required=required)
        if data is None:
            return None
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise CompareError(f"bundle member must be UTF-8 text: {name}") from exc

    def _json(self, name: str, *, required: bool = False) -> Any:
        text = self._text(name, required=required)
        if text is None:
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise CompareError(f"malformed JSON in bundle member: {name}") from exc

    def _validate_checksums(self) -> None:
        text = self._text("SHA256SUMS.txt", required=True)
        assert text is not None
        checksums: dict[str, str] = {}
        for line_no, line in enumerate(text.splitlines(), start=1):
            if not line:
                continue
            match = _CHECKSUM_RE.fullmatch(line)
            if not match:
                raise CompareError(f"malformed checksum line {line_no}")
            digest, member = match.groups()
            _safe_member_name(member)
            if member.endswith("/"):
                raise CompareError(f"checksum references a directory: {member}")
            if member == "SHA256SUMS.txt":
                raise CompareError("SHA256SUMS.txt must not checksum itself")
            if member in checksums:
                raise CompareError(f"duplicate checksum entry: {member}")
            if member not in self.files:
                raise CompareError(f"checksum references missing member: {member}")
            checksums[member] = digest.lower()

        expected = set(self.files) - {"SHA256SUMS.txt"}
        actual = set(checksums)
        if actual != expected:
            missing = sorted(expected - actual)
            extra = sorted(actual - expected)
            detail = []
            if missing:
                detail.append(f"missing checksum entries: {', '.join(missing[:5])}")
            if extra:
                detail.append(f"unexpected checksum entries: {', '.join(extra[:5])}")
            suffix = ": " + "; ".join(detail) if detail else ""
            raise CompareError("checksum coverage mismatch" + suffix)

        for member in sorted(expected):
            data = self._bytes(member, required=True)
            assert data is not None
            actual_digest = hashlib.sha256(data).hexdigest()
            if actual_digest != checksums[member]:
                raise CompareError(f"checksum mismatch: {member}")


def _sorted_unique(values: list[Any]) -> list[Any]:
    keyed: dict[str, Any] = {}
    for value in values:
        key = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        keyed[key] = value
    return [keyed[key] for key in sorted(keyed)]


def _json_list(reader: _BundleReader, name: str) -> list[Any] | None:
    value = reader._json(name)
    if value is None:
        return None
    if not isinstance(value, list):
        raise CompareError(f"{name} must contain a JSON array")
    return value


def _text_value(reader: _BundleReader, name: str) -> str | object:
    value = reader._text(name)
    if value is None:
        return _MISSING
    return value.strip()


def _normalize_v03(reader: _BundleReader, fields: dict[str, Any]) -> None:
    m = reader.manifest
    incident = m.get("incident") if isinstance(m.get("incident"), dict) else {}
    fields["bundle.capture_mode"] = incident.get("capture_mode") or "local"
    if isinstance(m.get("project"), str):
        fields["identity.project"] = m["project"]

    commit = incident.get("incident_commit") if incident else None
    if not commit:
        commit = _text_value(reader, "git/head.txt")
    if commit is not _MISSING and commit:
        fields["git.commit"] = commit
    current_head = incident.get("current_head") if incident else None
    if current_head:
        fields["git.current_head"] = current_head

    diff_text = reader._text("git/diff.patch")
    if diff_text is not None:
        names: list[str] = []
        for a_name, b_name in _DIFF_FILE_RE.findall(diff_text):
            names.append(b_name if b_name != "/dev/null" else a_name)
        fields["git.changed_files"] = sorted(set(names))

    commands = m.get("commands") if isinstance(m.get("commands"), list) else []
    failed: list[dict[str, Any]] = []
    for item in commands:
        if not isinstance(item, dict):
            continue
        if item.get("timed_out") or item.get("exit_code") not in (0, None):
            failed.append(
                {
                    "command": item.get("command"),
                    "exit_code": item.get("exit_code"),
                    "timed_out": bool(item.get("timed_out")),
                }
            )
    fields["failure.commands"] = _sorted_unique(failed)

    stacks = m.get("stacks") if isinstance(m.get("stacks"), list) else None
    if stacks is not None:
        names = [
            item.get("stack")
            for item in stacks
            if isinstance(item, dict) and item.get("stack")
        ]
        fields["runtime.stacks"] = sorted(set(names))

    system = reader._json("system.json")
    if system is not None:
        if not isinstance(system, dict):
            raise CompareError("system.json must contain an object")
        if system.get("python") is not None:
            fields["runtime.python"] = system.get("python")
        if system.get("platform") is not None:
            fields["runtime.platform"] = system.get("platform")


def _normalize_v04(reader: _BundleReader, fields: dict[str, Any]) -> None:
    m = reader.manifest
    fields["bundle.capture_mode"] = m.get("capture_mode") or "github-actions-failure"
    for field, key in (
        ("identity.repository", "repository"),
        ("identity.workflow", "workflow"),
        ("identity.run_id", "run_id"),
        ("git.commit", "head_sha"),
    ):
        if m.get(key) is not None:
            fields[field] = m.get(key)

    jobs = _json_list(reader, "github/jobs.json")
    if jobs is not None:
        failed_jobs: list[dict[str, Any]] = []
        failed_steps: list[dict[str, Any]] = []
        for job in jobs:
            if not isinstance(job, dict) or job.get("conclusion") != "failure":
                continue
            failed_jobs.append({"id": job.get("id"), "name": job.get("name")})
            for step in job.get("steps") or []:
                if isinstance(step, dict) and step.get("conclusion") == "failure":
                    failed_steps.append(
                        {
                            "job": job.get("name"),
                            "number": step.get("number"),
                            "name": step.get("name"),
                        }
                    )
        fields["failure.failed_jobs"] = _sorted_unique(failed_jobs)
        fields["failure.failed_steps"] = _sorted_unique(failed_steps)

    commit = reader._json("github/commit.json")
    if commit is not None:
        if not isinstance(commit, dict):
            raise CompareError("github/commit.json must contain an object")
        files = commit.get("files") if isinstance(commit.get("files"), list) else []
        names = [
            item.get("filename")
            for item in files
            if isinstance(item, dict) and item.get("filename")
        ]
        fields["git.changed_files"] = sorted(set(names))


def _normalize_v05(reader: _BundleReader, fields: dict[str, Any]) -> None:
    m = reader.manifest
    fields["bundle.capture_mode"] = m.get("capture_mode") or "otlp-file"
    selected = m.get("selected") if isinstance(m.get("selected"), dict) else {}
    trace_ids = selected.get("trace_ids") if isinstance(selected.get("trace_ids"), list) else []
    fields["production.trace_ids"] = sorted(str(x) for x in trace_ids)

    exceptions = _json_list(reader, "production/exceptions.json")
    if exceptions is not None:
        compact: list[dict[str, Any]] = []
        for item in exceptions:
            if not isinstance(item, dict):
                continue
            compact.append(
                {
                    "source": item.get("source"),
                    "type": item.get("type"),
                    "message": item.get("message"),
                    "trace_id": item.get("trace_id"),
                    "span_id": item.get("span_id"),
                }
            )
        fields["failure.exceptions"] = _sorted_unique(compact)

    services = _json_list(reader, "production/services.json")
    if services is not None:
        compact_services = [item for item in services if isinstance(item, dict)]
        fields["production.services"] = _sorted_unique(compact_services)

    traces = _json_list(reader, "production/traces.json")
    if traces is not None:
        names = [
            item.get("name")
            for item in traces
            if isinstance(item, dict) and item.get("name")
        ]
        fields["production.span_names"] = sorted(set(names))


def _normalize(reader: _BundleReader) -> dict[str, Any]:
    schema = reader.manifest["schema"]
    fields: dict[str, Any] = {"bundle.schema": schema}
    if schema == "fixbundle/0.3":
        _normalize_v03(reader, fields)
    elif schema == "fixbundle/0.4":
        _normalize_v04(reader, fields)
    elif schema == "fixbundle/0.5":
        _normalize_v05(reader, fields)
    return fields


def compare_bundles(baseline: Path, incident: Path) -> dict[str, Any]:
    baseline = Path(baseline)
    incident = Path(incident)
    with _BundleReader(baseline) as base_reader, _BundleReader(incident) as incident_reader:
        base = _normalize(base_reader)
        current = _normalize(incident_reader)

    changes: list[dict[str, Any]] = []
    unchanged = 0
    counts = {status: 0 for status in STATUS_ORDER}
    for field in FIELD_ORDER:
        before = base.get(field, _MISSING)
        after = current.get(field, _MISSING)
        if before is _MISSING and after is _MISSING:
            status = "unavailable"
            item = {"field": field, "status": status, "baseline": None, "incident": None}
        elif before is _MISSING:
            status = "added"
            item = {"field": field, "status": status, "baseline": None, "incident": after}
        elif after is _MISSING:
            status = "removed"
            item = {"field": field, "status": status, "baseline": before, "incident": None}
        elif before != after:
            status = "changed"
            item = {"field": field, "status": status, "baseline": before, "incident": after}
        else:
            unchanged += 1
            continue
        counts[status] += 1
        changes.append(item)

    return {
        "schema": "fixbundle/compare-0.1",
        "baseline": {
            "name": baseline.name,
            "schema": base.get("bundle.schema"),
            "capture_mode": base.get("bundle.capture_mode"),
        },
        "incident": {
            "name": incident.name,
            "schema": current.get("bundle.schema"),
            "capture_mode": current.get("bundle.capture_mode"),
        },
        "summary": {**counts, "unchanged": unchanged},
        "changes": changes,
    }


def _display(value: Any) -> str:
    if value is None:
        return "<unavailable>"
    if isinstance(value, (dict, list)):
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(", ", ": "),
        )
    return str(value)


def render_text(report: dict[str, Any]) -> str:
    baseline = report["baseline"]
    incident = report["incident"]
    lines = [
        "FixBundle Compare",
        f"Baseline: {baseline['name']} ({baseline.get('schema')} / {baseline.get('capture_mode')})",
        f"Incident: {incident['name']} ({incident.get('schema')} / {incident.get('capture_mode')})",
        "",
    ]
    changes = report.get("changes") or []
    for status in STATUS_ORDER:
        group = [item for item in changes if item.get("status") == status]
        if not group:
            continue
        lines.append(status.upper())
        for item in group:
            lines.append(
                f"- {item['field']}: {_display(item.get('baseline'))} -> {_display(item.get('incident'))}"
            )
        lines.append("")
    summary = report["summary"]
    lines.append(
        "Summary: "
        + ", ".join(
            f"{key}={summary[key]}"
            for key in ("changed", "added", "removed", "unavailable", "unchanged")
        )
    )
    return "\n".join(lines) + "\n"


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
