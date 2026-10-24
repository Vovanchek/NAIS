import pytest

from test_me.api.assertions import assert_status
from test_me.api.client import ApiClient
from test_me.api.models import Product
from test_me.ui.cart_page import CartPage
from test_me.ui.catalog_page import CatalogPage


def _in_stock_product(settings) -> Product:
    api = ApiClient(settings)
    try:
        response = api.list_products(limit=20)
        assert_status(response, 200, "Get products for additional UI E2E tests")
        payload = next(
            (item for item in response.json()["items"] if item["stock"] > 0), None
        )
        assert payload is not None, "Catalog must contain an in-stock product"
        return Product.from_payload(payload)
    finally:
        api.close()


@pytest.mark.ui
@pytest.mark.regression
def test_checkout_express_delivery_creates_confirmed_order(driver, settings) -> None:
    product = _in_stock_product(settings)

    catalog = CatalogPage(driver, settings).load()
    catalog.add_to_cart(product)
    catalog.open_cart()

    cart = CartPage(driver, settings)
    cart.wait_until_open()
    cart.select_delivery("express")
    expected_total = product.price + 15_000
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

    assert order_page.order_count() == 1
    assert "Підтверджено" in order_page.order_card_text()
    assert order_page.cart_count() == "0"

    order_page.reload()
    order_page.wait_for_order_count(1)
    assert order_page.order_count() == 1


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.negative
def test_checkout_rejects_invalid_payment_value_without_creating_order(
    driver, settings
) -> None:
    product = _in_stock_product(settings)

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

    driver.execute_script(
        """
        const payment = document.querySelector('#payment');
        const option = document.createElement('option');
        option.value = 'invalid-payment';
        option.textContent = 'invalid-payment';
        payment.appendChild(option);
        payment.value = 'invalid-payment';
        payment.dispatchEvent(new Event('change', { bubbles: true }));
        """
    )

    ui_api = ApiClient(settings, cart.ui_workspace_token())
    try:
        error = cart.place_order_and_wait_for_error()
        assert error.strip(), "Invalid payment value must show checkout error"

        orders = ui_api.list_orders()
        assert_status(orders, 200, "Verify invalid payment value created no order")
        assert orders.json()["items"] == []
        assert product.name in cart.dialog_text()
    finally:
        ui_api.close()
