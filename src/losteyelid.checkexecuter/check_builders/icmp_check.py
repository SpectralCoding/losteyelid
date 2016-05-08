#!/usr/bin/env python
"""Executes ICMP checks against a remote host."""

import logger


LOGGER = logger.get_logger(__name__)

class ICMPCheck:
    """Executes ICMP checks against a remote host."""

    @staticmethod
    def execute(check_data):
        """Executes the check."""
        #pylint: disable=unused-argument
        return "This is the ICMP Check Output!"
