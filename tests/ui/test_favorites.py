import pytest

from test_me.api.assertions import assert_status
from test_me.api.client import ApiClient
from test_me.api.models import Product
from test_me.ui.catalog_page import CatalogPage


@pytest.mark.ui
@pytest.mark.regression
def test_favorite_toggle_persists_after_reload(driver, settings) -> None:
    api = ApiClient(settings)
    try:
        response = api.list_products(limit=20)
        assert_status(response, 200, "Select product for UI favorite test")
        payload = next(iter(response.json()["items"]), None)
        assert payload is not None, "Catalog must contain at least one product"
        product = Product.from_payload(payload)
    finally:
        api.close()

    catalog = CatalogPage(driver, settings).load()
    assert catalog.favorite_pressed(product.id) == "false"
    catalog.toggle_favorite(product.id)
    catalog.wait_for_favorite_state(product.id, True)

    catalog.reload()
    assert catalog.favorite_pressed(product.id) == "true"

    catalog.toggle_favorite(product.id)
    catalog.wait_for_favorite_state(product.id, False)
