import pytest
import allure
import logging

from utils.api_client import APIClient
from config.environment import config
from mcp.test_data_generator import TestDataGenerator


# =========================
# LOGGER SETUP
# =========================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@pytest.mark.api
@pytest.mark.regression
@allure.feature("API - MCP Generated Multiple Notes")
class TestCreateMultipleNotes:


    @allure.story("Create multiple notes using MCP AI-generated test data")
    def test_create_multiple_notes(self):

        logger.info("========== TEST START: MCP CREATE MULTIPLE NOTES ==========")

        # =========================
        # INIT API CLIENT
        # =========================
        api = APIClient(config["api_base_url"])
        logger.info(f"API Base URL: {config['api_base_url']}")

        # =========================
        # LOGIN
        # =========================
        logger.info("Logging in user...")

        login_resp = api.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

        logger.info(f"Login Status Code: {login_resp.status_code}")
        logger.info(f"Login Response: {login_resp.text}")

        assert login_resp.status_code == 200, "Login failed"
        assert api.token is not None, "Token not generated"

        logger.info("Login successful. Token generated.")

        # =========================
        # MCP TEST DATA GENERATION
        # =========================
        logger.info("Generating test data using MCP...")

        generator = TestDataGenerator()
        notes_data = generator.generate_note_data()

        logger.info(f"MCP Generated Data: {notes_data}")

        assert isinstance(notes_data, list), "MCP did not return list"
        assert len(notes_data) >= 3, "MCP should generate at least 3 notes"

        created_note_ids = []

        # =========================
        # CREATE NOTES
        # =========================
        for note in notes_data:

            logger.info(f"Creating note -> Title: {note['title']}")

            with allure.step(f"Creating note: {note['title']}" ):

                create_resp = api.create_note(
                    category=note["category"],
                    title=note["title"],
                    description=note["description"]
                )

                logger.info(f"Create Response Code: {create_resp.status_code}")
                logger.info(f"Create Response Body: {create_resp.text}")

                assert create_resp.status_code == 200, f"Failed to create note: {note['title']}"

                response_json = create_resp.json()

                note_id = response_json.get("data", {}).get("_id")

                logger.info(f"Extracted Note ID: {note_id}")

                if note_id:
                    created_note_ids.append(note_id)

                assert response_json.get("message") == "Note successfully created"

        # =========================
        # VALIDATE NOTES
        # =========================
        logger.info("Validating created notes...")

        with allure.step("Validate notes are present in system"):

            get_resp = api.get_notes()

            logger.info(f"Get Notes Status Code: {get_resp.status_code}")
            logger.info(f"Get Notes Response: {get_resp.text}")

            assert get_resp.status_code == 200

            notes_list = get_resp.json().get("data", [])

            logger.info(f"Total Notes Found: {len(notes_list)}")

            assert isinstance(notes_list, list)
            assert len(notes_list) > 0

        # =========================
        # CLEANUP
        # =========================
        logger.info("Starting cleanup of created notes...")

        with allure.step("Cleanup created notes"):

            for note_id in created_note_ids:

                logger.info(f"Deleting note ID: {note_id}")

                delete_resp = api.delete_note(note_id)

                logger.info(f"Delete Response Code: {delete_resp.status_code}")
                logger.info(f"Delete Response Body: {delete_resp.text}")

                assert delete_resp.status_code in [200, 204], f"Delete failed for {note_id}"

        logger.info("========== TEST COMPLETED SUCCESSFULLY ==========")