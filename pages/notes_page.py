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
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.home_logo)
            )
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.logout_btn)
            )
            return True
        except:
            return False

    # =========================================================
    # 🔹 CREATE NOTE (POSITIVE + NEGATIVE SAFE)
    # =========================================================

    def create_note(self, category, title, description, expect_success=True):

        self.safe_click(self.add_note_btn)
        self.wait_visible(self.category_dropdown)

        Select(self.find(self.category_dropdown)).select_by_visible_text(category)

        self.send_keys(self.title_input, title)
        self.send_keys(self.description_input, description)

        element = self.wait_clickable(self.submit_btn)
        self.driver.execute_script("arguments[0].click();", element)

        # ✔ Only wait for success flow
        if expect_success:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.submit_btn)
            )

    # =========================================================
    # 🔹 Note validation (STRICT - FIXED)
    # =========================================================

    def is_note_present(self, title):
        if not title:
            return False  # 🔥 IMPORTANT FIX

        try:
            WebDriverWait(self.driver, 10).until(
                EC.text_to_be_present_in_element(self.notes_list, title)
            )
            return True
        except:
            return False

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

    def get_success_message(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.success_message)
            )
            return element.text
        except:
            return None

    # =========================================================
    # 🔴 VALIDATION ERRORS
    # =========================================================

    def get_title_error(self):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.title_error)
            ).text.strip()
        except:
            return ""

    def get_description_error(self):
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.description_error)
            ).text.strip()
        except:
            return ""

    def get_field_error(self, field):

        locator_map = {
            "title": self.title_error,
            "description": self.description_error
        }

        locator = locator_map.get(field)

        if not locator:
            return ""

        try:
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(locator)
            ).text.strip()
        except:
            return ""