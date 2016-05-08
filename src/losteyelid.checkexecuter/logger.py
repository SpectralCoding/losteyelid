#!/usr/bin/env python
"""Provides a logging facility for structured log output."""

import logging
import logging.config
import time
import os
import json


def get_logger(name):
    """Return a Logger object that can be used to write structured logs.

    :param name: The name of the calling class.
    :param level: The logging level to import before the line."""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logger = logging.getLogger('checkexecuter.' + name)
    config_data = json.load(open('logging.json', 'r'))
    logging.config.dictConfig(config_data)
    # Force all times to GMT and to use . as delimiter instead of ,
    for cur_handler in logging.getLogger().handlers:
        cur_handler.formatter.converter = time.gmtime
        cur_handler.formatter.default_msec_format = '%s.%03d'
    return logger


LOG = get_logger("losteyelid.checkexecutor")
