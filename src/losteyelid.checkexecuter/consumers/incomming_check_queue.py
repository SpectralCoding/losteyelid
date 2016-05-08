#!/usr/bin/env python
"""Submits tasks to the RabbitMQ Queue."""

import json
import pika
import logger
from check.check import Check
from check.check_result import CheckResult
from producers.outgoing_check_results import OutgoingCheckResults

LOGGER = logger.get_logger(__name__)

class IncommingCheckQueue:
    """Retreive tasks from the RabbitMQ Queue."""

    def __init__(self):
        self.connection = None
        self.channel = None
        self.outgoing_producer = None
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

    def start_consumer(self):
        """Starts consuming items off of the LEL.ChecksWaiting Queue."""
        self.channel.queue_declare(queue='LEL.ChecksWaiting')
        self.channel.basic_consume(self.receive_callback,
                                   queue='LEL.ChecksWaiting',
                                   no_ack=False)
        self.outgoing_producer = OutgoingCheckResults()
        self.outgoing_producer.connect()
        self.channel.start_consuming()

    def receive_callback(self, channel, method, properties, body):
        """Processes an item off of the LEL.ChecksWaiting Queue."""
        #pylint: disable=unused-argument
        body = body.decode("utf-8")
        LOGGER.debug("Received Check: " + body)
        check_result = self.execute_check(body)
        LOGGER.debug("Check Results: " + check_result)
        self.outgoing_producer.queue_results(check_result)
        return

    @staticmethod
    def execute_check(body):
        """Instantiates and Executes a check from a check_builder."""
        check_data = json.loads(body)
        cur_check = Check(check_data)
        LOGGER.debug("Executing Check.")
        output = cur_check.execute()
        check_result = CheckResult(cur_check, output)
        return json.dumps(check_result.__dict__)


    def disconnect(self):
        """Disconnects from RabbitMQ."""
        self.connection.close()
