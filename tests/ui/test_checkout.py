import pytest

from test_me.api.assertions import assert_status
from test_me.api.client import ApiClient
from test_me.api.models import Product
from test_me.ui.cart_page import CartPage
from test_me.ui.catalog_page import CatalogPage
from test_me.utils.money import discount_for_subtotal


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
def test_checkout_applies_coupon_persists_order_and_clears_cart(
    driver, settings
) -> None:
    catalog_api = ApiClient(settings)
    products_response = catalog_api.list_products(limit=20)
    assert_status(products_response, 200, "Get products for UI checkout")
    product_payload = next(
        item for item in products_response.json()["items"] if item["stock"] > 0
    )
    product = Product.from_payload(product_payload)
    catalog_api.close()

    catalog = CatalogPage(driver, settings).load()
    catalog.add_to_cart(product)
    catalog.open_cart()

    cart = CartPage(driver, settings)
    cart.wait_until_open()
    cart.apply_coupon("WELCOME10")
    cart.select_delivery("standard")
    expected_discount = discount_for_subtotal(product.price)
    expected_shipping = 0 if product.price >= 150_000 else 8_000
    expected_total = product.price - expected_discount + expected_shipping
    cart.wait_for_total_cents(expected_total)
    assert cart.total_cents() == expected_total

    cart.fill_contact(
        "QA Synthetic",
        "qa.synthetic@example.com",
        "Test Address 1",
    )
    cart.select_payment("approved")
    order_page = cart.submit_order()
    order_page.wait_for_order_count(1)

    order_card = order_page.order_card_text()
    assert "Підтверджено" in order_card
    assert order_page.order_count() == 1
    order_id = order_page.order_id()
    assert order_id

    ui_api = ApiClient(settings, order_page.ui_workspace_token())
    try:
        orders_response = ui_api.list_orders()
        assert_status(orders_response, 200, "Read browser workspace orders")
        orders = orders_response.json()["items"]
        matching = [item for item in orders if item["id"] == order_id]
        assert len(matching) == 1, f"Expected one order {order_id}, got {matching!r}"
        detail = ui_api.order(order_id)
        assert_status(detail, 200, f"Read browser order {order_id}")
        order = detail.json()
        assert order["status"] == "confirmed"
        assert order["items"] == [{"product_id": product.id, "quantity": 1}]
        assert order["totals"]["subtotal"] == product.price
        assert order["totals"]["discount"] == expected_discount
        assert order["totals"]["shipping"] == expected_shipping
        assert order["totals"]["total"] == expected_total
        assert len(orders) == 1
    finally:
        ui_api.close()

    order_page.reload()
    order_page.wait_for_order_count(1)
    assert order_page.order_count() == 1
    assert order_page.order_id() == order_id
    assert order_page.cart_count() == "0"


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.serial
def test_double_submit_guard_creates_only_one_order(driver, settings) -> None:
    catalog_api = ApiClient(settings)
    products_response = catalog_api.list_products(limit=20)
    assert_status(products_response, 200, "Get product for double-submit test")
    product = Product.from_payload(
        next(item for item in products_response.json()["items"] if item["stock"] > 0)
    )
    catalog_api.close()

    catalog = CatalogPage(driver, settings).load()
    catalog.add_to_cart(product)
    catalog.open_cart()
    cart = CartPage(driver, settings)
    cart.wait_until_open()
    cart.fill_contact(
        "QA Synthetic",
        "qa.synthetic@example.com",
        "Test Address 1",
    )
    cart.select_payment("approved")
    order_page = cart.submit_order_twice()
    order_page.wait_for_order_count(1)

    api = ApiClient(settings, order_page.ui_workspace_token())
    try:
        orders = api.list_orders()
        assert_status(orders, 200, "Check orders after double submit")
        assert len(orders.json()["items"]) == 1, orders.json()
    finally:
        api.close()


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.negative
def test_declined_payment_keeps_cart_and_does_not_create_order(
    driver, settings
) -> None:
    catalog_api = ApiClient(settings)
    try:
        products_response = catalog_api.list_products(limit=20)
        assert_status(products_response, 200, "Get product for declined UI checkout")
        payload = next(
            (item for item in products_response.json()["items"] if item["stock"] > 0),
            None,
        )
        assert payload is not None, "Catalog must contain an in-stock product"
        product = Product.from_payload(payload)
    finally:
        catalog_api.close()

    catalog = CatalogPage(driver, settings).load()
    catalog.add_to_cart(product)
    catalog.open_cart()
    cart = CartPage(driver, settings)
    cart.wait_until_open()
    cart.fill_contact(
        "QA Synthetic",
        "qa.synthetic@example.com",
        "Test Address 1",
    )
    cart.select_payment("declined")

    ui_api = ApiClient(settings, cart.ui_workspace_token())
    try:
        error = cart.place_order_and_wait_for_error()
        assert error.strip(), "Declined payment must display a checkout error"

        orders = ui_api.list_orders()
        assert_status(orders, 200, "Verify declined UI checkout created no order")
        assert orders.json()["items"] == []
        assert product.name in cart.dialog_text()
    finally:
        ui_api.close()
