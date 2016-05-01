#!/usr/bin/env python
"""Provides a logging facility for structured log output."""

import logging
import time


def get_logger(name, level=logging.DEBUG):
    """Return a Logger object that can be used to write structured logs.

    :param name: The name of the calling class.
    :param level: The logging level to import before the line."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(level)
        formatter = logging.Formatter("%(asctime)s [%(name)s.%(levelname)s]: %(message)s")
        formatter.default_msec_format = "%s.%03d"
        formatter.converter = time.gmtime
        consolehandler.setFormatter(formatter)
        logger.addHandler(consolehandler)

    return logger


LOG = get_logger("losteyelid.checkexecutor")
