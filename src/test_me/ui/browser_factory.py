from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from test_me.config import Settings


def create_driver(settings: Settings) -> WebDriver:
    if settings.browser == "chrome":
        options = ChromeOptions()
        if settings.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1100")
        return webdriver.Chrome(options=options)

    if settings.browser == "firefox":
        options = FirefoxOptions()
        if settings.headless:
            options.add_argument("-headless")
        return webdriver.Firefox(options=options)

    options = EdgeOptions()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1100")
    return webdriver.Edge(options=options)
