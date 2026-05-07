import time
import pytest
import allure

from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from utils.api_client import APIClient
from config.environment import config
from utils.logger import get_logger


# =========================================================
# 🔷 TC-E2E-01: UI → API Data Consistency
# =========================================================

@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("End to End Flow")
@allure.story("UI to API Data Validation")
@allure.title("TC-E2E-01: Validate UI created note exists in API")
def test_ui_to_api_validation(driver):

    logger = get_logger("TC-E2E-01")

    logger.info("===== TC-E2E-01 STARTED =====")

    api = APIClient(config["api_base_url"], logger)

    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    # 🔹 OPEN APP
    with allure.step("Open application"):
        driver.get(config["base_url"])
        logger.info("Application opened")

    # 🔹 LOGIN UI
    with allure.step("Login via UI"):
        login_page.go_to_login_page()
        login_page.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

    assert notes_page.is_home_page_loaded()

    # 🔹 CREATE NOTE
    title = f"E2E UI Note {int(time.time())}"
    description = "UI to API validation"
    category = "Home"

    with allure.step("Create note via UI"):
        notes_page.create_note(category, title, description)

    assert notes_page.is_note_present(title)

    # 🔹 API VALIDATION
    with allure.step("Validate note in API"):
        api.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

        response = api.get_notes()
        notes = response.json()["data"]

        match = any(
            n["title"] == title and n["description"] == description
            for n in notes
        )

        allure.attach(str(notes), "API Notes Response", allure.attachment_type.TEXT)

        assert match, "Note not found in API"

    logger.info("===== TC-E2E-01 COMPLETED =====")