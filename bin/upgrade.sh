#!/bin/sh
echo "Upgrading stadsarkiv_client"
LATEST_REMOTE_TAG=$(git describe --tags --abbrev=0)
echo "Latest remote tag: $LATEST_REMOTE_TAG"
./venv/bin/python -m stadsarkiv_client server-stop $@




