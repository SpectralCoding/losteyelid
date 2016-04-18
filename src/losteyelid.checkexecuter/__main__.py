import sys
import logger
import datetime
from winrm.winrm import WinRM

logger = logger.get_logger(__name__)

def main(args=None):
	__version__ = "0.1"
	if args is None:
		args = sys.argv[1:]
	logger.info("Started LostEyelid CheckExecutor v" + __version__)
	logger.info("Current System Time: " + datetime.datetime.now().isoformat())

	winrm = WinRM()
	winrm.run("set", "192.168.122.1", 5985, "/wsman", "RedactedUser", "RedactedPass")

	# Do argument parsing here (eg. with argparse) and anything else
	# you want your project to do.

if __name__ == "__main__":
	main()
