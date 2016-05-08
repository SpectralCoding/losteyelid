#!/usr/bin/env python
"""Executes Windows Command Interpreter commands against a remote host."""

import logger
from winrm.winrm import WinRM

LOGGER = logger.get_logger(__name__)

class CommandPromptCheck:
    """Executes Windows Command Interpreter commands against a remote host."""

    @staticmethod
    def execute(check_data):
        """Executes the check."""
        winrm = WinRM()
        parameters = ' '.join(check_data.parameters)
        output = winrm.run(
            "CMD", parameters,
            (check_data.target, 5985, "/wsman",
             check_data.credential['username'],
             check_data.credential['password'])
        )
        return output
