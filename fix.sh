#!/bin/sh
black .
mypy .
flake8 .