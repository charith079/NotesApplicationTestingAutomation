import pytest
import allure
from utils.api_client import APIClient
from config.environment import config
from utils.logger import get_logger


@pytest.mark.api
@pytest.mark.negative
@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("API Authentication")
@allure.story("Invalid Token Validation")
@allure.title("TC-NEG-02: Validate API rejects invalid token")
def test_invalid_api_token():

    logger = get_logger("TC-NEG-02")
    logger.info("===== TC-NEG-02 STARTED =====")

    client = APIClient(config["api_base_url"], logger)

    # 🔹 STEP 1: VALID LOGIN (baseline)
    login_resp = client.login(
        config["credentials"]["username"],
        config["credentials"]["password"]
    )

    assert login_resp.status_code == 200

    # 🔴 STEP 2: FORCE INVALID TOKEN
    client.set_token("sfags84gsd65ds4gd")

    with allure.step("Send request with invalid token"):
        response = client.get_notes()

        logger.info(f"[RESPONSE CODE] {response.status_code}")
        logger.info(f"[RESPONSE BODY] {response.text}")

        # ✅ SAFE RESPONSE HANDLING (JSON or HTML)
        try:
            response_body = response.json()
            attachment_type = allure.attachment_type.JSON
        except Exception:
            response_body = response.text
            attachment_type = allure.attachment_type.TEXT

        allure.attach(
            str(response_body),
            name="Invalid Token Response",
            attachment_type=attachment_type
        )

    # 🔹 ASSERTION
    assert response.status_code in [401, 403], \
        f"Expected 401/403 but got {response.status_code}"