from requests import Response

from test_me.utils.masking import redact_sensitive_text


def assert_status(response: Response, expected: int, context: str) -> None:
    body = redact_sensitive_text(response.text[:1000])
    retry_after = response.headers.get("Retry-After")
    if response.status_code == 429:
        assert retry_after, (
            f"{context}: HTTP 429 response is missing Retry-After header"
        )
    assert response.status_code == expected, (
        f"{context}: expected HTTP {expected}, got {response.status_code}; "
        f"retry_after={retry_after!r}; response={body}"
    )
