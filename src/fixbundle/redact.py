from __future__ import annotations

import re
from pathlib import Path

REDACTION = "<REDACTED>"

_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?i)(authorization\s*:\s*bearer\s+)[A-Za-z0-9._~+\-/=]+"), r"\1" + REDACTION),
    (re.compile(r"(?i)((?:api[_-]?key|token|secret|password|passwd|pwd|client[_-]?secret)\s*[=:]\s*)['\"]?[^\s'\";,]+"), r"\1" + REDACTION),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), REDACTION),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), REDACTION),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"), REDACTION),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{25,}\b"), REDACTION),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), REDACTION),
    (re.compile(r"(?i)(https?://[^\s/:]+:)[^@\s/]+(@)"), r"\1" + REDACTION + r"\2"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"), REDACTION),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), REDACTION),
]


def redact_text(text: str, *, project_root: Path | None = None, home: Path | None = None) -> tuple[str, int]:
    total = 0
    for pattern, repl in _PATTERNS:
        text, n = pattern.subn(repl, text)
        total += n

    replacements: list[tuple[str, str]] = []
    if project_root is not None:
        replacements.append((str(project_root.resolve()), "<PROJECT>"))
    if home is not None:
        replacements.append((str(home.resolve()), "<HOME>"))

    for raw, marker in replacements:
        variants = {raw, raw.replace("\\", "/"), raw.replace("/", "\\")}
        for variant in sorted(variants, key=len, reverse=True):
            if variant and variant in text:
                count = text.count(variant)
                text = text.replace(variant, marker)
                total += count
    return text, total
