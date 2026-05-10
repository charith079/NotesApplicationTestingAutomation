# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.self_healing import SelfHealing
from utils.retry_handler import retry_on_failure
from utils.intelligent_waits import IntelligentWaits


class BasePage:

    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

        self.healer = SelfHealing(driver, logger)
        self.smart_wait = IntelligentWaits(driver)

        self.logger.info(f"{self.__class__.__name__} initialized")

    # =========================================================
    #  Find Element
    # =========================================================

    def find(self, locator, timeout=10):

        self.logger.info(f"Finding element: {locator}")

        locators = locator if isinstance(locator, list) else [locator]

        element = self.healer.find_with_healing(
            locators,
            EC.presence_of_element_located,
            timeout
        )

        self.logger.info(f"Element found: {locator}")

        return element

    # =========================================================
    #  Wait Visible
    # =========================================================

    def wait_visible(self, locator, timeout=10):

        self.logger.info(f"Waiting for visible element: {locator}")

        locators = locator if isinstance(locator, list) else [locator]

        element = self.healer.find_with_healing(
            locators,
            EC.visibility_of_element_located,
            timeout
        )

        self.logger.info(f"Element visible: {locator}")

        return element

    # =========================================================
    #  Wait Clickable
    # =========================================================

    def wait_clickable(self, locator, timeout=10):

        self.logger.info(f"Waiting for clickable element: {locator}")

        locators = locator if isinstance(locator, list) else [locator]

        element = self.healer.find_with_healing(
            locators,
            EC.element_to_be_clickable,
            timeout
        )

        self.logger.info(f"Element clickable: {locator}")

        return element

    # =========================================================
    #  Send Keys
    # =========================================================

    @retry_on_failure(max_retries=3, delay=2)
    def send_keys(self, locator, text):

        self.logger.info(f"Sending text to element: {locator}")
        self.logger.info(f"Input text: {text}")

        self.smart_wait.wait_for_page_load()

        element = self.wait_visible(locator)

        self.smart_wait.wait_for_stability()

        element.clear()
        element.send_keys(text)

        self.logger.info("Text entered successfully")

    # =========================================================
    #  Click
    # =========================================================

    @retry_on_failure(max_retries=3, delay=2)
    def click(self, locator):

        self.logger.info(f"Clicking element: {locator}")

        self.smart_wait.wait_for_page_load()

        element = self.wait_clickable(locator)

        self.smart_wait.wait_for_stability()

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            element
        )

        try:
            element.click()
            self.logger.info("Normal click successful")

        except Exception as e:

            self.logger.warning(
                f"Normal click failed. Using JS click. Error: {e}"
            )

            self.driver.execute_script(
                "arguments[0].click();",
                element
            )

            self.logger.info("JS click successful")

    # =========================================================
    #  Safe Click
    # =========================================================

    def safe_click(self, locator):

        self.logger.info(f"Safe clicking element: {locator}")

        element = self.wait_clickable(locator)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

        self.logger.info("Safe click successful")

    # =========================================================
    #  Get Text
    # =========================================================

    def get_text(self, locator):

        self.logger.info(f"Getting text from element: {locator}")

        text = self.wait_visible(locator).text.strip()

        self.logger.info(f"Captured text: {text}")

        return text

    # =========================================================
    #  Intelligent Wait Wrappers
    # =========================================================

    def wait_for_page_load(self):

        self.logger.info("Waiting for page load")

        self.smart_wait.wait_for_page_load()

        self.logger.info("Page loaded successfully")

    def wait_for_dom_stability(self):

        self.logger.info("Waiting for DOM stability")

        self.smart_wait.wait_for_dom_stability()

        self.logger.info("DOM stable")

    def wait_for_element_stable(self, locator):

        self.logger.info(f"Waiting for element stability: {locator}")

        self.smart_wait.wait_for_element_stable(locator)

        self.logger.info("Element stable")

    def wait_for_text(self, element):

        self.logger.info("Waiting for text")

        self.smart_wait.wait_for_text(element)

        self.logger.info("Text appeared successfully")