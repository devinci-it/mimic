"""
    Setup script for your_package_name.

    This script configures the setup parameters for your_package_name and prepares it for distribution.

    Usage:
        - Replace placeholders with your actual package information.
        - Run 'python env_setup.py sdist bdist_wheel' to build the distribution package.
        - Upload the generated package to PyPI or another package repository.

    Configuration Overview:
        - name: Name of the package.
        - version: Version number of the package.
        - packages: List of packages to include in the distribution.
        - package_dir: Mapping of package names to directories.
        - install_requires: List of dependencies required by the package.
        - entry_points: Configuration for console scripts and other entry points.
        - author: Author name of the package.
        - author_email: Email address of the author.
        - description: Short description of the package.
        - long_description: Long description of the package.
        - long_description_content_type: Content type of the long description.
        - url: URL of the package repository.
        - classifiers: List of classifiers for the package.
        - license: License information for the package.
        - package_data: Additional data files to include in the distribution.

"""

from setuptools import setup, find_packages
    # from src.helper import wildcard
import glob
import os
def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()
def get_all_scripts(path):
    # Use glob to get all .py files in the given path
    all_py_files = glob.glob(os.path.join(path, '*.py'))

    # Filter out __init__.py files
    scripts = [file for file in all_py_files if not file.endswith('__init__.py')]

    return scripts
setup(
    name='mimic',
    version='0.1',
    packages=find_packages(['utils','src','src/app','src/cli','src/helper',
                            'src/install','src/log','src/run','src/config']),
    package_dir={ '': 'src',
                 'app':'src/app',
                 'cli':'src/cli',
                 'config':'src/config',
                 'helper':'src/helper',
                 'install':'src/install',
                 'log':'src/log',
                 'run':'src/run',
                 'utils': 'utils'},
    install_requires=['colorama==0.4.6', 'fernet==1.0.1', 'pyaes==1.6.1', 'tabulate==0.9.0'],
    entry_points={
        'console_scripts': [
            'mimic = app.app:run',
            'mimic-cli = app.terminal:run',
        ],
    },
    author='devinci-it',
    author_email='devinci-it@icloud.com',
    description='Simplify the learning process of Laravel',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/devinci-it/mimic',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    # scripts=['src/run/mimic.py','src/app/argparse_functions.py'],
    py_modules=['app/terminal','app/app','app/argparse_functions',
                'app/terminal','cli/cli' ,'config/config','helper/helper',
                'install/install','log/log','run/run','utils/utils'],
    data_files=([('', ['config.ini', 'LICENSE','README.md','requirements.txt']),('docs', ['docs/*.md'])]),
)

packages = find_packages()

print("Discovered packages:")
for package in packages:
    print(package)
#
# Please note that Python uses indentation to define blocks of code. Adding an extra level of indentation to your entire script might cause syntax errors if you try to run it.