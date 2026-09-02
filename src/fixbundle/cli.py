from __future__ import annotations

import argparse
import locale
import os
import sys
from pathlib import Path

from . import __version__
from .collect import build_bundle
from .github import DEFAULT_MAX_LOG_CHARS, build_github_bundle
from .history import build_historical_bundle
from .otlp import DEFAULT_MAX_INPUT_BYTES, DEFAULT_MAX_RECORDS, build_otlp_bundle
from .stack import detect_stacks


def _configure_stdio() -> None:
    """Prefer UTF-8 CLI output without crashing legacy Windows code pages."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                try:
                    reconfigure(errors="replace")
                except (OSError, ValueError):
                    pass


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fixbundle",
        description="Turn a software failure into a portable AI-ready evidence bundle.",
    )
    p.add_argument("project", nargs="?", default=".", help="Project directory (default: current directory)")
    p.add_argument("-o", "--output", default=".fixbundle", help="Output directory (default: .fixbundle)")
    p.add_argument("-r", "--run", action="append", default=[], metavar="COMMAND", help="Command to run and capture. Repeatable.")
    p.add_argument("--timeout", type=int, default=180, help="Per-command timeout in seconds")
    p.add_argument("--max-files", type=int, default=250, help="Maximum project text/config files to snapshot")
    p.add_argument("--recommend", action="store_true", help="Detect stack and print recommended verification commands, then exit")
    p.add_argument("--commit", metavar="REF", help="Capture an isolated historical Git snapshot without touching the current workspace")
    p.add_argument("--lang", choices=["auto", "tr", "en"], default="auto", help="CLI output language")
    p.add_argument("--version", action="version", version=f"fixbundle {__version__}")
    return p


def github_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fixbundle github",
        description="Turn a failed GitHub Actions run into a portable, redacted evidence bundle.",
    )
    p.add_argument("--repo", required=True, metavar="OWNER/REPO", help="GitHub repository")
    p.add_argument("--run", required=True, type=int, dest="run_id", metavar="RUN_ID", help="Completed failed Actions run id")
    p.add_argument("-o", "--output", default=".fixbundle", help="Output directory (default: .fixbundle)")
    p.add_argument("--token-env", default="GITHUB_TOKEN", help="Environment variable containing a read-only GitHub token")
    p.add_argument("--max-log-chars", type=int, default=DEFAULT_MAX_LOG_CHARS, help="Maximum characters captured per failed job log")
    p.add_argument("--lang", choices=["auto", "tr", "en"], default="auto", help="CLI output language")
    return p


def otlp_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fixbundle otlp",
        description="Turn OpenTelemetry Protocol File Exporter JSON/JSONL into a portable production evidence bundle.",
    )
    p.add_argument("--logs", required=True, metavar="FILE", help="OTLP JSON/JSONL logs file")
    p.add_argument("--traces", metavar="FILE", help="Optional OTLP JSON/JSONL traces file")
    p.add_argument("--trace-id", metavar="TRACE_ID", help="Select only records with this exact trace id")
    p.add_argument("--since", metavar="RFC3339", help="Inclusive lower timestamp bound")
    p.add_argument("--until", metavar="RFC3339", help="Inclusive upper timestamp bound")
    p.add_argument("-o", "--output", default=".fixbundle", help="Output directory (default: .fixbundle)")
    p.add_argument("--max-input-bytes", type=int, default=DEFAULT_MAX_INPUT_BYTES, help="Maximum bytes accepted per OTLP input file")
    p.add_argument("--max-records", type=int, default=DEFAULT_MAX_RECORDS, help="Maximum total normalized log + span records")
    p.add_argument("--lang", choices=["auto", "tr", "en"], default="auto", help="CLI output language")
    return p


def _lang(value: str) -> str:
    if value != "auto":
        return value
    loc = (locale.getlocale()[0] or "").lower()
    return "tr" if loc.startswith("tr") else "en"


def _recommend(root: Path, lang: str) -> int:
    stacks = detect_stacks(root)
    if not stacks:
        print("Yığın algılanamadı." if lang == "tr" else "No known stack detected.")
        return 0
    title = "Önerilen doğrulama komutları:" if lang == "tr" else "Recommended verification commands:"
    print(title)
    for stack in stacks:
        print(f"\n[{stack.stack}] ({stack.confidence})")
        for command in stack.recommended_commands:
            print(f"  {command}")
    return 0


def _github_main(argv: list[str]) -> int:
    args = github_parser().parse_args(argv)
    lang = _lang(args.lang)
    token = os.environ.get(args.token_env) if args.token_env else None
    try:
        zip_path, manifest = build_github_bundle(
            repo=args.repo,
            run_id=args.run_id,
            output_dir=Path(args.output),
            token=token,
            max_log_chars=max(1_000, args.max_log_chars),
        )
    except Exception as exc:
        msg = f"fixbundle github: paket oluşturulamadı: {exc}" if lang == "tr" else f"fixbundle github: failed: {exc}"
        print(msg, file=sys.stderr)
        return 1

    if lang == "tr":
        print("FixBundle GitHub kanıt paketi hazır [OK]")
        print(f"  ZIP: {zip_path}")
        print(f"  Repo: {manifest['repository']}")
        print(f"  Run: {manifest['run_id']}")
        print(f"  Başarısız job: {len(manifest['failed_jobs'])}")
        print(f"  Gizleme/yol maskeleme: {manifest['redactions']}")
    else:
        print("FixBundle GitHub evidence bundle created [OK]")
        print(f"  ZIP: {zip_path}")
        print(f"  Repo: {manifest['repository']}")
        print(f"  Run: {manifest['run_id']}")
        print(f"  Failed jobs: {len(manifest['failed_jobs'])}")
        print(f"  Redactions/path masks: {manifest['redactions']}")
    return 0


def _otlp_main(argv: list[str]) -> int:
    args = otlp_parser().parse_args(argv)
    lang = _lang(args.lang)
    try:
        zip_path, manifest = build_otlp_bundle(
            logs_path=Path(args.logs),
            traces_path=Path(args.traces) if args.traces else None,
            output_dir=Path(args.output),
            trace_id=args.trace_id,
            since=args.since,
            until=args.until,
            max_input_bytes=args.max_input_bytes,
            max_records=args.max_records,
        )
    except Exception as exc:
        msg = f"fixbundle otlp: paket oluşturulamadı: {exc}" if lang == "tr" else f"fixbundle otlp: failed: {exc}"
        print(msg, file=sys.stderr)
        return 1

    selected = manifest["selected"]
    if lang == "tr":
        print("FixBundle production kanıt paketi hazır [OK]")
        print(f"  ZIP: {zip_path}")
        print(f"  Log: {selected['logs']}")
        print(f"  Span: {selected['spans']}")
        print(f"  Exception: {selected['exceptions']}")
        print(f"  Trace: {len(selected['trace_ids'])}")
        print(f"  Gizleme/yol maskeleme: {manifest['redactions']}")
    else:
        print("FixBundle production evidence bundle created [OK]")
        print(f"  ZIP: {zip_path}")
        print(f"  Logs: {selected['logs']}")
        print(f"  Spans: {selected['spans']}")
        print(f"  Exceptions: {selected['exceptions']}")
        print(f"  Traces: {len(selected['trace_ids'])}")
        print(f"  Redactions/path masks: {manifest['redactions']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    _configure_stdio()
    raw = list(sys.argv[1:] if argv is None else argv)
    if raw and raw[0] == "github":
        return _github_main(raw[1:])
    if raw and raw[0] == "otlp":
        return _otlp_main(raw[1:])

    args = parser().parse_args(raw)
    lang = _lang(args.lang)
    root = Path(args.project)
    if not root.exists() or not root.is_dir():
        msg = f"fixbundle: proje klasörü bulunamadı: {root}" if lang == "tr" else f"fixbundle: project directory not found: {root}"
        print(msg, file=sys.stderr)
        return 2
    if args.recommend:
        return _recommend(root, lang)
    try:
        output_dir = Path(args.output)
        if args.commit:
            zip_path, manifest = build_historical_bundle(
                root=root,
                commit_ref=args.commit,
                output_dir=output_dir,
                commands=args.run,
                timeout=max(1, args.timeout),
                max_files=max(1, args.max_files),
            )
        else:
            if not output_dir.is_absolute():
                output_dir = root / output_dir
            zip_path, manifest = build_bundle(
                root=root,
                output_dir=output_dir,
                commands=args.run,
                timeout=max(1, args.timeout),
                max_files=max(1, args.max_files),
            )
    except Exception as exc:
        msg = f"fixbundle: paket oluşturulamadı: {exc}" if lang == "tr" else f"fixbundle: failed: {exc}"
        print(msg, file=sys.stderr)
        return 1

    if lang == "tr":
        print("FixBundle hazır [OK]")
        print(f"  ZIP: {zip_path}")
        print(f"  Dosya: {len(manifest['files_captured'])}")
        print(f"  Komut: {len(manifest['commands'])}")
        print(f"  Gizleme/yol maskeleme: {manifest['redactions']}")
        print("  ZIP'i ChatGPT, Codex, Claude Code, Cursor veya destek ekibine ver.")
    else:
        print("FixBundle created [OK]")
        print(f"  ZIP: {zip_path}")
        print(f"  Files: {len(manifest['files_captured'])}")
        print(f"  Commands: {len(manifest['commands'])}")
        print(f"  Redactions/path masks: {manifest['redactions']}")
        print("  Give the ZIP to ChatGPT, Codex, Claude Code, Cursor, or your support team.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
