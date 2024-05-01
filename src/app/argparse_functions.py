import os
import shutil
import subprocess
from utils import get_laravel_dir,get_template_dir

class ArgparseController:
    def __init__(self, app, logger, force=False, verbose=False):
        """
        Initialize the ArgparseController instance.

        Args:
            command (str): The Laravel Artisan command to execute.
            logger: The logger instance for logging.
            force (bool): Flag to force override files.
            verbose (bool): Flag to enable verbose logging.
        """
        self.command = None
        self.point_of_execution=os.getcwd()
        self.files_generated=[]
        self.app= app
        self.logger = logger
        self.force = force
        self.verbose = verbose
        self.laravel_dir=get_template_dir()

    def execute_command(self):
        """Execute the specified Artisan command."""
        laravel_dir = get_template_dir()
        os.chdir(laravel_dir)
        result=subprocess.run(f"php artisan {self.command}", shell=True,
                              check=True)
        return result

    def parse_files(self):
        """Parse the files generated using git status output."""

        # Use git status command to get the list of modified or untracked files

        os.chdir(self.laravel_dir)
        git_status_output = subprocess.run("git status --porcelain", shell=True,
                                           capture_output=True, text=True)
        modified_files = []
        for line in git_status_output.stdout.splitlines():
            if line.startswith("M ") or line.startswith("?? "):
                # Extract the file path from the git status output
                file_path = line.split(" ", 1)[1].strip()
                if os.path.isdir(file_path):
                    self.app.info(f"Extracting multiple files within"
                                  f" {file_path}")
                    # If it's a directory, get all files within it
                    for root, _, files in os.walk(file_path):
                        modified_files.extend(
                            [os.path.join(root, file) for file in files])
                else:
                    modified_files.append(file_path)
        self.files_generated.extend(modified_files)
        self.app.info(f"Files: {modified_files}")
        return modified_files
    def copy_files(self, force=False):
        """Copy modified files to the destination directory."""
        try:
            for modified_file in self.files_generated:
                dest_path = os.path.join(self.point_of_execution, modified_file)
                if not os.path.exists(dest_path) or force:
                    if os.path.isdir(modified_file):
                        shutil.copytree(modified_file, dest_path)
                        self.app.success(f"Copied directory {modified_file} to"
                                  f" {dest_path}")
                    else:
                        shutil.copy2(modified_file, dest_path)
                        self.app.info(f"Copied file {modified_file} to {dest_path}")
            self.app.success("Files copied successfully.")
        except Exception as e:
            self.app.error(f"An error occurred while copying files: {e}")

    def determine_relative_paths(self, modified_files):
        """Determine the relative path of the generated file from the template project root."""
        template_root = self.laravel_dir
        os.chdir(self.laravel_dir)


        relative_paths = []

        for path in modified_files:
            if os.path.isfile(path):
                relative_paths.extend(self._get_relative_file_path(path,
                                                                   template_root))
            elif os.path.isdir(path):
                relative_paths.extend(self._get_relative_files_in_directory(
                    path, template_root))

        return relative_paths
    def _get_relative_file_path(self, file_path, template_root):
        """Get the relative path of a file from the template project root."""
        relative_path = os.path.relpath(file_path, template_root)
        return [relative_path]
    def _get_relative_files_in_directory(self, directory_path, template_root):
        """Get the relative paths of all files in a directory from the template project root."""
        relative_paths = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), template_root)
                relative_paths.append(file_path)
        return relative_paths



    def create_dest_dir(self, dest_path, force=False):
        """Create a destination directory."""
        # Check if the path exists
        if not os.path.exists(dest_path):
            # If not, create the directory
            os.makedirs(dest_path)
            self.app.success(f"Directory created: {dest_path}")
        else:
            if os.path.isdir(dest_path):
                self.app.warning(f"Directory already exists: {dest_path}")
            elif os.path.isfile(dest_path):
                if force:
                    self.app.warning(f"Replacing file: {dest_path}")
                    os.remove(dest_path)
                    os.makedirs(dest_path)
                else:
                    self.app.error(f"File already exists: {dest_path}")
    def create_directories(self, relative_paths, force=False):
        """
        Run mkdir -p to create necessary directories in the destination repository.

        Args:
            relative_paths (list): List of relative paths to create.
            force (bool, optional): Whether to force directory creation if they already exist. Defaults to False.
        """
        for relative_path in relative_paths:
            source_path = os.path.join(relative_path)
            dest_path = os.path.join(self.point_of_execution,relative_path)
            # Check if the destination path corresponds to a file
            if os.path.isfile(source_path):
                self.app.info(f'{source_path} is file. Parsing path  directory.')
                dir_path, _ = os.path.split(source_path)

                self.app.info(dir_path)
                dest_path=os.path.join(self.point_of_execution,dir_path)
                self.create_dest_dir(dest_path, force)
                self.app.success(f"Directory created for file: {dir_path}")
            else:
                self.create_dest_dir(dest_path, force)
                self.app.success(f"Directory created: {source_path}")
    def add_and_commit_changes(self):
        """Add and commit the changes to the template Git repository."""
        os.chdir(self.laravel_dir)
        files_to_add = " ".join(self.files_generated)

        command=f"""
        #! /bin/bash
        cd {self.laravel_dir}
        git status
        git add {f"{files_to_add}"}
        git commit -m "{f'{files_to_add}: Cleaning tree'}"    
        """

        try:
            subprocess.run(command, shell=True, check=True)
            self.app.success('App ready to unmount. Bye.')
        except subprocess.CalledProcessError as e:
            self.app.error(f"Error executing command: {e}")
        except Exception as e:
            self.app.error(f"An unexpected error occurred: {e}")

    def run(self,command,force=False):
        """Execute the Laravel script."""
        try:
            self.command=command
            # Step 1: Execute the Laravel Artisan command
            self.app.header("Step 1: Executing the Laravel Artisan command")
            try:
                result = self.execute_command()
                self.app.info(result.stdout)
            except subprocess.CalledProcessError as e:
                print(e.stderr.decode())

            # Step 2: Parse the files generated
            self.app.header("Step 2: Parsing the files generated")
            modified_files = self.parse_files()
            self.app.info(f"Modified files: {modified_files}")

            # Step 3: Determine the relative paths of the generated files
            self.app.header("Step 3: Determining relative paths")
            relative_paths = self.determine_relative_paths(modified_files)
            self.app.info(f"Relative paths: {relative_paths}")

            # Step 4: Create directories for the generated files
            self.app.header("Step 4: Creating directories")
            self.create_directories(relative_paths)

            self.app.header("Step 5: Copy to destination directory")
            self.copy_files(force)


            # Step 5: Add and commit the changes to the template Git repository
            self.app.header(
                "Step 6: Adding and committing changes to Git repository")
            self.add_and_commit_changes()

            # Log success
            self.app.success("Script executed successfully.")

        except subprocess.CalledProcessError as e:

            self.app.error(f"Error executing command: {e}")
        except Exception as e:

            self.app.error(f"An error occurred: {e}")


#
# def parse_arguments():
#     """Parse command-line arguments."""
#     parser = argparse.ArgumentParser(description="Execute Laravel Artisan command")
#     parser.add_argument("command", help="The Laravel Artisan command to execute")
#     parser.add_argument("-f", "--force", action="store_true", help="Force override files")
#     parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
#     return parser.parse_args()
#
#
