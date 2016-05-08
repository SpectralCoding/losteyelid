#!/usr/bin/env python
"""Represents a individual command to run against a system."""

import logger

LOGGER = logger.get_logger(__name__)

class Check:
    """Represents a individual command to run against a system."""

    def __init__(self, check_data):
        self.node_id = check_data['node_id']
        self.metric_id = check_data['metric_id']
        self.target = check_data['target']
        self.check_module = check_data['check_module']
        self.check_type = check_data['check_type']
        self.credential = check_data['credential']
        self.parameters = check_data['parameters']
        return
        