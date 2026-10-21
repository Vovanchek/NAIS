import pytest

from test_me.api.assertions import assert_status
from test_me.api.client import ApiClient
from test_me.api.models import Product


def checkout_payload(product: Product, payment: str = "approved") -> dict[str, object]:
    return {
        "items": [{"product_id": product.id, "quantity": 1}],
        "coupon": "WELCOME10",
        "delivery": "standard",
        "name": "QA Synthetic",
        "email": "qa.synthetic@example.com",
        "address": "Test Address 1",
        "payment": payment,
    }


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.regression
def test_approved_order_lifecycle_and_repeat_cancel_conflict(
    api: ApiClient, available_product: Product
) -> None:
    payload = checkout_payload(available_product)
    quote_response = api.quote(
        {key: payload[key] for key in ("items", "coupon", "delivery")}
    )
    assert_status(quote_response, 200, "Pre-checkout quote")
    expected_totals = {
        "subtotal": available_product.price,
        "discount": available_product.price * 10 // 100,
        "shipping": 0 if available_product.price >= 150_000 else 8_000,
        "currency": "UAH",
    }
    expected_totals["total"] = (
        expected_totals["subtotal"]
        - expected_totals["discount"]
        + expected_totals["shipping"]
    )
    assert quote_response.json() == expected_totals

    created = api.create_order(payload)
    assert_status(created, 201, "Create approved order")
    order = created.json()
    order_id = order["id"]
    assert order["status"] == "confirmed"
    assert order["items"] == payload["items"]
    assert order["totals"] == expected_totals

    listing = api.list_orders()
    assert_status(listing, 200, "List workspace orders")
    matching = [item for item in listing.json()["items"] if item["id"] == order_id]
    assert len(matching) == 1, f"Expected one order {order_id}, got {matching!r}"

    detail = api.order(order_id)
    assert_status(detail, 200, f"Get order {order_id}")
    assert detail.json()["items"] == payload["items"]
    assert detail.json()["totals"] == expected_totals

    canceled = api.cancel_order(order_id)
    assert_status(canceled, 200, f"Cancel order {order_id}")
    assert canceled.json()["status"] == "cancelled"


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.known_defect
@pytest.mark.xfail(
    strict=True, reason="TM-DEF-003: repeat cancellation returns success"
)
def test_repeated_order_cancellation_returns_conflict(
    api: ApiClient, available_product: Product
) -> None:
    created = api.create_order(checkout_payload(available_product))
    assert_status(created, 201, "Create order for repeat-cancel check")
    order_id = created.json()["id"]

    canceled = api.cancel_order(order_id)
    assert_status(canceled, 200, "Cancel order first time")

    repeated_cancel = api.cancel_order(order_id)
    assert_status(repeated_cancel, 409, "Repeated order cancellation")


@pytest.mark.api
@pytest.mark.negative
def test_declined_payment_does_not_create_order(
    api: ApiClient, available_product: Product
) -> None:
    before = api.product(available_product.id)
    assert_status(before, 200, f"Read product {available_product.id} before decline")

    response = api.create_order(checkout_payload(available_product, payment="declined"))
    assert_status(response, 402, "Declined payment")

    orders = api.list_orders()
    assert_status(orders, 200, "Orders after declined payment")
    assert orders.json()["items"] == [], orders.json()

    after = api.product(available_product.id)
    assert_status(after, 200, f"Read product {available_product.id} after decline")
    assert after.json()["stock"] == before.json()["stock"]


@pytest.mark.api
@pytest.mark.negative
def test_order_is_not_visible_from_another_workspace(
    api: ApiClient, api_client: ApiClient, available_product: Product
) -> None:
    created = api.create_order(checkout_payload(available_product))
    assert_status(created, 201, "Create order in workspace A")
    order_id = created.json()["id"]

    workspace_b = api_client.create_workspace()
    assert_status(workspace_b, 201, "Create workspace B")
    token_b = workspace_b.json()["token"]
    foreign_order = api_client.request(
        "GET", f"/api/orders/{order_id}", workspace_token=token_b
    )
    workspace_b_orders = api_client.request(
        "GET", "/api/orders", workspace_token=token_b
    )

    assert_status(foreign_order, 404, "Read workspace A order from workspace B")
    assert_status(workspace_b_orders, 200, "List orders in new workspace B")
    assert workspace_b_orders.json()["items"] == []
