import pytest
import allure
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config
from utils.logger import get_logger


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.login

@allure.feature("Authentication")
@allure.story("Login")
@allure.title("TC-UI-01: Validate successful login with valid credentials")
def test_login(driver):

    logger = get_logger("test_login")

    logger.info("===== TEST STARTED: LOGIN =====")

    with allure.step("Open application"):
        driver.get(config["base_url"])

    login_page = LoginPage(driver , logger)
    notes_page = NotesPage(driver , logger)

    with allure.step("Navigate to login page"):
        login_page.go_to_login_page()

    with allure.step("Enter credentials and login"):
        login_page.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

    with allure.step("Validate dashboard loaded"):
        assert notes_page.is_home_page_loaded(), "Login failed"

    logger.info("Login successful")