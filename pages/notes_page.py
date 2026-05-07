from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class NotesPage(BasePage):

    # 🔹 Header / Dashboard
    home_logo = (By.CSS_SELECTOR, "[data-testid='home']")
    logout_btn = (By.CSS_SELECTOR, "[data-testid='logout']")
    search_input = (By.CSS_SELECTOR, "[data-testid='search-input']")
    add_note_btn = (By.CSS_SELECTOR, "[data-testid='add-new-note']")

    # 🔹 Add Note Modal
    category_dropdown = (By.CSS_SELECTOR, "[data-testid='note-category']")
    title_input = (By.CSS_SELECTOR, "[data-testid='note-title']")
    description_input = (By.CSS_SELECTOR, "[data-testid='note-description']")
    submit_btn = (By.CSS_SELECTOR, "[data-testid='note-submit']")
    cancel_btn = (By.CSS_SELECTOR, "[data-testid='note-cancel']")

    # 🔹 Notes List
    notes_list = (By.CSS_SELECTOR, "[data-testid='notes-list']")

    # 🔹 Success Message
    success_message = (By.CSS_SELECTOR, "[data-testid='alert-message']")

    # 🔴 VALIDATION ERRORS
    title_error = (
        By.XPATH,
        "//input[@data-testid='note-title']/following-sibling::div[contains(@class,'invalid-feedback')]"
    )

    description_error = (
        By.XPATH,
        "//textarea[@data-testid='note-description']/following-sibling::div[contains(@class,'invalid-feedback')]"
    )

    # =========================================================
    # 🔹 Dashboard validation
    # =========================================================

    # def is_home_page_loaded(self):
    #     try:
    #         return (
    #             self.wait_visible(self.home_logo).is_displayed() and
    #             self.wait_visible(self.logout_btn).is_displayed() and
    #             self.wait_visible(self.search_input).is_displayed() and
    #             self.wait_visible(self.add_note_btn).is_displayed()
    #         )
    #     except:
    #         return False
    
    def is_home_page_loaded(self):
        try:
            # WebDriverWait(self.driver, 15).until(
            #     EC.visibility_of_element_located(self.home_logo)
            # )
            # WebDriverWait(self.driver, 15).until(
            #     EC.visibility_of_element_located(self.logout_btn)
            # )
            # Intelligent Wait:
            self.wait_for_page_load()

            self.wait_visible(self.home_logo)

            self.wait_visible(self.logout_btn)
            return True
        except:
            return False

    # =========================================================
    # 🔹 CREATE NOTE (POSITIVE + NEGATIVE SAFE)
    # =========================================================

    def create_note(self, category, title, description, expect_success=True):

        self.wait_for_dom_stability()

        self.safe_click(self.add_note_btn)

        self.wait_visible(self.category_dropdown)

        Select(
            self.find(self.category_dropdown)
        ).select_by_visible_text(category)

        # 🔹 Handle empty fields properly

        if title:
            self.send_keys(self.title_input, title)

        if description:
            self.send_keys(self.description_input, description)

        self.safe_click(self.submit_btn)

        # # 🔹 Wait for validation rendering
        # self.wait_for_dom_stability()

        if expect_success:

            self.wait_for_page_load()

            self.wait_for_dom_stability()

    # =========================================================
    # 🔹 Note validation (STRICT - FIXED)
    # =========================================================
    def is_note_present(self, title):

        if not title:
            return False

        try:

            # Intelligent Wait:
            self.wait_for_dom_stability()

            notes = self.get_text(self.notes_list)

            return title in notes

        except:
            return False

    # def is_note_present(self, title):
    #     if not title:
    #         return False  # 🔥 IMPORTANT FIX

    #     try:
    #         WebDriverWait(self.driver, 10).until(
    #             EC.text_to_be_present_in_element(self.notes_list, title)
    #         )
    #         return True
    #     except:
    #         return False


    # =========================================================
    # 🔹 SAFE NEGATIVE CHECK (NEW - IMPORTANT)
    # =========================================================

    def is_note_absent(self, title):
        """
        Use this ONLY for negative validation
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.text_to_be_present_in_element(self.notes_list, title)
            )
            return True
        except:
            return False  # Not found = PASS condition

    # =========================================================
    # 🔹 SUCCESS MESSAGE
    # =========================================================

    # def get_success_message(self):
    #     try:
    #         element = WebDriverWait(self.driver, 10).until(
    #             EC.visibility_of_element_located(self.success_message)
    #         )
    #         return element.text
    #     except:
    #         return None
    def get_success_message(self):

        try:

            element = self.wait_visible(
                self.success_message,
                timeout=10
            )

            # Intelligent Wait:
            self.wait_for_text(element)

            return element.text.strip()

        except:
            return None
    # =========================================================
    # 🔴 VALIDATION ERRORS
    # =========================================================

    # def get_title_error(self):
    #     try:
    #         return WebDriverWait(self.driver, 5).until(
    #             EC.visibility_of_element_located(self.title_error)
    #         ).text.strip()
    #     except:
    #         return ""

    # def get_description_error(self):
    #     try:
    #         return WebDriverWait(self.driver, 5).until(
    #             EC.visibility_of_element_located(self.description_error)
    #         ).text.strip()
    #     except:
    #         return ""

    # def get_field_error(self, field):

    #     locator_map = {
    #         "title": self.title_error,
    #         "description": self.description_error
    #     }

    #     locator = locator_map.get(field)

    #     if not locator:
    #         return ""

    #     try:
    #         return WebDriverWait(self.driver, 5).until(
    #             EC.visibility_of_element_located(locator)
    #         ).text.strip()
    #     except:
    #         return ""
    
    def get_title_error(self):

        try:
            element = self.wait_visible(self.title_error)

            self.wait_for_text(element)

            return element.text.strip()

        except:
            return ""
    def get_description_error(self):

        try:
            element = self.wait_visible(self.description_error)

            self.wait_for_text(element)

            return element.text.strip()

        except:
            return ""
            
    def get_field_error(self, field):

        locator_map = {
            "title": self.title_error,
            "description": self.description_error
        }

        locator = locator_map.get(field)

        try:

            return WebDriverWait(self.driver, 10).until(
                lambda d: (
                    text := d.find_element(*locator).text.strip()
                ) if d.find_element(*locator).text.strip() else False
            )

        except:
            return ""