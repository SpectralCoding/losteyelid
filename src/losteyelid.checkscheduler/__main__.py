#!/usr/bin/env python
"""The main entrypoint for losteyelid.checkscheduler."""

import sys
import datetime
import logger
from producer.producer import Producer
from check.check import Check

LOGGER = logger.get_logger(__name__)

def main(args=None):
    """The main entrypoint for losteyelid.checkscheduler.

    :param args: The command line arguments."""
    __version__ = "0.1"
    if args is None:
        args = sys.argv[1:]
    LOGGER.info("Started LostEyelid CheckScheduler v" + __version__)
    LOGGER.info("Current System Time: " + datetime.datetime.now().isoformat())

    producer = Producer()
    producer.connect()
    cur_check = Check({
        'node_id': 0,
        'metric_id': 0,
        'target': '192.168.122.1',
        'check_module': 'dummy_check',
        'check_type': 'DummyCheck',
        'credential': None,
        'parameters': None})
    producer.queue_check(cur_check)
    cur_check = Check({
        'node_id': 0,
        'metric_id': 0,
        'target': '192.168.122.1',
        'check_module': 'icmp_check',
        'check_type': 'ICMPCheck',
        'credential': None,
        'parameters': None})
    producer.queue_check(cur_check)
    cur_check = Check({
        'node_id': 0,
        'metric_id': 0,
        'target': '192.168.122.1',
        'check_module': 'command_check',
        'check_type': 'CommandCheck',
        'credential': {'username':'WinRMUser', 'password':'WinRMPassword'},
        'parameters': ['SET']})
    producer.queue_check(cur_check)
    cur_check = Check({
        'node_id': 0,
        'metric_id': 0,
        'target': '192.168.122.1',
        'check_module': 'powershell_check',
        'check_type': 'PowerShellCheck',
        'credential': {'username':'WinRMUser', 'password':'WinRMPassword'},
        'parameters': ['Get-Childitem env:* | Select-Object -Property Name,Value'
                       ' | ConvertTo-Json -Compress']})
    producer.queue_check(cur_check)

if __name__ == "__main__":
    main()
