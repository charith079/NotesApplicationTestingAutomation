from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class LoginPage(BasePage):

    # 🔹 Locators
    login_link = (By.XPATH, "//a[contains(text(),'Login')]")
    email = (By.ID, "email")
    password = (By.ID, "password")
    login_btn = (By.CSS_SELECTOR, "button[type='submit']")

    # 🔹 Error message
    error_message = (By.CSS_SELECTOR, "[data-testid='alert-message']")
    error_close_btn = (By.CSS_SELECTOR, "[data-testid='alert-close']")

    # =========================================================
    # 🔹 Navigation
    # =========================================================

    def go_to_login_page(self):
        self.click(self.login_link)

    # =========================================================
    # 🔹 Login Action
    # =========================================================

    def login(self, username, pwd):
        self.wait_visible(self.email)

        self.send_keys(self.email, username)
        self.send_keys(self.password, pwd)

        self.safe_click(self.login_btn)

    # =========================================================
    # 🔹 FIXED: Get error message (STABLE + WAIT ADDED)
    # =========================================================

    def get_error_message(self):
        """
        Waits properly for error message before reading text.
        Fixes issue with parallel execution (xdist flakiness).
        """
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.error_message)
            )
            text = element.text.strip()
            return text if text else ""
        except:
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