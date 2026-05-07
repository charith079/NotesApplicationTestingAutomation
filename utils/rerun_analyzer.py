from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException
)


class RerunAnalyzer:

    RETRYABLE_EXCEPTIONS = (
        TimeoutException,
        StaleElementReferenceException,
        ElementClickInterceptedException,
        NoSuchElementException
    )

    @staticmethod
    def should_rerun(exception):

        # Retry only flaky Selenium issues
        if isinstance(exception, RerunAnalyzer.RETRYABLE_EXCEPTIONS):
            return True

        return False