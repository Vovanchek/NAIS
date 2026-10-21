from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from test_me.api.models import Product
from test_me.ui.base_page import BasePage


class CatalogPage(BasePage):
    _PRODUCT_GRID = (By.CSS_SELECTOR, "[data-testid='product-grid']")
    _CART_OPEN = (By.CSS_SELECTOR, "[data-testid='cart-open']")

    def load(self) -> "CatalogPage":
        self.open()
        self.wait.until(EC.visibility_of_element_located(self._PRODUCT_GRID))
        return self

    def add_to_cart(self, product: Product) -> None:
        self.click(
            (
                By.CSS_SELECTOR,
                f"[data-testid='product-{product.id}'] [data-add='{product.id}']",
            )
        )

    def open_cart(self) -> None:
        self.click(self._CART_OPEN)

    def favorite_pressed(self, product_id: str) -> str | None:
        locator = (By.CSS_SELECTOR, f"[data-favorite='{product_id}']")
        return self.wait.until(EC.visibility_of_element_located(locator)).get_attribute(
            "aria-pressed"
        )

    def toggle_favorite(self, product_id: str) -> None:
        self.click((By.CSS_SELECTOR, f"[data-favorite='{product_id}']"))

    def wait_for_favorite_state(self, product_id: str, pressed: bool) -> None:
        expected = str(pressed).lower()
        locator = (By.CSS_SELECTOR, f"[data-favorite='{product_id}']")
        self.wait.until(
            lambda driver: (
                driver.find_element(*locator).get_attribute("aria-pressed") == expected
            )
        )
