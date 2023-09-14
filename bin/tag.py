#!/usr/bin/env python3

# get first argument
import sys
import os

try:
    version = sys.argv[1]
except IndexError:
    print("No version provided")
    sys.exit(1)


# python function that changes the pyproject.toml version
def change_pyproject_version(version):
    with open("pyproject.toml", "r") as f:
        lines = f.readlines()
    with open("pyproject.toml", "w") as f:
        for line in lines:
            if line.startswith("version ="):
                f.write(f'version = "{version}"\n')
            else:
                f.write(line)


# python function that changes the __init__.py version
def change_init(version):
    with open("./stadsarkiv_client/__init__.py", "r") as f:
        lines = f.readlines()
    with open("./stadsarkiv_client/__init__.py", "w") as f:
        for line in lines:
            if line.startswith("__version__ ="):
                f.write(f'__version__ = "{version}"\n')
            else:
                f.write(line)


# change in README. Search for this string: git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@latest-version
# to git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@{version}
def change_readme(version):
    with open("README.md", "r") as f:
        lines = f.readlines()
    with open("README.md", "w") as f:
        for line in lines:
            if line.startswith("git+


change_pyproject_version(version)
change_init(version)

# git add, commit and push
os.system("git add .")
os.system(f'git commit -m "bump version to {version}"')
os.system("git push")

# create tag
os.system(f'git tag -a {version} -m "bump version to {version}"')
os.system("git push --tags")
