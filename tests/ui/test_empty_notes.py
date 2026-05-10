import pytest
import allure

from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config
from utils.logger import get_logger


# =========================================================
#  TC-NEG-01: Empty Note Creation Validation
# =========================================================

@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Notes Management")
@allure.story("Negative Testing - Note Creation")
@allure.title("TC-NEG-01: Validate empty note creation is blocked")
def test_empty_note_creation(driver):

    logger = get_logger("TC-NEG-01")

    logger.info("===== TC-NEG-01 STARTED =====")

    login_page = LoginPage(driver,logger)
    notes_page = NotesPage(driver,logger)

    #  OPEN APPLICATION
    with allure.step("Open application"):
        driver.get(config["base_url"])
        logger.info("Application opened")

    #  LOGIN
    with allure.step("Login with valid credentials"):
        login_page.go_to_login_page()
        login_page.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

    assert notes_page.is_home_page_loaded()

    #  ATTEMPT EMPTY NOTE CREATION
    with allure.step("Attempt to create empty note"):

        notes_page.create_note(
            category="Home",
            title="",
            description="",
            expect_success=False
        )

        logger.info("Empty note submission attempted")

    #  VALIDATE ERRORS
    with allure.step("Validate field-level error messages"):

        title_error = notes_page.get_field_error("title")
        description_error = notes_page.get_field_error("description")

        logger.info(f"Title Error: {title_error}")
        logger.info(f"Description Error: {description_error}")

        allure.attach(
            f"Title Error: {title_error}\nDescription Error: {description_error}",
            name="Validation Errors",
            attachment_type=allure.attachment_type.TEXT
        )

        assert title_error == "Title is required", \
            f"Unexpected title error: {title_error}"

        assert description_error == "Description is required", \
            f"Unexpected description error: {description_error}"


    logger.info("===== TC-NEG-01 COMPLETED =====")