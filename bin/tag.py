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


# change in README. Search for this string below <!-- LATEST-VERSION-START -->
# and change the line to \tpip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@{version}
def change_readme(version):
    write_ext_line = False
    with open("README.md", "r") as f:
        lines = f.readlines()
    with open("README.md", "w") as f:
        for line in lines:
            if write_ext_line:
                f.write(f"\tpip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@{version}\n")
                write_ext_line = False
            elif line.startswith("<!-- LATEST-VERSION-START -->"):
                f.write(line)
                write_ext_line = True
            else:
                f.write(line)


change_readme(version)
change_pyproject_version(version)
change_init(version)

# git add, commit and push
# os.system("git add .")
# os.system(f'git commit -m "bump version to {version}"')
# os.system("git push")

# check if something needs to be commited
# if something needs to be commited, exit
if os.system("git diff-index --quiet HEAD --") != 0:
    print("There are uncommited changes")
    sys.exit(1)


# create tag
os.system(f'git tag -a {version} -m "bump version to {version}"')
os.system("git push --tags")
