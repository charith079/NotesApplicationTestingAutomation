# import time
# import allure

# from functools import wraps

# from selenium.common.exceptions import (
#     StaleElementReferenceException,
#     ElementClickInterceptedException,
#     TimeoutException,
#     ElementNotInteractableException
# )

# from utils.logger import get_logger


# # =========================================================
# # 🔹 Flaky Exceptions
# # =========================================================

# FLAKY_EXCEPTIONS = (
#     StaleElementReferenceException,
#     ElementClickInterceptedException,
#     TimeoutException,
#     ElementNotInteractableException
# )


# # =========================================================
# # 🔹 Retry Decorator
# # =========================================================

# def retry_on_failure(max_retries=3, delay=2):

#     def decorator(func):

#         @wraps(func)
#         def wrapper(*args, **kwargs):

#             logger = get_logger("retry_handler")

#             last_exception = None

#             for attempt in range(1, max_retries + 1):

#                 try:

#                     logger.info(
#                         f"[RETRY ENGINE] Attempt "
#                         f"{attempt}/{max_retries} "
#                         f"for function: {func.__name__}"
#                     )

#                     return func(*args, **kwargs)

#                 except FLAKY_EXCEPTIONS as e:

#                     last_exception = e

#                     logger.warning(
#                         f"[RETRY ENGINE] Flaky exception detected "
#                         f"in {func.__name__}"
#                     )

#                     logger.warning(f"Exception: {type(e).__name__}")
#                     logger.warning(f"Retry attempt: {attempt}")

#                     # =================================================
#                     # 🔹 Capture Screenshot
#                     # =================================================

#                     try:

#                         self_object = args[0]

#                         screenshot = (
#                             self_object.driver.get_screenshot_as_png()
#                         )

#                         allure.attach(
#                             screenshot,
#                             name=f"Retry_{attempt}_{func.__name__}",
#                             attachment_type=allure.attachment_type.PNG
#                         )

#                     except Exception as screenshot_error:

#                         logger.error(
#                             f"Screenshot capture failed: "
#                             f"{screenshot_error}"
#                         )

#                     # =================================================
#                     # 🔹 Wait before retry
#                     # =================================================

#                     time.sleep(delay)

#             logger.error(
#                 f"[RETRY ENGINE] All retry attempts failed "
#                 f"for {func.__name__}"
#             )

#             raise last_exception

#         return wrapper

#     return decorator

import time
import logging

from utils.rerun_analyzer import RerunAnalyzer

logger = logging.getLogger("retry_handler")


def retry_on_failure(max_retries=2, delay=2):

    def decorator(func):

        def wrapper(*args, **kwargs):

            last_exception = None

            for attempt in range(max_retries):

                try:

                    logger.info(
                        f"[RERUN ENGINE] Attempt "
                        f"{attempt + 1}/{max_retries}"
                    )

                    return func(*args, **kwargs)

                except Exception as e:

                    last_exception = e

                    logger.warning(
                        f"[RERUN ENGINE] Failure: {type(e).__name__}"
                    )

                    # =================================================
                    # 🔥 DECISION ENGINE
                    # =================================================

                    should_retry = RerunAnalyzer.should_rerun(e)

                    if not should_retry:

                        logger.error(
                            "[RERUN ENGINE] "
                            "Non-retryable failure detected"
                        )

                        raise e

                    logger.info(
                        "[RERUN ENGINE] "
                        "Retryable flaky failure detected"
                    )

                    time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator