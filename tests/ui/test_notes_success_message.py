# import time
# import pytest
# import allure
# from pages.login_page import LoginPage
# from pages.notes_page import NotesPage
# from config.environment import config
# from utils.logger import get_logger


# @pytest.mark.regression
# @pytest.mark.notes

# @allure.feature("Notes Management")
# @allure.story("Create Note - Success Message")
# @allure.title("TC-UI-06: Verify success message after note creation")

# def test_success_message_after_note_creation(driver):

#     logger = get_logger("test_success_message_note")

#     logger.info("===== TEST STARTED: SUCCESS MESSAGE VALIDATION =====")

#     #  Open Application
#     with allure.step("Open application"):
#         logger.info("Opening application URL")
#         driver.get(config["base_url"])

#     login_page = LoginPage(driver,logger)
#     notes_page = NotesPage(driver ,logger)

#     #  Login
#     with allure.step("Login with valid credentials"):
#         logger.info("Logging in")
#         login_page.go_to_login_page()
#         login_page.login(
#             config["credentials"]["username"],
#             config["credentials"]["password"]
#         )

#     #  Validate Dashboard
#     with allure.step("Validate dashboard is loaded"):
#         assert notes_page.is_home_page_loaded(), "Dashboard not loaded"

#     #  Test Data
#     title = f"Test Note {int(time.time())}"
#     description = "Success message validation"
#     category = "Home"

#     logger.info(f"Creating note → {title}")

#     #  Create Note
#     with allure.step("Create a new note"):
#         notes_page.create_note(category, title, description)

#     #  Validate Success Message
#     with allure.step("Validate success message is displayed"):
#         success_msg = notes_page.get_success_message()
#         logger.info(f"Success message: {success_msg}")

#         assert success_msg is not None, "Success message not displayed"
#         assert "success" in success_msg.lower(), \
#             f"Invalid success message: {success_msg}"

#     logger.info("Success message validated successfully")
#     logger.info("===== TEST COMPLETED =====")