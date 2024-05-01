import os

from setuptools import find_packages

def list_modules():
    packages = find_packages()
    for package in packages:
        print(f"Package: {package}")
        modules = find_modules(package)
        for module in modules:
            print(f"  - {module}")

def find_modules(package):
    modules = set()
    package_path = package.replace('.', '/')
    try:
        with open(f"{package_path}/__init__.py", 'r'):
            pass
    except FileNotFoundError:
        return modules

    try:
        files = os.listdir(package_path)
    except FileNotFoundError:
        return modules

    for file in files:
        if file.endswith('.py') and file != '__init__.py':
            modules.add(file[:-3])

    return modules

if __name__ == "__main__":
    list_modules()
