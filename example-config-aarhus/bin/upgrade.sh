#!/bin/sh

# This script upgrades the module to the latest tag, unless the latest tag is already checked out.
# Usage: bin/upgrade.sh

# Fetch tags from the origin
git fetch --tags

# Get the latest tag
latest_tag=$(git describe --tags `git rev-list --tags --max-count=1`)

# Check if latest tag is empty
if [ -z "$latest_tag" ]; then
    echo "No tags found in the repository."
    exit 1
fi

# Get the current checked out tag
current_tag=$(git describe --tags)

# Check if the current tag is the latest
if [ "$current_tag" = "$latest_tag" ]; then
    echo "Latest tag ($latest_tag) is already checked out."
    exit 0
fi

echo "Upgrading to the latest tag: $latest_tag"

# Stop the service
sudo systemctl stop stadsarkiv-client.service

# Upgrade the repo and checkout the latest tag
git checkout main
git pull
git checkout $latest_tag

# overwrite config files from example-config-aarhus to local/
# except hidden files and 'bin/' and '__pycache__/'
rsync -a --exclude='bin/' --exclude='__pycache__/' --exclude='.*' example-config-aarhus/ local/

# Activate virtual environment and install requirements
./venv/bin/pip install -r requirements.txt

# Start the service
sudo systemctl start stadsarkiv-client.service
