from __future__ import annotations

import json
from collections.abc import Generator
from contextlib import suppress
from datetime import UTC, datetime

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from test_me.api.assertions import assert_status
from test_me.api.client import ApiClient
from test_me.api.models import Product
from test_me.config import Settings
from test_me.ui.browser_factory import create_driver
from test_me.utils.artifacts import (
    safe_artifact_name,
    try_capture,
    write_text_safely,
)
from test_me.utils.masking import mask_token, redact_sensitive_text


@pytest.fixture
def settings() -> Settings:
    return Settings.from_env()


@pytest.fixture
def api_client(settings: Settings) -> Generator[ApiClient, None, None]:
    client = ApiClient(settings)
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def workspace_token(api_client: ApiClient) -> str:
    response = api_client.create_workspace()
    assert_status(response, 201, "Create isolated test workspace")
    payload = response.json()
    token = payload.get("token")
    assert isinstance(token, str) and token, "Workspace response must contain token"
    return token


@pytest.fixture
def api(
    settings: Settings,
    workspace_token: str,
) -> Generator[ApiClient, None, None]:
    client = ApiClient(settings, workspace_token)
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def available_product(api: ApiClient) -> Product:
    response = api.list_products(limit=20)
    assert_status(response, 200, "List products")
    products = [Product.from_payload(item) for item in response.json()["items"]]
    product = next((item for item in products if item.stock > 0), None)
    assert product is not None, "Catalog must contain an in-stock product"
    return product


@pytest.fixture
def driver(settings: Settings) -> Generator[WebDriver, None, None]:
    instance: WebDriver = create_driver(settings)
    try:
        yield instance
    finally:
        # A dead browser session must not replace the original test failure.
        with suppress(Exception):
            instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo[object],
) -> Generator[None, None, None]:
    outcome = yield
    report = outcome.get_result()
    if not report.failed or "driver" not in item.funcargs:
        return

    driver_instance: WebDriver = item.funcargs["driver"]
    settings: Settings = item.funcargs["settings"]
    artifact_dir = settings.artifact_dir / safe_artifact_name(item.nodeid)
    capture_errors: list[str] = []
    try_capture(
        "artifact directory",
        lambda: artifact_dir.mkdir(parents=True, exist_ok=True),
        capture_errors,
        None,
    )

    token = item.funcargs.get("workspace_token")
    if not token:
        token = try_capture(
            "workspace token",
            lambda: driver_instance.execute_script(
                "return JSON.parse(localStorage.getItem('test-me:v2') || '{}').token"
            ),
            capture_errors,
            None,
        )
    token = token if isinstance(token, str) and token else None

    try_capture(
        "screenshot",
        lambda: driver_instance.save_screenshot(str(artifact_dir / "screenshot.png")),
        capture_errors,
        False,
    )
    source = try_capture(
        "page source", lambda: driver_instance.page_source, capture_errors, ""
    )
    source = redact_sensitive_text(source)
    if token:
        source = source.replace(token, "<redacted>")
    if source:
        write_text_safely(artifact_dir / "page_source.html", source, capture_errors)

    browser_logs = try_capture(
        "browser logs", lambda: driver_instance.get_log("browser"), capture_errors, []
    )
    browser_logs_text = redact_sensitive_text(
        json.dumps(browser_logs, ensure_ascii=False)
    )
    current_url = redact_sensitive_text(
        try_capture(
            "current URL", lambda: driver_instance.current_url, capture_errors, ""
        )
    )
    failure = redact_sensitive_text(report.longreprtext or "")
    if token:
        browser_logs_text = browser_logs_text.replace(token, "<redacted>")
        current_url = current_url.replace(token, "<redacted>")
        failure = failure.replace(token, "<redacted>")

    diagnostics = [
        f"test={item.nodeid}",
        f"phase={report.when}",
        f"timestamp={datetime.now(UTC).isoformat()}",
        f"browser={settings.browser}",
        f"url={current_url}",
        f"workspace_token={mask_token(token)}"
        if token
        else "workspace_token=<unavailable>",
        f"browser_logs={browser_logs_text}",
        "",
        failure,
    ]
    if capture_errors:
        diagnostics.extend(["", "Artifact collection warnings:", *capture_errors])
    write_text_safely(
        artifact_dir / "failure.txt", "\n".join(diagnostics) + "\n", capture_errors
    )
