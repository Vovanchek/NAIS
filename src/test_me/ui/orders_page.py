import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from test_me.ui.base_page import BasePage


class OrdersPage(BasePage):
    _ORDERS_LIST = (By.ID, "orders-list")
    _ORDER_CARDS = (By.CSS_SELECTOR, "#orders-list [data-testid='order-card']")
    _CART_COUNT = (By.ID, "cart-count")

    def wait_until_loaded(self) -> None:
        self.wait.until(EC.visibility_of_element_located(self._ORDERS_LIST))

    def wait_for_order_count(self, expected_count: int) -> None:
        self.wait.until(
            lambda driver: (
                len(driver.find_elements(*self._ORDER_CARDS)) == expected_count
            )
        )

    def order_count(self) -> int:
        return len(self.driver.find_elements(*self._ORDER_CARDS))

    def cart_count(self) -> str:
        return self.visible_text(self._CART_COUNT)

    def order_card_text(self, index: int = 0) -> str:
        cards = self.wait.until(EC.presence_of_all_elements_located(self._ORDER_CARDS))
        return cards[index].text

    def order_id(self, index: int = 0) -> str:
        cards = self.wait.until(EC.presence_of_all_elements_located(self._ORDER_CARDS))
        details = cards[index].find_element(By.CSS_SELECTOR, "details")
        if not details.get_attribute("open"):
            details.find_element(By.CSS_SELECTOR, "summary").click()
        order_id_text = details.find_element(By.CSS_SELECTOR, ".order-id").text
        match = re.search(r"Повний номер:\s*(\S+)", order_id_text)
        if not match:
            raise AssertionError(
                f"Full order id not found in order details: {order_id_text!r}"
            )
        return match.group(1)
