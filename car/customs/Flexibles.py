import os
import sys
import scrapy
import logging
from scrapy.utils.log import configure_logging

class CustomLogger:
    def __init__(self):
        configure_logging()
        self.logger = logging.getLogger(__name__)

    def custom_log(self, value, message=''):
        """
        Print out in terminal value with message.
        Args:
            value: The value to log
            message: Optional message (default: '')
        Output:
            Logs file path, message, value(s), and function name
        """
        caller_frame = sys._getframe().f_back
        self.logger.debug("##############################")
        self.logger.debug(message)
        self.logger.debug(f"Your value:\n{value}")
        self.logger.debug(f"File path: {os.path.abspath(caller_frame.f_code.co_filename)}")
        self.logger.debug(f"Function name: {caller_frame.f_code.co_name}")
        self.logger.debug("##############################")
