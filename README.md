# README

## Install for development

    git clone https://github.com/aarhusstadsarkiv/stadsarkiv-client.git

    cd stadsarkiv-client

    virtualenv venv # Python >= 3.10.6 should work   

    source venv/bin/activate

Or (Windows)

    source venv/Scripts/activate

Install requirements:

    pip install -r requirements.txt

## Run for development

    python -m stadsarkiv_client

Or: 

    ./bin/run-module.sh

## Install as requirement

    virtualenv venv

    source venv/bin/activate

Update version and install latest version:

    pip uninstall -y stadsarkiv-client
    pip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@main

You may also install a specific version:

    pip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@version

## Run required module

Usage: stadsarkiv-serve [OPTIONS]

    stadsarkiv-serve --help

    Options:
    --reload BOOLEAN   Reload uvicorn on changes.
    --port INTEGER     Server port.
    --workers INTEGER  Number of workers.
    --help             Show this message and exit.

Serve the default module on port 5555:

    stadsarkiv-serve

Or use some options:

    stadsarkiv-serve --port 5555 --reload true

## Modifying the module

You may override the default settings by overriding the following files and dirs:

    .env
    settings.py
    language.py
    hooks.py
    templates/
    static/

All the above files and dirs are optional. You may see examples of all the above files in the 
[example-config directory](https://github.com/aarhusstadsarkiv/stadsarkiv-client/tree/main/example-config)
(These files are well documented)

These files and dirs should be placed in the directory where you run the module from - otherwise they will be ignored.

## Fix code

Run black, mypy and flake8:

    ./bin/fix.sh

## openaws client

In order to update the openapi client you can `cd` into the `generate_openaws_client` directory

Instructions can be found in the [generate_openaws_client/README.md](generate_openaws_client/README.md) directory. 

The generated openaws client itself is just a python module which has it's own repository at: 

[aarhusstadsarkiv/openaws-client](https://github.com/aarhusstadsarkiv/openaws-client)
