#!/usr/bin/env python
"""Submits check results to the RabbitMQ Queue."""

import pika
import logger

LOGGER = logger.get_logger(__name__)

class OutgoingCheckResults:
    """Submits check results to the RabbitMQ Queue."""

    def __init__(self):
        self.connection = None
        self.channel = None
        return

    def connect(self):
        """Connects to RabbitMQ."""
        credentials = pika.credentials.PlainCredentials(
            'default', 'default')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            '192.168.122.50',
            6672,
            '/',
            credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='LEL.CheckRawResults')

    def queue_results(self, check_results):
        """Submits a check response to be processed to the queue."""
        self.channel.basic_publish(
            exchange='',
            routing_key='LEL.CheckRawResults',
            body=check_results)

    def disconnect(self):
        """Disconnects from RabbitMQ."""
        self.connection.close()
