from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class NotesPage(BasePage):

    # =========================================================
    #  Constructor
    # =========================================================

    def __init__(self, driver, logger):
        super().__init__(driver, logger)

        self.logger.info("NotesPage initialized")

    # =========================================================
    #  Header / Dashboard
    # =========================================================

    home_logo = (By.CSS_SELECTOR, "[data-testid='home']")
    logout_btn = (By.CSS_SELECTOR, "[data-testid='logout']")
    search_input = (By.CSS_SELECTOR, "[data-testid='search-input']")
    add_note_btn = (By.CSS_SELECTOR, "[data-testid='add-new-note']")

    # =========================================================
    #  Add Note Modal
    # =========================================================

    category_dropdown = (By.CSS_SELECTOR, "[data-testid='note-category']")
    title_input = (By.CSS_SELECTOR, "[data-testid='note-title']")
    description_input = (By.CSS_SELECTOR, "[data-testid='note-description']")
    submit_btn = (By.CSS_SELECTOR, "[data-testid='note-submit']")
    cancel_btn = (By.CSS_SELECTOR, "[data-testid='note-cancel']")

    # =========================================================
    # Notes List
    # =========================================================

    notes_list = (By.CSS_SELECTOR, "[data-testid='notes-list']")

    # =========================================================
    #  Success Message
    # =========================================================

    success_message = (By.CSS_SELECTOR, "[data-testid='alert-message']")

    # =========================================================
    # Validation Errors
    # =========================================================

    title_error = (
        By.XPATH,
        "//input[@data-testid='note-title']/following-sibling::div[contains(@class,'invalid-feedback')]"
    )

    description_error = (
        By.XPATH,
        "//textarea[@data-testid='note-description']/following-sibling::div[contains(@class,'invalid-feedback')]"
    )

    # =========================================================
    #  Dashboard Validation
    # =========================================================

    def is_home_page_loaded(self):

        self.logger.info("Validating Notes dashboard")

        try:

            self.wait_for_page_load()

            self.wait_visible(self.home_logo)

            self.wait_visible(self.logout_btn)

            self.logger.info("Dashboard loaded successfully")

            return True

        except Exception as e:

            self.logger.error(
                f"Dashboard validation failed: {e}"
            )

            return False

    # =========================================================
    #  Create Note
    # =========================================================

    def create_note(
        self,
        category,
        title,
        description,
        expect_success=True
    ):

        self.logger.info("Starting note creation")

        self.logger.info(
            f"Category: {category}, Title: {title}"
        )

        self.wait_for_dom_stability()

        self.logger.info("Clicking Add Note button")

        self.safe_click(self.add_note_btn)

        self.logger.info("Waiting for note modal")

        self.wait_visible(self.category_dropdown)

        self.logger.info(
            f"Selecting category: {category}"
        )

        Select(
            self.find(self.category_dropdown)
        ).select_by_visible_text(category)

        if title:

            self.logger.info(
                f"Entering note title: {title}"
            )

            self.send_keys(self.title_input, title)

        else:

            self.logger.warning(
                "Title field left empty"
            )

        if description:

            self.logger.info(
                "Entering note description"
            )

            self.send_keys(
                self.description_input,
                description
            )

        else:

            self.logger.warning(
                "Description field left empty"
            )

        self.logger.info("Submitting note")

        self.safe_click(self.submit_btn)

        if expect_success:

            self.logger.info(
                "Waiting for successful note creation"
            )

            self.wait_for_page_load()

            self.wait_for_dom_stability()

            self.logger.info(
                "Note created successfully"
            )

    # =========================================================
    #  Validate Note Presence
    # =========================================================

    def is_note_present(self, title):

        self.logger.info(
            f"Checking if note exists: {title}"
        )

        if not title:

            self.logger.warning(
                "Empty title passed for validation"
            )

            return False

        try:

            self.wait_for_dom_stability()

            notes = self.get_text(self.notes_list)

            result = title in notes

            self.logger.info(
                f"Note presence result: {result}"
            )

            return result

        except Exception as e:

            self.logger.error(
                f"Error checking note presence: {e}"
            )

            return False

    # =========================================================
    #  Validate Note Absence
    # =========================================================

    def is_note_absent(self, title):

        self.logger.info(
            f"Checking if note is absent: {title}"
        )

        try:

            WebDriverWait(self.driver, 5).until(
                EC.text_to_be_present_in_element(
                    self.notes_list,
                    title
                )
            )

            self.logger.warning(
                "Note unexpectedly found"
            )

            return True

        except Exception:

            self.logger.info(
                "Note correctly absent"
            )

            return False

    # =========================================================
    #  Success Message
    # =========================================================

    def get_success_message(self):

        self.logger.info(
            "Fetching success message"
        )

        try:

            element = self.wait_visible(
                self.success_message,
                timeout=10
            )

            self.wait_for_text(element)

            message = element.text.strip()

            self.logger.info(
                f"Success message: {message}"
            )

            return message

        except Exception as e:

            self.logger.error(
                f"Unable to fetch success message: {e}"
            )

            return None

    # =========================================================
    #  Title Validation Error
    # =========================================================

    def get_title_error(self):

        self.logger.info(
            "Fetching title validation error"
        )

        try:

            element = self.wait_visible(
                self.title_error
            )

            self.wait_for_text(element)

            error = element.text.strip()

            self.logger.warning(
                f"Title error: {error}"
            )

            return error

        except Exception as e:

            self.logger.error(
                f"Unable to fetch title error: {e}"
            )

            return ""

    # =========================================================
    #  Description Validation Error
    # =========================================================

    def get_description_error(self):

        self.logger.info(
            "Fetching description validation error"
        )

        try:

            element = self.wait_visible(
                self.description_error
            )

            self.wait_for_text(element)

            error = element.text.strip()

            self.logger.warning(
                f"Description error: {error}"
            )

            return error

        except Exception as e:

            self.logger.error(
                f"Unable to fetch description error: {e}"
            )

            return ""

    # =========================================================
    #  Generic Field Error
    # =========================================================

    def get_field_error(self, field):

        self.logger.info(
            f"Fetching validation error for field: {field}"
        )

        locator_map = {
            "title": self.title_error,
            "description": self.description_error
        }

        locator = locator_map.get(field)

        if not locator:

            self.logger.error(
                f"Invalid field provided: {field}"
            )

            return ""

        try:

            error = WebDriverWait(self.driver, 10).until(
                lambda d: (
                    text := d.find_element(
                        *locator
                    ).text.strip()
                ) if d.find_element(
                    *locator
                ).text.strip() else False
            )

            self.logger.warning(
                f"{field} validation error: {error}"
            )

            return error

        except Exception as e:

            self.logger.error(
                f"Unable to fetch field error: {e}"
            )

            return ""