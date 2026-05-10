import pytest
import allure
from utils.api_client import APIClient
from config.environment import config
from utils.logger import get_logger


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Notes API")
@allure.story("API Performance")
@allure.title("TC-API-02: Validate GET /notes response time < 2 seconds")
def test_get_notes_response_time():

    logger = get_logger("TC-API-02")

    logger.info("===== TC-API-02 STARTED =====")

    api = APIClient(config["api_base_url"], logger)

    #  LOGIN STEP
    with allure.step("Login to API"):
        login_response = api.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

    #  API CALL STEP
    with allure.step("Send GET /notes request and measure response time"):
        response = api.get_notes()

        allure.attach(
            f"Response Time: {response.response_time:.3f} sec",
            name="API Response Time",
            attachment_type=allure.attachment_type.TEXT
        )

    #  VALIDATION STEP
    with allure.step("Validate response time is within threshold"):

        logger.info(f"Response time: {response.response_time:.3f}s")

        assert response.response_time < 2, \
            f"API too slow: {response.response_time:.3f}s (expected < 2s)"

    logger.info("===== TC-API-02 COMPLETED =====")