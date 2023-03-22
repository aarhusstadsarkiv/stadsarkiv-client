#!/bin/sh

# check if directory exists 'openaws-client'
# if not clone it
if [ ! -d "openaws-client" ]; then
    git clone git@github.com:aarhusstadsarkiv/openaws-client.git
fi

# Mv git repo to tmp
mv openaws-client openaws-client-tmp

# generate new client
openapi-python-client generate --config config.yml --url http://localhost:8000/v1/openapi.json 

# copy new client code on top of old client
cp -rf openaws-client/* openaws-client-tmp/
rm -rf openaws-client
mv openaws-client-tmp openaws-client
