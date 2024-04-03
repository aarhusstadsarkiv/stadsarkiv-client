#!/bin/sh

# This script is used to restart the running Gunicorn web-server.
# on a linux server. E.g. after a new deployment.
sudo systemctl restart stadsarkiv-client.service