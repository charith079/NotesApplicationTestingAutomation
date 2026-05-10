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

    # remove old handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # PER TEST STREAM 
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

    return logger


def get_logs(logger):
    return logger.log_stream.getvalue()
