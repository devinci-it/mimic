import os
import subprocess
from colorama import Fore, Style
from utils import get_logs_dir, get_template_dir,get_root_dir
from config.config import Config

class Install:
    '''
    A class to handle the installation process.

    Methods:
        setup_laravel_project (method): Sets up a Laravel project.
        run_composer_update (method): Runs composer update.
        run_composer_install (method): Runs composer install.
        require_livewire (method): Installs the Livewire package.
        init_git_repo (method): Initializes a Git repository.
        add_and_commit (method): Adds and commits changes to Git.
    '''

    def __init__(self, app) -> None:
        '''
        Initializes the class with the app object.

        Args:
            app: The application object containing logging, configuration, and CLI utility instances.
        '''
        self.app = app

    def check_config(self) -> None:
        '''
        Checks if the config file exists, generates template if not.
        '''
        config_file = 'config.ini'
        if not os.path.exists(config_file):
            self.app.warning('Config file not present, generating template directory.')
            self.app.config.generate_config_template()
            self.app.success(f'{config_file} created')
            self.app.info(f'{get_root_dir()}/{config_file}')

    def create_logs_directory(self) -> None:
        '''
        Checks and creates the logs directory if it doesn't exist.
        '''
        logs_dir = get_logs_dir()
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
            self.app.success(f"Log directory '{logs_dir}' created.")

    def setup_laravel_project(self) -> bool:
        '''
        Sets up a Laravel project.
        '''

        self.app.info("Setting up Laravel project")
        laravel_dir = get_template_dir()
        contents = os.listdir(laravel_dir)

        for item in contents:
            if os.path.isfile(os.path.join(laravel_dir, item)):
                return True

        command =\
    f"""
        #!/bin/bash
        mkdir -p {laravel_dir}
        cd {laravel_dir} 
        composer create-project --prefer-dist laravel/laravel .
    """
        return self._exec_command(command, "Laravel setup")

    def run_composer_update(self) -> bool:
        '''
        Runs composer update.
        '''

        self.app.info("Updating composer dependencies.")
        laravel_dir = get_template_dir()
        command = f"""
        #!/bin/bash
        cd {laravel_dir}
        composer -v  > /dev/null
        composer update >/dev/null
        """
        return self._exec_command(command, "Composer update")

    def run_composer_install(self) -> bool:
        '''
        Runs composer install.
        '''
        self.app.info("Installing composer dependencies.")
        laravel_dir = get_template_dir()
        command = f"cd {laravel_dir} && composer install"
        return self._exec_command(command, "Composer install")

    def require_livewire(self) -> bool:
        '''
        Installs the Livewire package.
        '''
        self.app.info("Installing livewire/livewire dependency.")
        laravel_dir = get_template_dir()
        command = f"cd {laravel_dir} && composer require livewire/livewire && composer update && composer install"
        return self._exec_command(command, "Livewire installation")

    def init_git_repo(self) -> bool:
        '''
        Initializes a Git repository.
        '''
        self.app.info("Setting up git repository.")
        laravel_dir = get_template_dir()
        command = f"cd {laravel_dir} && git init && echo 'venv/' >> .gitignore && git add .gitignore && git commit -m '.gitignore' && git add . && git commit -m 'Fresh Installation'"
        return self._exec_command(command, "Git repository setup")

    def install(self) -> bool:
        '''
        Perform the installation process.

        Returns:
            bool: True if the installation was successful, False otherwise.
        '''
        self.check_config()
        self.create_logs_directory()
        return (
            self.setup_laravel_project()
            and self.run_composer_update()
            and self.run_composer_install()
            and self.require_livewire()
            and self.init_git_repo()
        )

    def _exec_command(self, command: str, task_name: str) -> bool:
        '''
        Executes a bash command.

        Args:
            command (str): The bash command to execute.
            task_name (str): Name of the task for logging purposes.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        '''

        self.app.info(f"Executing '{task_name}'.")
        try:

            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            output = result.stdout
            error = result.stderr
            if output:
                self.app.info(f"Command output:\n{Fore.GREEN}{output}{Style.RESET_ALL}")  # Green color for output
            if error:
                self.app.error(f"Command error:\n{Fore.RED}{error}{Style.RESET_ALL}")  # Red color for error
                self.app.success(f"{task_name} completed successfully.")
            return True
        except subprocess.CalledProcessError as e:
            self.app.error(f"{task_name} failed: {e}")
            return False
