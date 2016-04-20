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
	# Regular Command Prompt Commands
	winrm.run(
		"SET",
		"",
		("192.168.122.1", 5985, "/wsman", "WinRMUser", "WinRMPassword")
	)
	# Useful PowerShell Options:
	#    -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -WindowStyle Hidden
	# Other thoughts:
	#    Only select relevant object properties with "Select-Object -Property PropA,PropB,PropN
	#    Export all data as Minimized JSON with "ConvertTo-Json -Compress"
	winrm.run(
		"POWERSHELL",
		"-Command \"Get-Childitem env:* | Select-Object -Property Name,Value | ConvertTo-Json -Compress\"",
		("192.168.122.1", 5985, "/wsman", "WinRMUser", "WinRMPassword")
	)

	# Do argument parsing here (eg. with argparse) and anything else
	# you want your project to do.

if __name__ == "__main__":
	main()
