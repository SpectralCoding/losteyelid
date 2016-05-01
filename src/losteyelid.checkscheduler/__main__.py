#!/usr/bin/env python
"""The main entrypoint for losteyelid.checkscheduler."""

import sys
import datetime
import logger

LOGGER = logger.get_logger(__name__)

def main(args=None):
    """The main entrypoint for losteyelid.checkscheduler.

    :param args: The command line arguments."""
    __version__ = "0.1"
    if args is None:
        args = sys.argv[1:]
    LOGGER.info("Started LostEyelid CheckScheduler v" + __version__)
    LOGGER.info("Current System Time: " + datetime.datetime.now().isoformat())

if __name__ == "__main__":
    main()
