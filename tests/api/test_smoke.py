import pytest

from test_me.api.assertions import assert_status
from test_me.api.client import ApiClient
from test_me.api.models import Product


@pytest.mark.api
@pytest.mark.smoke
def test_health_endpoint_reports_service_status(api_client: ApiClient) -> None:
    response = api_client.health()

    assert_status(response, 200, "Health endpoint")
    payload = response.json()
    assert payload["status"] == "ok", payload
    assert payload["version"]
    assert payload["seed"]


@pytest.mark.api
@pytest.mark.smoke
def test_create_workspace_returns_token_without_authorization(
    api_client: ApiClient,
) -> None:
    response = api_client.create_workspace()

    assert_status(response, 201, "Create workspace")
    token = response.json().get("token")
    assert isinstance(token, str) and len(token) >= 16
    assert response.request.body is None
    assert "Authorization" not in response.request.headers
    assert "X-Workspace-Token" not in response.request.headers


@pytest.mark.api
@pytest.mark.smoke
def test_catalog_lists_products_and_product_detail(api_client: ApiClient) -> None:
    response = api_client.list_products()

    assert_status(response, 200, "List products")
    payload = response.json()
    assert payload["total"] >= len(payload["items"]) > 0
    assert payload["page"] == 1
    assert payload["limit"] == 6

    product = Product.from_payload(payload["items"][0])
    detail = api_client.product(product.id)

    assert_status(detail, 200, f"Product detail {product.id}")
    assert Product.from_payload(detail.json()) == product


@pytest.mark.api
@pytest.mark.negative
def test_protected_orders_reject_missing_and_invalid_workspace_tokens(
    api_client: ApiClient,
) -> None:
    missing = api_client.list_orders()
    invalid = api_client.request(
        "GET", "/api/orders", workspace_token="invalid-workspace-token"
    )

    assert_status(missing, 401, "Orders without workspace token")
    assert_status(invalid, 401, "Orders with invalid workspace token")
