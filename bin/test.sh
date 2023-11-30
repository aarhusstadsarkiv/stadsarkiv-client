#!/bin/sh

# This script runs tests
./venv/bin/python -m unittest tests/default/*.py

# Test teater client
export CONFIG_DIR="example-config-teater"
./venv/bin/python -m unittest tests/client/*.py