from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class IntelligentWaits:

    def __init__(self, driver):
        self.driver = driver

    # =========================================================
    #  Normalize Locator
    # =========================================================

    def _normalize_locator(self, locator):
        """
        Handles both:
        1. Single locator tuple
           (By.ID, "email")

        2. Self-healing locator list
           [
               (By.ID, "email"),
               (By.NAME, "email")
           ]
        """

        # If locator is self-healing list → take first locator
        if isinstance(locator, list):
            return locator[0]

        return locator

    # =========================================================
    #  Wait for DOM Ready
    # =========================================================

    def wait_for_page_load(self, timeout=20):

        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )

    # =========================================================
    #  Wait for AJAX Requests
    # =========================================================

    def wait_for_ajax(self, timeout=20):

        try:

            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script(
                    "return window.jQuery != undefined "
                    "&& jQuery.active === 0"
                )
            )

        except:
            # Ignore if jQuery not present
            pass

    # =========================================================
    #  Smart Visible Wait
    # =========================================================

    def smart_wait_visible(self, locator, timeout=15):

        locator = self._normalize_locator(locator)

        return WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=0.5
        ).until(
            EC.visibility_of_element_located(locator)
        )

    # =========================================================
    # Smart Clickable Wait
    # =========================================================

    def smart_wait_clickable(self, locator, timeout=15):

        locator = self._normalize_locator(locator)

        return WebDriverWait(
            self.driver,
            timeout,
            poll_frequency=0.5
        ).until(
            EC.element_to_be_clickable(locator)
        )

    # =========================================================
    #  Wait for Text
    # =========================================================

    def wait_for_text(
        self,
        locator,
        expected_text="",
        timeout=10
    ):

        locator = self._normalize_locator(locator)

        WebDriverWait(self.driver, timeout).until(
            lambda driver: expected_text in driver.find_element(
                *locator
            ).text
        )

    # =========================================================
    #  Wait for Element Stability
    # =========================================================

    def wait_for_element_stable(
        self,
        locator,
        timeout=10
    ):

        locator = self._normalize_locator(locator)

        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

        old_location = None

        for _ in range(10):

            current_location = element.location

            if current_location == old_location:
                return True

            old_location = current_location

            time.sleep(0.3)

        return False

    # =========================================================
    #  Wait for DOM Stability
    # =========================================================

    def wait_for_dom_stability(self, wait_time=1):

        """
        Useful after:
        - Modal opens
        - React rerenders
        - AJAX calls
        """

        time.sleep(wait_time)

    # =========================================================
    #  Generic Stability Wait
    # =========================================================

    def wait_for_stability(self, seconds=1):

        time.sleep(seconds)

    # =========================================================
    #  Loader Wait
    # =========================================================

    def wait_for_loader_to_disappear(
        self,
        loader_locator,
        timeout=15
    ):

        loader_locator = self._normalize_locator(loader_locator)

        try:

            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(loader_locator)
            )

        except TimeoutException:
            pass