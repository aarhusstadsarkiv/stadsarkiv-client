#!/usr/bin/env python
import os
import subprocess
import glob


def run_tests(config_dir, tests_path_pattern):
    if config_dir:
        os.environ["CONFIG_DIR"] = config_dir

    # get test files
    test_files = glob.glob(tests_path_pattern)
    if test_files:
        for test_file in test_files:
            print(f"Running tests in {test_file}")
            subprocess.run(["python", "-m", "unittest", test_file], check=True)
    else:
        print(f"No tests found matching pattern {tests_path_pattern}")


# Example usage
run_tests(None, "tests/config-default/*.py")
run_tests("example-config-teater", "tests/config-teater/*.py")
run_tests("example-config-aarhus", "tests/config-aarhus/*.py")
