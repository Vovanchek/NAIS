import pytest

from test_me.api.client import ApiClient
from test_me.api.models import Product


@pytest.mark.api
@pytest.mark.negative
def test_stateful_endpoints_reject_missing_and_invalid_tokens(
    api_client: ApiClient, available_product: Product
) -> None:
    order_id = "not-a-real-order-id"
    checkout = {
        "items": [{"product_id": available_product.id, "quantity": 1}],
        "coupon": "",
        "delivery": "standard",
        "name": "QA Synthetic",
        "email": "qa.synthetic@example.com",
        "address": "Test Address 1",
        "payment": "approved",
    }
    requests = (
        ("GET", "/api/favorites", None),
        ("PUT", "/api/favorites", {"product_ids": []}),
        ("GET", f"/api/products/{available_product.id}/review", None),
        (
            "POST",
            f"/api/products/{available_product.id}/review",
            {"rating": 5, "text": "Synthetic review text"},
        ),
        (
            "POST",
            "/api/quote",
            {
                "items": [{"product_id": available_product.id, "quantity": 1}],
                "coupon": "",
                "delivery": "standard",
            },
        ),
        ("GET", "/api/orders", None),
        ("GET", f"/api/orders/{order_id}", None),
        ("POST", f"/api/orders/{order_id}/cancel", None),
        ("POST", "/api/orders", checkout),
    )

    failures = []
    for method, path, body in requests:
        for token in (None, "invalid-workspace-token"):
            response = api_client.request(
                method, path, json=body, workspace_token=token
            )
            if response.status_code != 401:
                token_state = "missing" if token is None else "invalid"
                failures.append(
                    f"{method} {path} with {token_state} token returned "
                    f"HTTP {response.status_code}: {response.text[:200]}"
                )

    assert not failures, "Protected endpoint auth failures: " + "; ".join(failures)
