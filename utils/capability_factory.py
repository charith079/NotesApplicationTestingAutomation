from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class CapabilityFactory:

    @staticmethod
    def get_options(browser: str):

        browser = browser.lower()

        # ================= CHROME =================
        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-gpu")
            return options

        # ================= FIREFOX =================
        elif browser == "firefox":
            options = FirefoxOptions()
            options.add_argument("--start-maximized")
            return options

        # ================= EDGE =================
        elif browser == "edge":
            options = EdgeOptions()
            options.add_argument("--start-maximized")
            return options

        else:
            raise Exception(f"Unsupported browser: {browser}")