import pytest
from requests import Response

from test_me.api.assertions import assert_status
from test_me.config import Settings
from test_me.utils.masking import mask_token, redact_sensitive_text
from test_me.utils.money import discount_for_subtotal, parse_uah


def test_redact_workspace_token_from_json_and_header_text() -> None:
    token = "ABCDEFGHIJKLMNOPQRSTUVWX"

    for diagnostic in (
        f'{{"token": "{token}"}}',
        f"X-Workspace-Token: {token}",
    ):
        assert token not in redact_sensitive_text(diagnostic)

    assert mask_token(token) == "ABC...VWX"


def test_parse_uah_handles_regular_and_nonbreaking_spaces() -> None:
    assert parse_uah("2 160,00 грн") == 216_000
    assert parse_uah("2\u00a0160,05 грн") == 216_005


def test_discount_uses_floor_in_integer_kopecks() -> None:
    assert discount_for_subtotal(101) == 10
    assert discount_for_subtotal(109) == 10
    assert discount_for_subtotal(110) == 11


def test_settings_reject_non_allowed_host_and_path(monkeypatch) -> None:
    monkeypatch.setenv("BASE_URL", "https://example.com")
    with pytest.raises(ValueError, match="BASE_URL must use"):
        Settings.from_env()

    monkeypatch.setenv("BASE_URL", "https://test-me.vzl.one/other")
    with pytest.raises(ValueError, match="BASE_URL must use"):
        Settings.from_env()


def test_rate_limit_diagnostics_require_retry_after_header() -> None:
    response = Response()
    response.status_code = 429
    response._content = b'{"detail":"rate limited"}'

    with pytest.raises(AssertionError, match="missing Retry-After"):
        assert_status(response, 201, "Rate-limited request")

    response.headers["Retry-After"] = "30"
    with pytest.raises(AssertionError, match="retry_after='30'"):
        assert_status(response, 201, "Rate-limited request")


def test_safe_artifact_name_removes_cross_platform_invalid_characters() -> None:
    from test_me.utils.artifacts import safe_artifact_name

    value = safe_artifact_name('tests/ui/test_checkout.py::test_case[param:*?"<>|]')

    assert value
    assert not any(character in value for character in '<>:"/\\|?*')


def test_try_capture_returns_default_and_records_diagnostic_failure() -> None:
    from test_me.utils.artifacts import try_capture

    errors: list[str] = []

    def failing_operation() -> str:
        raise RuntimeError("browser session is gone")

    result = try_capture("screenshot", failing_operation, errors, "fallback")

    assert result == "fallback"
    assert errors == [
        "screenshot capture failed: RuntimeError: browser session is gone"
    ]
