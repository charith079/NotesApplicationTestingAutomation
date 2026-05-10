import pytest
import allure
import time

from utils.api_client import APIClient
from config.environment import config
from utils.logger import get_logger


# =========================================================
#  TC-API-03: Delete Note via API (PARALLEL SAFE)
# =========================================================

@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Notes API")
@allure.story("Delete Note API")
@allure.title("TC-API-03: Validate DELETE /notes removes note successfully")
def test_delete_note_api():

    logger = get_logger("TC-API-03")
    logger.info("===== TC-API-03 STARTED =====")

    api = APIClient(config["api_base_url"], logger)

    #  LOGIN STEP
    with allure.step("Login to API"):
        login_resp = api.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

        assert login_resp.status_code == 200

    # CREATE UNIQUE NOTE (PARALLEL SAFE FIX)
    with allure.step("Create a fresh note for deletion"):

        unique_title = f"Delete_Test_{int(time.time() * 1000)}"

        create_resp = api.create_note(
            category="Home",   
            title=unique_title,
            description="Temp note for delete test"
        )

        #  SAFE CHECK (avoid JSON crash)
        assert create_resp.status_code in [200, 201], \
            f"Create failed: {create_resp.text}"

        try:
            create_data = create_resp.json()
            note_id = create_data["data"]["id"]
        except Exception:
            pytest.fail(f"Invalid JSON response during create: {create_resp.text}")

        logger.info(f"Created note for deletion: {note_id}")

        allure.attach(
            str(create_data),
            name="Created Note",
            attachment_type=allure.attachment_type.JSON
        )

    #  DELETE NOTE STEP
    with allure.step("Delete note via API"):

        delete_response = api.delete_note(note_id)

        logger.info(f"Delete response: {delete_response.status_code}")

        allure.attach(
            delete_response.text,
            name="Delete Response",
            attachment_type=allure.attachment_type.TEXT
        )

        assert delete_response.status_code in [200, 204], \
            f"Unexpected status code: {delete_response.status_code} | {delete_response.text}"

    #  VERIFY DELETION
    with allure.step("Verify note is deleted"):

        verify_response = api.get_notes()

        assert verify_response.status_code == 200, \
            f"Fetch notes failed: {verify_response.text}"

        try:
            notes = verify_response.json()["data"]
        except Exception:
            pytest.fail(f"Invalid JSON in get_notes: {verify_response.text}")

        deleted_exists = any(n["id"] == note_id for n in notes)

        assert not deleted_exists, "Note still exists after deletion"

    logger.info("===== TC-API-03 COMPLETED =====")