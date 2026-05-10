import pytest
import allure
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config
from utils.logger import get_logger


@pytest.mark.regression
@pytest.mark.login
@pytest.mark.negative
@pytest.mark.serial
@allure.feature("Authentication")
@allure.story("Login - Negative Scenarios")

@pytest.mark.parametrize(
    "username,password,tc_id",
    [
        ("invalid_user@example.com", config["credentials"]["password"], "TC-UI-02"),
        (config["credentials"]["username"], "wrongpassword", "TC-UI-03"),
    ]
)

def test_invalid_login(driver, username, password, tc_id):

    logger = get_logger(f"test_invalid_login_{tc_id}")

    allure.dynamic.title(f"{tc_id}: Validate invalid login")

    logger.info(f"===== TEST STARTED: {tc_id} =====")

    # 🔹 Open application
    with allure.step("Open application"):
        driver.get(config["base_url"])

    login_page = LoginPage(driver,logger)
    notes_page = NotesPage(driver , logger)

    # 🔹 Navigate to login page
    with allure.step("Navigate to login page"):
        login_page.go_to_login_page()

    # 🔹 Perform login with invalid data
    with allure.step("Enter invalid credentials and login"):
        login_page.login(username, password)

    # 🔹 Validate error message
    with allure.step("Validate error message is displayed"):
        error_text = login_page.get_error_message()
        logger.info(f"Error message displayed: {error_text}")
        assert error_text != "", "Error message not displayed"

    # 🔹 Validate user NOT logged in (same approach as positive test)
    with allure.step("Validate user remains on login page"):
        assert not notes_page.is_home_page_loaded(), "User should NOT be logged in"

    logger.info(f"{tc_id} executed successfully")
    logger.info(f"===== TEST COMPLETED: {tc_id} =====")