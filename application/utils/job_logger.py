import logging
import logging.handlers
import os
from logging.handlers import TimedRotatingFileHandler


def job_logger(log_name='job_logger'):
    logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
    logging_format += "%(message)s"
    log_formatter = logging.Formatter(logging_format)

    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../logs/')
    os.makedirs(logs_dir, exist_ok=True)

    logs_file_name = logs_dir + log_name

    log_handler = TimedRotatingFileHandler(logs_file_name, when='midnight')
    log_handler.setFormatter(log_formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)

    logger = logging.getLogger(log_name)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)
    logger.addHandler(stream_handler)

    return logger
