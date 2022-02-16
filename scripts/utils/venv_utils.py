"""
venv_utils.py
=============

A set of virtualenv utils to make it easier to install a VM on the 
JASMIN Notebook Service.

Simplest usage is as follows:

```
from notebooks.mngmt.utils.venv_utils import *

venv_name = "my_venv"
packages = ["fixnc", "scipy"]

setup_venv(venv_name, packages)
```

NOTE: the import is relative so this assumes that your current notebook is at the top of
the `ceda-notebooks` repo. If not you can set the path with:

```
import sys
sys.path.insert(0, "<location_on_disk>/ceda-notebooks>")
```

"""

# Import the required packages
import pip
import os
import shutil
import importlib
import re
import sys


# Define and create the base directory install virtual environments
user_dir = os.path.join(os.path.expanduser("~"), "nb-venvs")


def create_venv(venv_name: str, venvs_dir: str = user_dir, force_recreate=False):
    """
    Create a virtualenv using the name `venv_name` under the directory `venvs_dir`.
    If `force_recreate` is True, then remove old venv and create a new one.

    @param venv_name: name of the venv
    @param venvs_dir: filepath to the venv. Default /$HOME/nb-venvs/
    @param force_recreate: flag whether to delete and recreate venv. Default False.

    """
    if not os.path.isdir(venvs_dir):
        print(f"Making venvs dir: {venvs_dir}")
        os.makedirs(venvs_dir)

    # Define the venv absolute path
    venv = os.path.join(venvs_dir, venv_name)
    sp_dir = "lib/python{}.{}/site-packages".format(sys.version_info.major, sys.version_info.minor)

    # Remove the old venv if flagged
    if os.path.isdir(venv) and force_recreate:
        print(f"Removing old venv: {venv}")
        shutil.rmtree(venv)

    # Create the virtual environment
    if not os.path.isdir(os.path.join(venv, sp_dir)):
        print(f"Making venv {venv_name} directory in {venvs_dir}")
        os.system(f"python -m venv {venv}")
    else:
        print(f"Venv already exists: {venv}\nforce_recreate must be True to recreate a venv")


def activate_venv(venv_name: str, venvs_dir: str = user_dir):
    """
    Activate an existing virtualenv using the name `venv_name` under the directory `venvs_dir`.
    Adds the venv site-packages to the system paths.
    """
    print(f"Activating virtualenv: {venv_name}")
    venv = os.path.join(venvs_dir, venv_name)
    sp_dir = "lib/python{}.{}/site-packages".format(sys.version_info.major, sys.version_info.minor)

    if not os.path.isdir(os.path.join(venv, sp_dir)):
        raise Exception(f"No venv found at {venv}, please create venv first.")

    sys.path.append(f"{venv}/lib/python3.8/site-packages/")


def install_packages(packages: list, venv_name: str, venvs_dir: str = user_dir, force_install=False):
    """
    Install packages into the a virtualenv.
    If `venv_dir` is "auto" then it tries to work out where the venv is located.
    Returns None, raises exception if cannot activate.

    @param packages: list of packages to pip install to the venv
    @param venv_name: name of the venv to install packages
    @param venvs_dir: location of the venv. Default $HOME/nb-venvs/
    @param force_install: flag to whether check for install or just install anyways. Default False.
    """
    # Install a set of required packages via `pip`
    for pkg in packages:
        install_package(pkg, venv_name, venvs_dir, force_install)


def install_package(package: str, venv_name: str, venvs_dir: str = user_dir, force_install=False):
    """

    @param package: name of single package to install to the venv
    @param venv_name: name of the venv to install packages
    @param venvs_dir: location of the venv. Default $HOME/nb-venvs/
    @param force_install: flag to whether check for install or just install anyways. Default False.
    """
    venv = os.path.join(venvs_dir, venv_name)
    if package in sys.modules.keys() and not force_install:
        print(f"{package} already installed in sys.modules")
    else:
        print(f"Installing package: {package}")
        pip.main(["install", "--prefix", venv, package])


def setup_venv(venv_name: str, packages: list, venvs_dir: str = user_dir, force_recreate=False, force_install=False):
    """
    All in one process to setup and venv and install packages.
    Create, and activate a virtualenv using the name `venv_name` under the directory `venvs_dir`.
    Then install `packages` if any provided.
    If `force_recreate` is True, then remove old venv and create a new one.
    """
    create_venv(venv_name, venvs_dir, force_recreate)
    activate_venv(venv_name, venvs_dir)
    install_packages(packages, venv_name, venvs_dir, force_install)
