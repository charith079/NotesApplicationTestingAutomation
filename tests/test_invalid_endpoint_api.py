import pytest
import allure
from utils.api_client import APIClient
from config.environment import config
from utils.logger import get_logger


# =========================================================
# 🔷 TC-NEG-03: Invalid API Endpoint Validation
# =========================================================

@pytest.mark.api
@pytest.mark.negative
@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("API Routing")
@allure.story("Invalid Endpoint Handling")
@allure.title("TC-NEG-03: Validate API returns 404 for invalid endpoint")
def test_invalid_api_endpoint():

    logger = get_logger("TC-NEG-03")
    logger.info("===== TC-NEG-03 STARTED =====")

    client = APIClient(config["api_base_url"], logger)

    # =========================================================
    # 🔹 STEP 1: LOGIN (valid flow baseline)
    # =========================================================
    with allure.step("Login to API"):
        login_resp = client.login(
            config["credentials"]["username"],
            config["credentials"]["password"]
        )

        logger.info(f"[LOGIN CODE] {login_resp.status_code}")
        assert login_resp.status_code == 200

    # =========================================================
    # 🔹 STEP 2: CALL INVALID ENDPOINT
    # =========================================================
    with allure.step("Send request to invalid endpoint"):

        response = client.get_invalid_endpoint("hello/invalidEndpoint123")

        logger.info(f"[RESPONSE CODE] {response.status_code}")
        logger.info(f"[RESPONSE BODY] {response.text}")

        # Safe parsing (JSON / HTML)
        try:
            body = response.json()
            is_json = True
        except:
            body = response.text
            is_json = False

        allure.attach(
            str(body),
            name="Invalid Endpoint Response",
            attachment_type=allure.attachment_type.TEXT
        )

    # =========================================================
    # 🔹 ASSERTION
    # =========================================================
    with allure.step("Validate 404 response"):

        assert response.status_code == 404, \
            f"Expected 404 but got {response.status_code}. Response: {response.text}"

        logger.info("TC-NEG-03 COMPLETED SUCCESSFULLY")