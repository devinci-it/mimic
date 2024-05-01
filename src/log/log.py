import logging
import os


class Log:
    """Logging functionality."""
    def __init__(self, cli,log_file,log_directory):
        self.cli = cli
        self.log_file=log_file
        self.log_directory=log_directory

    def log_message(self, log_level, message):
        """Logs a message with the specified log level."""
        log_message = f"[{log_level.upper()}] {message}"
        if log_level == "info":
            self.cli.info(log_message)
            self.log(log_message)
        elif log_level == "error":
            self.cli.error(log_message)
            self.log(log_message)
        elif log_level == "warning":
            self.cli.warning(log_message)
            self.log(log_message)
        elif log_level == "success":
            self.cli.success(log_message)
            self.log(log_message)
        elif log_level == "header":
            self.cli.header(log_message)
            self.log(log_message)

    def log_decorator(self, log_level):
        """Decorator function to simplify logging calls."""

        def log_decorator(log_level):
            """Decorator function to simplify logging calls."""

            def decorator(func):
                def wrapper(*args, **kwargs):
                    result = func(*args,
                                  **kwargs)
                    message = f"{func.__name__} returned: {result}"
                    self.log_message(log_level, message)
                    return result
                return wrapper

            return decorator
    def configure_logging(self, log_level=logging.INFO, log_format='%(asctime)s - %(levelname)s - %(message)s'):
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

        log_path = os.path.join(self.log_directory, self.log_file)

        logging.basicConfig(filename=log_path, level=log_level, format=log_format)

    def set_log_file(self, file_name):
        self.log_file = file_name

    def set_log_directory(self, directory):
        self.log_directory = directory

    def clear_logs(self):
        log_files = [f for f in os.listdir(self.log_directory) if f.endswith('.log')]
        for log_file in log_files:
            os.remove(os.path.join(self.log_directory, log_file))

    def add_gitignore(self):
        gitignore_path = os.path.join(self.log.log_directory, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write("*.log\n")

    @staticmethod
    def log(message, level=logging.INFO):
        """
        Log a message with the specified log level.

        Args:
            message (str): The message to log.
            level (int, optional): The log level (default: logging.INFO).
        """
        logging.log(level, message)
