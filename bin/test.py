#!/usr/bin/env python
import os

# Test default client
os.system("python -m unittest tests/config-default/*.py")

# Test teater client
os.environ["CONFIG_DIR"] = "example-config-teater"
os.system("python -m unittest tests/config-teater/*.py")

# Test aarhus client
os.environ["CONFIG_DIR"] = "example-config-aarhus"
os.system("python -m unittest tests/config-aarhus/*.py")
