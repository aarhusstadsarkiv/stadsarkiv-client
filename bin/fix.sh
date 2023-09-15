#!/bin/sh

# This script does linting, type checking, and formatting
# according to the project's standards. 
black .
mypy  --config-file pyproject.toml .
flake8 .