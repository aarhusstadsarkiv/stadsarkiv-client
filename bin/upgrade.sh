#!/bin/sh

# Exit on any error
# set -e

git fetch --tags

# check if tag is provided 
if [ -z "$1" ]; then
    tag=$(git describe --tags `git rev-list --tags --max-count=1`)
else
    tag=$1
fi

echo "Upgrading to tag $tag"

# Check if tag exists. User supplied tag.
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

./venv/bin/pip install -r requirements.txt

# Start the service
sudo systemctl start stadsarkiv-client.service
