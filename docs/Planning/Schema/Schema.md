LostEyelid - Features - Schema
==============================

LEM Keyspace (LostEyelid Master)
--------
  - lem.config
    - Application Configuration
	  - User Permissions
  - lem.log
    - Event Log Information
	  - Monitor Events
	- Audit Log Information
	  - LostEyelid System Change Events
  - lem.timeseries
    - Timeseries data for all metrics
  - lem.monitors
    - Will contain monitor configuration
  - lem.live
    - Live status of all systems

LEL Keyspace (LostEyelid Local)
-----------
  - Will contain local versions of most lem tables