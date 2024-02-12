#!/usr/bin/env python
import os

# This script does linting, type checking, and formatting
# according to the project's standards.

# execute command if __name__ == "__main__"
if __name__ == "__main__":
    os.system("black . --config pyproject.toml")
    os.system("mypy  --config-file pyproject.toml .")
    os.system("flake8 . --config .flake8")
