from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from test_me.ui.base_page import BasePage
from test_me.ui.orders_page import OrdersPage
from test_me.utils.money import parse_uah


class CartPage(BasePage):
    _DIALOG = (By.ID, "bag-dialog")
    _COUPON = (By.CSS_SELECTOR, "[data-testid='coupon']")
    _APPLY_COUPON = (By.ID, "apply-coupon")
    _DELIVERY = (By.ID, "delivery")
    _NAME = (By.ID, "customer-name")
    _EMAIL = (By.ID, "email")
    _ADDRESS = (By.ID, "address")
    _PAYMENT = (By.ID, "payment")
    _TOTAL = (By.CSS_SELECTOR, "[data-testid='cart-total']")
    _PLACE_ORDER = (By.CSS_SELECTOR, "[data-testid='place-order']")
    _ERROR = (By.ID, "checkout-error")

    def wait_until_open(self) -> None:
        self.wait.until(EC.visibility_of_element_located(self._DIALOG))

    def apply_coupon(self, coupon: str) -> None:
        field = self.wait.until(EC.visibility_of_element_located(self._COUPON))
        field.clear()
        field.send_keys(coupon)
        self.click(self._APPLY_COUPON)

    def select_delivery(self, delivery: str) -> None:
        Select(
            self.wait.until(EC.element_to_be_clickable(self._DELIVERY))
        ).select_by_value(delivery)

    def fill_contact(self, name: str, email: str, address: str) -> None:
        for locator, value in (
            (self._NAME, name),
            (self._EMAIL, email),
            (self._ADDRESS, address),
        ):
            field = self.wait.until(EC.visibility_of_element_located(locator))
            field.clear()
            field.send_keys(value)

    def select_payment(self, payment: str) -> None:
        Select(
            self.wait.until(EC.element_to_be_clickable(self._PAYMENT))
        ).select_by_value(payment)

    def total_cents(self) -> int:
        return parse_uah(self.visible_text(self._TOTAL))

    def wait_for_total_cents(self, expected: int) -> None:
        def total_matches(driver) -> bool:
            text = driver.find_element(*self._TOTAL).text
            return parse_uah(text) == expected

        self.wait.until(total_matches)

    def coupon_value(self) -> str:
        field = self.wait.until(EC.visibility_of_element_located(self._COUPON))
        return field.get_attribute("value") or ""

    def place_order_and_wait_for_error(self) -> str:
        self.click(self._PLACE_ORDER)
        return self.checkout_error()

    def dialog_text(self) -> str:
        return self.visible_text(self._DIALOG)

    def checkout_error(self) -> str:
        return self.visible_text(self._ERROR)

    def submit_order(self) -> OrdersPage:
        self.click(self._PLACE_ORDER)
        self.wait.until(EC.url_contains("#orders"))
        return OrdersPage(self.driver, self.settings)

    def submit_order_twice(self) -> OrdersPage:
        self.driver.execute_script(
            """
            const form = document.querySelector('#checkout-form');
            form.requestSubmit();
            form.requestSubmit();
            """
        )
        self.wait.until(EC.url_contains("#orders"))
        return OrdersPage(self.driver, self.settings)
