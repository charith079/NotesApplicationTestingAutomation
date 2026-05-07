import time
import pytest
import allure

from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from utils.api_client import APIClient
from config.environment import config
from utils.logger import get_logger


# =========================================================
# 🔷 TC-E2E-02: API → UI Delete Validation
# =========================================================

@pytest.mark.serial
@pytest.mark.e2e
@pytest.mark.regression
@allure.feature("End to End Flow")
@allure.story("API Delete reflected in UI")
@allure.title("TC-E2E-02: Validate API delete reflected in UI")
def test_api_delete_to_ui_validation(driver):

    logger = get_logger("TC-E2E-02")

    logger.info("===== TC-E2E-02 STARTED =====")

    api = APIClient(config["api_base_url"], logger)

    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    # # 🔹 OPEN APP
    with allure.step("Login"):
        driver.get(config["base_url"])

    # 🔹 LOGIN UI
    with allure.step("Login via UI"):
        login_page.go_to_login_page()
        login_page.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

    assert notes_page.is_home_page_loaded()

    # 🔹 CREATE NOTE (UI)
    title = f"E2E Delete {int(time.time())}"
    description = "Delete validation"
    category = "Home"

    with allure.step("Create note via UI"):
        notes_page.create_note(category, title, description)

    assert notes_page.is_note_present(title)

    # 🔹 LOGIN API
    api.login(
        config["credentials"]["username"],
        config["credentials"]["password"]
    )

    # 🔹 GET NOTES & FIND ID
    with allure.step("Fetch note ID from API"):
        response = api.get_notes()
        notes = response.json()["data"]

        note_id = next(
            (n["id"] for n in notes if n["title"] == title),
            None
        )

        assert note_id is not None, "Note ID not found"

    # 🔹 DELETE VIA API
    with allure.step("Delete note via API"):
        delete_response = api.delete_note(note_id)

        assert delete_response.status_code in [200, 204]

    # 🔹 REFRESH UI
    with allure.step("Refresh UI and validate deletion"):
        driver.refresh()

        assert not notes_page.is_note_present(title)

    logger.info("===== TC-E2E-02 COMPLETED =====")