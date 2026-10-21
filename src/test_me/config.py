import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_HOST = "test-me.vzl.one"


@dataclass(frozen=True)
class Settings:
    base_url: str
    api_connect_timeout: float
    api_read_timeout: float
    browser: str
    headless: bool
    artifact_dir: Path

    @classmethod
    def from_env(cls) -> "Settings":
        base_url = os.getenv("BASE_URL", f"https://{ALLOWED_HOST}").rstrip("/")
        parsed_url = urlparse(base_url)
        if (
            parsed_url.scheme != "https"
            or parsed_url.netloc != ALLOWED_HOST
            or parsed_url.path not in ("", "/")
            or parsed_url.query
            or parsed_url.fragment
        ):
            raise ValueError(f"BASE_URL must use https://{ALLOWED_HOST}")

        browser = os.getenv("BROWSER", "chrome").lower()
        if browser not in {"chrome", "firefox", "edge"}:
            raise ValueError("BROWSER must be chrome, firefox, or edge")

        return cls(
            base_url=base_url,
            api_connect_timeout=float(os.getenv("API_CONNECT_TIMEOUT", "5")),
            api_read_timeout=float(os.getenv("API_READ_TIMEOUT", "20")),
            browser=browser,
            headless=os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"},
            artifact_dir=Path(os.getenv("ARTIFACT_DIR", "artifacts")),
        )
