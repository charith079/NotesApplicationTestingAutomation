from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.self_healing import SelfHealing
from utils.retry_handler import retry_on_failure
from utils.intelligent_waits import IntelligentWaits

class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.healer = SelfHealing(driver)
        self.smart_wait = IntelligentWaits(driver)

    # 🔹 Find element
    # def find(self, locator):
    #     return WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located(locator)
    #     )
    
    def find(self, locator, timeout=10):

        locators = locator if isinstance(locator, list) else [locator]

        return self.healer.find_with_healing(
            locators,
            EC.presence_of_element_located,
            timeout
        )


    # 🔹 Wait for visible element
    # def wait_visible(self, locator, timeout=10):
    #     return WebDriverWait(self.driver, timeout).until(
    #         EC.visibility_of_element_located(locator)
    #     )
    def wait_visible(self, locator, timeout=10):

        locators = locator if isinstance(locator, list) else [locator]

        return self.healer.find_with_healing(
            locators,
            EC.visibility_of_element_located,
            timeout
        )

    # 🔹 Wait for clickable element
    # def wait_clickable(self, locator, timeout=10):
    #     return WebDriverWait(self.driver, timeout).until(
    #         EC.element_to_be_clickable(locator)
    #     )
    def wait_clickable(self, locator, timeout=10):

        locators = locator if isinstance(locator, list) else [locator]

        return self.healer.find_with_healing(
            locators,
            EC.element_to_be_clickable,
            timeout
        )

    # 🔹 Send keys (UPDATED NAME ✅)
    @retry_on_failure(max_retries=3, delay=2)
    def send_keys(self, locator, text):
        # element = self.wait_visible(locator)
        # Intelligent waits
        self.smart_wait.wait_for_page_load()
        element = self.smart_wait.smart_wait_visible(locator)
        self.smart_wait.wait_for_stability()

        element.clear()
        element.send_keys(text)

    # 🔹 Click (with fallback)
    @retry_on_failure(max_retries=3, delay=2)
    def click(self, locator):
        # element = self.wait_clickable(locator)
        self.smart_wait.wait_for_page_load()
        element = self.smart_wait.smart_wait_clickable(locator)
        self.smart_wait.wait_for_stability()

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    # 🔹 Safe click (JS based)
    def safe_click(self, locator):
        element = self.wait_clickable(locator)
        self.driver.execute_script("arguments[0].click();", element)

    # 🔹 Get text
    def get_text(self, locator):
        return self.wait_visible(locator).text.strip()
    
    def wait_for_page_load(self):
        self.smart_wait.wait_for_page_load()

    def wait_for_dom_stability(self):
        self.smart_wait.wait_for_dom_stability()

    def wait_for_element_stable(self, locator):
        self.smart_wait.wait_for_element_stable(locator)

    def wait_for_text(self, element):
        self.smart_wait.wait_for_text(element)