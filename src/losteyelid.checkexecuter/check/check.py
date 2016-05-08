#!/usr/bin/env python
"""Represents a an action to perform against a target system."""

import importlib
import logger

LOGGER = logger.get_logger(__name__)

class Check:
    """Represents a an action to perform against a target system."""

    def __init__(self, check_data):
        self.node_id = check_data['node_id']
        self.metric_id = check_data['metric_id']
        self.target = check_data['target']
        self.check_module = check_data['check_module']
        self.check_type = check_data['check_type']
        self.credential = check_data['credential']
        self.parameters = check_data['parameters']
        return

    def execute(self):
        """Creates an instance of the appropriate check_builder and executes it."""
        # Get the class for the check.
        check_obj = getattr(
            importlib.import_module("check_builders." + self.check_module),
            self.check_type)
        # Instansiate the class into "instance"
        #instance = check_obj()
        # Execute the check's code.
        output = check_obj.execute(self)
        return output
