import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.environment import config
from utils.logger import get_logger


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


# ======================================================
# 🚀 DRIVER FIXTURE
# ======================================================
@pytest.fixture(scope="function")
def driver(request):

    browser = request.config.getoption("--browser")
    execution_mode = config.get("execution_mode", "remote")
    grid_url = config.get("grid_url")

    logger = get_logger(f"TC-{browser.upper()}")

    driver = None

    # ======================================================
    # 🔵 CHROME CONFIG (STABLE + NO ADS POPUPS)
    # ======================================================
    if browser == "chrome":

        options = ChromeOptions()

        # --- UI / popup blocking ---
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-save-password-bubble")

        # --- stability ---
        options.add_argument("--start-maximized")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")

        # --- security / automation stability ---
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")

        # --- anti-renderer crash / timeout fix ---
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-features=TranslateUI")

        options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
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
                service=Service(ChromeDriverManager().install()),
                options=options
            )

    # ======================================================
    # 🟠 FIREFOX CONFIG (PROPER WAY - PREFS NOT ARGUMENTS)
    # ======================================================
    elif browser == "firefox":

        options = FirefoxOptions()

        # Firefox does NOT support Chrome flags like --disable-popup-blocking
        # so we use preferences instead

        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("dom.push.enabled", False)

        # disable popups
        options.set_preference("dom.disable_open_during_load", True)

        # performance / stability
        options.set_preference("browser.tabs.remote.autostart", True)
        options.set_preference("browser.cache.disk.enable", False)
        options.set_preference("browser.cache.memory.enable", False)

        # reduce tracking + interruptions
        options.set_preference("privacy.trackingprotection.enabled", True)

        if execution_mode == "remote":
            driver = webdriver.Remote(
                command_executor=grid_url,
                options=options
            )
        else:
            driver = webdriver.Firefox(options=options)

    else:
        raise Exception("Unsupported browser selected")

    driver.maximize_window()

    request.node.logger = logger

    yield driver

    driver.quit()


# ======================================================
# 📊 ALLURE + LOGS + SCREENSHOT
# ======================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call":

        logger = getattr(item, "logger", None)

        if logger and hasattr(logger, "log_stream"):
            logs = logger.log_stream.getvalue()

            if logs:
                allure.attach(
                    logs,
                    name="Execution Logs",
                    attachment_type=allure.attachment_type.TEXT
                )

        if report.failed:
            driver = item.funcargs.get("driver", None)

            if driver:
                try:
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name="Failure Screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception as e:
                    print(f"Screenshot capture failed: {e}")