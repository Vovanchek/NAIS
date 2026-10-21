import json
from datetime import UTC, datetime

import pytest
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from test_me.api.assertions import assert_status
from test_me.api.client import ApiClient
from test_me.api.models import Product
from test_me.config import Settings
from test_me.ui.browser_factory import create_driver
from test_me.utils.masking import mask_token, redact_sensitive_text


@pytest.fixture
def settings() -> Settings:
    return Settings.from_env()


@pytest.fixture
def api_client(settings: Settings):
    client = ApiClient(settings)
    yield client
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
def api(settings: Settings, workspace_token: str):
    client = ApiClient(settings, workspace_token)
    yield client
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
def driver(settings: Settings):
    instance: WebDriver = create_driver(settings)
    yield instance
    instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    if not report.failed or "driver" not in item.funcargs:
        return

    driver_instance = item.funcargs["driver"]
    settings = item.funcargs["settings"]
    artifact_dir = settings.artifact_dir / item.nodeid.replace("::", "_").replace(
        "/", "_"
    )
    artifact_dir.mkdir(parents=True, exist_ok=True)

    token = item.funcargs.get("workspace_token")
    if not token:
        try:
            token = driver_instance.execute_script(
                "return JSON.parse(localStorage.getItem('test-me:v2') || '{}').token"
            )
        except WebDriverException:
            token = None
    token_note = f"\nworkspace_token={mask_token(token)}" if token else ""

    driver_instance.save_screenshot(str(artifact_dir / "screenshot.png"))
    source = redact_sensitive_text(driver_instance.page_source)
    if token:
        source = source.replace(token, "<redacted>")
    (artifact_dir / "page_source.html").write_text(source, encoding="utf-8")

    try:
        browser_logs = driver_instance.get_log("browser")
    except WebDriverException:
        browser_logs = []
    browser_logs_text = redact_sensitive_text(
        json.dumps(browser_logs, ensure_ascii=False)
    )
    if token:
        browser_logs_text = browser_logs_text.replace(token, "<redacted>")

    current_url = redact_sensitive_text(driver_instance.current_url)
    failure = redact_sensitive_text(report.longreprtext or "")
    if token:
        failure = failure.replace(token, "<redacted>")
    (artifact_dir / "failure.txt").write_text(
        f"test={item.nodeid}\n"
        f"timestamp={datetime.now(UTC).isoformat()}\n"
        f"browser={settings.browser}\n"
        f"url={current_url}\n"
        f"browser_logs={browser_logs_text}\n"
        f"{failure}{token_note}\n",
        encoding="utf-8",
    )
