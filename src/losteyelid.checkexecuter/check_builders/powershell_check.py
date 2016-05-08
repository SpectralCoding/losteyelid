#!/usr/bin/env python
"""Executes PowerShell commands against a remote host."""

import logger
from winrm.winrm import WinRM

LOGGER = logger.get_logger(__name__)

class PowerShellCheck:
    """Executes PowerShell commands against a remote host."""

    @staticmethod
    def execute(check_data):
        """Executes the check."""
        winrm = WinRM()
        parameters = ' '.join(check_data.parameters)
        parameters = '-Command \"' + parameters + '\"'
        output = winrm.run(
            "POWERSHELL", parameters,
            (check_data.target, 5985, "/wsman",
             check_data.credential['username'],
             check_data.credential['password'])
        )
        return output
