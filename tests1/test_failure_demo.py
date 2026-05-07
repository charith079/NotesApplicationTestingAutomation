import allure
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config


@allure.feature("Failure Demo")
@allure.story("Intentional Failure for Reporting")
def test_login_failure_demo(driver):

    with allure.step("Open application"):
        driver.get(config["base_url"])

    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    with allure.step("Navigate to login page"):
        login_page.go_to_login_page()

    with allure.step("Perform login with valid credentials"):
        login_page.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

    with allure.step("Force failure (wrong assertion)"):
        # ❌ Intentionally wrong check
        assert "invalid_page" in driver.current_url, "Intentional failure to test reporting"