import pytest

from test_me.ui.catalog_page import CatalogPage


@pytest.mark.ui
@pytest.mark.regression
def test_favorite_toggle_persists_after_reload(driver, settings) -> None:
    catalog = CatalogPage(driver, settings).load()
    assert catalog.favorite_pressed("p01") == "false"
    catalog.toggle_favorite("p01")
    catalog.wait_for_favorite_state("p01", True)

    catalog.reload()
    assert catalog.favorite_pressed("p01") == "true"

    catalog.toggle_favorite("p01")
    catalog.wait_for_favorite_state("p01", False)
