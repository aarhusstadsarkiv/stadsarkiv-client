#!/bin/sh

# This script is used to run the CLI commands in the module.
#
# Usage: python -m stadsarkiv_client [OPTIONS] COMMAND [ARGS]...
#
# Options:
#   --help  Show this message and exit.
#
# Commands:
#   server-dev     Start the running Uvicorn dev-server.
#   server-docker  Start the production docker gunicorn server.
#   server-prod    Start the production gunicorn server.
#   server-secret  Generate a session secret.
#   server-stop    Stop the running Gunicorn server.

./venv/bin/python -m stadsarkiv_client $@
