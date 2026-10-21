import re

_TOKEN_PATTERN = re.compile(
    r"(?i)([\"']?(?:x-workspace-token|token)[\"']?\s*[:=]\s*[\"']?)"
    r"([A-Za-z0-9._-]{12,})"
)


def mask_token(token: str) -> str:
    if len(token) <= 8:
        return "<redacted>"
    return f"{token[:3]}...{token[-3:]}"


def redact_sensitive_text(value: str) -> str:
    return _TOKEN_PATTERN.sub(r"\1<redacted>", value)
