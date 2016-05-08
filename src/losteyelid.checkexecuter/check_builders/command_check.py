#!/usr/bin/env python
"""Executes Windows commands against a remote host."""

import logger
from winrm.winrm import WinRM

LOGGER = logger.get_logger(__name__)

class CommandCheck:
    """Executes Windows commands against a remote host."""

    @staticmethod
    def execute(check_data):
        """Executes the check."""
        winrm = WinRM()
        executable = check_data.parameters[0]
        parameters = ' '.join(check_data.parameters[1:])
        output = winrm.run(
            executable, parameters,
            (check_data.target, 5985, "/wsman",
             check_data.credential['username'],
             check_data.credential['password'])
        )
        return output
