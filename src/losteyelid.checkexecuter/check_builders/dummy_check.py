#!/usr/bin/env python
"""Executes a dummy check to gauge performance."""

import datetime
import logger

LOGGER = logger.get_logger(__name__)

class DummyCheck:
    """Executes a dummy check to gauge performance."""

    @staticmethod
    def execute(check_data):
        """Executes the check."""
        #pylint: disable=unused-argument
        return datetime.datetime.utcnow().isoformat()
