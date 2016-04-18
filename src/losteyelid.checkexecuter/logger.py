import logging
import time


def get_logger(name, level=logging.DEBUG):
	logger = logging.getLogger(name)
	logger.setLevel(level)

	if not logger.handlers:
		consolehandler = logging.StreamHandler()
		consolehandler.setLevel(level)
		formatter = logging.Formatter("%(asctime)s [%(name)s.%(levelname)s]: %(message)s")
		formatter.default_msec_format = "%s.%03d"
		formatter.converter = time.gmtime
		consolehandler.setFormatter(formatter)
		logger.addHandler(consolehandler)

	return logger


log = get_logger("losteyelid.checkexecutor")
