# Test

## Run all tests

    maya source-test

## Run a specific test

Specifify that you want to run a test:

    export TEST=TRUE

Set a config directory,
    
    export CONFIG_DIR=sites/aarhus

Run the test:

    python -m unittest tests/core/orders_test.py 