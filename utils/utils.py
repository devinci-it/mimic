import os
import inspect

def get_root_dir():
    """Returns the root directory of the project."""
    caller_frame = inspect.stack()[1]
    caller_script_dir = os.path.dirname(os.path.abspath(caller_frame.filename))

    return os.path.dirname(os.path.abspath(caller_script_dir))

def get_docs_dir():
    """Returns the directory path for documentation files."""
    return os.path.join(get_root_dir(), "docs")

def get_stubs_dir():
    """Returns the directory path for stub files."""
    return os.path.join(get_root_dir(), "stubs")

def get_storage_dir():
    """Returns the directory path for stub files."""
    return os.path.join(get_root_dir(), "storage")


def get_logs_dir():
    """Returns the directory path for stub files."""
    return os.path.join(get_root_dir(), "logs")

def get_laravel_dir():
    """Returns the directory path for stub files."""
    return os.path.join(get_storage_dir(), "laravel")

def get_template_dir():
    """Returns the directory path for stub files."""
    return os.path.join(get_laravel_dir(), "template")



