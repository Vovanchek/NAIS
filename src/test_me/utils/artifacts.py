from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")
_INVALID_WINDOWS_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]+')


def safe_artifact_name(nodeid: str, max_length: int = 180) -> str:
    """Return a stable cross-platform directory name for a pytest node id."""
    sanitized = _INVALID_WINDOWS_CHARS.sub("_", nodeid).strip(" ._")
    return (sanitized or "unknown-test")[:max_length]


def try_capture(
    label: str,
    operation: Callable[[], T],
    errors: list[str],
    default: T,
) -> T:
    """Run diagnostic collection without masking the original test failure."""
    try:
        return operation()
    except Exception as exc:  # diagnostics must never replace the test exception
        errors.append(f"{label} capture failed: {type(exc).__name__}: {exc}")
        return default


def write_text_safely(path: Path, content: str, errors: list[str]) -> None:
    try_capture(
        f"write {path.name}",
        lambda: path.write_text(content, encoding="utf-8"),
        errors,
        0,
    )
