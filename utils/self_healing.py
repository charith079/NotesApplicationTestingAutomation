from selenium.webdriver.support.ui import WebDriverWait

from mcp.locator_suggester import LocatorSuggester
from utils.logger import get_logger


class SelfHealing:

    def __init__(self, driver , logger):
        self.logger = logger
        self.driver = driver
        self.ai = LocatorSuggester()

    # =========================================================
    # SELF HEALING CORE FUNCTION
    # =========================================================
    def find_with_healing(
        self,
        locators,
        condition,
        timeout=10
    ):

        last_exception = None

        # =====================================================
        # 1. RULE-BASED LOCATOR HEALING
        # =====================================================
        for locator in locators:

            try:
                self.logger.info(
                    f"[HEALING] Trying locator: {locator}"
                )

                element = WebDriverWait(
                    self.driver,
                    timeout
                ).until(
                    condition(locator)
                )

                self.logger.info(
                    f"[HEALING SUCCESS] {locator}"
                )

                return element

            except Exception as e:

                self.logger.warning(
                    f"[HEALING FAILED] {locator}"
                )

                last_exception = e

        # =====================================================
        # 2. AI-BASED HEALING (MCP + LONGCAT)
        # =====================================================
        self.logger.warning(
            "[MCP HEALING] All locators failed. Asking AI..."
        )

        try:

            html = self.driver.page_source

            ai_result = self.ai.suggest_locator(
                html_snippet=html,
                old_locator=str(locators)
            )

            self.logger.info(
                f"🚨 MCP AI RESPONSE:\n{ai_result}"
            )

            # =================================================
            # Extract Best Locator
            # =================================================
            new_locator = (
                ai_result.get("xpath")
                or ai_result.get("css")
            )

            if not new_locator:
                raise Exception(
                    "AI did not return valid locator"
                )

            self.logger.info(
                f"[MCP HEALING] Trying AI locator: {new_locator}"
            )

            element = WebDriverWait(
                self.driver,
                timeout
            ).until(
                condition(new_locator)
            )

            self.logger.info(
                "[MCP HEALING SUCCESS] AI locator worked"
            )

            return element

        except Exception as e:

            self.logger.error(
                f"[MCP HEALING FAILED] AI also failed: {str(e)}"
            )

            # fallback to original failure
            raise last_exception