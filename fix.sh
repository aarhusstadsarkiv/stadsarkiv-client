#!/bin/sh
# Format all files according to black. Black settings are in pyproject.toml
find . -type f -name "*.py" ! -path "./venv/*" -exec black  {} + 
mypy .