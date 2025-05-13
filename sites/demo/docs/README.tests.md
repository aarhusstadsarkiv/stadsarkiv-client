# Test

## Run all tests

    stadsarkiv-client source-test

## Run a specific test

    # Information about the test
    export TEST=TRUE

    # Set a config directory - optional
    # This config directory will be used for the test
    # Settings in the config directory will override the default settings
    export CONFIG_DIR=example-config-aarhus

    python -m unittest tests/core/orders_test.py 