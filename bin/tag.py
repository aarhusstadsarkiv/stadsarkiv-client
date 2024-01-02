#!/usr/bin/env python3

"""
This script is used to bump the version of the package.
It will change the version in the pyproject.toml file,
the __init__.py file and the README.md file.

It will exit if there are uncommited changes to prevent
accidental commits.

Usage:

    ./bin/tag.py <version>

"""

import sys
import os
import toml
import re


# get first argument as version
try:
    version = sys.argv[1]
except IndexError:
    print("No version provided")
    print("Usage: ./bin/tag.py <version>")
    sys.exit(1)


def parse_version_tag(tag):
    # Remove leading 'v' if it exists
    if tag.startswith("v"):
        return tag[1:]

    return tag


# python function that changes the pyproject.toml version
def change_pyproject_version(version):
    with open("pyproject.toml", "r") as f:
        lines = f.readlines()
    with open("pyproject.toml", "w") as f:
        for line in lines:
            if line.startswith("version ="):
                version = parse_version_tag(version)
                f.write(f'version = "{version}"\n')
            else:
                f.write(line)


# python function that changes the __init__.py version
def change_init(path, version):
    with open(path, "r") as f:
        lines = f.readlines()
    with open(path, "w") as f:
        for line in lines:
            if line.startswith("__version__ ="):
                f.write(f'__version__ = "{version}"\n')
            else:
                f.write(line)


def change_setup(file_path, version):
    # Match version line
    version_pattern = re.compile(r"version=['\"](.*?)['\"]")

    with open(file_path, "r") as file:
        content = file.read()

    # update version
    version = parse_version_tag(version)
    updated_content = version_pattern.sub(f"version='{version}'", content)

    with open(file_path, "w") as file:
        file.write(updated_content)


# change in README. Search for this string below <!-- LATEST-VERSION-START -->
# and change the line to \tpip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@{version}
def change_markdown(file, str_search, replace):
    dynamic_next_line = False
    with open(file, "r") as f:
        lines = f.readlines()
    with open(file, "w") as f:
        for line in lines:
            if dynamic_next_line:
                f.write(replace)
                dynamic_next_line = False
            elif line.startswith(str_search):
                f.write(line)
                dynamic_next_line = True
            else:
                f.write(line)


def replace_version(version):
    pyproject = {}

    try:
        with open("pyproject.toml", "r") as f:
            pyproject = toml.load(f)

    except FileNotFoundError:
        pass

    # Alter pyproject.toml
    if os.path.exists("pyproject.toml"):
        change_pyproject_version(version)

    # Alter setup.py
    if os.path.exists("setup.py"):
        change_setup("setup.py", version)

    # Check if tool.bumptag.version_files exists
    # Change version __init__.py files
    try:
        version_files = pyproject["tool"]["bumptag"]["version_files"]
        for file in version_files:
            change_init(file, version)
    except KeyError:
        pass

    try:
        replace_patterns = pyproject["tool"]["bumptag"]["replace_patterns"]
        # print(replace_patterns)
        for _, pattern in replace_patterns.items():
            # version = parse_version_tag(version)
            # replace 'version' with the new version
            pattern["replace"] = pattern["replace"].replace("{version}", version)
            change_markdown(pattern["file"], pattern["search"], pattern["replace"])
    except KeyError:
        pass


# check if something needs to be commited
# if something needs to be commited, exit
if os.system("git diff-index --quiet HEAD --") != 0:
    print("There are uncommited changes")
    sys.exit(1)

# change the version in the files
replace_version(version)

# commit the changed files
os.system("git add .")
os.system(f'git commit -m "bump version to {version}"')
os.system("git push")

# create tag
os.system(f'git tag -a {version} -m "bump version to {version}"')
os.system("git push --tags")
