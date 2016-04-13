LostEyelid - Features - Architecture
=============================

Scalable
--------
  - Hand-in-hand with distributed

Distributed
-----------
  - Central Management
      - Web Interface
          - Functionality:
              - Monitoring Changes
              - Alert Changes
              - Access Changes
              - Large Cassandra Database
                  - Long Term Metrics
                  - Current Status Data
                  - Application Configuration
                  - Monitoring Configuration
      - Data Processor
          - Functionality:
              - Retrieves data from the RabbitMQ "Historical Queue" and "Live Queue" and performs tasks based on content
                  - Update Cassandra
      - Coordinator
          - Functionality:
              - Retrieves data from all remote RabbitMQ "Outgoing Queue"s distributes the work based on content
  - Local Execution
      - Web Interface
          - Features:
              - No Configuration Options!
          - Functionality:
              - Basic control (Auth creds pushed from master):
                  - Reboot/Reinitialize
                  - Silence
                  - Diagnostics?
              - Assigned nodes
              - Execution status/load
              - Job queue display
              - Connectivity display:
                  - Master / other services
              - Read/Writes exclusively to Cassandra
      - Alert Assessor
          - Functionality:
              - Analyses Cassandra for outstanding issues
              - Outputs fully formatted alerts to RabbitMQ "Alert Queue"
      - Alert Executer
          - Functionality:
              - Listens on RabbitMQ's "Alert Queue" for alerts to send
              - Executes alert tasks:
                  - Send email
                  - Run executable/script
      - Check Scheduler
          - Functionality:
              - Submits Jobs to the RabbitMQ "Job Queue" with proper info/order/timestamps
      - Check Executer
          - Functionality:
              - Listens for new Jobs on the RabbitMQ "Job Queue"
              - Executes job tasks
                  - Ping, WMI, SNMP, Scripts, etc
              - Reports results to RabbitMQ "Result Queue"
      - Data Processor:
          - Functionality:
              - Reads results from RabbitMQ "Result Queue" and stores it in Cassandra
              - Seeds data into the RabbitMQ "Outgoing Queue"
      - Coordinator:
          - Functionality:
              - Reads data from the local RabbitMQ "Incoming Queue" and performs tasks based on content
                  - Configuration Changes
                  - Service Control

Performant
----------

  - Redis as cache? Is this necessary?
