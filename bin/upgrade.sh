#!/bin/sh

# Exit on any error
# set -e

# check if tag is provided 
if [ -z "$1" ]; then
    echo "No tag argument supplied"
    exit 1
fi

tag=$1

# Fetch latest changes without modifying the working tree
git fetch

# Check if tag exists in the fetched data
if ! git rev-parse $tag >/dev/null 2>&1; then
    echo "Tag $tag does not exist in the repo"
    exit 1
fi

# Stop the service
sudo systemctl stop stadsarkiv-client.service

# Upgrade the repo
git checkout main
git pull
git checkout $tag

# Activate virtual environment and install requirements
source ./venv/bin/activate
pip install -r requirements.txt

# Start the service
sudo systemctl start stadsarkiv-client.service
