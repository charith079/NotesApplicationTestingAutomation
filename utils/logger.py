# import logging
# import os
# from io import StringIO
# from datetime import datetime

# # 🔹 In-memory stream for Allure
# log_stream = StringIO()


# def get_logger(test_name="test"):
#     # Create logs folder
#     if not os.path.exists("logs"):
#         os.makedirs("logs")

#     # 🔹 Unique log file per test (IMPORTANT ✅)
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     log_file = f"logs/{test_name}_{timestamp}.log"

#     logger = logging.getLogger(test_name)
#     logger.setLevel(logging.INFO)

#     # 🔹 Remove old handlers (important for parallel runs)
#     if logger.hasHandlers():
#         logger.handlers.clear()

#     # 🔹 File handler (UTF-8)
#     file_handler = logging.FileHandler(log_file, encoding="utf-8")
#     file_handler.setLevel(logging.INFO)

#     # 🔹 Console handler
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.INFO)

#     # 🔹 Memory handler (for Allure)
#     stream_handler = logging.StreamHandler(log_stream)
#     stream_handler.setLevel(logging.INFO)

#     # 🔹 Format
#     formatter = logging.Formatter(
#         "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
#     )

#     file_handler.setFormatter(formatter)
#     console_handler.setFormatter(formatter)
#     stream_handler.setFormatter(formatter)

#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)
#     logger.addHandler(stream_handler)

#     return logger


# # 🔹 Get logs for Allure
# def get_logs():
#     return log_stream.getvalue()


# # 🔹 Clear logs after each test
# def clear_logs():
#     log_stream.truncate(0)
#     log_stream.seek(0)

import logging
import os
from io import StringIO
from datetime import datetime
import pytest


def get_logger(test_name="test"):

    if not os.path.exists("logs"):
        os.makedirs("logs")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    log_file = f"logs/{test_name}_{timestamp}.log"

    logger = logging.getLogger(test_name)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    # 🔥 PER TEST STREAM (SAFE)
    log_stream = StringIO()

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    console_handler = logging.StreamHandler()
    stream_handler = logging.StreamHandler(log_stream)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(stream_handler)

    logger.log_stream = log_stream

    # 🔥 AUTO REGISTER WITH PYTEST ITEM (NO TEST CHANGE NEEDED)
    try:
        from _pytest.fixtures import FixtureRequest
        request = pytest.request
        if request:
            request.node.logger = logger
    except:
        pass

    return logger


def get_logs(logger):
    return logger.log_stream.getvalue()


def clear_logs():
    pass  # no longer needed (handled per test isolation)