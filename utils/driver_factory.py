from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_driver(browser, grid_url):

    if browser.lower() == "chrome":
        options = Options()
        options.add_argument("--start-maximized")

        driver = webdriver.Remote(
            command_executor=grid_url,
            options=options
        )

    elif browser.lower() == "firefox":
        options = FirefoxOptions()

        driver = webdriver.Remote(
            command_executor=grid_url,
            options=options
        )

    else:
        raise Exception(f"Browser not supported: {browser}")

    return driver