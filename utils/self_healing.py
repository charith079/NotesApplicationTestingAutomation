from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SelfHealing:

    def __init__(self, driver):
        self.driver = driver

    # =========================================================
    # 🔹 TRY MULTIPLE LOCATORS
    # =========================================================

    def find_with_healing(
        self,
        locators,
        condition,
        timeout=10
    ):

        last_exception = None

        for locator in locators:

            try:

                print(f"[HEALING] Trying locator: {locator}")

                element = WebDriverWait(
                    self.driver,
                    timeout
                ).until(
                    condition(locator)
                )

                print(f"[HEALING SUCCESS] {locator}")

                return element

            except Exception as e:

                print(f"[HEALING FAILED] {locator}")

                last_exception = e

        raise last_exception