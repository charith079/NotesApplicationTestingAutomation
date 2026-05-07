import time
import pytest
import allure
from pages.login_page import LoginPage
from pages.notes_page import NotesPage
from config.environment import config


# 🔹 Step functions for Allure reporting

@allure.step("Open application URL")
def open_application(driver):
    driver.get(config["base_url"])


@allure.step("Navigate to login page")
def navigate_to_login(login_page):
    login_page.go_to_login_page()


@allure.step("Login with username: {username}")
def perform_login(login_page, username, password):
    login_page.login(username, password)


@allure.step("Validate home page is loaded")
def validate_home(notes_page):
    assert notes_page.is_home_page_loaded(), "Home page not loaded"


@allure.step("Create note with Title: {title}, Category: {category}")
def create_note(notes_page, category, title, description):
    notes_page.create_note(category, title, description)


@allure.step("Validate note is present: {title}")
def validate_note(notes_page, title):
    assert notes_page.is_note_present(title), "Note not found"


# 🔹 Main Test with Allure metadata

@allure.feature("Notes Application")
@allure.story("Create Note via UI")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify user can create a note successfully")
@allure.description("This test verifies that a user can login and create a note, and the note appears in UI.")
def test_create_note_allure(driver):

    # 🔹 Initialize Pages
    login_page = LoginPage(driver)
    notes_page = NotesPage(driver)

    # 🔹 Steps
    open_application(driver)
    navigate_to_login(login_page)

    perform_login(
        login_page,
        config["credentials"]["username"],
        config["credentials"]["password"]
    )

    validate_home(notes_page)

    # 🔹 Dynamic Test Data
    title = f"Test Note {int(time.time())}"
    description = "Allure Automation Test"
    category = "Home"

    # 🔹 Attach test data to report
    allure.attach(title, name="Note Title", attachment_type=allure.attachment_type.TEXT)
    allure.attach(description, name="Note Description", attachment_type=allure.attachment_type.TEXT)

    create_note(notes_page, category, title, description)

    validate_note(notes_page, title)