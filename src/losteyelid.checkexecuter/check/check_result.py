#!/usr/bin/env python
"""Represents a results of a check against a target system."""

import logger

LOGGER = logger.get_logger(__name__)

class CheckResult:
    """Represents a results of a check against a target system."""

    def __init__(self, check_obj, result):
        self.node_id = check_obj.node_id
        self.metric_id = check_obj.metric_id
        self.target = check_obj.target
        self.check_module = check_obj.check_module
        self.check_type = check_obj.check_type
        self.credential = check_obj.credential
        self.parameters = check_obj.parameters
        self.response = result
        return
        