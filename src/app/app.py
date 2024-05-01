import logging.config

import configparser
import os
import inspect

from log.log import Log
from config.config import Config
from cli.cli import CommandLine
from utils import get_logs_dir



class App:
    """Class representing the main application."""

    def __init__(self,log):
        """
        Initialize the App.

        Args:
            log (Log): The logging utility instance.
            config (ConfigParser): The configuration parser instance.
            cli (CommandLine): The command-line interface utility instance.
        """
        self.app_name = None
        self.cli = CommandLine()
        self.log_level =50
        self.log = log
        self.log_message('MIMIC')

        self.header = self.cli.header("header")(self.log.log_message)
        self.info = self.cli.info("info")(self.log.log_message)
        self.error = self.cli.error("error")(self.log.log_message)
        self.warning = self.cli.warning("warning")(self.log.log_message)
        self.success = self.cli.success("success")(self.log.log_message)

        self.config = config.Config()


    def log_message(self, message):
        """Log a message."""
        pass

    def setup_logging(self):
        """Set up logging configuration."""
        self.info("Setting up logging configurations")
        log_format = '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'
        self.log.configure_logging(self.log_level,log_format)
        # logging.basicConfig(level=self.log_level, format=log_format)


    def parse_config(self):
        """Parse configuration file and set configuration values."""
        try:
            name = self.config.get('General','AppName')
            self.app_name = name
            self.log_level = int(self.config.get('Logging', 'LogLevel'))
            return True
        except Exception as e:
            self.cli.error(f"Parsing error occurred: {str(e)}")
            return False

    def run(self):
        """Main method to run the application."""
        try:
            self.info("Now running `app.py`.")
            self.cli.header(f"Welcome")
            self._initialize_configuration()
            self.success("Initialization successful.")
            self.cli.header(f"Logging Config")
            self.info("Attempting to initialize logging configurations.")
            self._initialize_logging()
            self._initialize_application()
        except Exception as e:
            self._handle_error(e)


    def _initialize_configuration(self):
        """Initialize configuration parsing."""
        self.info("Initializing configuration parsing.")
        if self.parse_config():
            self.success("Configuration parsing successful.")
        else:
            self.error("Parsing error occurred")
            raise RuntimeError("Configuration parsing failed")

    def _initialize_logging(self):
        """Initialize logging."""
        self.info("Setting up logging.")
        self.setup_logging()
        self.success("Logging setup successful.")

    def _initialize_application(self):
        """Initialize the application."""
        self.info(" Application initializing.")
        self.cli.header(f"Running {self.app_name}")
        self.success(f"{self.app_name} started.")

    def _handle_error(self, error):
        """Handle application errors."""
        self.error(f"Error running the application: {str(error)}")
