
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
                    #  DECISION ENGINE
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