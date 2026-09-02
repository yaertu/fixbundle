from __future__ import annotations

import argparse
import locale
import sys
from pathlib import Path

from . import __version__
from .collect import build_bundle
from .stack import detect_stacks


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="fixbundle",
        description="Turn a broken project into an AI-ready debugging bundle.",
    )
    p.add_argument("project", nargs="?", default=".", help="Project directory (default: current directory)")
    p.add_argument("-o", "--output", default=".fixbundle", help="Output directory (default: .fixbundle)")
    p.add_argument("-r", "--run", action="append", default=[], metavar="COMMAND", help="Command to run and capture. Repeatable.")
    p.add_argument("--timeout", type=int, default=180, help="Per-command timeout in seconds")
    p.add_argument("--max-files", type=int, default=250, help="Maximum project text/config files to snapshot")
    p.add_argument("--recommend", action="store_true", help="Detect stack and print recommended verification commands, then exit")
    p.add_argument("--lang", choices=["auto", "tr", "en"], default="auto", help="CLI output language")
    p.add_argument("--version", action="version", version=f"fixbundle {__version__}")
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


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    lang = _lang(args.lang)
    root = Path(args.project)
    if not root.exists() or not root.is_dir():
        msg = f"fixbundle: proje klasörü bulunamadı: {root}" if lang == "tr" else f"fixbundle: project directory not found: {root}"
        print(msg, file=sys.stderr)
        return 2
    if args.recommend:
        return _recommend(root, lang)
    try:
        zip_path, manifest = build_bundle(
            root=root,
            output_dir=Path(args.output),
            commands=args.run,
            timeout=max(1, args.timeout),
            max_files=max(1, args.max_files),
        )
    except Exception as exc:
        msg = f"fixbundle: paket oluşturulamadı: {exc}" if lang == "tr" else f"fixbundle: failed: {exc}"
        print(msg, file=sys.stderr)
        return 1

    if lang == "tr":
        print("FixBundle hazır ✅")
        print(f"  ZIP: {zip_path}")
        print(f"  Dosya: {len(manifest['files_captured'])}")
        print(f"  Komut: {len(manifest['commands'])}")
        print(f"  Gizleme/yol maskeleme: {manifest['redactions']}")
        print("  ZIP'i ChatGPT, Codex, Claude Code, Cursor veya destek ekibine ver.")
    else:
        print("FixBundle created ✅")
        print(f"  ZIP: {zip_path}")
        print(f"  Files: {len(manifest['files_captured'])}")
        print(f"  Commands: {len(manifest['commands'])}")
        print(f"  Redactions/path masks: {manifest['redactions']}")
        print("  Give the ZIP to ChatGPT, Codex, Claude Code, Cursor, or your support team.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
