from image_uploader.commons.constants import LOGGING_LEVEL
import structlog

import logging


def load_log_config():
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("python_dynamodb_lock").setLevel(logging.WARNING)
    log_level = {
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "error": logging.ERROR,
        "warning": logging.WARNING
    }
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level[LOGGING_LEVEL])
    )

    root_logger = structlog.get_logger(__name__)

    return root_logger


logger = load_log_config()
