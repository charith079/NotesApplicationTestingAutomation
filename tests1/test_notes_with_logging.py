import time
import pytest
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config
from utils.logger import get_logger

# 🔹 Initialize logger
logger = get_logger("NotesTest")


def test_create_note_with_logging(driver):
    logger.info("===== TEST STARTED: Create Note =====")

    # 🔹 Open Application
    logger.info("Opening application URL")
    driver.get(config["base_url"])

    # 🔹 Initialize pages
    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    # 🔹 Navigate to login
    logger.info("Navigating to login page")
    login_page.go_to_login_page()

    # 🔹 Perform login
    logger.info("Performing login")
    login_page.login(
        config["credentials"]["username"],
        config["credentials"]["password"]
    )

    # 🔹 Validate login
    logger.info("Validating home page load")
    assert notes_page.is_home_page_loaded(), "Login failed"
    logger.info("Login successful [PASS]")

    # 🔹 Dynamic Test Data
    title = f"Test Note {int(time.time())}"
    description = "Automation Logging Test"
    category = "Home"

    logger.info(f"Creating note with title: {title}")

    # 🔹 Create Note
    notes_page.create_note(category, title, description)

    logger.info("Note creation submitted, validating presence")

    # 🔹 Validate Note
    if notes_page.is_note_present(title):
        logger.info("Note created successfully [PASS]")
    else:
        logger.error("Note creation failed [FAIL]")
        pytest.fail("Note was not created successfully")

    logger.info("===== TEST COMPLETED =====\n")