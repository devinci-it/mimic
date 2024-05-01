import os
import fcntl

class InstallationLock:
    """
    Utility class for managing the installation lock.
    """

    @staticmethod
    def is_installed(lock_file_path):
        """
        Checks if the app is already installed.

        Args:
            lock_file_path (str): Path to the lock file.

        Returns:
            bool: True if installed, False otherwise.
        """
        return os.path.exists(lock_file_path)

    @staticmethod
    def mark_installed(lock_file_path):
        """
        Marks the app as installed.

        Args:
            lock_file_path (str): Path to the lock file.
        """
        with open(lock_file_path, "w") as file:
            file.write("installed")

    @staticmethod
    def acquire_lock(lock_file_path):
        """
        Acquires the installation lock.

        Args:
            lock_file_path (str): Path to the lock file.
        """
        lock_file = open(lock_file_path, "w")
        fcntl.flock(lock_file, fcntl.LOCK_EX)

    @staticmethod
    def release_lock(lock_file_path):
        """
        Releases the installation lock.

        Args:
            lock_file_path (str): Path to the lock file.
        """
        lock_file = open(lock_file_path, "w")
        fcntl.flock(lock_file, fcntl.LOCK_UN)
