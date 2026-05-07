from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time

class LoginPage(BasePage):

    # 🔹 Locators
    # login_link = (By.XPATH, "//a[contains(text(),'Login')]")
    # email = (By.ID, "email")
    # password = (By.ID, "password")
    # login_btn = (By.CSS_SELECTOR, "button[type='submit']")

    # =========================================================
    # 🔹 SELF-HEALING LOCATORS
    # =========================================================

    login_link = [
        (By.XPATH, "//a[contains(text(),'Login')]"),
        (By.LINK_TEXT, "Login"),
        (By.PARTIAL_LINK_TEXT, "Log")
    ]

    email = [
        (By.ID, "email"),
        (By.NAME, "email"),
        (By.CSS_SELECTOR, "[data-testid='login-email']"),
        (By.CSS_SELECTOR, "input[type='text']"),
        (By.XPATH, "//input[@id='email']")
    ]

    password = [
        (By.ID, "password"),
        (By.NAME, "password"),
        (By.CSS_SELECTOR, "[data-testid='login-password']"),
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.XPATH, "//input[@id='password']")
    ]

    login_btn = [
        (By.CSS_SELECTOR, "[data-testid='login-submit']"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(text(),'Login')]")
    ]

    # 🔹 Error message
    # error_message = (By.CSS_SELECTOR, "[data-testid='alert-message']")
    # error_close_btn = (By.CSS_SELECTOR, "[data-testid='alert-close']")

    error_message = [
        (By.CSS_SELECTOR, "[data-testid='alert-message']"),
        (By.CLASS_NAME, "toast-body")
    ]

    error_close_btn = [
        (By.CSS_SELECTOR, "[data-testid='alert-close']")
    ]

    # =========================================================
    # 🔹 Navigation
    # =========================================================

    def go_to_login_page(self):
        # Intelligent Wait:
        # Wait until page fully loaded before clicking
        self.wait_for_page_load()

        self.click(self.login_link)

    # =========================================================
    # 🔹 Login Action
    # =========================================================

    def login(self, username, pwd):
        # self.wait_visible(self.email)
                # Intelligent Wait:
        # Wait until input becomes stable
        self.wait_visible(self.email)

        # Intelligent Wait:
        # Wait until DOM becomes stable
        self.wait_for_dom_stability()

        self.send_keys(self.email, username)
        self.send_keys(self.password, pwd)

        # Intelligent Wait:
        # Wait until button enabled
        self.wait_clickable(self.login_btn)
        self.safe_click(self.login_btn)
        # Intelligent Wait:
        # Wait after login click
        self.wait_for_page_load()

    # =========================================================
    # 🔹 FIXED: Get error message (STABLE + WAIT ADDED)
    # =========================================================

    def get_error_message(self):
        end_time = time.time() + 10

        while time.time() < end_time:
            for locator in self.error_message:
                try:
                    elements = self.driver.find_elements(*locator)

                    for el in elements:
                        text = el.text.strip()
                        if el.is_displayed() and text:
                            return text
                except:
                    continue

            time.sleep(0.5)

        return ""

    # =========================================================
    # 🔹 FIXED: Better validation helper
    # =========================================================

    def is_error_displayed(self):
        """
        Safer check for error visibility
        """
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.error_message)
            ).is_displayed()
        except:
            return False

    # =========================================================
    # 🔹 Optional: Close alert
    # =========================================================

    def close_error(self):
        try:
            self.safe_click(self.error_close_btn)
        except:
            pass