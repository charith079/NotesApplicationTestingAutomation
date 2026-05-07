import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config.environment import config
from utils.capability_factory import CapabilityFactory


@pytest.fixture(scope="function")
def driver():

    browser = config.get("browser", "chrome")
    execution_mode = config.get("execution_mode", "local")

    options = CapabilityFactory.get_options(browser)

    driver = None  # IMPORTANT for safety

    # ======================================================
    # 🔵 LOCAL EXECUTION
    # ======================================================
    if execution_mode == "local":

        if browser == "chrome":
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
        else:
            raise Exception("Local execution supports only Chrome for now")

    # ======================================================
    # 🔴 SELENIUM GRID EXECUTION
    # ======================================================
    elif execution_mode == "remote":

        grid_url = config.get("grid_url", "http://localhost:4444/wd/hub")

        driver = webdriver.Remote(
            command_executor=grid_url,
            options=options
        )

    # ======================================================
    # 🟣 CLOUD EXECUTION (future ready)
    # ======================================================
    elif execution_mode in ["browserstack", "lambdatest"]:

        driver = webdriver.Remote(
            command_executor=config.get("grid_url"),
            options=options
        )

    else:
        raise Exception(f"Invalid execution mode: {execution_mode}")

    driver.maximize_window()

    yield driver

    driver.quit()