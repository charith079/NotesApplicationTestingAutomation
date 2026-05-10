from utils.api_client import APIClient
from config.environment import config
from utils.logger import get_logger


logger = get_logger("API_TESTS")


def setup_api():

    logger.info("Initializing API Client")

    api = APIClient(config["api_base_url"])

    logger.info("Performing API Login")

    api.login(
        config["credentials"]["username"],
        config["credentials"]["password"]
    )

    logger.info("API Login Successful")

    return api


# =========================================================
# TC-API-01 → GET Notes
# =========================================================
def test_get_notes():

    logger.info("===== TEST STARTED: GET NOTES =====")

    api = setup_api()

    logger.info("Sending GET Notes request")

    response = api.get_notes()

    data = response.json()

    logger.info(f"GET Notes Response: {data}")

    # Validations
    assert response.status_code == 200

    logger.info("Validated status code = 200")

    assert "data" in data

    logger.info("'data' key present in response")

    assert isinstance(data["data"], list)

    logger.info("Validated response data is list")

    logger.info("===== TEST PASSED: GET NOTES =====")


# =========================================================
# TC-API-03 → Delete Note
# =========================================================
def test_delete_note():

    logger.info("===== TEST STARTED: DELETE NOTE =====")

    api = setup_api()

    logger.info("Fetching existing notes")

    notes = api.get_notes().json()["data"]

    if not notes:

        logger.warning("No notes available to delete")

        return

    note_id = notes[0]["id"]

    logger.info(f"Deleting note with ID: {note_id}")

    response = api.delete_note(note_id)

    logger.info(
        f"Delete API Response Status: {response.status_code}"
    )

    # Validate deletion
    logger.info("Validating note deletion")

    updated_notes = api.get_notes().json()["data"]

    assert note_id not in [
        note["id"] for note in updated_notes
    ]

    logger.info("Note deletion validated successfully")

    logger.info("===== TEST PASSED: DELETE NOTE =====")