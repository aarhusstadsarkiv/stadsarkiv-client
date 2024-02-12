#!/usr/bin/env python
import os

# This script does linting, type checking, and formatting
# according to the project's standards.
os.system("black . --config pyproject.toml")
os.system("mypy  --config-file pyproject.toml .")
os.system("flake8 . --config .flake8")
