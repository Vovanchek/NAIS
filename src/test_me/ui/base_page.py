from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from test_me.config import Settings


class BasePage:
    def __init__(
        self,
        driver: WebDriver,
        settings: Settings,
        timeout: float = 12.0,
    ) -> None:
        self.driver = driver
        self.settings = settings
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> None:
        self.driver.get(f"{self.settings.base_url}/")

    def reload(self) -> None:
        self.driver.refresh()

    def click(self, locator: tuple[str, str]) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def visible_text(self, locator: tuple[str, str]) -> str:
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def ui_workspace_token(self) -> str:
        token = self.driver.execute_script(
            "return JSON.parse(localStorage.getItem('test-me:v2') || '{}').token"
        )
        if not isinstance(token, str) or not token:
            raise AssertionError("UI workspace token was not available in localStorage")
        return token
