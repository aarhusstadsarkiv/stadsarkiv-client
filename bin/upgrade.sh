#!/bin/sh

# This script upgrades the module to a specific tag.
# Usage: bin/upgrade.sh TAG
# if first argument is empty, exit
if [ -z "$1" ]
  then
    echo "No tag supplied"
    echo "Usage: bin/upgrade.sh TAG"
    exit 1
fi

tag=$1

# Stop the service
sudo systemctl stop stadsarkiv-client.service

# Upgrade the repo
git checkout main
git pull
git checkout $tag

# Activate virtual environment and install requirements
./venv/bin/pip install -r requirements.txt

# Start the service
sudo systemctl start stadsarkiv-client.service
