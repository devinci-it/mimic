import argparse
import subprocess

import utils
from app.app import App as DevinciApp
from cli.cli import CommandLine as DevinciCommandLine
from log.log import Log as DevinciLog


from argparse_functions import ArgparseController


class TerminalApp:
    @classmethod
    def mimic_artisan(cls, app, logger,arg_controller):
        parser = argparse.ArgumentParser(
            description="Mimic Laravel Artisan command")
        parser.add_argument("command", nargs='?',
                            help="The Laravel Artisan command to execute")
        parser.add_argument("-f", "--force", action="store_true",
                            help="Force override files")
        parser.add_argument("-v", "--verbose", action="store_true",
                            help="Enable verbose logging")

        args = parser.parse_args()
        artisan_command = args.command
        print(f"\nartisan_command")

        # Strip "php artisan" from the command string
        if args.command and args.command.startswith("php artisan "):
            args.command = args.command[len("php artisan "):]

        # Build the Laravel Artisan command to execute
        print(args.command)

        # Add options if provided
        if args.force:
            artisan_command.append("--force")
        if args.verbose:
            artisan_command.append("--verbose")

        if args.command is None:
            parser.print_help()
            return

        # Execute the Laravel Artisan command
        try:
            arg_controller.run(artisan_command)
        except subprocess.CalledProcessError as e:
            print(e.stderr.decode())


#
#
# # # Example of calling the method from another module:
if __name__ == "__main__":

    cli=DevinciCommandLine()

    logger = DevinciLog.Log(cli,"app.log",utils.get_logs_dir())
    app = DevinciApp(logger)
    mimic_cli=TerminalApp()
    argparse_controller = ArgparseController(app, logger)
    mimic_cli.mimic_artisan(app, logger,argparse_controller)




