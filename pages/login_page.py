from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class LoginPage(BasePage):

    # =========================================================
    #  Constructor
    # =========================================================

    def __init__(self, driver, logger):
        super().__init__(driver, logger)

        self.logger.info("LoginPage initialized")

    # =========================================================
    #  SELF-HEALING LOCATORS
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

    error_message = [
        (By.CSS_SELECTOR, "[data-testid='alert-message']"),
        (By.CLASS_NAME, "toast-body")
    ]

    error_close_btn = [
        (By.CSS_SELECTOR, "[data-testid='alert-close']")
    ]

    # =========================================================
    #  Navigation
    # =========================================================

    def go_to_login_page(self):

        self.logger.info("Navigating to login page")

        self.wait_for_page_load()

        self.click(self.login_link)

        self.logger.info("Successfully navigated to login page")

    # =========================================================
    #  Login Action
    # =========================================================

    def login(self, username, pwd):

        self.logger.info("Starting login process")

        self.logger.info("Waiting for email field")

        self.wait_visible(self.email)

        self.logger.info("Waiting for DOM stability")

        self.wait_for_dom_stability()

        self.logger.info(f"Entering username: {username}")

        self.send_keys(self.email, username)

        self.logger.info("Entering password")

        self.send_keys(self.password, pwd)

        self.logger.info("Waiting for login button")

        self.wait_clickable(self.login_btn)

        self.logger.info("Clicking login button")

        self.safe_click(self.login_btn)

        self.logger.info("Waiting for page load after login")

        self.wait_for_page_load()

        self.logger.info("Login process completed")

    # =========================================================
    #  Get Error Message
    # =========================================================

    def get_error_message(self):

        self.logger.info("Fetching login error message")

        end_time = time.time() + 10

        while time.time() < end_time:

            for locator in self.error_message:

                try:

                    elements = self.driver.find_elements(*locator)

                    for el in elements:

                        text = el.text.strip()

                        if el.is_displayed() and text:

                            self.logger.error(
                                f"Login error displayed: {text}"
                            )

                            return text

                except Exception as e:

                    self.logger.warning(
                        f"Error while reading error message: {e}"
                    )

                    continue

            time.sleep(0.5)

        self.logger.warning("No error message displayed")

        return ""

    # =========================================================
    #  Validate Error Visibility
    # =========================================================

    def is_error_displayed(self):

        self.logger.info("Checking if login error is displayed")

        try:

            result = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    self.error_message[0]
                )
            ).is_displayed()

            self.logger.info(
                f"Error visibility status: {result}"
            )

            return result

        except Exception as e:

            self.logger.warning(
                f"Error message not visible: {e}"
            )

            return False

    # =========================================================
    #  Close Error Alert
    # =========================================================

    def close_error(self):

        self.logger.info("Attempting to close login error alert")

        try:

            self.safe_click(self.error_close_btn)

            self.logger.info("Error alert closed successfully")

        except Exception as e:

            self.logger.warning(
                f"Unable to close error alert: {e}"
            )