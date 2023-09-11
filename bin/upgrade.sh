#!/bin/sh

# check if first argument is set 
if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 1
fi

# tag is the first argument
TAG=$1

sudo systemctl stop stadsarkiv-client.service

git pull
git checkout $TAG
./venv/bin/pip install -r requirements.txt

sudo systemctl start stadsarkiv-client.service
