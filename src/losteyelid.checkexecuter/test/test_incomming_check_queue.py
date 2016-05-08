#!/usr/bin/env python
"""Tests the IncommingCheckQueue module."""

import json
import re
import unittest
from consumers.incomming_check_queue import IncommingCheckQueue

class IncommingCheckQueueTest(unittest.TestCase):
    """Tests the IncommingCheckQueue."""

    @unittest.skip("Not a good test candidate. Has external dependency.")
    def test_connect(self):
        """Tests IncommingCheckQueue.connect()."""

    @unittest.skip("Not a good test candidate. Has external dependency.")
    def test_start_consumer(self):
        """Tests IncommingCheckQueue.start_consumer()."""

    @unittest.skip("Not a good test candidate. Has external dependency.")
    def test_receive_callback(self):
        """Tests IncommingCheckQueue.receive_callback()."""

    def test_execute_check(self):
        """Tests IncommingCheckQueue.execute_check()."""
        test_body = ('{"metric_id": 0, "check_module": "dummy_check", "parameters": null, "node_id'
                     '": 0, "check_type": "DummyCheck", "target": "192.168.122.1", "credential": n'
                     'ull}')
        test_result = IncommingCheckQueue.execute_check(test_body)
        result_data = json.loads(test_result)
        self.assertTrue(result_data['metric_id'] == 0)
        self.assertTrue(result_data['check_module'] == 'dummy_check')
        self.assertTrue(result_data['parameters'] is None)
        self.assertTrue(result_data['node_id'] == 0)
        self.assertTrue(result_data['check_type'] == 'DummyCheck')
        self.assertTrue(result_data['target'] == '192.168.122.1')
        self.assertTrue(result_data['credential'] is None)
        # Matches a valid ISO8601 date
        regex = re.compile(r'^(?:[1-9]\d{3}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1\d|2[0-8])|(?:0[13-9]|'
                           r'1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[1-9]\d(?:0[48]|[2468][04'
                           r'8]|[13579][26])|(?:[2468][048]|[13579][26])00)-02-29)T(?:[01]\d|2[0-3'
                           r']):[0-5]\d:[0-5]\d(\.\d+)?(?:Z|[+-][01]\d:[0-5]\d)?$')
        self.assertTrue(regex.match(result_data['response']))

    @unittest.skip("Not a good test candidate. Has external dependency.")
    def test_disconnect(self):
        """Tests IncommingCheckQueue.disconnect()."""
