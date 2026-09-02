from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(frozen=True)
class StackSignal:
    stack: str
    confidence: str
    evidence: list[str]
    recommended_commands: list[str]


_RULES: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = [
    ("node", ("package.json",), ("npm test", "npm run build")),
    ("python", ("pyproject.toml", "requirements.txt", "Pipfile"), ("pytest -q", "python -m build")),
    ("rust", ("Cargo.toml",), ("cargo test", "cargo build --release")),
    ("dotnet", ("*.sln", "*.csproj"), ("dotnet test", "dotnet build -c Release")),
    ("go", ("go.mod",), ("go test ./...", "go build ./...")),
    ("java", ("pom.xml", "build.gradle", "build.gradle.kts"), ("mvn test", "mvn package -DskipTests")),
]


def _matches(root: Path, pattern: str) -> list[str]:
    if "*" in pattern:
        return sorted(p.name for p in root.glob(pattern) if p.is_file())
    p = root / pattern
    return [pattern] if p.is_file() else []


def detect_stacks(root: Path) -> list[StackSignal]:
    found: list[StackSignal] = []
    for stack, patterns, commands in _RULES:
        evidence: list[str] = []
        for pattern in patterns:
            evidence.extend(_matches(root, pattern))
        if evidence:
            found.append(
                StackSignal(
                    stack=stack,
                    confidence="high" if len(evidence) >= 2 or len(patterns) == 1 else "medium",
                    evidence=sorted(set(evidence)),
                    recommended_commands=list(commands),
                )
            )
    return found


def stacks_as_dicts(root: Path) -> list[dict]:
    return [asdict(item) for item in detect_stacks(root)]
