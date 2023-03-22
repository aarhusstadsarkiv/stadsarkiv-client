#!/bin/sh
black .
mypy --config-file pyproject.toml .
flake8 .