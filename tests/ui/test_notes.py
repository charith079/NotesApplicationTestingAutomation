import time
import pytest
import allure
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config
from utils.logger import get_logger


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.notes

@allure.feature("Notes Management")
@allure.story("Create Note")
@allure.title("TC-UI-04: Create note via UI")

def test_create_note(driver):

    logger = get_logger("test_create_note")

    logger.info("===== TEST STARTED: CREATE NOTE =====")

    # 🔹 Open Application
    with allure.step("Open application"):
        logger.info("Opening application URL")
        driver.get(config["base_url"])

    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    # 🔹 Login
    with allure.step("Login to application"):
        logger.info("Logging in with valid credentials")
        login_page.go_to_login_page()
        login_page.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

    # 🔹 Validate Dashboard
    with allure.step("Validate dashboard is loaded"):
        logger.info("Validating dashboard")
        assert notes_page.is_home_page_loaded(), "Dashboard not loaded"

    # 🔹 Dynamic Test Data
    title = f"Test Note {int(time.time())}"
    description = "Automation Test Description"
    category = "Home"

    logger.info(f"Test Data → Title: {title}, Category: {category}")

    # 🔹 Create Note
    with allure.step("Create a new note"):
        logger.info("Creating note")
        notes_page.create_note(category, title, description)

    # 🔹 Validate Note Appears
    with allure.step("Validate note is created and visible"):
        logger.info("Validating note presence in UI")
        assert notes_page.is_note_present(title), "Note was not created successfully"

    logger.info("Note created successfully")
    logger.info("===== TEST COMPLETED =====")