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
import virtualenv
import pip
import os
import shutil
import importlib
import re

# Define and create the base directory install virtual environments
venvs_dir = os.path.join(os.path.expanduser("~"), "nb-venvs")


def create_venv(venv_name, venvs_dir=venvs_dir, force_recreate=False):
    """
    Create a virtualenv using the name `venv_name` under the directory `venvs_dir`.
    If `force_recreate` is True, then remove old venv and create a new one.
    Returns None, raises exception if cannot create VM.
    """
    print(f"Making venvs dir: {venvs_dir}")
    if not os.path.isdir(venvs_dir):
        os.makedirs(venvs_dir)
    
    # Define the venv directory
    venv_dir = os.path.join(venvs_dir, venv_name)
    
    # Do we need to remove the old venv
    if os.path.isdir(venv_dir) and force_recreate:
        print(f"Removing old venv: {venv_dir}")
        shutil.rmtree(venv_dir)

    # Create the virtual environment
    if not os.path.isdir(venv_dir):
        print(f"Making venv in: {venvs_dir}")
        virtualenv.create_environment(venv_dir)
        
        
def activate_venv(venv_name, venv_dir="auto", venvs_dir=venvs_dir):
    """
    Activate an existing virtualenv using the name `venv_name` under the directory `venvs_dir`.
    If `venv_dir` is "auto" then it tries to work out where the venv is located.
    Returns None, raises exception if cannot activate.
    """
    print(f"Activating virtualenv: {venv_name}")
    if venv_dir == "auto":
        venv_dir = os.path.join(venvs_dir, venv_name)

    activate_file = os.path.join(venv_dir, "bin", "activate_this.py")
    exec(open(activate_file).read(), dict(__file__=activate_file))
    
    
def install_packages(packages, venv_name=None, venv_dir="auto", venvs_dir=venvs_dir):
    """
    Install packages into the a virtualenv.
    If `venv_dir` is "auto" then it tries to work out where the venv is located.
    Returns None, raises exception if cannot activate.
    """
    if not packages:
        print("No packages specified for installation")
        return

    if not venv_name and venv_dir == "auto":
        raise Exception("Please provide valid `venv_name` or `venv_dir` parameter.")

    if venv_dir == "auto":
        venv_dir = os.path.join(venvs_dir, venv_name)

    # Install a set of required packages via `pip`
    print(f"Installing packages: {packages}")
    for pkg in packages:
        pip.main(["install", "--prefix", venv_dir, pkg])
        
    print("Installation complete!")
    

def setup_venv(venv_name, packages=None, venvs_dir=venvs_dir, force_recreate=False, force_install=False):
    """
    Create, and activate a virtualenv using the name `venv_name` under the directory `venvs_dir`.
    Then install `packages` if any provided.
    If `force_recreate` is True, then remove old venv and create a new one.
    Returns None, raises exception if cannot create VM.
    """
    create_venv(venv_name, venvs_dir, force_recreate)
    activate_venv(venv_name)
    if force_install:
        install_packages(packages, venv_name)
    elif packages:
        try:
            importlib.__import__(re.split("[=<>\[]", packages[-1])[0])
        except ModuleNotFoundError:
            install_packages(packages, venv_name)
    else:
        print("No packages specified for installation")
