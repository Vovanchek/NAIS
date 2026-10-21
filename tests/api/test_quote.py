import pytest

from test_me.api.assertions import assert_status
from test_me.api.client import ApiClient
from test_me.api.models import Product, Quote


def products(api: ApiClient) -> list[Product]:
    response = api.list_products(limit=20)
    assert_status(response, 200, "List products for quote")
    return [Product.from_payload(item) for item in response.json()["items"]]


def quote_for(
    api: ApiClient, product: Product, quantity: int = 1, **values: str
) -> Quote:
    payload = {
        "items": [{"product_id": product.id, "quantity": quantity}],
        "coupon": values.get("coupon", ""),
        "delivery": values.get("delivery", "standard"),
    }
    response = api.quote(payload)
    assert_status(response, 200, f"Quote for {product.id} x {quantity}")
    return Quote.from_payload(response.json())


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.known_defect
@pytest.mark.xfail(strict=True, reason="TM-DEF-001: coupon matching is case-sensitive")
def test_welcome_coupon_is_case_and_whitespace_insensitive(
    api: ApiClient, available_product: Product
) -> None:
    results = []
    for coupon in ("WELCOME10", "welcome10", " WELCOME10 "):
        response = api.quote(
            {
                "items": [{"product_id": available_product.id, "quantity": 1}],
                "coupon": coupon,
                "delivery": "standard",
            }
        )
        results.append((coupon, response))

    failures = [
        f"{coupon!r}: HTTP {response.status_code} {response.text[:300]}"
        for coupon, response in results
        if response.status_code != 200
    ]
    assert not failures, "WELCOME10 normalization failed: " + "; ".join(failures)

    for _, response in results:
        quote = Quote.from_payload(response.json())
        expected_discount = available_product.price * 10 // 100
        expected_shipping = 0 if available_product.price >= 150_000 else 8_000
        assert quote.subtotal == available_product.price
        assert quote.discount == expected_discount
        assert quote.shipping == expected_shipping
        assert quote.total == quote.subtotal - quote.discount + quote.shipping
        assert quote.currency == "UAH"


@pytest.mark.api
@pytest.mark.negative
def test_unknown_coupon_is_rejected(api: ApiClient, available_product: Product) -> None:
    response = api.quote(
        {
            "items": [{"product_id": available_product.id, "quantity": 1}],
            "coupon": "NOT-A-REAL-COUPON",
            "delivery": "standard",
        }
    )

    assert_status(response, 422, "Unknown promotion code")


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.known_defect
@pytest.mark.xfail(
    strict=True, reason="TM-DEF-002: free-shipping threshold is not inclusive"
)
def test_standard_shipping_threshold_is_inclusive(api: ApiClient) -> None:
    catalog = products(api)
    at_threshold = next(
        (item for item in catalog if item.stock > 0 and item.price == 150_000), None
    )
    above_threshold = next(
        (item for item in catalog if item.stock > 0 and item.price > 150_000), None
    )
    below_threshold = max(
        (item for item in catalog if item.stock > 0 and item.price < 150_000),
        key=lambda item: item.price,
        default=None,
    )
    assert at_threshold is not None, (
        "Seed catalog must contain an in-stock 150000-cent product"
    )
    assert above_threshold is not None, (
        "Seed catalog must contain an in-stock product above the threshold"
    )
    assert below_threshold is not None, (
        "Seed catalog must contain a product below threshold"
    )

    free_shipping = quote_for(api, at_threshold, coupon="WELCOME10")
    above_threshold_quote = quote_for(api, above_threshold)
    paid_shipping = quote_for(api, below_threshold)

    assert free_shipping.shipping == 0
    assert above_threshold_quote.shipping == 0
    assert paid_shipping.shipping == 8_000


@pytest.mark.api
@pytest.mark.regression
def test_delivery_charge_is_not_discounted(
    api: ApiClient,
) -> None:
    catalog = [item for item in products(api) if item.stock > 0]
    low_product = min(catalog, key=lambda item: item.price)
    high_product = max(catalog, key=lambda item: item.price)
    for product in (low_product, high_product):
        expected_standard = 0 if product.price >= 150_000 else 8_000
        for delivery, expected_shipping in (
            ("standard", expected_standard),
            ("express", 15_000),
        ):
            quote = quote_for(api, product, coupon="WELCOME10", delivery=delivery)

            assert quote.discount == product.price * 10 // 100
            assert quote.shipping == expected_shipping
            assert quote.total == product.price - quote.discount + expected_shipping


@pytest.mark.api
@pytest.mark.regression
def test_valid_quantity_boundaries_are_quoted(api: ApiClient) -> None:
    product = next(item for item in products(api) if item.stock >= 10)
    for quantity in (1, 10):
        quote = quote_for(api, product, quantity=quantity)

        assert quote.subtotal == product.price * quantity
        assert quote.total == quote.subtotal + quote.shipping


@pytest.mark.api
@pytest.mark.negative
def test_quantity_outside_schema_bounds_returns_422(
    api: ApiClient, available_product: Product
) -> None:
    for quantity in (0, 11):
        response = api.quote(
            {
                "items": [{"product_id": available_product.id, "quantity": quantity}],
                "coupon": "",
                "delivery": "standard",
            }
        )

        assert_status(response, 422, f"Invalid quantity {quantity}")


@pytest.mark.api
@pytest.mark.negative
def test_stock_shortage_returns_409(api: ApiClient) -> None:
    product = next(item for item in products(api) if 0 < item.stock < 10)
    response = api.quote(
        {
            "items": [{"product_id": product.id, "quantity": product.stock + 1}],
            "coupon": "",
            "delivery": "standard",
        }
    )

    assert_status(response, 409, f"Insufficient stock for {product.id}")


@pytest.mark.api
@pytest.mark.negative
def test_out_of_stock_product_cannot_be_quoted(api: ApiClient) -> None:
    product = next(item for item in products(api) if item.stock == 0)
    response = api.quote(
        {
            "items": [{"product_id": product.id, "quantity": 1}],
            "coupon": "",
            "delivery": "standard",
        }
    )

    assert_status(response, 409, f"Out-of-stock product {product.id}")
