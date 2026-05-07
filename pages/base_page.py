from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    # 🔹 Find element
    def find(self, locator):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )

    # 🔹 Wait for visible element
    def wait_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    # 🔹 Wait for clickable element
    def wait_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    # 🔹 Send keys (UPDATED NAME ✅)
    def send_keys(self, locator, text):
        element = self.wait_visible(locator)
        element.clear()
        element.send_keys(text)

    # 🔹 Click (with fallback)
    def click(self, locator):
        element = self.wait_clickable(locator)

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
        return self.wait_visible(locator).text