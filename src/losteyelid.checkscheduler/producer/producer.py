#!/usr/bin/env python
"""Submits tasks to the RabbitMQ Queue."""

import logger

LOGGER = logger.get_logger(__name__)

class Producer:
    """Submits tasks to the RabbitMQ Queue."""

    def __init__(self):
        return

    def queue_command(self):
        """Submits a command to be run to the queue."""
        