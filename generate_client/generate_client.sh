#!/bin/sh
rm -rf stadsarkivet-client
openapi-python-client generate --url http://localhost:8000/v1/openapi.json --config config.yml
# --config config.yml 