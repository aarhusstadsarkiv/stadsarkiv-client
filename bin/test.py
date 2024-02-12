#!/usr/bin/env python
import os


# is os is nt when rewrite paths to windows
def rewrite_path(path):
    if os.name == "nt":
        return path.replace("/", "\\")
    return path


# Test default client
os.system(f"python -m unittest {rewrite_path('tests/config-default/*.py')}")

# Test teater client
os.environ["CONFIG_DIR"] = "example-config-teater"
os.system(f"python -m unittest {rewrite_path('tests/config-teater/*.py')}")

# Test aarhus client
os.environ["CONFIG_DIR"] = "example-config-aarhus"
os.system(f"python -m unittest {rewrite_path('tests/config-aarhus/*.py')}")
