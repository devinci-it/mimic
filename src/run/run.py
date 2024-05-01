"""
Main script for running the application.

    This script initializes and runs the application, configuring logging,
    loading configuration settings, and handling command-line interface (CLI) utility.

    Usage:
        $ python run.py

    This script checks for the existence of a configuration file ('config.ini').
    If the file doesn't exist, it generates a template for the configuration file.
    It also ensures the existence of a directory for log files ('logs').

    Attributes:
        log (Log): An instance of the logging utility.
        config (Config): An instance of the configuration handler.
        cli (CommandLine): An instance of the command-line interface utility.
"""
import os

import dotenv

import utils
from app import app as DevinciApp
from app.terminal import TerminalApp
from app.argparse_functions import ArgparseController
from cli.cli import CommandLine as DevinciCommandLine
from config.config import Config
from helper.installation_lock import InstallationLock
from install.install import Install
from log import log as DevinciLog
from log import log as Log


def is_installed(lockfile='mimic.lock'):

    if InstallationLock.is_installed(lockfile):
        return True
    return False


def main(lock_file='mimic.lock'):
    dotenv.load_dotenv()


    command_line=DevinciCommandLine()
    config=Config(os.path.join(utils.get_root_dir(),'config.ini'))
    log=DevinciLog.Log(command_line,'app.log',utils.get_logs_dir())
    log.configure_logging()
    mimic=DevinciApp.App(log)
    secret_key = os.getenv("SECRET_KEY")

    log_level = 10
    lock_file =config.get('General','lock_file')

    log_format = config.get_logging_format()
    log.configure_logging(log_level,log_format)

    mimic_cli=TerminalApp()
    arg_controller= ArgparseController(mimic,log)

    mimic_cli.mimic_artisan(mimic,log,arg_controller)

    mimic.cli.header("INSTALLATION")

    if is_installed(lock_file):
        mimic.cli.info("Lockfile present no installation needed.")

    else:
        mimic.cli.info("Initializing Installation & Setup")
        installer = Install(mimic)
        try:
            installer.install()
            mimic.cli.success("Installation complete.\n RUN `mimic -h` for "
                           "more "
                      "info")
        except:
            mimic.cli.error("Error occurred during installation.Refer to "
                      "storage/logs/app.log for more info.")
    mimic.run()
    # terminal_app=t_app.get_terminal_app(app,log,"Artisan")
    # t_app.run()
# # Example of calling the method from another module:
if __name__ == "__main__":


    main('mimic.lock')

    # argparse_controller=ArgparseController()
    # mimic_cli = TerminalApp()
    # logger = None  # Set your logger instance here
    # mimic_cli.mimic_artisan(app, logger)
    #
    # script.execute_command()
    #
    # paths=script.parse_files()
    # rels=script.determine_relative_paths(paths)
    # script.create_directories(paths)
    # script.create_directories(rels,force=True)
    # script.copy_files()
    # script.add_and_commit_changes()
