import os
from datetime import datetime

import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.environment import config

from mcp.failure_analyzer import FailureAnalyzer


# ======================================================
# PARSE CUSTOM CLI OPTION
# ======================================================
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


# ======================================================
# DRIVER FIXTURE
# ======================================================
@pytest.fixture(scope="function")
def driver(request):

    browser = request.config.getoption("--browser")
    execution_mode = config.get("execution_mode", "local")
    grid_url = config.get("grid_url")

    driver = None

    # ==================================================
    # CHROME CONFIG
    # ==================================================
    if browser == "chrome":

        options = ChromeOptions()

        # UI / popup blocking
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-save-password-bubble")

        # stability
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")

        # security / automation stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")

        # anti-renderer crash / timeout fix
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-features=TranslateUI")

        options.add_argument(
            "--enable-features=NetworkService,NetworkServiceInProcess"
        )

        options.add_argument("--max_old_space_size=4096")

        if execution_mode == "remote":

            driver = webdriver.Remote(
                command_executor=grid_url,
                options=options
            )

        else:

            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager

            driver = webdriver.Chrome(
                service=Service(
                    ChromeDriverManager().install()
                ),
                options=options
            )

    # ==================================================
    # FIREFOX CONFIG
    # ==================================================
    elif browser == "firefox":

        options = FirefoxOptions()

        options.set_preference(
            "dom.webnotifications.enabled",
            False
        )

        options.set_preference(
            "dom.push.enabled",
            False
        )

        # disable popups
        options.set_preference(
            "dom.disable_open_during_load",
            True
        )

        # performance / stability
        options.set_preference(
            "browser.tabs.remote.autostart",
            True
        )

        options.set_preference(
            "browser.cache.disk.enable",
            False
        )

        options.set_preference(
            "browser.cache.memory.enable",
            False
        )

        # reduce tracking + interruptions
        options.set_preference(
            "privacy.trackingprotection.enabled",
            True
        )

        if execution_mode == "remote":

            driver = webdriver.Remote(
                command_executor=grid_url,
                options=options
            )

        else:

            driver = webdriver.Firefox(
                options=options
            )

    else:
        raise Exception("Unsupported browser selected")

    driver.maximize_window()

    yield driver

    driver.quit()


# ======================================================
# FAILURE + LOG + MCP ANALYSIS
# ======================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    # ==================================================
    # ONLY AFTER TEST EXECUTION
    # ==================================================
    if report.when == "call":

        logger = getattr(item, "logger", None)

        # ==================================================
        # ATTACH LOGS TO ALLURE
        # ==================================================
        if logger and hasattr(logger, "log_stream"):

            logs = logger.log_stream.getvalue()

            if logs:

                allure.attach(
                    logs,
                    name="Execution Logs",
                    attachment_type=allure.attachment_type.TEXT
                )

        # ==================================================
        # FAILURE HANDLING + MCP AI
        # ==================================================
        if report.failed:

            driver = item.funcargs.get("driver", None)

            error_message = str(call.excinfo.value)

            # ==============================================
            # SCREENSHOT CAPTURE
            # ==============================================
            if driver:

                try:

                    # --------------------------------------
                    # Create screenshots folder
                    # --------------------------------------
                    screenshot_dir = "screenshots"

                    if not os.path.exists(screenshot_dir):
                        os.makedirs(screenshot_dir)

                    # --------------------------------------
                    # Unique screenshot name
                    # --------------------------------------
                    timestamp = datetime.now().strftime(
                        "%Y%m%d_%H%M%S_%f"
                    )

                    screenshot_name = (
                        f"{item.name}_{timestamp}.png"
                    )

                    screenshot_path = os.path.join(
                        screenshot_dir,
                        screenshot_name
                    )

                    # --------------------------------------
                    # Save screenshot to folder
                    # --------------------------------------
                    driver.save_screenshot(
                        screenshot_path
                    )

                    # --------------------------------------
                    # Attach screenshot to Allure
                    # --------------------------------------
                    allure.attach.file(
                        screenshot_path,
                        name="Failure Screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )

                    print(
                        f"Screenshot saved: {screenshot_path}"
                    )

                except Exception as e:

                    print(
                        f"Screenshot capture failed: {e}"
                    )

            # ==============================================
            # MCP FAILURE ANALYSIS
            # ==============================================
            try:

                analyzer = FailureAnalyzer()

                analysis = analyzer.analyze_failure(
                    test_name=item.name,
                    error_logs=error_message
                )

                print(
                    "\n🚨 MCP FAILURE ANALYSIS:\n",
                    analysis
                )

                allure.attach(
                    analysis,
                    name="MCP Failure Analysis",
                    attachment_type=allure.attachment_type.TEXT
                )

            except Exception as e:

                print(f"MCP Analysis Failed: {e}")