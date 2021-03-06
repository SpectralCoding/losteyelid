#!/usr/bin/env python
"""Submits tasks to the RabbitMQ Queue."""

import json
import pika
import logger

LOGGER = logger.get_logger(__name__)

class Producer:
    """Submits tasks to the RabbitMQ Queue."""

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
        self.channel.queue_declare(queue='LEL.ChecksWaiting')
        return

    def queue_check(self, check):
        """Submits a command to be run to the queue."""
        self.channel.basic_publish(
            exchange='',
            routing_key='LEL.ChecksWaiting',
            body=json.dumps(check.__dict__))

    def disconnect(self):
        """Disconnects from RabbitMQ."""
        self.connection.close()
        