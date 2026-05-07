import pytest
import allure
import json

from utils.api_client import APIClient
from config.environment import config
from utils.logger import get_logger


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Notes API")
@allure.story("Get Notes API")
@allure.title("TC-API-01: Validate GET /notes API returns all notes")
def test_get_notes_api():

    logger = get_logger("TC-API-01")

    logger.info("===== TC-API-01 STARTED =====")

    api = APIClient(config["api_base_url"], logger)

    # 🔐 LOGIN STEP
    with allure.step("Login to API"):
        logger.info("Performing login API call")

        login_response = api.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

        allure.attach(
            json.dumps(login_response.json(), indent=2),
            name="Login Response",
            attachment_type=allure.attachment_type.JSON
        )

    # 📥 GET NOTES STEP
    with allure.step("Send GET /notes request"):
        logger.info("Calling GET /notes API")

        response = api.get_notes()

        allure.attach(
            response.text,
            name="GET Notes Response",
            attachment_type=allure.attachment_type.JSON
        )

    # 📊 VALIDATION STEP
    with allure.step("Validate response"):
        data = response.json()

        logger.info(f"Response JSON: {data}")

        assert response.status_code == 200, \
            f"Expected 200 but got {response.status_code}"

        assert "data" in data, "Response missing 'data' key"

        assert isinstance(data["data"], list), "Data is not a list"

    logger.info("===== TC-API-01 COMPLETED SUCCESSFULLY =====")